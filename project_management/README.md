# プロジェクト管理ディレクトリ

このディレクトリには、第21回飛行ロボコンのデプロイ作業に関する管理ファイルが格納されています。

## ファイル一覧

### 進捗管理
- **PROGRESS_20250105.md** - 作業進捗の記録
- **INCIDENT_RECORD.md** - インシデント（問題）の記録と対策
- **IMPORTANT_NOTES.md** - 重要な連絡事項

### 分析レポート
- **IMAGE_ANALYSIS_REPORT.md** - 画像参照の分析結果（analyze_images.ps1実行後に生成）

### バックアップ
- **mkdocs.yml.backup_20th** - 第20回版のmkdocs.yml（更新後に生成）
- **index.md.backup_20th** - 第20回版のindex.md（更新後に生成）

## スクリプト（プロジェクトルート）

- **safety_check.ps1** - デプロイ前の安全確認スクリプト
- **analyze_images.ps1** - 画像参照分析スクリプト

## 使用方法

1. 作業開始時に`PROGRESS_20250105.md`を確認
2. 問題発生時は`INCIDENT_RECORD.md`を参照
3. デプロイ前に`safety_check.ps1`を実行
4. 画像対応時は`analyze_images.ps1`を実行

## 重要事項

- バックアップパス: `C:\temp\flying-robot-backup-20250804_161932`
- 現在のブランチ: update-21st-competition-2025
- **git pullは絶対に実行しない**