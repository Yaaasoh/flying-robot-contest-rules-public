#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正しい画像置換スクリプト
GitHub Pages用に画像参照を直接パス形式に変更
"""

import re
from pathlib import Path
from datetime import datetime
import json

# 正しい画像マッピング（元ファイルのキャプションに基づく）
IMAGE_MAPPINGS = {
    'image1': {
        'caption': '図　一般部門・自動操縦部門・ユニークデザイン部門のフィールド',
        'path': 'images/field/field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア_21.png'
    },
    'image2': {
        'caption': '図　滑走路（※実際の滑走路は約5.4m、高さ約20mm）',
        'path': 'images/equipment/equipment-滑走路_21.png'
    },
    'image3': {
        'caption': '図　マルチコプター部門のフィールド',
        'path': 'images/field/field-マルチコプター部門_フィールドレイアウト全体図_21.png'
    },
    'image4': {
        'caption': '図　マーカーコーン',
        'path': 'images/equipment/equipment-マーカーコーン_21.png'
    },
    'image5': {
        'caption': '図　ミニハードル',
        'path': 'images/equipment/equipment-ミニハードル_21.png'
    },
    'image6': {
        'caption': '図　チキンラーメンmini',
        'path': 'images/equipment/equipment-チキンラーメンmini_21.png'
    },
    'image7': {
        'caption': '図　救援物資運搬の流れ',
        'path': 'images/missions/missions-救援物資運搬ミッション図解_21.png'
    },
    'image8': {
        'caption': '図　ラインの定義とポール旋回の経路',
        'path': 'images/missions/missions-ポール旋回ミッション図解_21.png'
    },
    'image9': {
        'caption': '図　水平旋回',
        'path': 'images/missions/missions-自動水平旋回ビギナー部門水平旋回ミッション図解_21.png'
    },
    'image10': {
        'caption': '図　８の字飛行',
        'path': 'images/missions/missions-自動８の字飛行ミッション図解_21.png'
    },
    'image11': {
        'caption': '図　水平旋回',
        'path': 'images/missions/missions-自動水平旋回ビギナー部門水平旋回ミッション図解_21.png'
    },
    'image12': {
        'caption': '図　８の字飛行',
        'path': 'images/missions/missions-マルチコプター部門８の字飛行ミッション図解_21.png'
    },
    'image13': {
        'caption': '図　上昇旋回',
        'path': 'images/missions/missions-自動上昇旋回ミッション図解_21.png'
    },
    'image14': {
        'caption': '図　自動離着陸の流れと点数区別',
        'path': 'images/missions/missions-自動離着陸ミッション図解_21.png'
    },
    'image15': {
        'caption': '図　チキンラーメンmini',
        'path': 'images/equipment/equipment-チキンラーメンmini_21.png'
    },
    'image16': {
        'caption': '図　チキンラーメン',
        'path': 'images/equipment/equipment-チキンラーメン_21.png'
    },
    'image17': {
        'caption': '図　高所物資運搬台',
        'path': 'images/equipment/equipment-高所物資運搬台_21.png'
    },
    'image18': {
        'caption': '図　物資投下エリア',
        'path': 'images/field/field-物資投下エリア_21.png'
    },
    'image19': {
        'caption': '図 ８の字飛行におけるライン設定',
        'path': 'images/missions/missions-マルチコプター部門８の字飛行ミッション図解_21.png'
    }
}

def replace_image_references(file_path: str):
    """
    画像参照を正しい形式に置換
    
    Args:
        file_path: 修正対象のMarkdownファイルパス
    """
    file_path = Path(file_path)
    
    # ファイルを読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # 変更ログ
    changes = []
    
    # Step 1: ![][imageN] 形式を置換
    print("=== Step 1: 画像参照の置換 ===")
    for img_num, mapping in IMAGE_MAPPINGS.items():
        old_pattern = f'![]\\[{img_num}\\]'
        new_reference = f"![{mapping['caption']}]({mapping['path']})"
        
        # 置換実行
        count = len(re.findall(old_pattern, content))
        if count > 0:
            content = re.sub(old_pattern, new_reference, content)
            changes.append({
                'type': 'reference',
                'image': img_num,
                'count': count,
                'new_format': new_reference
            })
            print(f"  {img_num}: {count}箇所を置換")
    
    # Step 2: ファイル末尾の画像定義を削除
    print("\n=== Step 2: 画像定義の削除 ===")
    lines = content.split('\n')
    new_lines = []
    definitions_removed = 0
    
    for line in lines:
        # [imageN]: path 形式の行を除外
        if re.match(r'^\[image\d+\]:', line):
            definitions_removed += 1
            changes.append({
                'type': 'definition_removed',
                'line': line
            })
        else:
            new_lines.append(line)
    
    print(f"  {definitions_removed}個の画像定義を削除")
    
    # 最終的なコンテンツ
    final_content = '\n'.join(new_lines)
    
    # Step 3: ファイルを保存
    output_path = file_path.parent / f"{file_path.stem}_fixed{file_path.suffix}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\n=== 完了 ===")
    print(f"出力ファイル: {output_path}")
    
    # Step 4: 変更ログを保存
    log_path = file_path.parent / 'temp' / 'correct' / 'replacement_log.json'
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'input_file': str(file_path),
        'output_file': str(output_path),
        'changes': changes,
        'summary': {
            'references_replaced': sum(1 for c in changes if c['type'] == 'reference'),
            'definitions_removed': definitions_removed
        }
    }
    
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"変更ログ: {log_path}")
    
    return output_path

def verify_result(file_path: str):
    """
    置換結果を検証
    
    Args:
        file_path: 検証対象のファイルパス
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n=== 検証結果 ===")
    
    # 残っている ![][imageN] 形式をチェック
    old_refs = re.findall(r'!\[\]\[image\d+\]', content)
    if old_refs:
        print(f"❌ エラー: {len(old_refs)}個の古い形式が残っています")
        for ref in old_refs:
            print(f"  - {ref}")
    else:
        print("✅ すべての古い形式が置換されました")
    
    # 残っている画像定義をチェック
    definitions = re.findall(r'^\[image\d+\]:', content, re.MULTILINE)
    if definitions:
        print(f"❌ エラー: {len(definitions)}個の画像定義が残っています")
        for def_ in definitions:
            print(f"  - {def_}")
    else:
        print("✅ すべての画像定義が削除されました")
    
    # 新しい形式の画像参照をカウント
    new_refs = re.findall(r'!\[.*?\]\(images/.*?\.png\)', content)
    print(f"ℹ️ {len(new_refs)}個の正しい形式の画像参照があります")
    
    return len(old_refs) == 0 and len(definitions) == 0

def main():
    """メイン処理"""
    target_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md"
    
    if not Path(target_file).exists():
        print(f"エラー: {target_file} が見つかりません")
        return 1
    
    # 置換実行
    output_file = replace_image_references(target_file)
    
    # 検証
    success = verify_result(output_file)
    
    if success:
        print("\n✅ 置換が正常に完了しました")
        print(f"次のステップ: {output_file} をMkDocsでプレビューして確認してください")
        return 0
    else:
        print("\n❌ エラーが検出されました。手動で確認してください")
        return 1

if __name__ == "__main__":
    exit(main())