Write-Host "=== デプロイ前安全確認 ==="
Write-Host "実行日時: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

$checks = @{
    "ブランチ確認" = (git branch --show-current) -eq "update-21st-competition-2025"
    "第21回ファイル（通常部門）" = Test-Path "docs\21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md"
    "第21回ファイル（ビギナー）" = Test-Path "docs\21FlyRobo_Beginner_Regulations_text.md"
    "mkdocs.yml存在" = Test-Path "mkdocs.yml"
    "index.md存在" = Test-Path "docs\index.md"
    "バックアップ存在" = Test-Path "C:\temp\flying-robot-backup-20250804_161932"
}

# mkdocs.ymlとindex.mdの内容確認
if (Test-Path mkdocs.yml) {
    $mkdocsContent = Get-Content mkdocs.yml -Raw
    $checks["mkdocs.yml更新済み"] = $mkdocsContent -match "第21回"
}

if (Test-Path docs\index.md) {
    $indexContent = Get-Content docs\index.md -Raw
    $checks["index.md更新済み"] = $indexContent -match "126チーム"
}

Write-Host "=== チェック結果 ==="
$allPassed = $true
foreach ($check in $checks.GetEnumerator()) {
    $status = if ($check.Value) { "✅" } else { "❌"; $allPassed = $false }
    Write-Host "$status $($check.Key)"
}

Write-Host ""
if (-not $allPassed) {
    Write-Host "❌ 安全確認に失敗しました。デプロイを中止してください。" -ForegroundColor Red
    Write-Host ""
    Write-Host "対処法："
    Write-Host "1. 失敗した項目を確認"
    Write-Host "2. 必要な作業を完了"
    Write-Host "3. 再度このスクリプトを実行"
    exit 1
} else {
    Write-Host "✅ すべての確認項目をパスしました。デプロイ可能です。" -ForegroundColor Green
    Write-Host ""
    Write-Host "次のステップ："
    Write-Host "1. mkdocs serve でローカル確認"
    Write-Host "2. 問題なければ mkdocs gh-deploy --force"
}

# ファイルサイズも表示
Write-Host ""
Write-Host "=== ファイルサイズ確認 ==="
$files = @(
    "docs\21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md",
    "docs\21FlyRobo_Beginner_Regulations_text.md"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Host "📄 $(Split-Path $file -Leaf): $($size) bytes"
    }
}