#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
シンプルなモジュールテスト実行
文字エンコーディング問題を回避
"""

import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime

def create_backup():
    """安全バックアップの作成"""
    print("=== バックアップ作成中 ===")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"temp/backups/safety_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    target_files = [
        "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md",
        "21FlyRobo_Beginner_Regulations_text_EDIT.md", 
        "index.md",
        "../mkdocs.yml"
    ]
    
    backed_up = 0
    for file in target_files:
        file_path = Path(file)
        if file_path.exists():
            try:
                if file == "../mkdocs.yml":
                    dest = backup_dir / "mkdocs.yml"
                else:
                    dest = backup_dir / file_path.name
                shutil.copy2(file_path, dest)
                print(f"  バックアップ完了: {file}")
                backed_up += 1
            except Exception as e:
                print(f"  バックアップ失敗: {file} - {e}")
                return False
        else:
            print(f"  ファイル不在: {file}")
    
    print(f"バックアップ完了: {backed_up}個のファイル -> {backup_dir}")
    return True

def test_module_b():
    """Module B のテスト"""
    print("\n=== Module B テスト ===")
    
    script = "temp/correct/module_b_replace_existing.py"
    
    try:
        result = subprocess.run([sys.executable, script], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("Module B 実行成功")
            
            # 作業ファイルの確認
            work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
            if Path(work_file).exists():
                with open(work_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                new_count = content.count('![](')
                old_count = content.count('![][image')
                print(f"  新形式画像: {new_count}個")
                print(f"  旧形式画像: {old_count}個")
                return True, {"new": new_count, "old": old_count}
            else:
                print("  作業ファイルが作成されていません")
                return False, {}
        else:
            print(f"Module B 実行失敗: {result.stderr}")
            return False, {"error": result.stderr}
            
    except Exception as e:
        print(f"Module B エラー: {e}")
        return False, {"error": str(e)}

def test_module_c():
    """Module C のテスト"""
    print("\n=== Module C テスト ===")
    
    work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
    if not Path(work_file).exists():
        print("作業ファイルがありません。Module B を先に実行してください。")
        return False, {}
    
    # 実行前の画像数
    with open(work_file, 'r', encoding='utf-8') as f:
        content_before = f.read()
    count_before = content_before.count('![](')
    
    script = "temp/correct/module_c_add_new_images.py"
    
    try:
        result = subprocess.run([sys.executable, script],
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("Module C 実行成功")
            
            # 実行後の画像数
            with open(work_file, 'r', encoding='utf-8') as f:
                content_after = f.read()
            count_after = content_after.count('![](')
            added = count_after - count_before
            
            print(f"  実行前: {count_before}個")
            print(f"  実行後: {count_after}個")
            print(f"  追加: {added}個")
            
            return True, {"before": count_before, "after": count_after, "added": added}
        else:
            print(f"Module C 実行失敗: {result.stderr}")
            return False, {"error": result.stderr}
            
    except Exception as e:
        print(f"Module C エラー: {e}")
        return False, {"error": str(e)}

def test_module_d():
    """Module D のテスト"""
    print("\n=== Module D テスト ===")
    
    work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
    
    # 実行前の定義数
    with open(work_file, 'r', encoding='utf-8') as f:
        content_before = f.read()
    
    import re
    defs_before = len(re.findall(r'\[image\d+\]:', content_before))
    
    script = "temp/correct/module_d_remove_definitions.py"
    
    try:
        result = subprocess.run([sys.executable, script],
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("Module D 実行成功")
            
            # 実行後の定義数
            with open(work_file, 'r', encoding='utf-8') as f:
                content_after = f.read()
            defs_after = len(re.findall(r'\[image\d+\]:', content_after))
            
            print(f"  実行前定義: {defs_before}個")
            print(f"  実行後定義: {defs_after}個")
            print(f"  削除: {defs_before - defs_after}個")
            
            return True, {"before": defs_before, "after": defs_after}
        else:
            print(f"Module D 実行失敗: {result.stderr}")
            return False, {"error": result.stderr}
            
    except Exception as e:
        print(f"Module D エラー: {e}")
        return False, {"error": str(e)}

def main():
    """メイン実行"""
    print("=== 第21回飛行ロボコン修正作業テスト ===")
    print("開始時刻:", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    
    success_count = 0
    total_tests = 4
    
    # 1. バックアップ
    if create_backup():
        success_count += 1
        print("  [1/4] バックアップ: OK")
    else:
        print("  [1/4] バックアップ: ERROR")
        return False
    
    # 2. Module B
    success_b, stats_b = test_module_b()
    if success_b:
        success_count += 1
        print(f"  [2/4] Module B: OK (新形式: {stats_b.get('new', 0)}個)")
    else:
        print("  [2/4] Module B: ERROR")
        return False
    
    # 3. Module C
    success_c, stats_c = test_module_c()
    if success_c:
        success_count += 1
        print(f"  [3/4] Module C: OK (追加: {stats_c.get('added', 0)}個)")
    else:
        print("  [3/4] Module C: ERROR")
        return False
    
    # 4. Module D
    success_d, stats_d = test_module_d()
    if success_d:
        success_count += 1
        print(f"  [4/4] Module D: OK (定義削除: {stats_d.get('before', 0)}個)")
    else:
        print("  [4/4] Module D: ERROR")
        return False
    
    print("\n=== テスト完了 ===")
    print(f"成功: {success_count}/{total_tests}")
    print("終了時刻:", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    
    if success_count == total_tests:
        print("\n全てのテストが成功しました！")
        print("作業ファイル: 21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md")
        print("次のステップ: 内容を確認後、元のファイル名にリネーム")
        return True
    else:
        print(f"\n{total_tests - success_count}個のテストが失敗しました")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)