# GitHub Pages セットアップガイド

このドキュメントでは、飛行ロボットコンテストのドキュメント管理システムをGitHub Pagesで公開する方法について説明します。

## 概要

GitHub Pagesは、GitHubリポジトリからHTMLやマークダウンファイルを直接ウェブサイトとして公開するサービスです。このプロジェクトでは、`docs/` ディレクトリのファイルを使ってウェブサイトを構築し、MkDocsで拡張機能を追加しています。

## セットアップ手順

### 1. GitHub Pagesの有効化

1. リポジトリのページで **Settings** タブをクリック
2. 左側のメニューから **Pages** を選択
3. 以下の設定を行う：
   - **Source**: Deploy from a branch
   - **Branch**: `gh-pages` を選択（GitHub Actionsによって自動生成される）
   - **Folder**: `/` (root)
4. **Save** をクリック

**注意**: GitHub Actionsのワークフローが既に設定されているため、`main` ブランチへのプッシュ時に自動的に `gh-pages` ブランチが更新されます。

### 2. カスタムドメインの設定（オプション）

1. **Settings** > **Pages** で、Custom domain セクションに希望するドメイン名を入力
2. DNSプロバイダで、以下のDNSレコードを設定：
   - **Type**: `CNAME`
   - **Name**: サブドメイン（例：`docs`）
   - **Value**: `{username}.github.io` または `{organization}.github.io`
3. DNSが伝播するまで待つ（最大24時間）
4. **Enforce HTTPS** オプションを有効にする

## ウェブサイトの構造

このプロジェクトのウェブサイトは以下のような構造になっています：

```
/                   # トップページ
├── beginner/       # ビギナー部門ルール
├── regular/        # 通常部門ルール
├── image-gallery/  # 画像ギャラリー
└── resources/      # 各種リソース
```

## コンテンツの更新方法

### Markdownファイルの更新

1. `docs/` ディレクトリ内の対応するMarkdownファイルを編集
2. 変更をコミットして `main` ブランチにプッシュ
3. GitHub Actionsが自動的にサイトをビルドし、デプロイ

### 画像の追加・更新

1. 画像ファイルを `docs/images/{category}/` ディレクトリに追加
2. 命名規則：`{category}-{description}-{year}.{extension}`
3. メタデータファイル `docs/metadata/images-metadata.json` も更新
4. 変更をコミットしてプッシュ

## ローカルでのプレビュー

ウェブサイトの変更をプッシュする前にローカルでプレビューするには：

```bash
# MkDocsのインストール
pip install mkdocs mkdocs-material

# サイトのプレビュー（http://127.0.0.1:8000 でアクセス可能）
mkdocs serve
```

## GitHub Actions ワークフロー

このプロジェクトでは、以下の自動化が設定されています：

1. Markdownの目次（Table of Contents）の自動生成
2. Markdownの書式チェック
3. MkDocsを使ったサイトのビルド
4. GitHub Pagesへのデプロイ

ワークフローの設定は `.github/workflows/docs.yml` で確認できます。

## トラブルシューティング

### ビルドエラー

1. GitHub Actionsのログを確認
   - リポジトリの **Actions** タブで最新のワークフローを選択
   - エラーメッセージを確認
2. よくある問題：
   - MkDocs設定ファイル（`mkdocs.yml`）の構文エラー
   - ドキュメントリンクの不整合
   - 画像パスの誤り

### 表示の問題

1. キャッシュのクリア
   - ブラウザのキャッシュをクリアして再読み込み
2. 数分待ってから再確認（GitHub Pagesのキャッシュ更新に時間がかかる場合がある）

### ローカルプレビューとのずれ

1. `mkdocs.yml` の設定が正しいか確認
2. GitHub Actionsの環境と互換性があるか確認（Python、MkDocsのバージョン）

## 参考リンク

- [GitHub Pages 公式ドキュメント](https://docs.github.com/ja/pages)
- [MkDocs 公式ドキュメント](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

---

最終更新日: 2025年3月11日
