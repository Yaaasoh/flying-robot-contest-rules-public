#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飛行ロボコン21 画像タグ分析スクリプト
タスク1: 修正履歴の完全調査
"""

import re
import csv
from datetime import datetime
from pathlib import Path

def analyze_image_tags():
    """画像タグの分析を実行"""
    
    # ファイルパス設定
    edit_file = Path("21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md")
    current_file = Path("21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md")
    
    # 画像タグパターン
    image_pattern = r'!\[.*?\]\[image\d+\]'
    
    # ファイル読み込み
    with open(edit_file, 'r', encoding='utf-8') as f:
        edit_content = f.readlines()
    
    with open(current_file, 'r', encoding='utf-8') as f:
        current_content = f.readlines()
    
    # 画像タグ抽出
    edit_tags = []
    current_tags = []
    
    for i, line in enumerate(edit_content, 1):
        matches = re.findall(image_pattern, line)
        for match in matches:
            if m := re.search(r'\[image(\d+)\]', match):
                edit_tags.append({
                    'line_number': i,
                    'image_number': f"image{m.group(1)}",
                    'full_tag': match
                })
    
    for i, line in enumerate(current_content, 1):
        matches = re.findall(image_pattern, line)
        for match in matches:
            if m := re.search(r'\[image(\d+)\]', match):
                current_tags.append({
                    'line_number': i,
                    'image_number': f"image{m.group(1)}",
                    'full_tag': match
                })
    
    # modification_history.txt 作成
    with open('temp/modification_history.txt', 'w', encoding='utf-8') as f:
        f.write("=== 画像タグ変更履歴 ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        f.write(f"修正前ファイル: {edit_file.name}\n")
        f.write(f"修正後ファイル: {current_file.name}\n")
        f.write("\n")
        f.write(f"修正前の画像タグ数: {len(edit_tags)}\n")
        f.write(f"修正後の画像タグ数: {len(current_tags)}\n")
        f.write("\n")
        f.write("=== 詳細情報 ===\n")
        f.write("\n")
        f.write("【修正前の画像タグ】\n")
        for tag in edit_tags:
            f.write(f"Line {tag['line_number']}: {tag['full_tag']}\n")
        
        f.write("\n")
        f.write("【修正後の画像タグ】\n")
        for tag in current_tags:
            f.write(f"Line {tag['line_number']}: {tag['full_tag']}\n")
        
        # 画像番号ごとの使用状況
        f.write("\n")
        f.write("=== 画像番号別の使用状況 ===\n")
        
        # 修正前の画像番号集計
        edit_image_counts = {}
        for tag in edit_tags:
            img_num = tag['image_number']
            if img_num not in edit_image_counts:
                edit_image_counts[img_num] = []
            edit_image_counts[img_num].append(tag['line_number'])
        
        # 修正後の画像番号集計
        current_image_counts = {}
        for tag in current_tags:
            img_num = tag['image_number']
            if img_num not in current_image_counts:
                current_image_counts[img_num] = []
            current_image_counts[img_num].append(tag['line_number'])
        
        all_images = sorted(set(list(edit_image_counts.keys()) + list(current_image_counts.keys())), 
                          key=lambda x: int(x.replace('image', '')))
        
        for img in all_images:
            edit_lines = edit_image_counts.get(img, [])
            current_lines = current_image_counts.get(img, [])
            f.write(f"\n{img}:\n")
            f.write(f"  修正前: {len(edit_lines)}回使用 (行: {', '.join(map(str, edit_lines))})\n")
            f.write(f"  修正後: {len(current_lines)}回使用 (行: {', '.join(map(str, current_lines))})\n")
    
    # image_tag_changes.csv 作成
    with open('temp/image_tag_changes.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Type', 'LineNumber', 'ImageNumber', 'FullTag'])
        
        for tag in edit_tags:
            writer.writerow(['BEFORE', tag['line_number'], tag['image_number'], tag['full_tag']])
        
        for tag in current_tags:
            writer.writerow(['AFTER', tag['line_number'], tag['image_number'], tag['full_tag']])
    
    print(f"完了: modification_history.txt と image_tag_changes.csv を作成しました")
    print(f"修正前: {len(edit_tags)} タグ")
    print(f"修正後: {len(current_tags)} タグ")
    
    return len(edit_tags), len(current_tags)

if __name__ == "__main__":
    analyze_image_tags()