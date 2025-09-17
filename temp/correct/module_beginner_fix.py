#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ビギナー部門画像参照修正スクリプト
第21回飛行ロボコン - ビギナー部門の画像参照をGitHub Pages準拠形式に変換
"""

import re
from pathlib import Path
from datetime import datetime

# ビギナー部門の画像マッピング
BEGINNER_IMAGE_MAPPING = {
    "image1": "images/field/field-ビギナー部門フィールドレイアウト図_21.png",
    "image2": "images/field/field-ビギナー部門競技エリア_21.png",
    "image3": "images/field/field-物資投下エリア_21.png",
    "image4": "images/equipment/equipment-滑走路_21.png",
    "image5": "images/equipment/equipment-マーカーコーン_21.png",
    "image6": "images/missions/missions-ビギナー部門水平旋回ミッション図解_21.png",
    "image7": "images/equipment/equipment-チキンラーメンmini_21.png",
    "image8": "images/missions/missions-ビギナー部門水平旋回ミッション図解_21.png"
}

def backup_file(file_path: str) -> str:
    """ファイルのバックアップを作成"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    backup_path = backup_dir / f"Beginner_backup_{timestamp}.md"
    source = Path(file_path)
    
    if source.exists():
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK バックアップ作成: {backup_path}")
        return str(backup_path)
    return ""

def replace_image_references(file_path: str) -> tuple[bool, list[str]]:
    """画像参照を置換"""
    print(f"\n=== ビギナー部門画像参照の置換 ===")
    print(f"対象ファイル: {file_path}")
    
    if not Path(file_path).exists():
        return False, [f"ファイルが見つかりません: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    replacements_made = 0
    
    # 各画像参照を置換
    for img_id, img_path in BEGINNER_IMAGE_MAPPING.items():
        old_pattern = f"![][{img_id}]"
        new_pattern = f"![]({img_path})"
        
        count = content.count(old_pattern)
        if count > 0:
            content = content.replace(old_pattern, new_pattern)
            replacements_made += count
            print(f"  OK {img_id}: {count}箇所置換 -> {img_path}")
    
    # ファイルを保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n  置換総数: {replacements_made}箇所")
    return len(errors) == 0, errors

def remove_image_definitions(file_path: str) -> tuple[bool, list[str]]:
    """画像定義（base64）を削除"""
    print(f"\n=== 画像定義の削除 ===")
    
    if not Path(file_path).exists():
        return False, [f"ファイルが見つかりません: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    definitions_removed = 0
    errors = []
    in_definition_section = False
    
    for i, line in lines:
        # [imageN]: で始まる行を検出
        if re.match(r'^\[image\d+\]:', line):
            in_definition_section = True
            definitions_removed += 1
            print(f"  OK 削除: 行{i+1} - {line[:50]}...")
            continue  # この行をスキップ
        
        # base64データの継続行も削除
        if in_definition_section and line.strip() and not line.startswith('['):
            # まだbase64データが続いている
            continue
        else:
            in_definition_section = False
            new_lines.append(line)
    
    # ファイルを保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n  削除した定義数: {definitions_removed}")
    return True, errors

def verify_conversion(file_path: str) -> tuple[bool, list[str]]:
    """変換結果を検証"""
    print(f"\n=== 変換結果の検証 ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    # 旧形式が残っていないか確認
    old_format_pattern = r'!\[\]\[image\d+\]'
    old_matches = re.findall(old_format_pattern, content)
    
    if old_matches:
        for match in old_matches:
            errors.append(f"旧形式が残っています: {match}")
            print(f"  ERROR 旧形式が残存: {match}")
    else:
        print(f"  OK 旧形式: 0個（完全除去）")
    
    # 新形式の数を確認
    new_format_pattern = r'!\[\]\(images/.*?\.png\)'
    new_matches = re.findall(new_format_pattern, content)
    print(f"  OK 新形式: {len(new_matches)}個")
    
    # base64定義が残っていないか確認
    definition_pattern = r'^\[image\d+\]:'
    def_matches = re.findall(definition_pattern, content, re.MULTILINE)
    
    if def_matches:
        for match in def_matches:
            errors.append(f"画像定義が残っています: {match}")
            print(f"  ERROR 画像定義が残存: {match}")
    else:
        print(f"  OK 画像定義: 0個（完全削除）")
    
    # データURLが残っていないか確認
    if 'data:image/png;base64' in content:
        errors.append("base64データが残っています")
        print(f"  ERROR base64データが残存")
    else:
        print(f"  OK base64データ: 完全削除")
    
    if errors:
        print(f"\n  ERROR 検証失敗: {len(errors)}個のエラー")
        for error in errors:
            print(f"    - {error}")
    else:
        print(f"\n  SUCCESS 検証成功: GitHub Pages形式に完全準拠")
    
    return len(errors) == 0, errors

def main():
    """メイン処理"""
    # 対象ファイル
    target_file = "21FlyRobo_Beginner_Regulations_text.md"
    work_file = "21FlyRobo_Beginner_Regulations_text_WORK.md"
    
    print("=" * 60)
    print("ビギナー部門画像参照修正スクリプト")
    print("=" * 60)
    
    # 元ファイルから作業ファイルを作成
    if not Path(work_file).exists():
        if Path(target_file).exists():
            print(f"\n作業ファイルを作成中...")
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(work_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  OK 作業ファイル作成: {work_file}")
        else:
            print(f"ERROR 対象ファイルが見つかりません: {target_file}")
            return False
    
    # バックアップ作成
    backup_path = backup_file(work_file)
    if not backup_path:
        print("ERROR バックアップ作成に失敗しました")
        return False
    
    # Step 1: 画像参照の置換
    success, errors = replace_image_references(work_file)
    if not success:
        print("\nERROR 画像参照の置換に失敗しました")
        for error in errors:
            print(f"  - {error}")
        return False
    
    # Step 2: 画像定義の削除
    success, errors = remove_image_definitions(work_file)
    if not success:
        print("\nERROR 画像定義の削除に失敗しました")
        for error in errors:
            print(f"  - {error}")
        return False
    
    # Step 3: 結果の検証
    success, errors = verify_conversion(work_file)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ SUCCESS: ビギナー部門の修正が完了しました")
        print(f"  作業ファイル: {work_file}")
        print(f"  バックアップ: {backup_path}")
        print("\n次のステップ:")
        print(f"  1. {work_file} の内容を確認")
        print(f"  2. 問題なければ: copy {work_file} {target_file}")
        print(f"  3. mkdocs serve でプレビュー確認")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ FAILURE: 変換は実行されましたが、検証でエラーが検出されました")
        print(f"  バックアップから復元: copy {backup_path} {work_file}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)