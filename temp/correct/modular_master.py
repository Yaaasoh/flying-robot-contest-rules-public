#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
モジュラー実行マスタースクリプト
第21回飛行ロボコン修正作業を段階的に実行
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import shutil

def print_header(title: str):
    """ヘッダーを表示"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def create_backup():
    """Module A: バックアップ作成"""
    print_header("Module A: バックアップとセットアップ")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"temp/backups/{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_backup = [
        "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md",
        "21FlyRobo_Beginner_Regulations_text_EDIT.md",
        "index.md"
    ]
    
    # mkdocs.ymlは親ディレクトリにある
    if Path("../mkdocs.yml").exists():
        files_to_backup.append("../mkdocs.yml")
    
    backup_success = True
    for file in files_to_backup:
        if Path(file).exists():
            shutil.copy2(file, backup_dir)
            print(f"  ✅ バックアップ: {file}")
        else:
            print(f"  ⚠️ ファイルが見つかりません: {file}")
    
    print(f"\n  バックアップ場所: {backup_dir}")
    
    # 作業ファイルの作成
    original = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md"
    work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
    
    if Path(original).exists():
        shutil.copy2(original, work_file)
        print(f"  ✅ 作業ファイル作成: {work_file}")
    else:
        print(f"  ❌ 元ファイルが見つかりません: {original}")
        return False
    
    return True

def run_module(module_name: str, script_name: str) -> bool:
    """
    モジュールを実行
    
    Args:
        module_name: モジュール名（表示用）
        script_name: 実行するスクリプト名
    
    Returns:
        成功した場合True
    """
    print_header(f"{module_name} 実行中")
    
    script_path = Path(f"temp/correct/{script_name}")
    if not script_path.exists():
        print(f"  ❌ スクリプトが見つかりません: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        print(result.stdout)
        if result.stderr:
            print(f"  警告: {result.stderr}")
        
        if result.returncode == 0:
            print(f"\n  ✅ {module_name} 成功")
            return True
        else:
            print(f"\n  ❌ {module_name} 失敗 (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"  ❌ エラー: {e}")
        return False

def confirm_continue(message: str) -> bool:
    """ユーザーに続行確認"""
    print(f"\n{message}")
    response = input("続行しますか？ (y/n): ").lower().strip()
    return response == 'y'

def main():
    """メイン処理"""
    print_header("第21回飛行ロボコン モジュラー修正実行")
    
    print("""
このスクリプトは以下のモジュールを段階的に実行します：
  Module A: バックアップとセットアップ
  Module B: 既存画像参照の置換
  Module C: 新規画像の追加
  Module D: 画像定義の削除
  Module E: テキスト修正（index.md, mkdocs.yml）

各モジュール実行後に確認を求めます。
問題があれば、いつでも中断できます。
    """)
    
    if not confirm_continue("開始しますか？"):
        print("中断しました")
        return
    
    # Module A: バックアップ
    if not create_backup():
        print("\n❌ バックアップ作成に失敗しました")
        return
    
    if not confirm_continue("Module B（既存画像置換）を実行しますか？"):
        print("中断しました")
        return
    
    # Module B: 既存画像置換
    if not run_module("Module B", "module_b_replace_existing.py"):
        print("\n❌ Module B で失敗しました")
        if not confirm_continue("エラーを無視して続行しますか？"):
            print("中断しました")
            return
    
    if not confirm_continue("Module C（新規画像追加）を実行しますか？"):
        print("中断しました")
        return
    
    # Module C: 新規画像追加
    if not run_module("Module C", "module_c_add_new_images.py"):
        print("\n❌ Module C で失敗しました")
        if not confirm_continue("エラーを無視して続行しますか？"):
            print("中断しました")
            return
    
    if not confirm_continue("Module D（画像定義削除）を実行しますか？"):
        print("中断しました")
        return
    
    # Module D: 画像定義削除
    if not run_module("Module D", "module_d_remove_definitions.py"):
        print("\n❌ Module D で失敗しました")
        if not confirm_continue("エラーを無視して続行しますか？"):
            print("中断しました")
            return
    
    # 最終確認
    print_header("作業完了")
    
    print("""
画像関連の修正が完了しました。

次のステップ：
1. 生成された _WORK.md ファイルを確認
2. 問題なければ、元のファイル名にリネーム：
   21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md 
   → 21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md

3. MkDocsでプレビュー確認：
   mkdocs serve

4. index.mdとmkdocs.ymlの修正も必要です（Module E）

問題があった場合は、temp/backups/ から復元できます。
    """)

if __name__ == "__main__":
    main()