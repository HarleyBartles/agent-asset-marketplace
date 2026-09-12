#!/usr/bin/env python3
"""Tests for live acquisition + feedback-history policy (Plan 2 Task 4)."""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS = TESTS_DIR.parent / "scripts"
sys.path.insert(0, str(TESTS_DIR))
sys.path.insert(0, str(SCRIPTS))

from review_core import model, policy, witness_log  # noqa: E402
from review_core import acquisition as acq  # noqa: E402
from review_core import feedback_policy as fbp  # noqa: E402

BASE = "b" * 40
HEAD = "c" * 40
TREE = "d" * 40
MB = "e" * 40
REPO_ID = "o/r"
PR_URL = "https://github.com/o/r/pull/7"


def _pr_meta(**over):
    meta = {
        "number": 7, "url": PR_URL, "title": "T", "body": "B",
        "isDraft": True, "state": "OPEN",
        "baseRefOid": BASE, "headRefOid": HEAD, "baseRefName": "main",
        "closingIssuesReferences": [{"number": 12}],
        "labels": [{"name": "bug"}], "assignees": [{"login": "me"}],
        "milestone": None, "author": {"login": "a"},
    }
    meta.update(over)
    return meta


class FakeGit:
    def __init__(self, files, *, head=HEAD, base=BASE, merge_base=MB,
                 tree=TREE, obj_format="sha1", porcelain="",
                 merge_bases=None, diff="diff-bytes", override=None):
        self.files = dict(files)
        self.head = head
        self.base = base
        self.merge_bases = [merge_base] if merge_bases is None else merge_bases
        self.tree = tree
        self.obj_format = obj_format
        self.porcelain = porcelain
        self.diff = diff
        self.override = override
        self.calls = []

    def __call__(self, args):
        self.calls.append(list(args))
        if args[:2] == ["rev-parse", "--is-shallow-repository"]:
            return 0, "false\n", ""
        if args[:2] == ["merge-base", "--all"]:
            return 0, "".join(f"{m}\n" for m in self.merge_bases), ""
        if args[:2] == ["status", "--porcelain"]:
            return 0, self.porcelain, ""
        if args[:2] == ["rev-parse", "HEAD"]:
            return 0, self.head + "\n", ""
        if args[:2] == ["rev-parse", "--show-object-format"]:
            return 0, self.obj_format + "\n", ""
        if args[:2] == ["rev-parse", f"{self.head}^{{tree}}"]:
            return 0, self.tree + "\n", ""
        if args[0] == "diff":
            return 0, self.diff, ""
        if args[:2] == ["ls-tree", "-r"]:
            return 0, "\n".join(sorted(self.files)) + "\n", ""
        if args[0] == "show" and ":" in args[1]:
            _sha, path = args[1].split(":", 1)
            if path == ".agents/iterative-review/authority-policy.json":
                return (0, self.override, "") if self.override else (1, "", "nf")
            if path in self.files:
                return 0, self.files[path], ""
            return 1, "", f"missing {path}"
        return 1, "", f"unsupported {args}"


class FakeGh:
    def __init__(self, *, authed=True, repo=REPO_ID, pr=None,
                 head_remote=True, threads=(), reviews=(),
                 issues=None, contents=None, protection=None,
                 graphql_error=False):
        self.authed = authed
        self.repo = repo
        self.pr = pr if pr is not None else _pr_meta()
        self.head_remote = head_remote
        self.threads = list(threads)
        self.reviews = list(reviews)
        self.issues = issues or {}
        self.contents = contents or {}
        self.protection = protection
        self.graphql_error = graphql_error
        self.calls = []

    def __call__(self, args):
        self.calls.append(list(args))
        if args[:2] == ["auth", "status"]:
            return (0, "ok", "") if self.authed else (1, "", "not logged in")
        if args[:2] == ["repo", "view"]:
            return 0, json.dumps({"nameWithOwner": self.repo}), ""
        if args[0] == "pr" and args[1] == "view":
            return 0, json.dumps(self.pr), ""
        if args[0] == "api" and args[1] == "graphql":
            if self.graphql_error:
                return 0, json.dumps({"errors": [{"message": "boom"}]}), ""
            pr = {
                "reviewThreads": {
                    "pageInfo": {"hasNextPage": False},
                    "nodes": list(self.threads),
                },
                "reviews": {
                    "pageInfo": {"hasNextPage": False},
                    "nodes": list(self.reviews),
                },
            }
            return 0, json.dumps(
                {"data": {"repository": {"pullRequest": pr}}}), ""
        if args[0] == "api":
            path = args[1]
            if "/commits/" in path:
                return (0, "{}") + ("",) if self.head_remote else (1, "", "404")
            if "/issues/" in path:
                n = path.rsplit("/", 1)[-1]
                if n in self.issues:
                    return 0, json.dumps(self.issues[n]), ""
                return 1, "", "404"
            if "/contents/" in path:
                key = path.split("/contents/", 1)[1].split("?")[0]
                if key in self.contents:
                    body = base64.b64encode(self.contents[key].encode()).decode()
                    return 0, json.dumps({"content": body}), ""
                return 1, "", "404"
            if "/protection" in path:
                if self.protection is None:
                    return 1, "", "404"
                return 0, json.dumps(self.protection), ""
        return 1, "", f"unsupported {args}"


