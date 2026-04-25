param(
    [string]$JdkHome,
    [string]$RunLabel = "batch",
    [switch]$NoRun,
    [switch]$AllowDirtyOutput
)

$ErrorActionPreference = "Stop"

$runnerRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$configPath = Join-Path $runnerRoot "config\config.json"
$outputDir = Join-Path $runnerRoot "output"
$manifestDir = Join-Path $runnerRoot "run_manifests"

function Fail([string]$Message) {
    Write-Host ""
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    exit 1
}

function Note([string]$Message) {
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Capture-Command([string]$Command, [string[]]$Arguments) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.WorkingDirectory = $runnerRoot
    $quotedArgs = $Arguments | ForEach-Object {
        if ($_ -match '[\s"]') {
            '"' + ($_ -replace '"', '\"') + '"'
        }
        else {
            $_
        }
    }
    $commandExt = [System.IO.Path]::GetExtension($Command)
    if ($commandExt -in @(".cmd", ".bat")) {
        $quotedCommand = '"' + ($Command -replace '"', '\"') + '"'
        $psi.FileName = "cmd.exe"
        $psi.Arguments = "/d /c $quotedCommand " + ($quotedArgs -join " ")
    }
    else {
        $psi.FileName = $Command
        $psi.Arguments = ($quotedArgs -join " ")
    }

    $proc = New-Object System.Diagnostics.Process
    $proc.StartInfo = $psi
    try {
        $null = $proc.Start()
    }
    catch {
        throw "Failed to start command: $($psi.FileName) $($psi.Arguments)`n$($_.Exception.Message)"
    }
    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    $proc.WaitForExit()
    $text = ($stdout + $stderr).Trim()
    $exitCode = $proc.ExitCode

    return [pscustomobject]@{
        ExitCode = $exitCode
        Text = $text.Trim()
    }
}

if (-not (Test-Path -LiteralPath $configPath)) {
    Fail "Missing config file: $configPath"
}

$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json

if (-not $JdkHome) {
    $JdkHome = $env:JAVA_HOME
}

if (-not $JdkHome) {
    Fail "JdkHome not provided and JAVA_HOME is empty."
}

$javaExe = Join-Path $JdkHome "bin\java.exe"
if (-not (Test-Path -LiteralPath $javaExe)) {
    Fail "java.exe not found under JdkHome: $javaExe"
}

$env:JAVA_HOME = $JdkHome
$existingPathParts = @()
if ($env:Path) {
    $existingPathParts = $env:Path -split ";" | Where-Object { $_ }
}
$env:Path = (@("$JdkHome\bin") + $existingPathParts | Select-Object -Unique) -join ";"

if (-not (Test-Path -LiteralPath $config.project_root)) {
    Fail "Configured project_root does not exist: $($config.project_root)"
}

$mvnCmd = $config.mvn_cmd
if (-not (Test-Path -LiteralPath $mvnCmd)) {
    Fail "Configured mvn_cmd does not exist: $mvnCmd"
}

$javaInfo = Capture-Command $javaExe @("-version")
if ($javaInfo.ExitCode -ne 0) {
    Fail "java -version failed.`n$($javaInfo.Text)"
}
if ($javaInfo.Text -notmatch 'version "17\.') {
    Fail "java -version is not Java 17.`n$($javaInfo.Text)"
}

$mvnInfo = Capture-Command $mvnCmd @("-version")
if ($mvnInfo.ExitCode -ne 0) {
    Fail "mvn -version failed.`n$($mvnInfo.Text)"
}
if ($mvnInfo.Text -notmatch 'Java version:\s*17\.') {
    Fail "Maven is not using Java 17.`n$($mvnInfo.Text)"
}

$pythonInfo = Capture-Command "python" @("--version")
if ($pythonInfo.ExitCode -ne 0) {
    Fail "python --version failed.`n$($pythonInfo.Text)"
}

$ollamaCmd = Get-Command "ollama" -ErrorAction SilentlyContinue
if (-not $ollamaCmd) {
    Fail "ollama command not found in PATH."
}

$ollamaInfo = Capture-Command $ollamaCmd.Source @("list")
if ($ollamaInfo.ExitCode -ne 0) {
    Fail "ollama list failed.`n$($ollamaInfo.Text)"
}
if ($config.model -and ($ollamaInfo.Text -notmatch [regex]::Escape($config.model))) {
    Fail "Configured model '$($config.model)' not found in ollama list."
}

if (-not (Test-Path -LiteralPath $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$outputItems = Get-ChildItem -LiteralPath $outputDir -Force
$nonReadmeItems = @($outputItems | Where-Object { $_.Name -ne "README.md" })
if ($nonReadmeItems.Count -gt 0 -and -not $AllowDirtyOutput) {
    $names = ($nonReadmeItems | Select-Object -ExpandProperty Name) -join ", "
    Fail "output is not clean. Remove/archive these first: $names"
}

if (-not (Test-Path -LiteralPath $manifestDir)) {
    New-Item -ItemType Directory -Path $manifestDir | Out-Null
}

$configHash = (Get-FileHash -LiteralPath $configPath -Algorithm SHA256).Hash
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$computer = if ($env:COMPUTERNAME) { $env:COMPUTERNAME } else { "unknown-host" }
$manifestPath = Join-Path $manifestDir "$timestamp-$computer-$RunLabel.txt"

$manifestLines = @(
    "timestamp_local=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "computer_name=$computer",
    "run_label=$RunLabel",
    "runner_root=$runnerRoot",
    "project_root=$($config.project_root)",
    "config_path=$configPath",
    "config_sha256=$configHash",
    "java_home=$JdkHome",
    "model=$($config.model)",
    "prompt_profile=$($config.prompt_profile)",
    "generation_profile=$($config.generation_profile)",
    "max_repair_attempts=$($config.max_repair_attempts)",
    "enable_mutation_augment=$($config.enable_mutation_augment)",
    "artifact_write_mode=$($config.artifact_write_mode)",
    "output_clean=$($nonReadmeItems.Count -eq 0)",
    "",
    "[java -version]",
    $javaInfo.Text,
    "",
    "[mvn -version]",
    $mvnInfo.Text,
    "",
    "[python --version]",
    $pythonInfo.Text,
    "",
    "[ollama list]",
    $ollamaInfo.Text
)

Set-Content -LiteralPath $manifestPath -Value $manifestLines

Write-Host ""
Write-Host "=== Verified Batch Preflight ===" -ForegroundColor Green
Write-Host "Computer: $computer"
Write-Host "Run label: $RunLabel"
Write-Host "JAVA_HOME: $JdkHome"
Write-Host "Model: $($config.model)"
Write-Host "Prompt profile: $($config.prompt_profile)"
Write-Host "Generation profile: $($config.generation_profile)"
Write-Host "Max repair attempts: $($config.max_repair_attempts)"
Write-Host "Manifest: $manifestPath"
Write-Host ""
Write-Host $javaInfo.Text
Write-Host ""
Write-Host $mvnInfo.Text
Write-Host ""
Write-Host $pythonInfo.Text
Write-Host ""
Write-Host "[PASS] Environment verified for Java 17 batch run." -ForegroundColor Green

if ($NoRun) {
    Write-Host "[INFO] NoRun specified; batch not started." -ForegroundColor Yellow
    exit 0
}

Push-Location $runnerRoot
try {
    & python batch_runner.py
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
