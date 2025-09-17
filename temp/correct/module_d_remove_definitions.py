#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module D: 画像定義の削除
第21回飛行ロボコン - ファイル末尾の画像定義を削除
"""

import re
from pathlib import Path

def remove_image_definitions(file_path: str) -> tuple[bool, list[str]]:
    """
    ファイル末尾の[imageN]: path形式を削除
    
    Returns:
        (success, errors): 成功フラグとエラーリスト
    """
    print(f"\n=== Module D: 画像定義の削除 ===")
    print(f"対象ファイル: {file_path}")
    
    if not Path(file_path).exists():
        return False, [f"ファイルが見つかりません: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 画像定義行を検出して除外
    new_lines = []
    definitions_removed = 0
    errors = []
    
    for line in lines:
        # [imageN]: で始まる行を検出
        if re.match(r'^\[image\d+\]:', line):
            definitions_removed += 1
            print(f"  OK 削除: {line.strip()[:50]}...")  # 最初の50文字を表示
        else:
            new_lines.append(line)
    
    # ファイルを保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n  削除した定義数: {definitions_removed}")
    
    return True, errors

def test_definitions_removed(file_path: str) -> tuple[bool, list[str]]:
    """
    画像定義が削除されたか確認
    
    Returns:
        (success, errors): テスト成功フラグとエラーリスト
    """
    print(f"\n=== Module D: テスト実行 ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    # 画像定義が残っていないか確認
    pattern = r'\[image\d+\]:'
    matches = re.findall(pattern, content)
    
    if matches:
        for match in matches:
            errors.append(f"画像定義が残っています: {match}")
            print(f"  ERROR 画像定義が残っています: {match}")
    else:
        print(f"  OK 全ての画像定義が削除されました")
    
    # GitHub Pages形式の確認
    # 正しい形式の画像参照があるか確認
    direct_refs = re.findall(r'!\[.*?\]\(images/.*?\.png\)', content)
    if direct_refs:
        print(f"  OK 直接参照形式の画像: {len(direct_refs)}個")
    
    # 間違った形式が残っていないか確認
    wrong_refs = re.findall(r'!\[\]\[image\d+\]', content)
    if wrong_refs:
        for ref in wrong_refs:
            errors.append(f"古い参照形式が残っています: {ref}")
            print(f"  ERROR 古い参照形式が残っています: {ref}")
    
    if errors:
        print(f"\n  ERROR テスト失敗: {len(errors)}個のエラー")
        for error in errors:
            print(f"    {error}")
    else:
        print(f"\n  SUCCESS テスト成功: GitHub Pages形式に完全準拠しています")
    
    return len(errors) == 0, errors

def main():
    """メイン処理"""
    work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
    
    if not Path(work_file).exists():
        print(f"❌ 作業ファイルが見つかりません: {work_file}")
        print("Module B, Cを先に実行してください")
        return False
    
    # 画像定義削除実行
    success, errors = remove_image_definitions(work_file)
    
    if not success:
        print("\n❌ 定義削除中にエラーが発生しました:")
        for error in errors:
            print(f"  {error}")
        return False
    
    # テスト実行
    test_success, test_errors = test_definitions_removed(work_file)
    
    if test_success:
        print("\n✅ Module D 完了: 画像定義の削除が成功しました")
        print("  GitHub Pages形式への変換が完了しました")
        return True
    else:
        print("\n❌ Module D 失敗: テストでエラーが検出されました")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)