def _scratch(tmp_path):
    s = tmp_path / "scratch"
    (s / "transcripts").mkdir(parents=True)
    (s / "witness").mkdir(parents=True)
    return s


def _enumerate(tmp_path, git=None, gh=None, epoch=1):
    scratch = _scratch(tmp_path)
    out_dir = scratch / "acquire" / "latest"
    git = git or FakeGit({"AGENTS.md": "# law"})
    gh = gh or FakeGh()
    summary = acq.enumerate_acquisition(
        run_git=git, run_gh=gh, repo_root=tmp_path, pr_number=7,
        out_dir=out_dir, scratch_dir=scratch, epoch=epoch)
    return summary, out_dir, scratch


def _transcript_with_marker(scratch, enumeration_id, *, session="s1",
                            tool_use="exec_1", out_dir=None, extra_pre=()):
    lines = list(extra_pre)
    lines.append({
        "hook_event_name": "PreToolUse", "tool_name": "exec",
        "tool_input": {"command": f"reviewctl enumerate --out {out_dir or 'X'}"},
        "tool_use_id": tool_use, "session_id": session, "prompt_id": "p1",
    })
    lines.append({
        "hook_event_name": "PostToolUse", "tool_name": "exec",
        "tool_input": {"command": f"reviewctl enumerate --out {out_dir or 'X'}"},
        "tool_use_id": tool_use, "session_id": session, "prompt_id": "p1",
        "tool_response": {"success": True,
                          "output": f"enumeration-id: {enumeration_id}\n",
                          "error": None},
    })
    f = scratch / "transcripts" / f"{session}.jsonl"
    f.write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")
    return f


def _source(out_dir, scratch):
    return acq.LiveAuthorityDiscovery(
        acquisition_dir=out_dir,
        witness_log_path=scratch / "witness" / "witness-log.jsonl",
        transcript_root=scratch / "transcripts",
        review_id="rev-1",
    )


