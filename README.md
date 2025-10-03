# 飛行ロボットコンテスト ルール管理システム

> **⚠️ 警告**: これはテスト用リポジトリです。コンテンツには誤りが含まれる可能性があります。AI改ざんを含む可能性があるためご注意ください。

## 概要

飛行ロボットコンテストのルールとレギュレーションを管理するためのテスト用リポジトリです。このサイトは実際のコンテストルールを参照するためのものではなく、ルール管理システムの検討・実験用として作成されています。

## 目的

このテスト用リポジトリの目的：
- 飛行ロボットコンテストのルール管理を容易にする方法の検討
- 効率的な画像ファイル管理手法のテスト
- 共同編集ワークフローの実験

## 📚 第21回大会ルール（2025年）

### GitHub Pagesで閲覧
- [一般・自動操縦・ユニークデザイン・マルチコプター部門](https://yaaasoh.github.io/flying-robot-contest-rules-public/21FlyRobo_GeneralAutoUniqueMulti_Regulations_text/)
- [ビギナー部門](https://yaaasoh.github.io/flying-robot-contest-rules-public/21FlyRobo_Beginner_Regulations_text/)

### ファイルを直接ダウンロード
- [一般部門等（Markdown, 83KB）](https://raw.githubusercontent.com/Yaaasoh/flying-robot-contest-rules-public/main/docs/21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md)
- [ビギナー部門（Markdown, 28KB）](https://raw.githubusercontent.com/Yaaasoh/flying-robot-contest-rules-public/main/docs/21FlyRobo_Beginner_Regulations_text.md)

### リポジトリ統計
- ルール文書: 9ファイル
- 画像ファイル: 46枚（equipment: 15, field: 16, missions: 15）
- 対応部門: 5部門（一般、自動操縦、ユニークデザイン、マルチコプター、ビギナー）

## 効率的なリポジトリ利用方法

### 必要なファイルだけをクローンする方法

#### オプション1: 特定ディレクトリのみクローン（推奨）
```bash
# docsディレクトリとmkdocs.ymlだけをクローン
git clone --no-checkout https://github.com/Yaaasoh/flying-robot-contest-rules-public.git
cd flying-robot-contest-rules-public
git sparse-checkout init --cone
git sparse-checkout set docs mkdocs.yml
git checkout
```

#### オプション2: 画像ファイルを除外してクローン
```bash
# 大きな画像ファイルを除外してクローン
git clone --filter=blob:limit=100k https://github.com/Yaaasoh/flying-robot-contest-rules-public.git
```

#### オプション3: 浅いクローン（最新コミットのみ）
```bash
# 履歴を取得せず最新状態のみクローン
git clone --depth 1 https://github.com/Yaaasoh/flying-robot-contest-rules-public.git
```

## 標準的な作業フロー

1. リポジトリのクローン（目的に応じた方法を選択）
2. ファイルの編集
3. 変更の確認: `git status` および `git diff`
4. 変更のステージング: `git add <ファイル名>` または `git add .`
5. コミット: `git commit -m "変更内容の説明"`
6. プッシュ: `git push origin main`

## MkDocsでのプレビュー方法

1. MkDocsのインストール: `pip install mkdocs mkdocs-material`
2. ローカルサーバーの起動: `mkdocs serve`
3. ブラウザで確認: `http://127.0.0.1:8000/`

## GitHub Pagesへのデプロイ方法

GitHub Pagesへのデプロイは以下のコマンドで行います:

```bash
mkdocs gh-deploy --force
```

## 役割別クローン方法

### ルール文書の閲覧・編集のみ
最小限のスパースクローン（`docs/` + `mkdocs.yml`）を使用

### 画像ファイルの編集も必要
最小限のスパースクローンに `docs/images/` を追加

### リポジトリ管理者・メンテナー
完全なクローンを使用し、必要に応じてGit LFSを設定
