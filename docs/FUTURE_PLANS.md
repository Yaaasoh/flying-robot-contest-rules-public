# 飛行ロボットコンテスト ドキュメント・画像管理 今後の方針

## 1. Markdownの構造化と整理

### 1.1 目次の自動生成

手動で目次を書くと更新の手間がかかるため、`doctoc` を使って目次を自動生成します。

**実装手順**:
1. Node.js環境の確認/セットアップ
2. `doctoc` のインストール: `npm install -g doctoc`
3. 各ルールファイルに目次セクションを追加
4. 目次更新の自動化スクリプトを作成

```bash
#!/bin/bash
# ルールファイルの目次を更新するスクリプト
echo "ルールファイルの目次を更新しています..."
doctoc docs/beginner/index.md
doctoc docs/regular/index.md
echo "目次の更新が完了しました"
```

### 1.2 Markdownの書式統一

`markdownlint` を導入し、Markdownの書式を統一します。

**実装手順**:
1. `markdownlint-cli` のインストール: `npm install -g markdownlint-cli`
2. カスタムルールを `.markdownlint.json` に定義
   ```json
   {
     "MD013": false,
     "MD033": false,
     "MD007": { "indent": 4 },
     "MD024": { "allow_different_nesting": true }
   }
   ```
3. 書式チェックスクリプトの作成
4. 編集環境にExtensionとして追加し、リアルタイムでチェック

## 2. 画像管理の効率化

既存の画像管理システムに以下の改善を加えます：

1. **画像の圧縮と最適化の自動化**
   - `imagemin` を使用した画像最適化スクリプトの追加
   - `create_metadata.py` に画像サイズ最適化機能を組み込む

2. **画像プレビューの改善**
   - GitHub Pagesで画像ギャラリーを作成
   - 画像のメタデータと一緒に表示する機能

## 3. GitHub Pages の活用

### 3.1 `docs/` ディレクトリの整理

**実装計画**:
1. `docs/` ディレクトリに以下の構造を作成
   ```
   docs/
   ├── index.md            # GitHub Pagesのトップページ
   ├── beginner/           # ビギナー部門ルール
   ├── regular/            # 通常部門ルール
   ├── images/             # 既存の画像ディレクトリ
   │   ├── field/
   │   ├── equipment/
   │   └── missions/
   ├── image-gallery.md    # 画像ギャラリーページ
   └── _config.yml         # GitHub Pages設定
   ```

2. MkDocsの導入
   - `pip install mkdocs mkdocs-material`
   - `mkdocs.yml` の基本設定

   ```yaml
   site_name: 飛行ロボットコンテスト ルール管理
   theme:
     name: material
     language: ja
   nav:
     - ホーム: index.md
     - ルール:
       - ビギナー部門: beginner/index.md
       - 通常部門: regular/index.md
     - 画像ギャラリー: image-gallery.md
   ```

### 3.2 GitHub Pagesの設定

1. リポジトリ設定 → `Settings` → `Pages`
2. ソースを`Branch: main` の `/docs` に設定
3. カスタムドメインを必要に応じて設定

## 4. GitHub Actions による自動化

文書更新・画像処理の自動化フローを構築します：

```yaml
name: Document Update

on:
  push:
    paths:
      - 'docs/**/*.md'
      - 'docs/images/**/*'

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
          
      - name: Install dependencies
        run: |
          npm install -g doctoc markdownlint-cli
          pip install mkdocs mkdocs-material
          
      - name: Update TOCs
        run: |
          doctoc docs/beginner/index.md
          doctoc docs/regular/index.md
          
      - name: Check Markdown formatting
        run: markdownlint docs/**/*.md
        
      - name: Build MkDocs site
        run: mkdocs build
        
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

## 実装ロードマップ

### フェーズ1: 基本環境の準備 (1-2週間)
- Node.js と必要なツールのインストール
- `.markdownlint.json` の設定
- 目次自動生成の導入

### フェーズ2: ドキュメント整備 (2-3週間)
- `docs/` ディレクトリの構成整理
- MkDocsの導入と基本設定
- 各ページの作成と整備

### フェーズ3: 画像管理高度化 (2-3週間)
- 画像ギャラリーの構築
- 画像最適化スクリプトの拡張
- メタデータ連携の強化

### フェーズ4: 自動化の実装 (1-2週間)
- GitHub Actionsのワークフロー設定
- 自動化テストと調整
- ドキュメントの最終確認

---

最終更新日: 2025年3月11日
