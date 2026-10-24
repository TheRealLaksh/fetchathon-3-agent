# Keeps the four Mandi agents alive: every 60 s it checks each agent's local /agent_info and restarts one that stopped answering.
# Run once, hidden:  Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","scripts\watchdog.ps1"
# Stop it with:      Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'watchdog\.ps1' } | % { Stop-Process -Id $_.ProcessId -Force }
$root = Split-Path -Parent $PSScriptRoot
$py = Join-Path $root ".venv\Scripts\python.exe"
$logDir = Join-Path $root "logs"
New-Item -ItemType Directory -Force $logDir | Out-Null
$wlog = Join-Path $logDir "watchdog.log"
$agents = @(
    @{ name = "price_agent";     port = 8002; mailbox = $false },
    @{ name = "logistics_agent"; port = 8003; mailbox = $false },
    @{ name = "weather_agent";   port = 8004; mailbox = $false },
    @{ name = "front_agent";     port = 8001; mailbox = $true }
)
$misses = @{}

function Log($msg) { Add-Content -Path $wlog -Value ("{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg) }

function Alive($port) {
    try { return (Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$port/agent_info" -TimeoutSec 8).StatusCode -eq 200 } catch { return $false }
}

function Restart-Agent($a) {
    # remove any half-dead process of this agent first, then start it the same way scripts\start-agents.ps1 does
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match ("mandi\." + $a.name) } |
        ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Seconds 3
    $log = Join-Path $logDir ($a.name + ".log")
    $mb = if ($a.mailbox) { "`$env:USE_MAILBOX='1'; " } else { "" }
    $cmd = "cd '$root'; `$env:PYTHONIOENCODING='utf-8'; `$env:PYTHONUTF8='1'; $mb& '$py' -u -m mandi.$($a.name) 2>&1 | Tee-Object -FilePath '$log'"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $cmd
    Log ("restarted " + $a.name)
}

Log "watchdog started"
while ($true) {
    foreach ($a in $agents) {
        if (Alive $a.port) { $misses[$a.name] = 0; continue }
        $misses[$a.name] = 1 + [int]$misses[$a.name]
        if ($misses[$a.name] -ge 2) {          # two failed checks in a row (about two minutes), not a blip
            Restart-Agent $a
            $misses[$a.name] = 0
            Start-Sleep -Seconds 20
        }
    }
    Start-Sleep -Seconds 60
}
