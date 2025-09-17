#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module B: 既存画像参照の置換
第21回飛行ロボコン - 既存の画像参照を直接パス形式に置換
"""

import re
from pathlib import Path
from datetime import datetime

# 画像参照マッピングテーブル（統一形式：キャプションなし）
IMAGE_MAPPING = {
    "image1": None,  # 削除予定（新規画像で置き換え）
    "image2": None,  # 削除予定（新規画像で置き換え）
    "image3": None,  # 削除予定（削除のみ）
    "image4": "images/equipment/equipment-マーカーコーン_21.png",
    "image5": "images/equipment/equipment-ミニハードル_21.png",
    "image6": "images/equipment/equipment-チキンラーメンmini_21.png",
    "image7": "images/missions/missions-救援物資運搬ミッション図解_21.png",
    "image8": "images/missions/missions-ポール旋回ミッション図解_21.png",
    "image9": "images/missions/missions-自動水平旋回ビギナー部門水平旋回ミッション図解_21.png",
    "image10": "images/missions/missions-自動８の字飛行ミッション図解_21.png",
    "image11": "images/missions/missions-自動水平旋回ビギナー部門水平旋回ミッション図解_21.png",
    "image12": "images/missions/missions-マルチコプター部門８の字飛行ミッション図解_21.png",
    "image13": "images/missions/missions-自動上昇旋回ミッション図解_21.png",
    "image14": "images/missions/missions-自動離着陸ミッション図解_21.png",
    "image15": "images/equipment/equipment-チキンラーメンmini_21.png",
    "image16": "images/equipment/equipment-チキンラーメン_21.png",
    "image17": "images/equipment/equipment-高所物資運搬台_21.png",
    "image18": "images/equipment/equipment-識別用紙_正解の台_21.png",
    "image19": "images/missions/missions-マルチコプター部門８の字飛行ミッション図解_21.png",
}

def replace_existing_images(file_path: str) -> tuple[bool, list[str]]:
    """
    既存の画像参照を置換
    
    Returns:
        (success, errors): 成功フラグとエラーリスト
    """
    print(f"\n=== Module B: 既存画像参照の置換 ===")
    print(f"対象ファイル: {file_path}")
    
    if not Path(file_path).exists():
        return False, [f"ファイルが見つかりません: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    errors = []
    replacements_made = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 行内の全ての![][imageN]パターンを検出・置換
        matches = re.findall(r'!\[\]\[(image\d+)\]', line)
        if matches:
            new_line = line
            skip_line = False
            
            for img_id in matches:
                if img_id in IMAGE_MAPPING:
                    path = IMAGE_MAPPING[img_id]
                    
                    if path is None:
                        # 削除対象（後で新規画像を追加する箇所）
                        print(f"  SKIP {img_id}: 削除対象（新規画像で置き換え予定）")
                        skip_line = True
                        break
                    else:
                        # 置換対象（統一形式：キャプションなし）
                        new_line = new_line.replace(f'![][{img_id}]', f'![]({path})')
                        replacements_made += 1
                        print(f"  OK {img_id}: -> {path}")
                else:
                    errors.append(f"未知の画像ID: {img_id}")
            
            if skip_line:
                # この行をスキップ
                i += 1
                # 次の行がキャプションの場合もスキップ
                if i < len(lines) and lines[i].strip().startswith('図'):
                    i += 1
                continue
            else:
                new_lines.append(new_line)
        else:
            new_lines.append(line)
        
        i += 1
    
    # ファイルを保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n  置換数: {replacements_made}")
    
    return len(errors) == 0, errors

def test_replacements(file_path: str) -> tuple[bool, list[str]]:
    """
    置換結果をテスト
    
    Returns:
        (success, errors): テスト成功フラグとエラーリスト
    """
    print(f"\n=== Module B: テスト実行 ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    # 古い形式が残っていないか確認（削除対象以外）
    for img_id, path in IMAGE_MAPPING.items():
        if path is not None:  # 削除対象でない場合
            old_format = f'![][{img_id}]'
            if old_format in content:
                errors.append(f"ERROR 古い画像参照が残っています: {old_format}")
    
    # 新しい形式が正しく挿入されているか確認（統一形式）
    for img_id, path in IMAGE_MAPPING.items():
        if path:  # 削除対象でない場合
            expected = f"![]({path})"
            if expected not in content:
                errors.append(f"ERROR {img_id}: 期待される形式が見つかりません: {expected}")
            else:
                print(f"  OK {img_id}: 正しく置換されています")
    
    if errors:
        print(f"\n  ERROR テスト失敗: {len(errors)}個のエラー")
        for error in errors:
            print(f"    {error}")
    else:
        print(f"\n  SUCCESS テスト成功: 全ての置換が正しく実行されました")
    
    return len(errors) == 0, errors

def main():
    """メイン処理"""
    work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
    
    # 作業ファイルが存在しない場合は作成
    if not Path(work_file).exists():
        original = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md"
        if Path(original).exists():
            print(f"作業ファイルを作成: {work_file}")
            with open(original, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(work_file, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"ERROR 元ファイルが見つかりません: {original}")
            return False
    
    # 置換実行
    success, errors = replace_existing_images(work_file)
    
    if not success:
        print("\nERROR 置換中にエラーが発生しました:")
        for error in errors:
            print(f"  {error}")
        return False
    
    # テスト実行
    test_success, test_errors = test_replacements(work_file)
    
    if test_success:
        print("\nSUCCESS Module B 完了: 既存画像の置換が成功しました")
        return True
    else:
        print("\nERROR Module B 失敗: テストでエラーが検出されました")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)