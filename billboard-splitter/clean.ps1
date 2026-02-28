param(
  # Nazwa pliku EXE (bez ścieżki)
  [string]$ExeName = "billboard-splitter.exe",

  # (Opcjonalnie) ścieżka do katalogu, w którym leży EXE.
  # Gdy nie podasz: skrypt spróbuje sam odnaleźć EXE (w bieżącym katalogu skryptu i podkatalogach).
  [string]$AppDir
)

Write-Host "== DETEKCJA KATALOGU APLIKACJI =="

function Resolve-AppDir {
  param([string]$ExeName, [string]$AppDir)

  if ($AppDir -and (Test-Path (Join-Path $AppDir $ExeName))) {
    return (Resolve-Path $AppDir).Path
  }

  # 1) Spróbuj obok skryptu
  $try1 = Join-Path $PSScriptRoot $ExeName
  if (Test-Path $try1) {
    return $PSScriptRoot
  }

  # 2) Spróbuj w podkatalogach obok skryptu (typowy onedir: .\dist\...\EXE)
  $candidates = Get-ChildItem -Path $PSScriptRoot -Recurse -Filter $ExeName -ErrorAction SilentlyContinue |
                Where-Object { -not $_.PSIsContainer }
  if ($candidates.Count -gt 1) {
    Write-Host "Znaleziono kilka instancji EXE:"
    $i = 0
    $candidates | ForEach-Object { "{0}. {1}" -f $i++, $_.DirectoryName } | Write-Host
    $sel = Read-Host "Wybierz indeks instancji do wyczyszczenia"
    return $candidates[[int]$sel].DirectoryName
  } elseif ($candidates.Count -eq 1) {
    return $candidates[0].DirectoryName
  }

  throw "Nie znaleziono $ExeName. Podaj -AppDir lub umieść skrypt obok EXE."
}

try {
  $AppDir = Resolve-AppDir -ExeName $ExeName -AppDir $AppDir
  Write-Host "Katalog aplikacji: $AppDir"
} catch {
  Write-Error $_
  exit 1
}

# === ŚCIEŻKI I STAŁE ===
$ExePath   = Join-Path $AppDir $ExeName
$ProcName  = ($ExeName -replace "\.exe$","")
$VSRoot    = Join-Path $Env:LOCALAPPDATA "VirtualStore"

Write-Host "== Zatrzymuję proces =="
Get-Process -Name $ProcName -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "== Czyszczę VirtualStore dla tej instancji =="
# VirtualStore mapuje ścieżkę bez litery dysku
$VSAppDir = Join-Path $VSRoot ($AppDir -replace "^[A-Za-z]:\\","")
if (Test-Path $VSAppDir) {
  Remove-Item $VSAppDir -Recurse -Force -ErrorAction SilentlyContinue
  Write-Host "Usunięto: $VSAppDir"
} else {
  Write-Host "Brak VirtualStore dla tej instancji."
}

Write-Host "== Usuwam lokalny settings.json (odtworzy się przy starcie) =="
$SettingsPath = Join-Path $AppDir "settings.json"
if (Test-Path $SettingsPath) {
  Remove-Item $SettingsPath -Force -ErrorAction SilentlyContinue
  Write-Host "Usunięto: $SettingsPath"
} else {
  Write-Host "Brak lokalnego settings.json obok EXE."
}

Write-Host "== Gotowe =="
Write-Host "Wyczyść/Skopiuj świeżą dystrybucję (jeśli trzeba) i uruchom: $ExePath"