class TestEnumerateAcquisition:
    def test_freeze_payload_full_identity(self, tmp_path):
        summary, out_dir, _s = _enumerate(tmp_path)
        data = json.loads((out_dir / "data.json").read_text())
        snap = data["snapshot"]
        assert snap["epoch"] == 1
        assert snap["repository_id"] == REPO_ID
        assert snap["pr_number"] == 7 and snap["pr_url"] == PR_URL
        assert snap["git_object_format"] == "sha1"
        assert snap["base_sha"] == BASE and snap["head_sha"] == HEAD
        assert snap["tree_sha"] == TREE
        assert snap["diff_sha256"] == model.sha256_hex(b"diff-bytes")
        for key in model.SNAPSHOT_SUBJECT_FIELDS:
            assert key in snap, key
        assert "fingerprint" not in snap
        assert summary["enumeration_id"] == model.sha256_json(
            model.authority_discovery_subject(
                {**snap, "fingerprint": model.snapshot_fingerprint(snap)},
                data["manifest_payload"]))

    def test_blocks_on_missing_gh_auth(self, tmp_path):
        with pytest.raises(acq.AcquisitionError) as ei:
            _enumerate(tmp_path, gh=FakeGh(authed=False))
        assert ei.value.blocker_class == "tool-blocked"

    def test_blocks_on_ambiguous_merge_base(self, tmp_path):
        git = FakeGit({"AGENTS.md": "x"}, merge_bases=[MB, "f" * 40])
        with pytest.raises(acq.AcquisitionError) as ei:
            _enumerate(tmp_path, git=git)
        assert ei.value.blocker_class == "snapshot-drift"

    def test_blocks_on_shallow_repo(self, tmp_path):
        git = FakeGit({"AGENTS.md": "x"})

        def git_shallow(a):
            if a[:2] == ["rev-parse", "--is-shallow-repository"]:
                return 0, "true\n", ""
            return git(a)
        with pytest.raises(acq.AcquisitionError) as ei:
            _enumerate(tmp_path, git=git_shallow)
        assert ei.value.blocker_class == "snapshot-drift"

    def test_blocks_on_dirty_worktree(self, tmp_path):
        git = FakeGit({"AGENTS.md": "x"}, porcelain=" M f.py\n")
        with pytest.raises(acq.AcquisitionError) as ei:
            _enumerate(tmp_path, git=git)
        assert ei.value.blocker_class == "snapshot-drift"

    def test_blocks_on_non_remote_head(self, tmp_path):
        with pytest.raises(acq.AcquisitionError) as ei:
            _enumerate(tmp_path, gh=FakeGh(head_remote=False))
        assert ei.value.blocker_class == "snapshot-drift"

    def test_blocks_on_head_mismatch(self, tmp_path):
        git = FakeGit({"AGENTS.md": "x"}, head="0" * 40)
        with pytest.raises(acq.AcquisitionError) as ei:
            _enumerate(tmp_path, git=git)
        assert ei.value.blocker_class == "snapshot-drift"

    def test_required_authority_unavailable_blocks(self, tmp_path):
        # AGENTS.md in ls-tree but unreadable at base -> authority-missing
        git = FakeGit({"AGENTS.md": "x"})
        orig = git.__call__

        def flaky(args):
            if args[0] == "show" and args[1].endswith(":AGENTS.md"):
                return 1, "", "corrupt object"
            return orig(args)
        with pytest.raises(acq.AcquisitionError) as ei:
            _enumerate(tmp_path, git=flaky)
        assert ei.value.blocker_class == "authority-missing"

    def test_optional_authority_degrades_to_unavailable(self, tmp_path):
        gh = FakeGh(issues={})  # issue 12 fetch 404s
        summary, out_dir, _s = _enumerate(tmp_path, gh=gh)
        data = json.loads((out_dir / "data.json").read_text())
        unavailable = [a for a in data["manifest_payload"]["authorities"]
                       if a["availability"] == "unavailable"]
        assert unavailable and unavailable[0]["failure_sha256"]
        assert unavailable[0]["kind"] == "issue"

    def test_feedback_resolved_before_freeze_still_enumerated(self, tmp_path):
        threads = [{
            "id": "PRRT_1", "isResolved": True, "isOutdated": False,
            "path": "a.py", "line": 3,
            "comments": {"pageInfo": {"hasNextPage": False},
                         "nodes": [{"body": "nit", "author": {"login": "rev"},
                                    "createdAt": "2026-01-01T00:00:00Z"}]},
        }]
        _sum, out_dir, _s = _enumerate(tmp_path, gh=FakeGh(threads=threads))
        data = json.loads((out_dir / "data.json").read_text())
        fb = [a for a in data["manifest_payload"]["authorities"]
              if a["kind"] == "review-feedback"]
        assert len(fb) == 1 and fb[0]["availability"] == "loaded"
        findings = data["findings"]
        assert any(f["source_kind"] == "feedback" and f["disposition"] == "open"
                   for f in findings)

    def test_pr_metadata_projection_excludes_lifecycle(self, tmp_path):
        _s1, out1, _ = _enumerate(tmp_path / "a", gh=FakeGh(pr=_pr_meta(isDraft=True)))
        _s2, out2, _ = _enumerate(tmp_path / "b", gh=FakeGh(pr=_pr_meta(isDraft=False)))
        d1 = json.loads((out1 / "data.json").read_text())
        d2 = json.loads((out2 / "data.json").read_text())
        assert d1["snapshot"]["pr_metadata_sha256"] == \
            d2["snapshot"]["pr_metadata_sha256"]

    def test_manifest_payload_field_contract(self, tmp_path):
        _s, out_dir, _ = _enumerate(tmp_path)
        data = json.loads((out_dir / "data.json").read_text())
        payload = data["manifest_payload"]
        assert set(payload) == set(model.MANIFEST_PAYLOAD_FIELDS)
        assert "authority_manifest_id" not in payload


