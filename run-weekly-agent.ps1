# ========================================================================
# LifeAsCarers AI Agent Weekly Runner
# Runs the full Docker pipeline, waits for Ollama to become ready,
# executes the agentic_pipeline.py once, logs output, and shuts down cleanly.
# ========================================================================

# --- CONFIGURATION ---
$projectPath = "F:\agentic-ai"
$logPath = "$projectPath\logs"
$timestamp = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss")
$logFile = "$logPath\agent_run_$timestamp.log"

# --- Ensure log directory exists ---
if (!(Test-Path $logPath)) { New-Item -ItemType Directory -Path $logPath | Out-Null }

# --- Start Docker Desktop if it's not running ---
if (-not (Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue)) {
    Write-Host "🔄 Starting Docker Desktop..."
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    Start-Sleep -Seconds 30
}

# --- Navigate to project folder ---
Set-Location $projectPath

# --- Bring up containers ---
Write-Host "🚀 Starting Docker containers..."
docker compose up -d --build | Out-File -Append $logFile

# --- Wait for Ollama to be healthy ---
Write-Host "🧠 Waiting for Ollama to become healthy..."
$maxAttempts = 20
$attempt = 0
$healthy = $false

while (-not $healthy -and $attempt -lt $maxAttempts) {
    $status = docker inspect --format='{{.State.Health.Status}}' ollama 2>$null
    if ($status -eq "healthy") {
        $healthy = $true
    } else {
        Start-Sleep -Seconds 15
        $attempt++
    }
}

if (-not $healthy) {
    Write-Host "❌ Ollama never became healthy. Exiting."
    docker compose down
    exit 1
}

# --- Run the agentic pipeline ---
Write-Host "🤖 Running the AI Agent pipeline..."
docker exec ai-agent python /app/agentic_pipeline.py | Tee-Object -FilePath $logFile -Append

# --- Backup results ---
Write-Host "💾 Copying new summaries..."
$backupPath = "$projectPath\backups"
if (!(Test-Path $backupPath)) { New-Item -ItemType Directory -Path $backupPath | Out-Null }
Copy-Item "$projectPath\data\p
