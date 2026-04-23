# Frozen Experiment Configuration — Follow-up v2

Frozen: 2026-04-22
Purpose: Pin all experiment parameters before the guided-lite follow-up run.
Any change after this date must be documented as a deviation.

---

## 1. Dataset (CUT Inventory)

Total: **40 CUTs**, all byte-identical to SF110-20130704-src originals.
Source directory: `D:\Project\testgen-lab\src\main\java`

| # | CUT | SF110 Project |
|--:|-----|---------------|
| 1 | ArrayUtil | 89_jiggler |
| 2 | Axis | 24_saxpath |
| 3 | Base32 | 104_vuze |
| 4 | Base64 | 7_sfmis |
| 5 | Base64Coder | 33_javaviewcontrol |
| 6 | BigDecimalUtil | 108_liferay |
| 7 | BinaryDisplayConverter | 102_squirrel-sql |
| 8 | ByteVector | 80_wheelwebtool |
| 9 | CaselessStringMap | 78_caloriecount |
| 10 | CommandLine | 66_openjms |
| 11 | DateTools | 96_heal |
| 12 | DateUtil | 92_jcvi-javacommon |
| 13 | DisplayHelper | 30_bpmail |
| 14 | EmailFacadeState | 30_bpmail |
| 15 | FilterMatcher | 102_squirrel-sql |
| 16 | GridLayout2 | 97_feudalismgame |
| 17 | HashCodeUtils | 104_vuze |
| 18 | HtmlEncoder | 36_schemaspy |
| 19 | IndexedString | 39_diffi |
| 20 | Inflection | 36_schemaspy |
| 21 | InspirentoUtilities | 17_inspirento |
| 22 | MapUtil | 78_caloriecount |
| 23 | MathUtil | 92_jcvi-javacommon |
| 24 | NaturalSort | 35_corina |
| 25 | ObjectsUtil | 92_jcvi-javacommon |
| 26 | Reference | 5_templateit |
| 27 | Region | 5_templateit |
| 28 | SAXPathException | 24_saxpath |
| 29 | SimpleCounter | 108_liferay |
| 30 | SortedArrayList | 108_liferay |
| 31 | SortedMapVector | 105_freemind |
| 32 | StringComparator | 35_corina |
| 33 | StringEncoder64 | 73_fim1 |
| 34 | StringLink | 39_diffi |
| 35 | StringList | 91_classviewer |
| 36 | StringUtils | 35_corina |
| 37 | ToStringConverter | 63_objectexplorer |
| 38 | UniqueTimestampGenerator | 44_summa |
| 39 | Util | 1_tullibee |
| 40 | Version | 36_schemaspy |

Constraint: No additions, removals, or source modifications after freeze.
Deviation recorded 2026-04-23: five legacy/non-target CUTs were replaced before rerunning the baseline so the benchmark remains a 40-CUT UTF-8 compilable SF110 subset.

---

## 2. Generation Prompts (frozen text)

Three generation profiles are used. Repair/augmentation prompts are shared
across all profiles.

### Generation prompts

| File | Bytes | SHA-256 (prefix) | Role |
|------|------:|-------------------|------|
| baseline_behavior.txt | 1655 | 5a37133f27303389 | standard profile |
| guided_lite_behavior.txt | 2252 | 74b6e8d8beb61c42 | guided-lite profile (new) |
| detailed_behavior.txt | 3220 | 103b4885828b3ec7 | detailed profile |

### Repair & augmentation prompts (shared across all profiles)

| File | Bytes | SHA-256 (prefix) |
|------|------:|-------------------|
| compile_repair.txt | 1107 | 8d435503ea145262 |
| semantic_repair.txt | 1626 | d9dfa7556fb1dde0 |
| mutation_augment.txt | 857 | 9abc6afb2cce1998 |

Constraint: No wording changes after freeze. If a prompt must be changed,
create a new versioned file and document the deviation.

---

## 3. Model & Inference Configuration

### Model identity

| Parameter | Value |
|-----------|-------|
| Ollama model tag | `deepseek-coder:6.7b` |
| Ollama model ID | `ce298d984115` |
| Architecture | llama |
| Parameters | 6.7B |
| Quantisation | Q4_0 |
| Context length | 16384 |
| Embedding length | 4096 |
| Ollama version | 0.21.0 |