class TestEnumerateFeedback:
    def test_threads_and_changes_requested_enumerated(self):
        threads = [{"id": "T1", "isResolved": False, "isOutdated": False,
                    "path": "a.py", "line": 1,
                    "comments": {"pageInfo": {"hasNextPage": False}, "nodes": []}}]
        reviews = [{"id": "R1", "state": "CHANGES_REQUESTED", "body": "fix",
                    "author": {"login": "x"}, "submittedAt": "t"}]
        items = fbp.enumerate_feedback(
            run_gh=FakeGh(threads=threads, reviews=reviews), pr_url=PR_URL)
        ids = {i.canonical_id for i in items}
        assert ids == {"github:thread:T1", "github:review:R1"}

    def test_next_page_fails_closed(self):
        gh = FakeGh()
        orig = gh.__call__

        def paged(args):
            rc, out, err = orig(args)
            if args[0] == "api" and args[1] == "graphql":
                obj = json.loads(out)
                obj["data"]["repository"]["pullRequest"]["reviewThreads"][
                    "pageInfo"]["hasNextPage"] = True
                return rc, json.dumps(obj), err
            return rc, out, err
        with pytest.raises(fbp.FeedbackPolicyError):
            fbp.enumerate_feedback(run_gh=paged, pr_url=PR_URL)

    def test_graphql_errors_fail_closed(self):
        with pytest.raises(fbp.FeedbackPolicyError):
            fbp.enumerate_feedback(run_gh=FakeGh(graphql_error=True), pr_url=PR_URL)

    def test_severity_table(self):
        items = [
            fbp.FeedbackItem("github:review:R1", "github", "R1",
                             "unresolved", "x" * 64, b"r"),
            fbp.FeedbackItem("github:thread:T1", "github", "T1",
                             "unresolved", "y" * 64, b"t"),
            fbp.FeedbackItem("github:thread:T2", "github", "T2",
                             "resolved", "z" * 64, b"t2"),
        ]
        findings = fbp.feedback_findings(items, policy=fbp.default_policy())
        sev = {f["source_id"]: f["severity"] for f in findings}
        assert sev["github:review:R1"] == "blocking"
        assert sev["github:thread:T1"] == "important"
        assert sev["github:thread:T2"] == "minor"

    def test_history_digests_split_unresolved(self):
        items = [
            fbp.FeedbackItem("github:thread:T1", "github", "T1",
                             "unresolved", "y" * 64, b"t"),
            fbp.FeedbackItem("github:thread:T2", "github", "T2",
                             "resolved", "z" * 64, b"t2"),
        ]
        assert fbp.feedback_history_sha256(items) != \
            fbp.unresolved_feedback_sha256(items)


