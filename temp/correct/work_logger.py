#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作業ログシステム
各段階の実行結果を詳細に記録
"""

import datetime
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

class WorkLogger:
    """作業ログを管理するクラス"""
    
    def __init__(self, log_dir: str = "temp"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"work_log_{self.timestamp}.txt"
        self.json_log = self.log_dir / f"work_log_{self.timestamp}.json"
        
        self.session_data = {
            "session_id": self.timestamp,
            "start_time": datetime.datetime.now().isoformat(),
            "phases": [],
            "status": "started",
            "total_errors": 0,
            "total_warnings": 0
        }
        
        self._write_header()
    
    def _write_header(self):
        """ログファイルのヘッダーを書き込み"""
        header = f"""
{'='*60}
第21回飛行ロボコン修正作業ログ
{'='*60}
セッションID: {self.timestamp}
開始時刻: {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
作業者: Claude Code (自動化システム)
{'='*60}

"""
        self._append_log(header)
    
    def _append_log(self, message: str):
        """ログファイルにメッセージを追記"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(message)
    
    def _save_json_log(self):
        """JSON形式でログを保存"""
        with open(self.json_log, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2)
    
    def start_phase(self, phase_name: str, description: str) -> Dict[str, Any]:
        """フェーズ開始をログに記録"""
        phase_data = {
            "phase_name": phase_name,
            "description": description,
            "start_time": datetime.datetime.now().isoformat(),
            "end_time": None,
            "status": "in_progress",
            "commands": [],
            "results": [],
            "errors": [],
            "warnings": []
        }
        
        self.session_data["phases"].append(phase_data)
        
        log_message = f"""
{'='*40}
Phase: {phase_name}
{'='*40}
説明: {description}
開始時刻: {datetime.datetime.now().strftime('%H:%M:%S')}

"""
        self._append_log(log_message)
        self._save_json_log()
        
        return phase_data
    
    def log_command(self, command: str, description: str = ""):
        """実行コマンドをログに記録"""
        current_phase = self.session_data["phases"][-1]
        
        command_data = {
            "command": command,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        current_phase["commands"].append(command_data)
        
        log_message = f"""
>>> コマンド実行: {command}
    説明: {description}
    時刻: {datetime.datetime.now().strftime('%H:%M:%S')}

"""
        self._append_log(log_message)
        self._save_json_log()
    
    def log_result(self, result: str, status: str = "info"):
        """実行結果をログに記録"""
        current_phase = self.session_data["phases"][-1]
        
        result_data = {
            "result": result,
            "status": status,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        current_phase["results"].append(result_data)
        
        status_symbol = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "info": "ℹ️"
        }.get(status, "•")
        
        log_message = f"    {status_symbol} {result}\n"
        self._append_log(log_message)
        self._save_json_log()
    
    def log_error(self, error_message: str, error_details: str = ""):
        """エラーをログに記録"""
        current_phase = self.session_data["phases"][-1]
        
        error_data = {
            "message": error_message,
            "details": error_details,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        current_phase["errors"].append(error_data)
        self.session_data["total_errors"] += 1
        
        log_message = f"""
    ❌ エラー: {error_message}
    詳細: {error_details}
    時刻: {datetime.datetime.now().strftime('%H:%M:%S')}

"""
        self._append_log(log_message)
        self._save_json_log()
    
    def log_warning(self, warning_message: str):
        """警告をログに記録"""
        current_phase = self.session_data["phases"][-1]
        
        warning_data = {
            "message": warning_message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        current_phase["warnings"].append(warning_data)
        self.session_data["total_warnings"] += 1
        
        log_message = f"    ⚠️ 警告: {warning_message}\n"
        self._append_log(log_message)
        self._save_json_log()
    
    def end_phase(self, status: str = "completed", notes: str = ""):
        """フェーズ終了をログに記録"""
        current_phase = self.session_data["phases"][-1]
        current_phase["end_time"] = datetime.datetime.now().isoformat()
        current_phase["status"] = status
        if notes:
            current_phase["notes"] = notes
        
        duration = self._calculate_duration(current_phase["start_time"], current_phase["end_time"])
        
        status_symbol = {
            "completed": "✅",
            "failed": "❌",
            "skipped": "⏭️",
            "paused": "⏸️"
        }.get(status, "•")
        
        log_message = f"""
{status_symbol} Phase完了: {current_phase['phase_name']}
状態: {status}
所要時間: {duration}
コマンド数: {len(current_phase['commands'])}
エラー数: {len(current_phase['errors'])}
警告数: {len(current_phase['warnings'])}
"""
        if notes:
            log_message += f"備考: {notes}\n"
        
        log_message += "\n"
        
        self._append_log(log_message)
        self._save_json_log()
    
    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """実行時間を計算"""
        start = datetime.datetime.fromisoformat(start_time)
        end = datetime.datetime.fromisoformat(end_time)
        duration = end - start
        
        minutes = int(duration.total_seconds() // 60)
        seconds = int(duration.total_seconds() % 60)
        
        return f"{minutes}分{seconds}秒"
    
    def create_backup_record(self, files_backed_up: List[str]):
        """バックアップ記録を作成"""
        backup_data = {
            "backup_timestamp": self.timestamp,
            "files": files_backed_up,
            "created_at": datetime.datetime.now().isoformat()
        }
        
        backup_log = self.log_dir / f"backup_record_{self.timestamp}.json"
        with open(backup_log, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        log_message = f"""
💾 バックアップ作成完了
バックアップID: {self.timestamp}
対象ファイル数: {len(files_backed_up)}
"""
        for file in files_backed_up:
            log_message += f"  - {file}\n"
        log_message += "\n"
        
        self._append_log(log_message)
    
    def finalize_session(self, final_status: str = "completed"):
        """セッション終了処理"""
        self.session_data["end_time"] = datetime.datetime.now().isoformat()
        self.session_data["status"] = final_status
        
        total_duration = self._calculate_duration(
            self.session_data["start_time"], 
            self.session_data["end_time"]
        )
        
        summary = f"""
{'='*60}
作業セッション完了
{'='*60}
最終状態: {final_status}
総実行時間: {total_duration}
実行フェーズ数: {len(self.session_data['phases'])}
総エラー数: {self.session_data['total_errors']}
総警告数: {self.session_data['total_warnings']}

完了時刻: {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
ログファイル: {self.log_file}
詳細ログ: {self.json_log}
{'='*60}

"""
        self._append_log(summary)
        self._save_json_log()
        
        return {
            "log_file": str(self.log_file),
            "json_log": str(self.json_log),
            "session_id": self.timestamp,
            "status": final_status,
            "duration": total_duration
        }

# 使用例とテスト関数
def example_usage():
    """使用例"""
    logger = WorkLogger("temp")
    
    # Phase 0: 準備
    phase0 = logger.start_phase("Phase0", "事前準備と現状確認")
    logger.log_command("git status", "現在のファイル状態確認")
    logger.log_result("3個のファイルが変更済みを確認", "info")
    logger.log_command("mkdir -p temp/backups", "バックアップフォルダ作成")
    logger.log_result("バックアップフォルダ作成完了", "success")
    logger.end_phase("completed")
    
    # Phase 1: Module B
    phase1 = logger.start_phase("Phase1", "既存画像参照の置換")
    logger.log_command("python module_b_replace_existing.py", "画像置換実行")
    logger.log_result("19個の画像参照を処理", "info")
    logger.log_warning("image1, image2, image3は削除対象のためスキップ")
    logger.log_result("16個の画像参照を正常に置換", "success")
    logger.end_phase("completed")
    
    # セッション終了
    result = logger.finalize_session("completed")
    print(f"ログファイル作成: {result['log_file']}")

if __name__ == "__main__":
    example_usage()