# 第21回飛行ロボコン 画像参照分析スクリプト

Write-Host "=== 第21回ファイルの画像参照を分析 ==="
Write-Host ""

$files = @(
    "docs\21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md",
    "docs\21FlyRobo_Beginner_Regulations_text.md"
)

$totalImages = 0
$imageDetails = @{}

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "分析中: $(Split-Path $file -Leaf)"
        
        $content = Get-Content $file -Raw -Encoding UTF8
        $imageRefs = [regex]::Matches($content, '\[image(\d+)\]:\s*<>')
        
        $imageNums = @()
        foreach ($match in $imageRefs) {
            $imageNum = [int]$match.Groups[1].Value
            $imageNums += $imageNum
        }
        
        $imageDetails[$file] = @{
            Count = $imageRefs.Count
            Numbers = $imageNums | Sort-Object
        }
        
        $totalImages += $imageRefs.Count
        
        Write-Host "  - 画像参照数: $($imageRefs.Count)"
        Write-Host "  - 画像番号: $($imageNums -join ', ')"
        Write-Host ""
    } else {
        Write-Host "❌ ファイルが見つかりません: $file"
    }
}

Write-Host "=== 分析結果サマリー ==="
Write-Host "総画像参照数: $totalImages"
Write-Host ""

# レポート生成
$report = @"
# 第21回飛行ロボコン 画像参照分析レポート
生成日時: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 分析結果サマリー
- 総画像参照数: $totalImages
- 分析ファイル数: $($files.Count)

## ファイル別詳細
"@

foreach ($file in $imageDetails.Keys) {
    $details = $imageDetails[$file]
    $report += @"

### $(Split-Path $file -Leaf)
- 画像参照数: $($details.Count)
- 画像番号範囲: image$($details.Numbers[0]) ～ image$($details.Numbers[-1])
- 画像番号リスト: $($details.Numbers -join ', ')
"@
}

$report += @"

## 画像準備状況
現在、すべての画像参照は空（`<>`）です。以下の対応が必要です：

1. **Placeholder画像の作成**
   - 汎用placeholder画像を作成
   - すべての画像参照に適用

2. **実画像の収集**
   - Google Docsから画像を保存
   - PDFから画像を抽出
   - 必要に応じて新規作成

3. **画像配置**
   ```
   docs/images/
   ├── field/       # フィールドレイアウト
   ├── equipment/   # 機材・設備
   ├── missions/    # ミッション説明
   └── items/       # アイテム（チキンラーメン等）
   ```
"@

# レポートを保存
if (-not (Test-Path "project_management")) {
    New-Item -ItemType Directory -Path "project_management" -Force
}

$report | Out-File "project_management\IMAGE_ANALYSIS_REPORT.md" -Encoding UTF8
Write-Host "✅ レポートを保存しました: project_management\IMAGE_ANALYSIS_REPORT.md"