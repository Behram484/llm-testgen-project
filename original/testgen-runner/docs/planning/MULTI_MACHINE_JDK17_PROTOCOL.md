# Multi-Machine JDK17 Protocol

Use this protocol when running batch experiments across multiple lab PCs.

## Goal

Ensure every machine:

- uses Java 17 for both `java` and Maven
- uses the same `config.json`
- confirms the configured Ollama model exists locally
- starts only from a clean `output/`
- leaves an environment manifest for later audit

## Preflight Script

Run from `D:\Project\testgen-runner`:

```powershell
.\start_verified_batch.ps1 -JdkHome "C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot" -RunLabel "pc1-run1-32b" -NoRun
```

If the check passes, start the real batch:

```powershell
.\start_verified_batch.ps1 -JdkHome "C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot" -RunLabel "pc1-run1-32b"
```

The script will:

- set `JAVA_HOME`
- prepend the JDK `bin` directory in the current PowerShell session
- verify `java -version`
- verify `mvn -version`
- verify `python --version`
- verify the configured Ollama model is present
- refuse to run if `output/` is not clean
- write an audit report to `run_manifests/`

## Recommended Labels

- `pc1-32b-main-run1`
- `pc2-32b-main-run2`
- `pc3-32b-main-run3`
- `pc4-32b-attempt15-run1`

## Recommended Parallel Plan

If the main priority is the clean 32B baseline under JDK17:

1. PC1: `32B`, baseline prompt, `5 attempts`, run 1
2. PC2: `32B`, baseline prompt, `5 attempts`, run 2
3. PC3: `32B`, baseline prompt, `5 attempts`, run 3
4. PC4: keep free for retries or start the next ablation only after the main three runs are safely archived

## Rules

- Do not mix JDK17 and JDK25 data in the same comparison table.
- Do not start from a dirty `output/`.
- Do not change `config.json` after preflight without re-running the preflight script.
- Archive each finished `output/` immediately after the run completes.