### Inference parameters

`runner.py` calls `ollama run <model>` via stdin/stdout with **no explicit
parameter overrides**. All sampling parameters therefore use Ollama runtime
defaults for this model.

| Parameter | Value | Source |
|-----------|-------|--------|
| temperature | 0.8 | Ollama default (not pinned) |
| top_p | 0.9 | Ollama default (not pinned) |
| top_k | 40 | Ollama default (not pinned) |
| repeat_penalty | 1.1 | Ollama default (not pinned) |
| seed | 0 (random) | Ollama default (not pinned) |
| num_ctx | 16384 | Model-defined |
| num_predict | -1 (unlimited) | Ollama default (not pinned) |

**Known limitation**: Sampling parameters are not explicitly pinned in this
experiment. Results are therefore configuration-documented rather than
fully parameter-frozen. This is consistent with the main experiment and
noted as a limitation in the paper (Section 5).

To pin in the future, pass parameters via Ollama API or Modelfile override.

---

## 4. Pipeline Version

### Core scripts

| File | SHA-256 (prefix) |
|------|-------------------|
| runner.py | 7ac12d690a8da2b7 |
| batch_runner.py | 53dba204cb32a8ce |
| mutant_summary.py | 1503d12bd75d3671 |

### Build

| File | SHA-256 (prefix) |
|------|-------------------|
| pom.xml (testgen-lab) | 47879022886adcec |

### Auxiliary scripts (not part of experiment pipeline)

| File | SHA-256 (prefix) |
|------|-------------------|
| provenance_audit.py | c78b7a90cc50428b |
| cleanup_runner_output.py | b0793720cf844e8f |
| summarize_batch.py | 1cfbb5b23835dee1 |
| run_prompt_profile_followup.py | e30149b967fd84fc |

Constraint: No changes to runner.py, batch_runner.py, mutant_summary.py,
or pom.xml after freeze. If a bug fix is necessary, document the change
and re-hash.

---

## 5. Evaluation Configuration

### From config.json

| Parameter | Value | Notes |
|-----------|-------|-------|
| max_repair_attempts | 5 | Repair budget per CUT per run (aligned with main experiment) |
| regenerate_after_same_failures | 2 | Consecutive same-failure threshold for regen |
| enable_programmatic_fix | true | Auto-patch assertEquals with correct actual |
| enable_mutation_augment | true | Mutation-guided augmentation enabled |
| enable_cut_api_prepass | true | Static API hallucination gate |
| enable_compile_failure_family_regen | true | Regen on repeated compile failures |
| inject_method_signatures_in_prompts | true | Inject public API signatures into all prompts |
| mvn_timeout_sec | 500 | Maven subprocess timeout |
| ollama_timeout_sec | 180 | LLM subprocess timeout |
| artifact_write_mode | minimal | Prompt/raw-LLM artifact writing |
| prompt_profile | semantic_repair | Repair prompt selection |
| mvn_cmd | D:/University of Sussex/3rd Year/apache-maven-3.9.12/bin/mvn.cmd | Maven path |
| project_root | D:/Project/testgen-lab | Project root |

### Derived evaluation parameters

| Parameter | Value |
|-----------|-------|
| batch_runner timeout per CUT | 900 sec |
| JUnit version | 5 (jupiter) via pom.xml |
| Mutation tool | PIT (pitest-maven) via pom.xml |
| Success criterion | mvn test pass + PIT report generated |

Constraint: No changes to evaluation config after freeze.

---

## 6. Follow-up Experiment Matrix

This follow-up tests one factor: **generation_profile**.

| Run | generation_profile | Model |
|-----|--------------------|-------|
| A | baseline_behavior | deepseek-coder:6.7b |
| B | guided_lite_behavior | deepseek-coder:6.7b |
| C | detailed_behavior | deepseek-coder:6.7b |

All other parameters are held constant across runs A, B, C.
Each run processes all 40 CUTs via batch_runner.py.

---

## Deviation Log

| Date | Item Changed | Old Value | New Value | Reason |
|------|-------------|-----------|-----------|--------|
| 2026-04-22 | max_repair_attempts | 15 | 5 | Align with main experiment repair budget; follow-up tests prompt effect under identical conditions |
