# Usage: mux.ps1 -Scene 03 -Ss 2.9 -Dur 29.9 [-Mask] [-Label "text"] [-Speed 1]
# Trims clips\rawNN.mp4 (2560x1440), scales to 1920x1080, optionally masks Brave's debugging infobar (y 92-155 at 1080p),
# adds an on-screen label, and muxes audio\sceneNN.wav. Output clips\sceneNN.mp4.
param([Parameter(Mandatory)][string]$Scene, [double]$Ss = 0, [Parameter(Mandatory)][double]$Dur, [switch]$Mask, [string]$Label = "", [double]$Speed = 1, [string]$Raw = "")
$root = Split-Path -Parent $PSScriptRoot
$in = if ($Raw) { $Raw } else { Join-Path $root "clips\raw$Scene.mp4" }
$vf = @()
if ($Speed -ne 1) { $vf += "setpts=PTS/$Speed" }
$vf += "scale=1920:1080:flags=lanczos"
if ($Mask) { $vf += "drawbox=x=0:y=93:w=1920:h=62:color=0x1e1e1e:t=fill" }
if ($Label) { $vf += "drawtext=fontfile='C\:/Windows/Fonts/segoeui.ttf':text='$Label':x=36:y=h-72:fontsize=30:fontcolor=white:box=1:boxcolor=0x000000@0.65:boxborderw=12" }
$vf += "fps=30"
$vfs = $vf -join ","
$aud = Join-Path $root "audio\scene$Scene.wav"
$out = Join-Path $root "clips\scene$Scene.mp4"
& ffmpeg -hide_banner -loglevel error -y -ss $Ss -t $Dur -i $in -i $aud -filter_complex "[0:v]$vfs[v];[1:a]apad=pad_dur=2,atrim=0:$Dur[a]" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 44100 -ac 1 $out
& ffprobe -v error -show_entries format=duration -of csv=p=0 $out
