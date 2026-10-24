# Usage: place-window.ps1 -Process brave        (or powershell / WindowsTerminal)
# Moves the main window of the process to the top-left, 2560x1440 physical px, topmost, and brings it forward.
param([string]$Process = "brave", [int]$W = 2560, [int]$H = 1440, [switch]$NoTopmost)
Add-Type -TypeDefinition @'
using System; using System.Runtime.InteropServices;
public class W {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
}
'@
[W]::SetProcessDPIAware() | Out-Null
$p = Get-Process $Process -ErrorAction Stop | Where-Object { $_.MainWindowHandle -ne 0 } | Sort-Object { $_.MainWindowTitle.Length } -Descending | Select-Object -First 1
if (-not $p) { throw "no window for $Process" }
[W]::ShowWindow($p.MainWindowHandle, 9) | Out-Null          # SW_RESTORE
$after = if ($NoTopmost) { [IntPtr]::Zero } else { [IntPtr](-1) }   # HWND_TOPMOST
[W]::SetWindowPos($p.MainWindowHandle, $after, 0, 0, $W, $H, 0x0040) | Out-Null
[W]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
"placed: $($p.ProcessName) '$($p.MainWindowTitle)'"
