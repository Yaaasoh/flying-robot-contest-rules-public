#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module C: 新規画像の追加
第21回飛行ロボコン - 修正依頼書に基づく新規画像の追加
"""

import re
from pathlib import Path

# 新規画像挿入設定
NEW_IMAGES = [
    {
        "position": "before",
        "marker": "図　一般部門・自動操縦部門フィールドレイアウト全体図",
        "images": [
            "![](images/field/field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア_21.png)",
            "![](images/field/field-一般部門_自動操縦部門_フィールドレイアウト全体図_21.png)",
            "![](images/field/field-物資投下エリア_21.png)"
        ]
    },
    {
        "position": "before", 
        "marker": "図　滑走路（※実際の滑走路は約5.4m、高さ約20mm）",
        "images": [
            "![](images/equipment/equipment-滑走路_21.png)"
        ]
    },
    {
        "position": "after",
        "marker": "図　滑走路（※実際の滑走路は約5.4m、高さ約20mm）",
        "images": [
            "![](images/field/field-マルチコプター部門競技エリア_21.png)",
            "![](images/field/field-マルチコプター部門_フィールドレイアウト全体図_21.png)"
        ]
    }
]

def add_new_images(file_path: str) -> tuple[bool, list[str]]:
    """
    新規画像を指定位置に追加
    
    Returns:
        (success, errors): 成功フラグとエラーリスト
    """
    print(f"\n=== Module C: 新規画像の追加 ===")
    print(f"対象ファイル: {file_path}")
    
    if not Path(file_path).exists():
        return False, [f"ファイルが見つかりません: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    errors = []
    images_added = 0
    
    # 各挿入設定を処理
    for config in NEW_IMAGES:
        marker = config["marker"]
        position = config["position"]
        images = config["images"]
        
        print(f"\n  処理中: {marker}")
        print(f"    位置: {position}")
        print(f"    画像数: {len(images)}")
        
        # マーカーを探す
        marker_found = False
        new_lines = []
        
        for i, line in enumerate(lines):
            if marker in line:
                marker_found = True
                
                if position == "before":
                    # マーカーの前に画像を挿入
                    for img in images:
                        new_lines.append(img + '\n')
                        images_added += 1
                        print(f"    OK 追加: {img}")
                    new_lines.append('\n')  # 空行を追加
                    new_lines.append(line)  # マーカー行
                    
                elif position == "after":
                    # マーカーの後に画像を挿入
                    new_lines.append(line)  # マーカー行
                    new_lines.append('\n')  # 空行を追加
                    for img in images:
                        new_lines.append(img + '\n')
                        images_added += 1
                        print(f"    OK 追加: {img}")
            else:
                new_lines.append(line)
        
        if not marker_found:
            errors.append(f"マーカーが見つかりません: {marker}")
            print(f"    ERROR マーカーが見つかりません")
        else:
            lines = new_lines  # 更新されたlines を次のループで使用
    
    # ファイルを保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n  追加画像数: {images_added}")
    
    return len(errors) == 0, errors

def test_new_images(file_path: str) -> tuple[bool, list[str]]:
    """
    新規画像が正しく追加されたか確認
    
    Returns:
        (success, errors): テスト成功フラグとエラーリスト
    """
    print(f"\n=== Module C: テスト実行 ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 全ての必要な新規画像
    required_images = [
        "![](images/field/field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア_21.png)",
        "![](images/field/field-一般部門_自動操縦部門_フィールドレイアウト全体図_21.png)",
        "![](images/field/field-物資投下エリア_21.png)",
        "![](images/equipment/equipment-滑走路_21.png)",
        "![](images/field/field-マルチコプター部門競技エリア_21.png)",
        "![](images/field/field-マルチコプター部門_フィールドレイアウト全体図_21.png)"
    ]
    
    errors = []
    for img in required_images:
        if img in content:
            print(f"  OK 画像が見つかりました: {img}")
        else:
            errors.append(f"新規画像が見つかりません: {img}")
            print(f"  ERROR 画像が見つかりません: {img}")
    
    # 画像ファイルの存在確認
    print(f"\n  画像ファイルの存在確認:")
    for img in required_images:
        # パスを抽出
        match = re.search(r'\((.*?)\)', img)
        if match:
            img_path = match.group(1)
            full_path = Path(img_path)
            if full_path.exists():
                print(f"    OK ファイル存在: {img_path}")
            else:
                errors.append(f"画像ファイルが存在しません: {img_path}")
                print(f"    ERROR ファイル不在: {img_path}")
    
    if errors:
        print(f"\n  ERROR テスト失敗: {len(errors)}個のエラー")
        for error in errors:
            print(f"    {error}")
    else:
        print(f"\n  SUCCESS テスト成功: 全ての新規画像が正しく追加されました")
    
    return len(errors) == 0, errors

def main():
    """メイン処理"""
    work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
    
    if not Path(work_file).exists():
        print(f"❌ 作業ファイルが見つかりません: {work_file}")
        print("Module Bを先に実行してください")
        return False
    
    # 新規画像追加実行
    success, errors = add_new_images(work_file)
    
    if not success:
        print("\nERROR 画像追加中にエラーが発生しました:")
        for error in errors:
            print(f"  {error}")
        return False
    
    # テスト実行
    test_success, test_errors = test_new_images(work_file)
    
    if test_success:
        print("\nSUCCESS Module C 完了: 新規画像の追加が成功しました")
        return True
    else:
        print("\nERROR Module C 失敗: テストでエラーが検出されました")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)