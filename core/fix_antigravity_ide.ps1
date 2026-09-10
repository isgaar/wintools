$dir = Join-Path $env:APPDATA "Antigravity IDE\User"
if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}
$file = Join-Path $dir "settings.json"
$obj = @{}
if (Test-Path $file) {
    try {
        $obj = (Get-Content $file -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable)
    } catch {}
}
if ($null -eq $obj) { $obj = @{} }
$obj["window.openWithoutArgumentsInNewWindow"] = "off"
$obj["window.restoreWindows"] = "one"
$obj["window.openFoldersInNewWindow"] = "off"
$obj["window.newWindowDimensions"] = "inherit"
$obj["workbench.editor.restoreViewState"] = $true
$json = ($obj | ConvertTo-Json -Depth 10)
[System.IO.File]::WriteAllText($file, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "[OK] settings.json actualizado exitosamente en $file"
Write-Host "     - Ventana unica sin argumentos: 'off'"
Write-Host "     - Restaurar ultimo directorio: 'one'"
Write-Host "     - Reutilizar ventana al abrir carpetas: 'off'"
Write-Host "[EXITO] Correccion de Antigravity IDE aplicada correctamente."
