# 画像ディレクトリ

このディレクトリには飛行ロボットコンテストのルール内で参照される図表を保存します。

## ディレクトリ構造

```
docs/images/
├─ field/            # フィールドレイアウト関連
├─ equipment/        # マーカーコーン、ミニハードル等
├─ missions/         # ミッション関連画像
├─ scripts/          # 画像処理スクリプト
├─ README.md         # このファイル
├─ GUIDE.md          # 画像管理の詳細ガイドライン
├─ OPTIMIZATION-GUIDE.md # 画像最適化手順
├─ USAGE-EXAMPLES.md # 画像参照の使用例
└─ IMAGE-EXTRACTION-GUIDE.md # 画像抽出・管理ガイド
```

## 含まれる画像

- フィールドレイアウト図
- マーカーコーン
- ミニハードル
- ミッション関連図表
- その他競技に必要な図表

## ガイドラインと手順

画像の管理と使用には以下のドキュメントを参照してください：

- [画像管理ガイドライン](GUIDE.md) - 画像管理の基本方針と手順
- [画像最適化ガイド](OPTIMIZATION-GUIDE.md) - 画像の最適化手順の詳細
- [画像参照の使用例](USAGE-EXAMPLES.md) - マークダウンでの画像参照方法
- [画像抽出・管理ガイド](IMAGE-EXTRACTION-GUIDE.md) - 画像抽出と管理の詳細手順

## 命名規則

- **フィールド関連**: `field-[内容]-[年度].[拡張子]` (例: field-layout-2024.svg)
- **装置・設備関連**: `equipment-[内容]-[年度].[拡張子]` (例: equipment-marker-cone-2024.svg)
- **ミッション関連**: `missions-[内容]-[年度].[拡張子]` (例: missions-supply-drop-2024.svg)

## メタデータ管理

画像ファイルには以下のメタデータが関連付けられています：

- **ファイル情報**: ファイル名、パス、更新日時
- **分類情報**: カテゴリ、タグ
- **部門情報**: 各画像が関連する部門（一般部門、自動操縦部門、マルチコプター部門、ビギナー部門）

メタデータは以下のファイルで管理されています：

```
docs/metadata/
├─ images_metadata.json     # すべての画像のメタデータ
├─ metadata_field.json     # フィールド関連画像メタデータ
├─ metadata_equipment.json # 装置・機材関連画像メタデータ
├─ metadata_missions.json  # ミッション関連画像メタデータ
└─ METADATA_GUIDE.md       # メタデータ管理ガイド
```

画像メタデータの管理と更新については、[METADATA_GUIDE.md](../metadata/METADATA_GUIDE.md) を参照してください。

メタデータの更新履歴は [METADATA_UPDATE_PROGRESS.md](../metadata/METADATA_UPDATE_PROGRESS.md) に記録されています。

## 注意事項

- 画像をアップロードする前に最適化を行ってください
- 高解像度の画像を使用して、詳細が明確に見えるようにしてください
- SVG形式が推奨されますが、必要に応じてPNGやJPGも使用可能です
- 画像の更新時は同名ファイルで上書きし、古いバージョンは保持しないでください
- 部門情報の更新時はメタデータファイルも必ず修正してください
- メタデータの更新後は `generate_metadata.bat` を実行してカテゴリ別メタデータファイルを更新してください
- 画像の部門情報は、ルール文書との整合性を保つために重要です
