#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飛行ロボコン21 キャプション分析スクリプト
タスク2: キャプション調査
"""

import re
from pathlib import Path
from datetime import datetime

def analyze_captions():
    """キャプション（図　で始まる行）の分析を実行"""
    
    # ファイルパス設定
    edit_file = Path("21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md")
    current_file = Path("21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md")
    
    # ファイル読み込み
    with open(edit_file, 'r', encoding='utf-8') as f:
        edit_lines = f.readlines()
    
    with open(current_file, 'r', encoding='utf-8') as f:
        current_lines = f.readlines()
    
    # キャプション抽出（「図　」で始まる行）
    edit_captions = []
    current_captions = []
    
    for i, line in enumerate(edit_lines, 1):
        if line.strip().startswith('図　'):
            edit_captions.append({
                'line_number': i,
                'text': line.strip()
            })
    
    for i, line in enumerate(current_lines, 1):
        if line.strip().startswith('図　'):
            current_captions.append({
                'line_number': i,
                'text': line.strip()
            })
    
    # caption_analysis.txt 作成
    with open('temp/caption_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("=== キャプション分析レポート ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        f.write(f"修正前ファイル: {edit_file.name}\n")
        f.write(f"修正後ファイル: {current_file.name}\n")
        f.write("\n")
        f.write(f"修正前のキャプション数: {len(edit_captions)}\n")
        f.write(f"修正後のキャプション数: {len(current_captions)}\n")
        f.write("\n")
        
        # 詳細情報
        f.write("=== 修正前のキャプション ===\n")
        for cap in edit_captions:
            f.write(f"Line {cap['line_number']}: {cap['text']}\n")
        
        f.write("\n")
        f.write("=== 修正後のキャプション ===\n")
        for cap in current_captions:
            f.write(f"Line {cap['line_number']}: {cap['text']}\n")
        
        # 新規追加・削除されたキャプションの特定
        edit_texts = {cap['text'] for cap in edit_captions}
        current_texts = {cap['text'] for cap in current_captions}
        
        added = current_texts - edit_texts
        removed = edit_texts - current_texts
        kept = edit_texts & current_texts
        
        f.write("\n")
        f.write("=== 変更分析 ===\n")
        f.write(f"新規追加: {len(added)} 件\n")
        f.write(f"削除: {len(removed)} 件\n")
        f.write(f"維持: {len(kept)} 件\n")
    
    # captions_to_remove.txt 作成（新規追加されたものを削除対象とする）
    with open('temp/captions_to_remove.txt', 'w', encoding='utf-8') as f:
        f.write("=== 削除すべきキャプション（新規追加分） ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        
        if added:
            f.write("以下のキャプションは修正作業で新規追加されたものです：\n")
            for text in sorted(added):
                f.write(f"- {text}\n")
                # 該当行番号も記載
                for cap in current_captions:
                    if cap['text'] == text:
                        f.write(f"  （Line {cap['line_number']}）\n")
        else:
            f.write("新規追加されたキャプションはありません。\n")
    
    # captions_to_keep.txt 作成
    with open('temp/captions_to_keep.txt', 'w', encoding='utf-8') as f:
        f.write("=== 保持すべきキャプション（元から存在） ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        
        if kept:
            f.write("以下のキャプションは元から存在していたものです：\n")
            for text in sorted(kept):
                f.write(f"- {text}\n")
                # 該当行番号も記載
                for cap in current_captions:
                    if cap['text'] == text:
                        f.write(f"  （現在: Line {cap['line_number']}）\n")
        else:
            f.write("元から存在していたキャプションはありません。\n")
    
    print(f"完了: キャプション分析ファイルを作成しました")
    print(f"修正前: {len(edit_captions)} キャプション")
    print(f"修正後: {len(current_captions)} キャプション")
    print(f"新規追加: {len(added)} 件")
    print(f"削除: {len(removed)} 件")
    print(f"維持: {len(kept)} 件")

if __name__ == "__main__":
    analyze_captions()