class TestLoadAcquisition:
    def test_acquire_freeze_builds_witness_and_payload(self, tmp_path):
        summary, out_dir, scratch = _enumerate(tmp_path)
        _transcript_with_marker(scratch, summary["enumeration_id"],
                                out_dir=out_dir)
        src = _source(out_dir, scratch)
        payload = src.acquire(action="freeze-review-input", current_snapshot=None)
        env = json.loads(payload.raw_data)
        assert set(env["data"]) == set(
            policy.ACTION_PAYLOAD_KEYS["freeze-review-input"])
        witnesses = env["witnesses"]
        assert len(witnesses) == 1
        rec = witnesses[0]
        assert rec["kind"] == "authority-discovery"
        assert rec["record_positions"] and rec["chain_head_at_record"]
        assert rec["transcript_range"]["session_id"] == "s1"
        # verify with the Task-1 verifier
        verifier = witness_log.TranscriptWitnessVerifier(
            witness_log.TranscriptWitnessPolicy(
                transcript_root=scratch / "transcripts",
                witness_root=scratch / "witness"),
            witness_root=scratch / "witness", review_id="rev-1")
        snap = env["data"]["snapshot"]
        data = json.loads((out_dir / "data.json").read_text())
        subject = model.authority_discovery_subject(snap, data["manifest_payload"])
        verified = verifier.verify(
            stored_record_bytes=model.canonical_json(rec),
            expected_kind="authority-discovery",
            expected_review_id="rev-1",
            expected_dispatch_id=None,
            expected_snapshot_epoch=snap["epoch"],
            expected_snapshot_fingerprint=snap["fingerprint"],
            expected_subject=model.canonical_json(subject),
            expected_tool_use_id=rec["tool_use_id"],
            expected_agent_id=None,
        )
        assert verified.kind == "authority-discovery"

    def test_acquire_refresh_epoch_plus_one_and_drift_reasons(self, tmp_path):
        # second enumeration on a different head + all feedback resolved
        git2 = FakeGit({"AGENTS.md": "# law"}, head="9" * 40, tree="8" * 40,
                       diff="new-diff")
        gh2 = FakeGh(pr=_pr_meta(headRefOid="9" * 40),
                     threads=[{"id": "T1", "isResolved": True,
                               "isOutdated": False, "path": "a.py", "line": 1,
                               "comments": {"pageInfo": {"hasNextPage": False},
                                            "nodes": []}}])
        gh2_a = FakeGh(threads=[{"id": "T1", "isResolved": False,
                                 "isOutdated": False, "path": "a.py", "line": 1,
                                 "comments": {"pageInfo": {"hasNextPage": False},
                                              "nodes": []}}])
        # first enumerate must include the unresolved thread so unresolved
        # digest differs after resolution; refresh re-uses the same scratch
        # root so the witness-policy digest stays constant
        scratch = _scratch(tmp_path)
        out1 = scratch / "acquire" / "e1"
        acq.enumerate_acquisition(
            run_git=FakeGit({"AGENTS.md": "# law"}), run_gh=gh2_a,
            repo_root=tmp_path, pr_number=7, out_dir=out1,
            scratch_dir=scratch)
        d1 = json.loads((out1 / "data.json").read_text())
        old_snap = dict(d1["snapshot"])
        old_snap["fingerprint"] = model.snapshot_fingerprint(old_snap)
        out2 = scratch / "acquire" / "e2"
        summary2 = acq.enumerate_acquisition(
            run_git=git2, run_gh=gh2, repo_root=tmp_path, pr_number=7,
            out_dir=out2, scratch_dir=scratch, epoch=old_snap["epoch"] + 1)
        _transcript_with_marker(scratch, summary2["enumeration_id"],
                                out_dir=out2)
        src = _source(out2, scratch)
        payload = src.acquire(action="refresh-review-input",
                              current_snapshot=old_snap)
        env = json.loads(payload.raw_data)
        snap = env["data"]["snapshot"]
        assert snap["epoch"] == old_snap["epoch"] + 1
        assert set(env["data"]["drift_reasons"]) == {
            "head_sha", "tree_sha", "diff_sha256", "authority_manifest",
            "feedback_history", "unresolved_feedback"}

    def test_refresh_requires_current_snapshot(self, tmp_path):
        summary, out_dir, scratch = _enumerate(tmp_path)
        _transcript_with_marker(scratch, summary["enumeration_id"],
                                out_dir=out_dir)
        src = _source(out_dir, scratch)
        with pytest.raises(acq.AcquisitionError):
            src.acquire(action="refresh-review-input", current_snapshot=None)

    def test_missing_marker_in_transcript_fails_closed(self, tmp_path):
        summary, out_dir, scratch = _enumerate(tmp_path)
        _transcript_with_marker(scratch, "0" * 64, out_dir=out_dir)
        src = _source(out_dir, scratch)
        with pytest.raises(Exception):
            src.acquire(action="freeze-review-input", current_snapshot=None)

    def test_acquired_dir_tamper_detected(self, tmp_path):
        summary, out_dir, scratch = _enumerate(tmp_path)
        _transcript_with_marker(scratch, summary["enumeration_id"],
                                out_dir=out_dir)
        ev = out_dir / "evidence"
        victim = next(ev.iterdir())
        if victim.name == "manifest.json":
            victim = next(p for p in ev.iterdir() if p.name != "manifest.json")
        raw = bytearray(victim.read_bytes())
        raw[0] ^= 0xFF
        victim.write_bytes(bytes(raw))
        src = _source(out_dir, scratch)
        with pytest.raises(acq.AcquisitionError):
            src.acquire(action="freeze-review-input", current_snapshot=None)

    def test_resolve_between_enumerate_and_refresh(self, tmp_path):
        unresolved = [{"id": "T1", "isResolved": False, "isOutdated": False,
                       "path": "a.py", "line": 1,
                       "comments": {"pageInfo": {"hasNextPage": False},
                                    "nodes": []}}]
        resolved = [dict(unresolved[0], isResolved=True)]
        _s1, out1, _ = _enumerate(tmp_path / "a", gh=FakeGh(threads=unresolved))
        _s2, out2, _ = _enumerate(tmp_path / "b", gh=FakeGh(threads=resolved))
        d2 = json.loads((out2 / "data.json").read_text())
        items = [a for a in d2["manifest_payload"]["authorities"]
                 if a["kind"] == "review-feedback"]
        assert len(items) == 1
        # finding still ships open; lifecycle owns closure
        f = [x for x in d2["findings"] if x["source_kind"] == "feedback"]
        assert f and f[0]["disposition"] == "open"
