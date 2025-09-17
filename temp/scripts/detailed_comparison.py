#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飛行ロボコン21 詳細比較スクリプト
タスク5: 修正前後の詳細比較
"""

import re
import csv
from pathlib import Path
from datetime import datetime

def detailed_comparison():
    """修正前後の詳細比較を実行"""
    
    # ファイルパス設定
    edit_file = Path("21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md")
    current_file = Path("21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md")
    
    # ファイル読み込み
    with open(edit_file, 'r', encoding='utf-8') as f:
        edit_lines = f.readlines()
    
    with open(current_file, 'r', encoding='utf-8') as f:
        current_lines = f.readlines()
    
    # セクションパターン
    section_pattern = r'^#+\s*\d+\)\s*(.+)$'
    
    # セクション検出
    sections_info = []
    current_section = "前文"
    
    for i, line in enumerate(current_lines, 1):
        match = re.match(section_pattern, line)
        if match:
            section_name = match.group(1).strip()
            sections_info.append({
                'name': section_name,
                'start_line': i
            })
    
    # 画像タグの位置情報を収集
    image_pattern = r'!\[.*?\]\[(image\d+)\]'
    tag_locations = []
    
    for i, line in enumerate(current_lines, 1):
        matches = re.findall(image_pattern, line)
        for match in matches:
            # どのセクションに属するか判定
            section = "前文"
            for sec in sections_info:
                if i >= sec['start_line']:
                    section = sec['name']
                else:
                    break
            
            tag_locations.append({
                'line_number': i,
                'image_number': match,
                'section': section,
                'content': line.strip()[:100]  # 最初の100文字
            })
    
    # image_tag_locations.csv 作成
    with open('temp/image_tag_locations.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['LineNumber', 'ImageNumber', 'Section', 'ContentPreview'])
        
        for tag in tag_locations:
            writer.writerow([
                tag['line_number'],
                tag['image_number'],
                tag['section'],
                tag['content']
            ])
    
    # 画像定義部分の比較
    edit_definitions = []
    current_definitions = []
    
    # 最後の30行から画像定義を抽出
    for line in edit_lines[-30:]:
        if line.strip().startswith('[image'):
            edit_definitions.append(line.strip())
    
    for line in current_lines[-30:]:
        if line.strip().startswith('[image'):
            current_definitions.append(line.strip())
    
    # image_definitions_comparison.txt 作成
    with open('temp/image_definitions_comparison.txt', 'w', encoding='utf-8') as f:
        f.write("=== 画像定義部分の詳細比較 ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        
        f.write("## 修正前の画像定義\n")
        for def_line in sorted(edit_definitions):
            f.write(f"{def_line}\n")
        
        f.write("\n")
        f.write("## 修正後の画像定義\n")
        for def_line in sorted(current_definitions):
            f.write(f"{def_line}\n")
        
        f.write("\n")
        f.write("## 差分\n")
        
        # 差分を検出
        for i in range(max(len(edit_definitions), len(current_definitions))):
            edit_def = edit_definitions[i] if i < len(edit_definitions) else "（なし）"
            current_def = current_definitions[i] if i < len(current_definitions) else "（なし）"
            
            if edit_def != current_def:
                f.write(f"\n差分発見:\n")
                f.write(f"  修正前: {edit_def}\n")
                f.write(f"  修正後: {current_def}\n")
    
    # section_impact_report.txt 作成
    with open('temp/section_impact_report.txt', 'w', encoding='utf-8') as f:
        f.write("=== セクション別の影響度レポート ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        
        # セクション別に画像使用状況を集計
        section_images = {}
        for tag in tag_locations:
            section = tag['section']
            if section not in section_images:
                section_images[section] = []
            section_images[section].append(tag['image_number'])
        
        f.write("## セクション別画像使用状況\n")
        f.write("\n")
        
        for section, images in section_images.items():
            f.write(f"### {section}\n")
            f.write(f"使用画像数: {len(images)}\n")
            f.write(f"使用画像: {', '.join(sorted(set(images)))}\n")
            
            # image15が含まれている場合は警告
            if 'image15' in images:
                f.write("⚠️ 警告: image15（誤った参照）が使用されています\n")
            
            f.write("\n")
        
        f.write("## 影響度評価\n")
        f.write("\n")
        
        # image15を使用しているセクションを特定
        affected_sections = [section for section, images in section_images.items() if 'image15' in images]
        
        if affected_sections:
            f.write("### 修正が必要なセクション\n")
            for section in affected_sections:
                f.write(f"- {section}: image15の参照修正が必要\n")
        else:
            f.write("image15を使用しているセクションはありません。\n")
        
        f.write("\n")
        f.write("## 総合評価\n")
        f.write(f"- 総画像使用数: {len(tag_locations)}\n")
        f.write(f"- 影響を受けたセクション数: {len(affected_sections)}\n")
        f.write(f"- 主な問題: image15の誤った画像ファイル参照\n")
        f.write(f"- 修正必要度: 高（画像が正しく表示されない）\n")
    
    print(f"完了: 詳細比較ファイルを作成しました")
    print(f"画像タグ総数: {len(tag_locations)}")
    print(f"セクション数: {len(section_images)}")

if __name__ == "__main__":
    detailed_comparison()