# 画像メタデータ

このディレクトリには、画像ファイルに関するメタデータを保存しています。メタデータはJSONファイル形式で管理され、画像の属性情報や説明などを含んでいます。

## メタデータの内容

各画像のメタデータには以下の情報が含まれます：

- ファイル名
- カテゴリ
- 説明文
- 作成日
- 最終更新日
- ファイルサイズ
- 解像度
- 撮影者/作成者
- 関連ミッション/機材
- タグ

## ファイル構造

メタデータは以下のファイルに保存されています：

- `images-metadata.json`: すべての画像のメタデータを含む総合ファイル
- `field-images.json`: フィールド関連画像のメタデータ
- `equipment-images.json`: 機材関連画像のメタデータ
- `missions-images.json`: ミッション関連画像のメタデータ

## JSONフォーマット例

```json
{
  "images": [
    {
      "filename": "field-layout-beginner-2025.png",
      "category": "field",
      "description": "2025年度ビギナー部門の競技フィールド全体図",
      "created": "2025-02-15",
      "updated": "2025-03-01",
      "filesize": "256KB",
      "resolution": "1920x1080",
      "author": "飛行ロボコン実行委員会",
      "related": ["beginner", "field-layout"],
      "tags": ["layout", "beginner", "2025"]
    },
    // 他の画像のメタデータ
  ]
}
```

## メタデータの更新

メタデータファイルは、新しい画像が追加されたとき、または既存の画像が更新されたときに更新されます。メタデータの更新には、`create_metadata.py`スクリプトを使用します。

```bash
python docs/tools/create_metadata.py
```

このスクリプトは画像ディレクトリをスキャンし、メタデータを自動的に生成・更新します。
