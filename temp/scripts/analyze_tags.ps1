# 画像タグ分析スクリプト
$editFile = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md"
$currentFile = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md"

# 修正履歴ファイルの作成
$history = @()
$history += "=== 画像タグ変更履歴 ==="
$history += "作成日時: $(Get-Date -Format 'yyyy/MM/dd HH:mm:ss')"
$history += ""
$history += "修正前ファイル: $editFile"
$history += "修正後ファイル: $currentFile"
$history += ""

# 画像タグの抽出
$editTags = Select-String -Path $editFile -Pattern '!\[.*?\]\[image\d+\]' -AllMatches
$currentTags = Select-String -Path $currentFile -Pattern '!\[.*?\]\[image\d+\]' -AllMatches

$history += "修正前の画像タグ数: $($editTags.Count)"
$history += "修正後の画像タグ数: $($currentTags.Count)"
$history += ""
$history += "=== 詳細情報 ==="

# 修正前のタグ詳細
$history += ""
$history += "【修正前の画像タグ】"
foreach ($tag in $editTags) {
    foreach ($match in $tag.Matches) {
        $line = "Line " + $tag.LineNumber + ": " + $match.Value
        $history += $line
    }
}

# 修正後のタグ詳細
$history += ""
$history += "【修正後の画像タグ】"
foreach ($tag in $currentTags) {
    foreach ($match in $tag.Matches) {
        $line = "Line " + $tag.LineNumber + ": " + $match.Value
        $history += $line
    }
}

$history | Out-File "temp\modification_history.txt" -Encoding UTF8

# CSV形式での変更履歴
$csv = @()
$csv += "Type,LineNumber,ImageNumber,FullTag"

# 修正前
foreach ($tag in $editTags) {
    foreach ($match in $tag.Matches) {
        if ($match.Value -match '\[image(\d+)\]') {
            $imageNum = $matches[1]
            $csv += "BEFORE,$($tag.LineNumber),image$imageNum,`"$($match.Value)`""
        }
    }
}

# 修正後
foreach ($tag in $currentTags) {
    foreach ($match in $tag.Matches) {
        if ($match.Value -match '\[image(\d+)\]') {
            $imageNum = $matches[1]
            $csv += "AFTER,$($tag.LineNumber),image$imageNum,`"$($match.Value)`""
        }
    }
}

$csv | Out-File "temp\image_tag_changes.csv" -Encoding UTF8

Write-Host "完了: modification_history.txt と image_tag_changes.csv を作成しました"
Write-Host "修正前: $($editTags.Count) タグ"
Write-Host "修正後: $($currentTags.Count) タグ"