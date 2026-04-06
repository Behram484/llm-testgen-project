# Lab PC Setup And Run Guide

This document is the step-by-step checklist for bringing up a new lab PC and running the local LLM test-generation experiments safely.

## 1. Things to install or prepare

Install or prepare these on each new lab PC:

- Git for Windows
- Python 3.x
- Ollama for Windows
- JDK 17
- Apache Maven 3.9.x
- This repository: `llm-testgen-project`

Recommended local paths used in the examples below:

- repo root: `C:\Users\<YOUR_USERNAME>\llm-testgen-project`
- runner: `C:\Users\<YOUR_USERNAME>\llm-testgen-project\testgen-runner`
- lab project: `C:\Users\<YOUR_USERNAME>\llm-testgen-project\testgen-lab`
- JDK 17: `C:\Users\<YOUR_USERNAME>\jdk-17.0.18+8`
- Maven: `C:\Users\<YOUR_USERNAME>\apache-maven-3.9.14`

If the machine blocks installers, prefer ZIP packages for JDK and Maven, then extract them into your user directory.

## 2. Clone the project

Open PowerShell and run:

```powershell
cd C:\Users\<YOUR_USERNAME>
git clone <YOUR_GIT_REPO_URL> llm-testgen-project
cd C:\Users\<YOUR_USERNAME>\llm-testgen-project
```

If `git` is not recognized, install Git for Windows first.

## 3. Check Python

```powershell
python --version
```

If Python is not recognized, install Python and reopen PowerShell.

## 4. Check or install Ollama

Check whether Ollama is available:

```powershell
ollama --version
ollama list
```

If Ollama is not installed, install it first, then reopen PowerShell.

Pull the model needed for the experiment:

```powershell
ollama pull qwen2.5-coder:32b
```

Optional extra model for 7B experiments:

```powershell
ollama pull deepseek-coder:6.7b
```

Confirm the model exists locally:

```powershell
ollama list
```

## 5. Check JDK 17

If you installed or extracted JDK 17 into your user directory, test it directly:

```powershell
& "C:\Users\<YOUR_USERNAME>\jdk-17.0.18+8\bin\java.exe" -version
```

You want to see Java 17 in the output.

## 6. Check Maven

If Maven is extracted into your user directory, test it directly:

```powershell
cmd /c ""C:\Users\<YOUR_USERNAME>\apache-maven-3.9.14\bin\mvn.cmd" -version"
```

You want to see:

- Apache Maven version information
- `Java version: 17...`

## 7. Update `config.json`

Open:

- `C:\Users\<YOUR_USERNAME>\llm-testgen-project\testgen-runner\config\config.json`

At minimum, make sure these fields are correct for the current machine:

```json
{
  "project_root": "C:/Users/<YOUR_USERNAME>/llm-testgen-project/testgen-lab",
  "model": "qwen2.5-coder:32b",
  "prompt_profile": "semantic_repair",
  "generation_profile": "baseline_behavior",
  "mvn_cmd": "C:/Users/<YOUR_USERNAME>/apache-maven-3.9.14/bin/mvn.cmd",
  "max_repair_attempts": 5,
  "artifact_write_mode": "minimal"
}
```

Useful experiment variants:

### Main 32B baseline run

```json
"model": "qwen2.5-coder:32b",
"generation_profile": "baseline_behavior",
"max_repair_attempts": 5
```

### 32B attempts ablation

```json
"model": "qwen2.5-coder:32b",
"generation_profile": "baseline_behavior",
"max_repair_attempts": 15
```

### 32B prompt ablation

```json
"model": "qwen2.5-coder:32b",
"generation_profile": "detailed_behavior",
"max_repair_attempts": 5
```

Important rule:

- For a fair experiment, change only the variable you are testing.
- Keep `prompt_profile` as `semantic_repair`.
- Use clean `output` directories for independent runs.

## 8. Clean the output directory before each formal run

Go to the runner directory:

