# Resolving a Pinned Standard Definition

Use the repository's declared subscription as the authority. It names a standard ID, source repository, immutable Git commit, definition path, and readable certification reference.

1. Read the selected record and identify its exact source repository, commit, and definition path.
2. Verify that the local checkout belongs to the declared source repository. Compare its configured source with the subscription using the repository's URL identity policy; do not infer identity from a familiar folder name.
3. If the commit is not available locally, report that fact. Retrieving it from the declared source is an explicit agent action. The helper does not clone or fetch.
4. Read the exact pinned path with `pinned_definition.py --source-root PATH --commit FULL_ID --definition RELATIVE_PATH --check`. The command returns the bytes from `git show COMMIT:PATH`; it does not use the current branch, working-tree contents, or the latest plugin definition as a fallback.
5. Assess the repository against those requirements and its readable certification. If the object or path is unavailable, report the missing authority and do not assess against a different revision.

An offline reference snapshot may help when the Git object cannot be retrieved, but the snapshot must identify the repository, full commit, and definition path, with evidence that it came from that pinned source. A downloaded Markdown file with no verifiable pin is not proof of historical authority.

The helper validates commit and path syntax and retrieves exact content. It does not prove the checkout identity, certify the definition's semantics, or determine whether the repository complies. Ambient plugin refresh changes available capability only; it does not change the subscription pin.
