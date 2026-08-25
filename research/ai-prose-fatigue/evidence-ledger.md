# Evidence ledger: AI prose fatigue

## Reading this ledger

Each family separates measured evidence from a bounded operational inference and a working hypothesis. A later profile may use only the bounded operational inference stated here; it must keep the listed limitations and preservation condition visible. None of these entries supports an AI-authorship verdict, detector score, universal word ban, or intentional degradation of prose.

### 1. Lexical concentration and repeated stock transitions

- **Evidence class:** Primary empirical corpus study; primary empirical domain-specific study.
- **Observed domain:** Kobak et al. measured post-2022 corpus-level excess vocabulary in PubMed biomedical abstracts, while Miletić and Falk studied ACL/NLP scholarly prose and synthetic improvements.
- **Measured finding:** Both records report lexical change in their respective scholarly domains; Kobak et al. measured style-word frequency shifts at corpus level, and Miletić and Falk report lower lexical diversity in their LLM-modified passages.
- **Bounded operational inference:** A repeated stock transition or phrase cluster is a candidate for a local, meaning-preserving review only when recurrence is visible in the supplied draft. Do not flag a word merely because it appears in a source.
- **Preserve when:** The recurrence establishes cadence, a motif, accessible cohesion, terminology consistency, or an intentional refrain.
- **Limitations:** Neither result identifies an individual text or covers all prose. The studies do not establish a word ban or prove that lexical repetition reduces quality.
- **Source IDs:** `kobak-2025-excess-vocabulary`, `miletic-falk-2026-scientific-communication`.

### 2. Structural regularity and paragraph-shape repetition

- **Evidence class:** Primary empirical domain-specific study; primary empirical multidomain study.
- **Observed domain:** LLM-modified NLP scholarly passages and multi-domain LLM rewrites.
- **Measured finding:** Miletić and Falk report certain syntactic constructions more frequently in LLM-modified texts. Sourati et al. report reduced writing-complexity variance across their datasets and tested models.
- **Bounded operational inference:** Review repetitive local paragraph or sentence shapes as a pattern cluster, not as a defect by default. Any repair should be the smallest one that clarifies a concrete audience need.
- **Preserve when:** Parallel form makes comparison, instruction, rhythm, legal precision, accessibility, or an argument’s sequence easier to follow.
- **Limitations:** The measurements depend on model, prompt, corpus, and complexity definition. They do not make varied sentence shape inherently better.
- **Source IDs:** `miletic-falk-2026-scientific-communication`, `sourati-2026-linguistic-diversity`.

### 3. Evaluative inflation and unsupported importance claims

- **Evidence class:** Working hypothesis, informed by primary empirical scholarly-domain studies.
- **Observed domain:** Biomedical and NLP scholarly writing, where measured shifts include style-affecting vocabulary and longer/more complex wording.
- **Measured finding:** The cited sources do not directly measure unsupported importance claims as a universal pattern.
- **Bounded operational inference:** Treat heightened evaluation as a factual-editing question: retain it only when the supplied evidence supports the claim. This is a general accuracy guard, not an AI-prose finding.
- **Preserve when:** The draft supplies a source, result, or clearly bounded rationale for the evaluation, or the text is intentionally persuasive and identifies its basis.
- **Limitations:** No ledger source licenses a list of inflated terms or a universal severity score. Do not label an author or text as AI-generated from evaluative language.
- **Source IDs:** `kobak-2025-excess-vocabulary`, `miletic-falk-2026-scientific-communication`.

### 4. Excessive signposting, summary repetition, and conclusion restatement

- **Evidence class:** Working hypothesis.
- **Observed domain:** No source in this ledger isolates signposting or conclusion restatement as a causal empirical finding.
- **Measured finding:** Not established by the registered sources.
- **Bounded operational inference:** Review only when the supplied reader goal shows that a repeated summary obscures rather than aids navigation. Prefer deletion or compression only after checking that the argument remains comprehensible.
- **Preserve when:** The audience needs orientation, the text is long or technical, a recap supports accessibility, or a conclusion distinguishes decision from evidence.
- **Limitations:** This is a testable drafting hypothesis, not a research-backed universal rule and not a detector feature.
- **Source IDs:** None; hypothesis deliberately retained as such.

### 5. Voice flattening and loss of culturally or personally meaningful variation

- **Evidence class:** Primary empirical controlled study; primary empirical multidomain study.
- **Observed domain:** Agarwal et al.’s Indian/US controlled autocomplete study and Sourati et al.’s seven datasets of LLM rewriting/use.
- **Measured finding:** Agarwal et al. report convergence toward American styles in the studied Indian-participant condition. Sourati et al. report reduced writing-complexity variance and suppression of some non-dominant patterns across their datasets and models.
- **Bounded operational inference:** When a user supplies current-task text or explicit preferences, derive only bounded tendencies and ask before overwriting distinctive choices. Do not retain their source corpus.
- **Preserve when:** A choice carries cultural context, identity, relationship, local register, deliberate informality, or a specific rhetorical purpose.
- **Limitations:** These studies do not identify a person’s culture from prose, judge a writer’s identity, or make all convergence harmful. They do not justify collecting or storing an author corpus.
- **Source IDs:** `agarwal-2025-cultural-homogenization`, `sourati-2026-linguistic-diversity`.

### 6. Legitimate-device preservation and false-positive risk

- **Evidence class:** Primary empirical tool audit; bounded inference from the other registered studies.
- **Observed domain:** Weber-Wulff et al.’s academic detector audit; the writing studies above each operate at a corpus, controlled-study, or model-rewrite level.
- **Measured finding:** Weber-Wulff et al. found the tested detectors unreliable in their audit conditions, with obfuscation worsening performance. Other sources do not establish authorship of individual texts.
- **Bounded operational inference:** Do not provide detector-evasion, detector scores, or AI-authorship conclusions. Do preserve deliberate devices unless their cost is concrete; offer a legitimate clarity/style revision when requested.
- **Preserve when:** Repetition, an em dash, a triad, contrast, rhetorical question, directness, or another device earns its place through meaning, rhythm, emphasis, or reader orientation.
- **Limitations:** The detector audit is dated and tool-specific; its boundary is abstention, not a claim that detection is impossible or a reason to evade it.
- **Source IDs:** `weber-wulff-2023-detection-tools`, `agarwal-2025-cultural-homogenization`, `sourati-2026-linguistic-diversity`.
