#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module C: 新規画像の追加（修正版）
第21回飛行ロボコン - 修正依頼書に基づく新規画像の追加
Version: 2.0 - インシデント対応修正版
"""

import re
from pathlib import Path

# 新規画像挿入設定（修正版：重複防止と正確なマーカー）
NEW_IMAGES = [
    {
        "position": "before",
        "marker": "図　一般部門・自動操縦部門フィールドレイアウト全体図",
        "marker_type": "exact",  # 完全一致
        "images": [
            "![](images/field/field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア_21.png)",
            "![](images/field/field-一般部門_自動操縦部門_フィールドレイアウト全体図_21.png)",
            "![](images/field/field-物資投下エリア_21.png)"
        ]
    },
    {
        "position": "before", 
        "marker": "図　滑走路（※実際の滑走路は約5.4m、高さ約20mm）",
        "marker_type": "exact",
        "images": [
            "![](images/equipment/equipment-滑走路_21.png)"
        ]
    },
    {
        "position": "after",
        "marker": "図　滑走路（※実際の滑走路は約5.4m、高さ約20mm）",
        "marker_type": "exact",
        "images": [
            "![](images/field/field-マルチコプター部門競技エリア_21.png)",
            "![](images/field/field-マルチコプター部門_フィールドレイアウト全体図_21.png)"
        ]
    }
]

def add_new_images(file_path: str) -> tuple[bool, list[str]]:
    """
    新規画像を指定位置に追加（修正版：重複防止）
    
    Returns:
        (success, errors): 成功フラグとエラーリスト
    """
    print(f"\n=== Module C: 新規画像の追加（修正版） ===")
    print(f"対象ファイル: {file_path}")
    
    if not Path(file_path).exists():
        return False, [f"ファイルが見つかりません: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    errors = []
    images_added = 0
    processed_markers = set()  # 処理済みマーカーを記録
    
    # 各挿入設定を処理
    for config_index, config in enumerate(NEW_IMAGES):
        marker = config["marker"]
        position = config["position"]
        images = config["images"]
        marker_type = config.get("marker_type", "contains")
        
        # 同じマーカーで同じ位置の処理は1回だけ
        marker_key = f"{marker}_{position}"
        if marker_key in processed_markers:
            print(f"  SKIP: {marker} ({position}) - 既に処理済み")
            continue
        
        print(f"\n  処理中: {marker}")
        print(f"    位置: {position}")
        print(f"    画像数: {len(images)}")
        print(f"    マーカータイプ: {marker_type}")
        
        # マーカーを探す
        marker_found = False
        new_lines = []
        
        for i, line in enumerate(lines):
            # マーカーの検索（完全一致 vs 部分一致）
            if marker_type == "exact":
                match = line.strip() == marker
            else:
                match = marker in line
            
            if match and not marker_found:  # 最初の一致のみ処理
                marker_found = True
                processed_markers.add(marker_key)
                
                if position == "before":
                    # マーカーの前に画像を挿入
                    for img in images:
                        new_lines.append(img + '\n')
                        images_added += 1
                        print(f"    OK 追加: {img[:50]}...")
                    new_lines.append('\n')  # 空行を追加
                    new_lines.append(line)  # マーカー行
                    
                elif position == "after":
                    # マーカーの後に画像を挿入
                    new_lines.append(line)  # マーカー行
                    new_lines.append('\n')  # 空行を追加
                    for img in images:
                        new_lines.append(img + '\n')
                        images_added += 1
                        print(f"    OK 追加: {img[:50]}...")
            else:
                new_lines.append(line)
        
        if not marker_found:
            errors.append(f"マーカーが見つかりません: {marker}")
            print(f"    ERROR マーカーが見つかりません")
        else:
            lines = new_lines  # 更新されたlinesを次のループで使用
    
    # ファイルを保存
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n  追加画像数: {images_added}")
    
    return len(errors) == 0, errors

def test_new_images(file_path: str) -> tuple[bool, list[str]]:
    """
    新規画像が正しく追加されたか確認（改善版）
    
    Returns:
        (success, errors): テスト成功フラグとエラーリスト
    """
    print(f"\n=== Module C: テスト実行（改善版） ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
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
    
    # 各画像の存在と数を確認
    print("  画像存在確認:")
    for img in required_images:
        count = content.count(img)
        if count == 0:
            errors.append(f"新規画像が見つかりません: {img}")
            print(f"    ERROR 見つかりません: {img[:50]}...")
        elif count > 1:
            # 警告のみ（エラーにはしない）
            print(f"    WARNING 複数存在 ({count}回): {img[:50]}...")
        else:
            print(f"    OK 正常: {img[:50]}...")
    
    # 画像の配置位置確認（新機能）
    print(f"\n  配置位置確認:")
    
    # フィールドレイアウト図の前に3つの画像があるか
    for i, line in enumerate(lines):
        if "図　一般部門・自動操縦部門フィールドレイアウト全体図" in line:
            # 前の3行に画像があるか確認
            if i >= 3:
                has_field_images = (
                    "field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア" in lines[i-3] and
                    "field-一般部門_自動操縦部門_フィールドレイアウト全体図" in lines[i-2] and
                    "field-物資投下エリア" in lines[i-1]
                )
                if has_field_images:
                    print("    OK フィールド画像の配置正常")
                else:
                    errors.append("フィールド画像の配置が不正")
                    print("    ERROR フィールド画像の配置が不正")
            break
    
    # 滑走路画像の配置確認
    for i, line in enumerate(lines):
        if "図　滑走路" in line and "実際の滑走路は約5.4m" in line:
            # 前に滑走路画像があるか
            if i >= 1 and "equipment-滑走路" in lines[i-1]:
                print("    OK 滑走路画像の配置正常（前）")
            else:
                errors.append("滑走路画像（前）の配置が不正")
                print("    ERROR 滑走路画像（前）の配置が不正")
            
            # 後にマルチコプター画像があるか
            if i < len(lines) - 2:
                has_multi_images = (
                    "field-マルチコプター部門競技エリア" in lines[i+1] or
                    "field-マルチコプター部門競技エリア" in lines[i+2]
                )
                if has_multi_images:
                    print("    OK マルチコプター画像の配置正常（後）")
                else:
                    print("    WARNING マルチコプター画像の確認推奨")
            break
    
    # 画像ファイルの存在確認
    print(f"\n  画像ファイルの物理的存在確認:")
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
        print(f"ERROR 作業ファイルが見つかりません: {work_file}")
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