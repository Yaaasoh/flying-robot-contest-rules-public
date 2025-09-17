#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module B: 既存画像参照の置換（修正版）
第21回飛行ロボコン - 既存の画像参照を直接パス形式に置換
Version: 2.0 - インシデント対応修正版
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
    既存の画像参照を置換（修正版）
    
    Returns:
        (success, errors): 成功フラグとエラーリスト
    """
    print(f"\n=== Module B: 既存画像参照の置換（修正版） ===")
    print(f"対象ファイル: {file_path}")
    
    if not Path(file_path).exists():
        return False, [f"ファイルが見つかりません: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    errors = []
    replacements_made = 0
    deletions_made = 0
    lines_to_skip = set()  # スキップする行番号を記録
    
    # まず削除対象の行を特定
    for i, line in enumerate(lines):
        # 削除対象のimage1-3のみを含む行を特定
        if re.search(r'!\[\]\[(image[123])\]', line):
            # この行に削除対象のみが含まれているか確認
            all_images = re.findall(r'!\[\]\[(image\d+)\]', line)
            delete_line = all([IMAGE_MAPPING.get(img) is None for img in all_images])
            
            if delete_line:
                lines_to_skip.add(i)
                # 次の行がキャプションの場合もスキップ
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('図'):
                    lines_to_skip.add(i + 1)
                deletions_made += len(all_images)
                print(f"  DELETE 行{i+1}: {line.strip()[:50]}...")
    
    # 置換処理を実行
    for i, line in enumerate(lines):
        if i in lines_to_skip:
            continue  # スキップ対象行は出力しない
        
        # 置換対象の画像参照を処理
        new_line = line
        matches = re.findall(r'!\[\]\[(image\d+)\]', line)
        
        for img_id in matches:
            if img_id in IMAGE_MAPPING:
                path = IMAGE_MAPPING[img_id]
                if path is not None:  # 置換対象
                    new_line = new_line.replace(f'![][{img_id}]', f'![]({path})')
                    replacements_made += 1
                    print(f"  REPLACE {img_id}: -> {path}")
                else:
                    # 削除対象だが他の画像と同じ行にある場合
                    new_line = new_line.replace(f'![][{img_id}]', '')
                    print(f"  REMOVE {img_id} from mixed line")
            else:
                errors.append(f"未知の画像ID: {img_id}")
        
        # 空行にならない限り出力
        if new_line.strip() or line == '\n':
            new_lines.append(new_line)
    
    # ファイルを保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n  置換数: {replacements_made}")
    print(f"  削除数: {deletions_made}")
    
    return len(errors) == 0, errors

def test_replacements(file_path: str) -> tuple[bool, list[str]]:
    """
    置換結果をテスト（改善版）
    
    Returns:
        (success, errors): テスト成功フラグとエラーリスト
    """
    print(f"\n=== Module B: テスト実行（改善版） ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    # 古い形式が残っていないか確認（削除対象以外）
    for img_id, path in IMAGE_MAPPING.items():
        if path is not None:  # 削除対象でない場合
            old_format = f'![][{img_id}]'
            if old_format in content:
                errors.append(f"ERROR 古い画像参照が残っています: {old_format}")
    
    # 新しい形式が正しく挿入されているか確認
    for img_id, path in IMAGE_MAPPING.items():
        if path:  # 削除対象でない場合
            expected = f"![]({path})"
            count = content.count(expected)
            if count == 0:
                errors.append(f"ERROR {img_id}: 期待される形式が見つかりません: {expected}")
            elif count > 1:
                print(f"  WARNING {img_id}: 複数回出現 ({count}回) - 意図的な可能性あり")
            else:
                print(f"  OK {img_id}: 正しく置換されています")
    
    # 削除対象が残っていないか確認
    for img_id in ["image1", "image2", "image3"]:
        if f"![][{img_id}]" in content:
            errors.append(f"ERROR 削除対象が残っています: {img_id}")
    
    # 配置の妥当性確認（新機能）
    print(f"\n  配置妥当性確認:")
    
    # フィールドセクションにmissions画像がないか確認
    field_section_pattern = r'図.*?フィールド.*?\n(.*?)(?=\n### |\Z)'
    field_sections = re.findall(field_section_pattern, content, re.DOTALL)
    for section in field_sections:
        if 'missions-' in section and len(section) < 500:  # 短いセクションのみ
            errors.append(f"ERROR フィールドセクションにmissions画像が混入")
            print(f"    ERROR: フィールドセクションに不適切な画像")
    
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