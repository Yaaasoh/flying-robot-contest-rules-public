# Phase 1 画像分析スクリプト
# base64画像の位置、サイズ、内容の一部を効率的に抽出

Write-Host "=== Phase 1: 画像の正確な位置と内容の特定 ===" -ForegroundColor Yellow

# 対象ファイル
$files = @(
    "docs\21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md",
    "docs\21FlyRobo_Beginner_Regulations_text.md"
)

# 結果格納用
$results = @()

foreach ($file in $files) {
    Write-Host "`n分析中: $file" -ForegroundColor Cyan
    
    $lineNumber = 0
    $imageCount = 0
    
    # ファイルを行単位で読み込み（メモリ効率化）
    $reader = [System.IO.StreamReader]::new($file)
    
    try {
        while ($null -ne ($line = $reader.ReadLine())) {
            $lineNumber++
            
            # base64画像の行を検出
            if ($line -match '^\[image(\d+)\]:\s*<data:image/(png|jpeg|jpg);base64,(.+)>$') {
                $imageCount++
                $imageNum = $matches[1]
                $imageType = $matches[2]
                $base64Data = $matches[3]
                
                # base64データのサイズ（文字数）
                $base64Size = $base64Data.Length
                
                # base64の最初の50文字を取得（画像の識別用）
                $base64Preview = if ($base64Data.Length -gt 50) { 
                    $base64Data.Substring(0, 50) + "..."
                } else { 
                    $base64Data 
                }
                
                # 推定画像サイズ（バイト）
                $estimatedSize = [Math]::Round($base64Size * 0.75 / 1024, 2)
                
                # 結果を記録
                $result = [PSCustomObject]@{
                    File = $file
                    LineNumber = $lineNumber
                    ImageNumber = "image$imageNum"
                    ImageType = $imageType
                    Base64Length = $base64Size
                    EstimatedSizeKB = $estimatedSize
                    Base64Preview = $base64Preview
                }
                
                $results += $result
                
                Write-Host "  Found: Line $lineNumber, $($result.ImageNumber), Type: $imageType, Size: ${estimatedSize}KB" -ForegroundColor Green
            }
        }
    }
    finally {
        $reader.Close()
    }
    
    Write-Host "  Total images found: $imageCount" -ForegroundColor Yellow
}

# 結果をJSON形式で保存
$jsonOutput = $results | ConvertTo-Json -Depth 3
$jsonOutput | Out-File "phase1_image_analysis_results.json" -Encoding UTF8

# サマリー表示
Write-Host "`n=== 分析結果サマリー ===" -ForegroundColor Yellow
Write-Host "総画像数: $($results.Count)" -ForegroundColor Green
Write-Host "一般部門: $($results | Where-Object {$_.File -like "*GeneralAutoUniqueMulti*"} | Measure-Object).Count 個" -ForegroundColor Cyan
Write-Host "ビギナー部門: $($results | Where-Object {$_.File -like "*Beginner*"} | Measure-Object).Count 個" -ForegroundColor Cyan

# 画像サイズの統計
$totalSizeKB = ($results | Measure-Object -Property EstimatedSizeKB -Sum).Sum
$avgSizeKB = [Math]::Round(($results | Measure-Object -Property EstimatedSizeKB -Average).Average, 2)
$maxSize = $results | Sort-Object EstimatedSizeKB -Descending | Select-Object -First 1

Write-Host "`n画像サイズ統計:" -ForegroundColor Yellow
Write-Host "  合計サイズ: ${totalSizeKB}KB" -ForegroundColor Green
Write-Host "  平均サイズ: ${avgSizeKB}KB" -ForegroundColor Green
Write-Host "  最大画像: $($maxSize.ImageNumber) at Line $($maxSize.LineNumber) (${($maxSize.EstimatedSizeKB)}KB)" -ForegroundColor Green

Write-Host "`n詳細な結果は phase1_image_analysis_results.json に保存されました" -ForegroundColor Yellow
