#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飛行ロボコン21 原因分析スクリプト
タスク4: 部分修正による全体破壊の原因分析
"""

import os
import re
from pathlib import Path
from datetime import datetime
import csv

def analyze_root_cause():
    """修正作業の原因分析を実行"""
    
    # バックアップファイルの確認
    backup_files = []
    current_dir = Path(".")
    
    # バックアップファイルのパターン
    backup_patterns = [
        "*backup*",
        "*EDIT*.backup*"
    ]
    
    for pattern in backup_patterns:
        for file in current_dir.glob(pattern):
            if file.is_file():
                stat = file.stat()
                backup_files.append({
                    'name': file.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'path': str(file)
                })
    
    # タイムライン順にソート
    backup_files.sort(key=lambda x: x['modified'])
    
    # modification_timeline.csv 作成
    with open('temp/modification_timeline.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'File', 'Size_KB'])
        
        for backup in backup_files:
            writer.writerow([
                backup['modified'].strftime('%Y-%m-%d %H:%M:%S'),
                backup['name'],
                round(backup['size'] / 1024, 2)
            ])
    
    # root_cause_analysis.txt 作成
    with open('temp/root_cause_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("=== 部分修正による全体破壊の原因分析 ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        
        f.write("## 1. 修正作業のタイムライン\n")
        f.write("\n")
        for backup in backup_files:
            f.write(f"- {backup['modified'].strftime('%Y-%m-%d %H:%M:%S')}: {backup['name']} ({round(backup['size'] / 1024, 2)} KB)\n")
        
        f.write("\n")
        f.write("## 2. 判明した問題点\n")
        f.write("\n")
        
        f.write("### 2.1 画像番号の重複問題\n")
        f.write("- image15が「equipment-チキンラーメンmini_21.png」を参照（誤り）\n")
        f.write("- 正しくは「equipment-ミニハードル_21.png」を参照すべき\n")
        f.write("- image16も「equipment-ミニハードル_21.png」を参照（重複）\n")
        f.write("\n")
        
        f.write("### 2.2 キャプション問題\n")
        f.write("- 「図　」で始まるキャプションが存在\n")
        f.write("- 修正前後で20個のキャプションが存在（新規追加0件）\n")
        f.write("- キャプション自体は問題なし\n")
        f.write("\n")
        
        f.write("### 2.3 部分修正の連鎖的影響\n")
        f.write("- 画像参照システムは相互依存性が高い\n")
        f.write("- 一箇所の誤りが全体の整合性を崩す\n")
        f.write("- 画像番号とファイルパスの対応関係が崩れた\n")
        f.write("\n")
        
        f.write("## 3. 根本原因\n")
        f.write("\n")
        f.write("1. **手動での部分的な修正**: 自動化されていない修正作業により、一貫性が失われた\n")
        f.write("2. **検証不足**: 修正後の整合性チェックが不十分だった\n")
        f.write("3. **画像番号の管理ミス**: image15の参照先を誤って設定した\n")
        f.write("4. **重複の見落とし**: image15とimage16の重複を見落とした\n")
        f.write("\n")
        
        f.write("## 4. 推奨される修正アプローチ\n")
        f.write("\n")
        f.write("1. 画像定義部分を一括で正しい内容に置換\n")
        f.write("2. 特にimage15の定義を修正\n")
        f.write("3. 全体の整合性を再確認\n")
        f.write("4. 自動化ツールの使用を検討\n")
    
    # impact_analysis.txt 作成
    with open('temp/impact_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("=== 影響範囲の詳細分析 ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        
        f.write("## 影響を受けた要素\n")
        f.write("\n")
        
        f.write("### 1. 画像定義（ファイル末尾）\n")
        f.write("- image15の定義が誤っている\n")
        f.write("- 他の画像定義は正しい\n")
        f.write("\n")
        
        f.write("### 2. 画像参照（本文中）\n")
        f.write("- 24箇所の画像参照が存在\n")
        f.write("- image15は2箇所で使用（Line 191, Line 1152）\n")
        f.write("- これらの箇所で誤った画像が表示される\n")
        f.write("\n")
        
        f.write("### 3. セクション別影響度\n")
        f.write("- 共通ルール: image10, image11, image5, image1, image13, image15, image12, image4, image5使用\n")
        f.write("- 一般部門: image6使用\n")
        f.write("- 自動操縦部門: image7, image8使用\n")
        f.write("- ユニークデザイン部門: image9, image10使用\n")
        f.write("- マルチコプター部門: 複数の画像使用\n")
        f.write("\n")
        
        f.write("### 4. 修正の優先度\n")
        f.write("1. **最優先**: image15の定義修正\n")
        f.write("2. **高**: 全体の整合性確認\n")
        f.write("3. **中**: 重複の解消（image16との関係）\n")
    
    print(f"完了: 原因分析ファイルを作成しました")
    print(f"バックアップファイル数: {len(backup_files)}")

if __name__ == "__main__":
    analyze_root_cause()