```powershell
cd C:\Users\<YOUR_USERNAME>\llm-testgen-project\testgen-runner
```

If you already archived the previous results, clean the active `output` directory so only `README.md` remains.

Example cleanup command:

```powershell
Get-ChildItem -LiteralPath .\output -Force |
Where-Object { $_.Name -ne 'README.md' } |
Remove-Item -Recurse -Force
```

This will also remove `last_successful`, which is required for cold-start repeated runs.

## 9. Run the verified preflight script

The repository includes a helper script that checks:

- Java is really 17
- Maven is really using Java 17
- Python works
- Ollama is installed
- the configured model exists locally
- the output directory is clean

Run the preflight first:

```powershell
cd C:\Users\<YOUR_USERNAME>\llm-testgen-project\testgen-runner
.\start_verified_batch.ps1 -JdkHome "C:\Users\<YOUR_USERNAME>\jdk-17.0.18+8" -RunLabel "pc1-32b-main-run1" -NoRun
```

If everything is correct, you should see:

```text
[PASS] Environment verified for Java 17 batch run.
[INFO] NoRun specified; batch not started.
```

## 10. Start the actual batch run

After the preflight passes, remove `-NoRun`:

```powershell
cd C:\Users\<YOUR_USERNAME>\llm-testgen-project\testgen-runner
.\start_verified_batch.ps1 -JdkHome "C:\Users\<YOUR_USERNAME>\jdk-17.0.18+8" -RunLabel "pc1-32b-main-run1"
```

Suggested run labels:

- `pc1-32b-main-run1`
- `pc2-32b-main-run2`
- `pc3-32b-main-run3`
- `pc4-32b-attempt15-run1`

## 11. Manual fallback if the script is not available

If needed, you can still verify the environment manually:

```powershell
cd C:\Users\<YOUR_USERNAME>\llm-testgen-project\testgen-runner

$env:JAVA_HOME="C:\Users\<YOUR_USERNAME>\jdk-17.0.18+8"
$env:Path="$env:JAVA_HOME\bin;$env:Path"

& "$env:JAVA_HOME\bin\java.exe" -version
cmd /c ""C:\Users\<YOUR_USERNAME>\apache-maven-3.9.14\bin\mvn.cmd" -version"
python --version
ollama list
```

If Java and Maven both show version 17, then you can run:

```powershell
python batch_runner.py
```

## 12. Multi-machine reminders

When using multiple lab PCs in parallel:

- each machine should have its own clean local output
- do not let multiple machines write into the same live output folder
- use one run label per machine and per run
- archive results after each run before starting the next one
- keep the environment the same across machines when comparing runs

## 13. Quick start checklist

Use this short checklist on every new lab PC:

1. Install Git, Python, Ollama, JDK 17, Maven.
2. Clone `llm-testgen-project`.
3. Pull `qwen2.5-coder:32b` with Ollama.
4. Update `config.json` paths for this machine.
5. Clean `testgen-runner\output`.
6. Run `start_verified_batch.ps1 ... -NoRun`.
7. Confirm `[PASS]`.
8. Run the same command without `-NoRun`.

## 14. Troubleshooting

### `git` is not recognized

Install Git for Windows, then reopen PowerShell.

### `ollama` is not recognized

Install Ollama, then reopen PowerShell.

### `mvn` says Java 25

Do not start the batch. Fix JDK first and rerun the preflight.

### The preflight says output is not clean

Archive old results, then clean `testgen-runner\output` and rerun the preflight.

### The model is missing

Run:

```powershell
ollama pull qwen2.5-coder:32b
```

Then rerun:

```powershell
ollama list
```

### The script fails because `mvn_cmd` does not exist

Open `config.json` and make sure `mvn_cmd` points to the real file, for example:

```json
"mvn_cmd": "C:/Users/<YOUR_USERNAME>/apache-maven-3.9.14/bin/mvn.cmd"
```

Not just the `bin` folder.
