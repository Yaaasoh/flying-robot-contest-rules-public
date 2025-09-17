#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
キャプション検証スクリプト - 正確な調査
"""

import re
from pathlib import Path
from datetime import datetime

def verify_captions():
    """キャプションの正確な検証"""
    
    # 各ファイルを分析
    files_to_check = [
        "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md.backup_20250910180919",  # 最初のバックアップ
        "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md.backup_20250911113004",  # 2番目のバックアップ
        "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md",  # 編集版
        "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md"  # 現在版
    ]
    
    results = {}
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 「図」で始まる行を収集（全角スペース、半角スペース両方）
            captions = []
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith('図　') or stripped.startswith('図 '):
                    captions.append({
                        'line': i,
                        'text': stripped,
                        'has_fullwidth_space': '　' in stripped[1:2],
                        'raw': repr(line.strip())
                    })
            
            results[file_path] = captions
    
    # レポート作成
    with open('temp/caption_verification_report.txt', 'w', encoding='utf-8') as f:
        f.write("=== キャプション詳細検証レポート ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        
        for file_path, captions in results.items():
            f.write(f"\n## {Path(file_path).name}\n")
            f.write(f"キャプション数: {len(captions)}\n")
            
            if captions:
                f.write("\n詳細:\n")
                for cap in captions:
                    space_type = "全角スペース" if cap['has_fullwidth_space'] else "半角スペース"
                    f.write(f"  Line {cap['line']}: {cap['text']} ({space_type})\n")
        
        # 差分分析
        f.write("\n\n=== 差分分析 ===\n")
        
        if "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md.backup_20250910180919" in results:
            original = results["21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md.backup_20250910180919"]
            current = results.get("21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md", [])
            
            original_texts = {cap['text'] for cap in original}
            current_texts = {cap['text'] for cap in current}
            
            added = current_texts - original_texts
            removed = original_texts - current_texts
            
            f.write(f"\n最初のバックアップ → 現在:\n")
            f.write(f"  追加されたキャプション: {len(added)}\n")
            if added:
                for text in added:
                    f.write(f"    - {text}\n")
            
            f.write(f"  削除されたキャプション: {len(removed)}\n")
            if removed:
                for text in removed:
                    f.write(f"    - {text}\n")
    
    print(f"検証完了: caption_verification_report.txt を作成")
    
    # 統計を表示
    for file_path, captions in results.items():
        print(f"{Path(file_path).name}: {len(captions)} キャプション")

if __name__ == "__main__":
    verify_captions()