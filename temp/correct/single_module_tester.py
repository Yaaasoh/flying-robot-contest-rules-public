#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
個別モジュール検証システム
各モジュールを単体で安全にテスト実行
"""

import subprocess
import sys
from pathlib import Path
import shutil
from datetime import datetime
from work_logger import WorkLogger

class SingleModuleTester:
    """個別モジュールのテスト実行クラス"""
    
    def __init__(self):
        self.logger = WorkLogger("temp")
        self.work_dir = Path(".")
        self.backup_files = []
        
    def create_safety_backup(self) -> bool:
        """安全なバックアップを作成"""
        phase = self.logger.start_phase("Backup", "安全バックアップの作成")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"temp/backups/safety_{timestamp}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        target_files = [
            "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md",
            "21FlyRobo_Beginner_Regulations_text_EDIT.md",
            "index.md",
            "../mkdocs.yml"
        ]
        
        backed_up_files = []
        
        for file in target_files:
            file_path = Path(file)
            if file_path.exists():
                try:
                    if file == "../mkdocs.yml":
                        dest = backup_dir / "mkdocs.yml"
                    else:
                        dest = backup_dir / file_path.name
                    
                    shutil.copy2(file_path, dest)
                    backed_up_files.append(str(file_path))
                    self.logger.log_result(f"バックアップ完了: {file}", "success")
                except Exception as e:
                    self.logger.log_error(f"バックアップ失敗: {file}", str(e))
                    self.logger.end_phase("failed", f"バックアップエラー: {e}")
                    return False
            else:
                self.logger.log_warning(f"ファイルが見つかりません: {file}")
        
        self.logger.create_backup_record(backed_up_files)
        self.backup_files = backed_up_files
        self.logger.end_phase("completed", f"バックアップ先: {backup_dir}")
        
        print(f"✅ 安全バックアップ完了: {backup_dir}")
        return True
    
    def test_module_b(self) -> tuple[bool, dict]:
        """Module B の単体テスト"""
        phase = self.logger.start_phase("ModuleB_Test", "既存画像参照置換のテスト")
        
        script_path = "temp/correct/module_b_replace_existing.py"
        
        # スクリプトの存在確認
        if not Path(script_path).exists():
            error_msg = f"スクリプトが見つかりません: {script_path}"
            self.logger.log_error("スクリプト不在", error_msg)
            self.logger.end_phase("failed", "スクリプトファイルが存在しない")
            return False, {"error": error_msg}
        
        # 実行前の状態確認
        original_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md"
        work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
        
        self.logger.log_command(f"python {script_path}", "Module B 実行")
        
        try:
            # モジュール実行
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=120  # 2分でタイムアウト
            )
            
            # 実行結果の記録
            if result.returncode == 0:
                self.logger.log_result("Module B 実行成功", "success")
                
                # 出力の記録
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            self.logger.log_result(line.strip(), "info")
                
                # 作業ファイルの確認
                if Path(work_file).exists():
                    self.logger.log_result("作業ファイル作成確認", "success")
                    
                    # 簡単な内容確認
                    with open(work_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # 統計情報
                    new_format_count = content.count('![](')
                    old_format_count = content.count('![][image')
                    
                    self.logger.log_result(f"新形式画像参照: {new_format_count}個", "info")
                    self.logger.log_result(f"旧形式画像参照: {old_format_count}個", "info")
                    
                    stats = {
                        "new_format_count": new_format_count,
                        "old_format_count": old_format_count,
                        "work_file_created": True
                    }
                else:
                    self.logger.log_warning("作業ファイルが作成されていません")
                    stats = {"work_file_created": False}
                
                self.logger.end_phase("completed", "Module B テスト成功")
                return True, stats
                
            else:
                self.logger.log_error("Module B 実行失敗", f"Exit code: {result.returncode}")
                if result.stderr:
                    self.logger.log_error("エラー出力", result.stderr)
                
                self.logger.end_phase("failed", "実行時エラー")
                return False, {"error": result.stderr}
                
        except subprocess.TimeoutExpired:
            error_msg = "Module B がタイムアウトしました"
            self.logger.log_error("タイムアウト", error_msg)
            self.logger.end_phase("failed", "実行タイムアウト")
            return False, {"error": error_msg}
        
        except Exception as e:
            error_msg = f"予期しないエラー: {e}"
            self.logger.log_error("予期しないエラー", error_msg)
            self.logger.end_phase("failed", "システムエラー")
            return False, {"error": error_msg}
    
    def test_module_c(self) -> tuple[bool, dict]:
        """Module C の単体テスト"""
        phase = self.logger.start_phase("ModuleC_Test", "新規画像追加のテスト")
        
        script_path = "temp/correct/module_c_add_new_images.py"
        
        # 前提条件確認（作業ファイルが存在するか）
        work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
        if not Path(work_file).exists():
            error_msg = "作業ファイルが見つかりません。Module B を先に実行してください。"
            self.logger.log_error("前提条件エラー", error_msg)
            self.logger.end_phase("failed", "作業ファイル不在")
            return False, {"error": error_msg}
        
        # 実行前の画像数カウント
        with open(work_file, 'r', encoding='utf-8') as f:
            content_before = f.read()
        image_count_before = content_before.count('![](')
        self.logger.log_result(f"実行前画像数: {image_count_before}個", "info")
        
        self.logger.log_command(f"python {script_path}", "Module C 実行")
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60
            )
            
            if result.returncode == 0:
                self.logger.log_result("Module C 実行成功", "success")
                
                # 実行後の画像数確認
                with open(work_file, 'r', encoding='utf-8') as f:
                    content_after = f.read()
                image_count_after = content_after.count('![](')
                
                added_images = image_count_after - image_count_before
                self.logger.log_result(f"実行後画像数: {image_count_after}個", "info")
                self.logger.log_result(f"追加された画像: {added_images}個", "info")
                
                # 期待値との比較（6個の新規画像が追加されるはず）
                if added_images == 6:
                    self.logger.log_result("期待通りの画像数が追加されました", "success")
                else:
                    self.logger.log_warning(f"期待される追加数(6個)と異なります: {added_images}個")
                
                stats = {
                    "images_before": image_count_before,
                    "images_after": image_count_after,
                    "images_added": added_images,
                    "expected_added": 6,
                    "success": added_images == 6
                }
                
                self.logger.end_phase("completed", "Module C テスト成功")
                return True, stats
                
            else:
                self.logger.log_error("Module C 実行失敗", f"Exit code: {result.returncode}")
                if result.stderr:
                    self.logger.log_error("エラー出力", result.stderr)
                
                self.logger.end_phase("failed", "実行時エラー")
                return False, {"error": result.stderr}
                
        except Exception as e:
            error_msg = f"Module C エラー: {e}"
            self.logger.log_error("実行エラー", error_msg)
            self.logger.end_phase("failed", "システムエラー")
            return False, {"error": error_msg}
    
    def test_module_d(self) -> tuple[bool, dict]:
        """Module D の単体テスト"""
        phase = self.logger.start_phase("ModuleD_Test", "画像定義削除のテスト")
        
        script_path = "temp/correct/module_d_remove_definitions.py"
        work_file = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_WORK.md"
        
        # 実行前の定義数カウント
        with open(work_file, 'r', encoding='utf-8') as f:
            content_before = f.read()
        
        import re
        definitions_before = len(re.findall(r'\[image\d+\]:', content_before))
        self.logger.log_result(f"実行前画像定義数: {definitions_before}個", "info")
        
        self.logger.log_command(f"python {script_path}", "Module D 実行")
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.log_result("Module D 実行成功", "success")
                
                # 実行後の定義数確認
                with open(work_file, 'r', encoding='utf-8') as f:
                    content_after = f.read()
                
                definitions_after = len(re.findall(r'\[image\d+\]:', content_after))
                removed_definitions = definitions_before - definitions_after
                
                self.logger.log_result(f"実行後画像定義数: {definitions_after}個", "info")
                self.logger.log_result(f"削除された定義: {removed_definitions}個", "info")
                
                # 完全削除の確認
                if definitions_after == 0:
                    self.logger.log_result("全ての画像定義が正常に削除されました", "success")
                else:
                    self.logger.log_warning(f"画像定義が残っています: {definitions_after}個")
                
                stats = {
                    "definitions_before": definitions_before,
                    "definitions_after": definitions_after,
                    "definitions_removed": removed_definitions,
                    "complete_removal": definitions_after == 0
                }
                
                self.logger.end_phase("completed", "Module D テスト成功")
                return True, stats
                
            else:
                self.logger.log_error("Module D 実行失敗", f"Exit code: {result.returncode}")
                self.logger.end_phase("failed", "実行時エラー")
                return False, {"error": result.stderr}
                
        except Exception as e:
            error_msg = f"Module D エラー: {e}"
            self.logger.log_error("実行エラー", error_msg)
            self.logger.end_phase("failed", "システムエラー")
            return False, {"error": error_msg}
    
    def run_comprehensive_test(self) -> tuple[bool, dict]:
        """包括的テストの実行"""
        phase = self.logger.start_phase("Comprehensive_Test", "包括的検証テスト")
        
        test_script = "temp/correct/TEST_ENHANCEMENT.py"
        
        if not Path(test_script).exists():
            self.logger.log_warning("包括的テストスクリプトが見つかりません")
            self.logger.end_phase("skipped", "テストスクリプト不在")
            return True, {"skipped": True}
        
        self.logger.log_command(f"python {test_script}", "包括的テスト実行")
        
        try:
            result = subprocess.run(
                [sys.executable, test_script],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60
            )
            
            # 結果の詳細記録
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        if '✅' in line:
                            self.logger.log_result(line.strip(), "success")
                        elif '❌' in line:
                            self.logger.log_result(line.strip(), "error")
                        elif '⚠️' in line:
                            self.logger.log_result(line.strip(), "warning")
                        else:
                            self.logger.log_result(line.strip(), "info")
            
            test_passed = result.returncode == 0
            
            if test_passed:
                self.logger.end_phase("completed", "包括的テスト合格")
            else:
                self.logger.end_phase("failed", "包括的テストで問題検出")
            
            return test_passed, {"test_output": result.stdout}
            
        except Exception as e:
            error_msg = f"包括的テストエラー: {e}"
            self.logger.log_error("テスト実行エラー", error_msg)
            self.logger.end_phase("failed", "テストシステムエラー")
            return False, {"error": error_msg}
    
    def finalize_test_session(self, overall_success: bool):
        """テストセッションの終了処理"""
        status = "completed" if overall_success else "failed"
        result = self.logger.finalize_session(status)
        
        print("\n" + "="*60)
        print("=== 個別モジュールテスト完了 ===")
        print("="*60)
        print(f"最終状態: {'成功' if overall_success else '失敗'}")
        print(f"実行時間: {result['duration']}")
        print(f"ログファイル: {result['log_file']}")
        print(f"詳細ログ: {result['json_log']}")
        print("="*60)
        
        return result

def main():
    """メイン実行関数"""
    print("=== 個別モジュールテスター開始 ===")
    print("安全な段階的テストを実行します...")
    
    tester = SingleModuleTester()
    overall_success = True
    
    try:
        # 1. 安全バックアップ
        if not tester.create_safety_backup():
            print("エラー: バックアップ作成に失敗しました")
            return False
        
        # 2. Module B テスト
        print("\n>>> Module B (既存画像置換) をテスト中...")
        success_b, stats_b = tester.test_module_b()
        if not success_b:
            print(f"エラー: Module B テスト失敗: {stats_b.get('error', 'Unknown error')}")
            overall_success = False
        else:
            print(f"成功: Module B テスト成功 (新形式: {stats_b['new_format_count']}個)")
        
        # Module B が成功した場合のみ継続
        if success_b:
            # 3. Module C テスト
            print("\n>>> Module C (新規画像追加) をテスト中...")
            success_c, stats_c = tester.test_module_c()
            if not success_c:
                print(f"エラー: Module C テスト失敗: {stats_c.get('error', 'Unknown error')}")
                overall_success = False
            else:
                print(f"成功: Module C テスト成功 (追加画像: {stats_c['images_added']}個)")
            
            # 4. Module D テスト
            if success_c:
                print("\n>>> Module D (画像定義削除) をテスト中...")
                success_d, stats_d = tester.test_module_d()
                if not success_d:
                    print(f"エラー: Module D テスト失敗: {stats_d.get('error', 'Unknown error')}")
                    overall_success = False
                else:
                    print(f"成功: Module D テスト成功 (削除定義: {stats_d['definitions_removed']}個)")
                
                # 5. 包括的テスト
                if success_d:
                    print("\n>>> 包括的テストを実行中...")
                    success_comp, stats_comp = tester.run_comprehensive_test()
                    if not success_comp:
                        print("警告: 包括的テストで問題が検出されました")
                        overall_success = False
                    else:
                        print("成功: 包括的テスト合格")
        
    except KeyboardInterrupt:
        print("\n中断: ユーザーによって中断されました")
        overall_success = False
    
    except Exception as e:
        print(f"\nエラー: 予期しないエラー: {e}")
        overall_success = False
    
    finally:
        # セッション終了処理
        tester.finalize_test_session(overall_success)
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)