#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テスト機能の強化版
画像挿入位置と包括的な検証を追加
"""

import re
from pathlib import Path

def verify_image_positions(content: str) -> list[str]:
    """
    新規画像が正しい位置に挿入されているか確認
    """
    errors = []
    
    # 1. 「図　一般部門...」の前に3つの画像があるか確認
    marker1 = "図　一般部門・自動操縦部門・ユニークデザイン部門のフィールド"
    marker1_pos = content.find(marker1)
    
    if marker1_pos > 0:
        before_marker1 = content[:marker1_pos]
        expected_before_marker1 = [
            "field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア_21.png",
            "field-一般部門_自動操縦部門_フィールドレイアウト全体図_21.png",
            "field-物資投下エリア_21.png"
        ]
        for img in expected_before_marker1:
            if img not in before_marker1:
                errors.append(f"❌ 画像が「{marker1}」の前にありません: {img}")
    else:
        errors.append(f"❌ マーカーが見つかりません: {marker1}")
    
    # 2. 「図　滑走路...」の前後に画像があるか確認
    marker2 = "図　滑走路（※実際の滑走路は約5.4m、高さ約20mm）"
    marker2_pos = content.find(marker2)
    
    if marker2_pos > 0:
        # 前に1つの画像
        before_marker2 = content[:marker2_pos]
        if "equipment-滑走路_21.png" not in before_marker2:
            errors.append(f"❌ 画像が「{marker2}」の前にありません: equipment-滑走路_21.png")
        
        # 後ろに2つの画像
        after_marker2 = content[marker2_pos:]
        expected_after_marker2 = [
            "field-マルチコプター部門競技エリア_21.png",
            "field-マルチコプター部門_フィールドレイアウト全体図_21.png"
        ]
        
        # 次のセクションまでの範囲を確認（大まかに500文字先まで）
        section_content = after_marker2[:1000] if len(after_marker2) > 1000 else after_marker2
        for img in expected_after_marker2:
            if img not in section_content:
                errors.append(f"❌ 画像が「{marker2}」の後にありません: {img}")
    else:
        errors.append(f"❌ マーカーが見つかりません: {marker2}")
    
    return errors

def comprehensive_image_test(file_path: str) -> tuple[bool, list[str]]:
    """
    包括的な画像テスト
    """
    print(f"\n=== 包括的画像テスト ===")
    
    if not Path(file_path).exists():
        return False, [f"ファイルが見つかりません: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    
    # 1. 古い形式の完全除去確認
    old_patterns = re.findall(r'!\[\]\[image\d+\]', content)
    if old_patterns:
        errors.append(f"❌ 古い画像参照が残存: {len(old_patterns)}個")
        for pattern in old_patterns[:5]:  # 最初の5個を表示
            errors.append(f"    - {pattern}")
    
    # 2. 画像定義の完全除去確認
    definition_patterns = re.findall(r'\[image\d+\]:\s*\S+', content)
    if definition_patterns:
        errors.append(f"❌ 画像定義が残存: {len(definition_patterns)}個")
        for pattern in definition_patterns[:3]:  # 最初の3個を表示
            errors.append(f"    - {pattern}")
    
    # 3. 新しい形式の画像参照カウント
    new_format_count = len(re.findall(r'!\[\]\([^)]+\.png\)', content))
    expected_count = 25  # 新規6個 + 既存19個
    
    if new_format_count < expected_count:
        errors.append(f"❌ 画像参照数が不足: {new_format_count}/{expected_count}")
    elif new_format_count > expected_count:
        errors.append(f"⚠️ 画像参照数が過多: {new_format_count}/{expected_count}")
    else:
        print(f"  ✅ 画像参照数が正しい: {new_format_count}個")
    
    # 4. 画像ファイルの物理的存在確認
    image_refs = re.findall(r'!\[\]\(([^)]+\.png)\)', content)
    missing_files = []
    for img_path in image_refs:
        if not Path(img_path).exists():
            missing_files.append(img_path)
    
    if missing_files:
        errors.append(f"❌ 存在しない画像ファイル: {len(missing_files)}個")
        for missing in missing_files[:5]:  # 最初の5個を表示
            errors.append(f"    - {missing}")
    
    # 5. 画像挿入位置の確認
    position_errors = verify_image_positions(content)
    errors.extend(position_errors)
    
    # 6. 重複画像の確認
    image_counts = {}
    for img_path in image_refs:
        image_counts[img_path] = image_counts.get(img_path, 0) + 1
    
    duplicates = {img: count for img, count in image_counts.items() if count > 1}
    if duplicates:
        errors.append(f"⚠️ 重複した画像参照があります:")
        for img, count in duplicates.items():
            errors.append(f"    - {img}: {count}回")
    
    if not errors:
        print(f"  ✅ 全てのテストが成功しました")
        print(f"    - 画像参照数: {new_format_count}")
        print(f"    - 物理ファイル存在: {len(image_refs) - len(missing_files)}/{len(image_refs)}")
        print(f"    - 挿入位置: 正常")
    
    return len(errors) == 0, errors

def create_rollback_function():
    """
    自動ロールバック機能（コード例）
    """
    code_example = '''
def auto_rollback(backup_timestamp: str = None) -> bool:
    """
    バックアップからの自動復元
    """
    backup_base = Path("temp/backups")
    
    if not backup_base.exists():
        print("❌ バックアップフォルダが見つかりません")
        return False
    
    if backup_timestamp:
        backup_dir = backup_base / backup_timestamp
    else:
        # 最新のバックアップを探す
        backups = sorted([d for d in backup_base.iterdir() if d.is_dir()], 
                        key=lambda x: x.name, reverse=True)
        if not backups:
            print("❌ バックアップが見つかりません")
            return False
        backup_dir = backups[0]
    
    if not backup_dir.exists():
        print(f"❌ 指定されたバックアップが存在しません: {backup_dir}")
        return False
    
    # 復元処理
    success_count = 0
    total_count = 0
    
    for backup_file in backup_dir.glob("*"):
        if backup_file.is_file():
            total_count += 1
            try:
                # ファイル名に基づいて復元先を決定
                if backup_file.name == "mkdocs.yml":
                    target = Path("../mkdocs.yml")
                else:
                    target = Path(backup_file.name)
                
                shutil.copy2(backup_file, target)
                print(f"  ✅ 復元: {backup_file.name}")
                success_count += 1
            except Exception as e:
                print(f"  ❌ 復元失敗: {backup_file.name} - {e}")
    
    print(f"\\n復元結果: {success_count}/{total_count} 成功")
    return success_count == total_count
'''
    return code_example

if __name__ == "__main__":
    # テスト実行例
    work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
    if Path(work_file).exists():
        success, errors = comprehensive_image_test(work_file)
        if not success:
            print("\\nエラー詳細:")
            for error in errors:
                print(f"  {error}")
    else:
        print(f"テスト対象ファイルが見つかりません: {work_file}")