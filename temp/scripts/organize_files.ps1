# ファイルを適切なフォルダに整理

# 間違った理解に基づくファイルをdeprecatedに移動
$deprecatedFiles = @(
    'comprehensive_recovery_plan.md',
    'practical_work_procedures.md', 
    'execution_plan.md',
    'executive_summary.md'
)

foreach ($file in $deprecatedFiles) {
    if (Test-Path "temp\$file") {
        Move-Item -Path "temp\$file" -Destination "temp\deprecated\" -Force
        Write-Host "Moved $file to deprecated/"
    }
}

# 調査・分析ファイルをinvestigationに移動
$investigationFiles = @(
    'critical_finding_report.md',
    'final_comprehensive_analysis.md',
    'complete_investigation_report.md',
    'image_definition_timeline_analysis.md',
    'investigation_summary_report.md'
)

foreach ($file in $investigationFiles) {
    if (Test-Path "temp\$file") {
        Move-Item -Path "temp\$file" -Destination "temp\investigation\" -Force
        Write-Host "Moved $file to investigation/"
    }
}

# テキストファイルとCSVファイルをinvestigationに移動
Get-ChildItem -Path "temp\" -Filter "*.txt" | ForEach-Object {
    Move-Item -Path $_.FullName -Destination "temp\investigation\" -Force
    Write-Host "Moved $($_.Name) to investigation/"
}

Get-ChildItem -Path "temp\" -Filter "*.csv" | Where-Object {$_.Name -ne 'image_management_sheet.csv'} | ForEach-Object {
    Move-Item -Path $_.FullName -Destination "temp\investigation\" -Force
    Write-Host "Moved $($_.Name) to investigation/"
}

# スクリプトファイルをscriptsに移動
Get-ChildItem -Path "temp\" -Filter "*.py" | Where-Object {$_.Directory.Name -eq 'temp'} | ForEach-Object {
    Move-Item -Path $_.FullName -Destination "temp\scripts\" -Force
    Write-Host "Moved $($_.Name) to scripts/"
}

Get-ChildItem -Path "temp\" -Filter "*.ps1" | Where-Object {$_.Name -ne 'organize_files.ps1'} | ForEach-Object {
    Move-Item -Path $_.FullName -Destination "temp\scripts\" -Force
    Write-Host "Moved $($_.Name) to scripts/"
}

Write-Host "`nFile organization completed!"