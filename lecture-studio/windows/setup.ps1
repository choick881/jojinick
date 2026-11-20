# HY FLIP 강의 편집기 — Windows 설치 스크립트 (1_설치하기.bat 이 실행)
# 이 폴더 안에 Python 가상환경(.venv), ffmpeg(tools\ffmpeg), 받아쓰기 모델(models)을 설치한다.
# 시스템 설정은 바꾸지 않는다 (Python 이 없을 때만 사용자 계정에 Python 3.12 설치).
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
function Step($m) { Write-Host ""; Write-Host "▶ $m" -ForegroundColor Cyan }
function Ok($m) { Write-Host "  ✓ $m" -ForegroundColor Green }

Write-Host "==============================================================="
Write-Host "  HY FLIP 강의 편집기 설치 (처음 한 번, 20~40분 걸릴 수 있습니다)"
Write-Host "  설치 위치: $Root"
Write-Host "==============================================================="

# 1) Python 3.12
Step "1/5 Python 확인"
$py = $null
$cands = @("$env:LOCALAPPDATA\Programs\Python\Python312\python.exe", "$env:ProgramFiles\Python312\python.exe")
foreach ($c in $cands) { if (Test-Path $c) { $py = $c; break } }
if (-not $py) {
  try { $p = (& py -3.12 -c "import sys;print(sys.executable)" 2>$null); if ($LASTEXITCODE -eq 0 -and $p) { $py = $p.Trim() } } catch {}
}
if (-not $py) {
  Write-Host "  Python 3.12 를 내려받아 설치합니다 (사용자 계정에만, 관리자 권한 불필요) …"
  $inst = Join-Path $env:TEMP "python-3.12.8-amd64.exe"
  Invoke-WebRequest "https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe" -OutFile $inst -UseBasicParsing
  Start-Process $inst -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 Include_test=0" -Wait
  $py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
  if (-not (Test-Path $py)) { throw "Python 설치에 실패했습니다. python.org 에서 3.12 를 직접 설치한 뒤 다시 실행하세요." }
}
Ok "Python: $py"

# 2) 가상환경 + 패키지
Step "2/5 프로그램 패키지 설치"
$venv = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $venv)) { & $py -m venv (Join-Path $Root ".venv") }
& $venv -m pip install --upgrade pip --quiet
& $venv -m pip install -r (Join-Path $Root "requirements.txt") --quiet
if ($LASTEXITCODE -ne 0) { throw "패키지 설치에 실패했습니다 (인터넷 연결 확인)" }
Ok "필수 패키지"
& $venv -m pip install mediapipe --quiet
if ($LASTEXITCODE -eq 0) { Ok "립싱크 자동 보정용 mediapipe" } else { Write-Host "  (mediapipe 설치 실패 — 립싱크 자동 보정 없이 동작합니다)" -ForegroundColor Yellow }

# 3) ffmpeg (자막 입히기 libass 포함 빌드)
Step "3/5 ffmpeg 설치"
$ffdir = Join-Path $Root "tools\ffmpeg\bin"
if (-not (Test-Path (Join-Path $ffdir "ffmpeg.exe"))) {
  $zip = Join-Path $env:TEMP "ffmpeg-release-essentials.zip"
  $tmp = Join-Path $env:TEMP "ffmpeg-unzip"
  Invoke-WebRequest "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile $zip -UseBasicParsing
  if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
  Expand-Archive $zip -DestinationPath $tmp -Force
  $bin = Get-ChildItem $tmp -Recurse -Filter ffmpeg.exe | Select-Object -First 1
  New-Item -ItemType Directory -Force -Path $ffdir | Out-Null
  Copy-Item (Join-Path $bin.DirectoryName "*") $ffdir -Force
  Remove-Item $tmp -Recurse -Force; Remove-Item $zip -Force
}
Ok "ffmpeg: $ffdir"
$env:PATH = "$ffdir;$env:PATH"

# 4) 받아쓰기·얼굴 모델
Step "4/5 받아쓰기 모델 내려받기 (약 940MB — 시간이 걸립니다)"
& $venv (Join-Path $Root "engine\setup_models.py") medium
if ($LASTEXITCODE -ne 0) { throw "받아쓰기 모델을 받지 못했습니다 (인터넷 연결 확인 후 다시 실행)" }
& $venv (Join-Path $Root "engine\setup_models.py") lipsync
Ok "모델"

# 5) 확인 + 바탕화면 바로가기
Step "5/5 마무리"
$edge = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($edge) { Ok "인쇄용 PDF: $edge" } else { Write-Host "  (엣지·크롬이 없어 인쇄용 PDF 는 건너뜁니다)" -ForegroundColor Yellow }
& $venv (Join-Path $Root "engine\tests\test_flip.py") | Out-Null
if ($LASTEXITCODE -eq 0) { Ok "자체 점검 통과" } else { Write-Host "  (자체 점검 일부 실패 — 사용은 가능합니다)" -ForegroundColor Yellow }
try {
  $sh = New-Object -ComObject WScript.Shell
  $lnk = $sh.CreateShortcut((Join-Path ([Environment]::GetFolderPath("Desktop")) "강의 편집기.lnk"))
  $lnk.TargetPath = Join-Path $PSScriptRoot "2_강의영상_편집.bat"
  $lnk.WorkingDirectory = $Root
  $lnk.Save()
  Ok "바탕화면에 '강의 편집기' 바로가기를 만들었습니다 (영상을 끌어다 놓으세요)"
} catch { Write-Host "  (바로가기를 만들지 못했습니다 — windows 폴더의 2_강의영상_편집.bat 을 쓰세요)" -ForegroundColor Yellow }

Write-Host ""
Write-Host "설치가 끝났습니다. 바탕화면 '강의 편집기' 위에 강의 영상을 끌어다 놓으세요." -ForegroundColor Green
