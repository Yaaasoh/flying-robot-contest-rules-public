#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元ファイルの[imageN]参照とキャプションの対応を分析
"""

import re
from pathlib import Path

def analyze_image_caption_mapping():
    """元ファイルの画像参照とキャプションの対応を分析"""
    
    file_path = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md.backup_20250910180919"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 画像参照とその前後のキャプションを収集
    mappings = []
    
    for i, line in enumerate(lines):
        if re.search(r'!\[\]\[(image\d+)\]', line):
            match = re.search(r'\[(image\d+)\]', line)
            if match:
                image_num = match.group(1)
                
                # 前の行のキャプションを探す
                caption_before = None
                if i > 0 and lines[i-1].strip().startswith('図'):
                    caption_before = lines[i-1].strip()
                
                # 次の行のキャプションを探す
                caption_after = None
                if i < len(lines) - 1 and lines[i+1].strip().startswith('図'):
                    caption_after = lines[i+1].strip()
                
                # 画像の行の内容も確認
                image_line_content = line.strip()
                
                mappings.append({
                    'line': i + 1,
                    'image_num': image_num,
                    'caption_before': caption_before,
                    'caption_after': caption_after,
                    'image_line': image_line_content[:50] if len(image_line_content) > 50 else image_line_content
                })
    
    # 結果を出力
    print("=== 元ファイルの画像番号とキャプションの対応 ===\n")
    print("行番号 | 画像番号 | キャプション")
    print("-------|----------|-------------")
    
    for m in mappings:
        caption = m['caption_after'] if m['caption_after'] else m['caption_before'] if m['caption_before'] else "(キャプションなし)"
        print(f"Line {m['line']:3} | {m['image_num']:8} | {caption}")
    
    # 画像番号の意図を推定
    print("\n=== 画像番号の元々の意図（推定） ===\n")
    
    # 画像管理シートの内容と比較
    sheet_mapping = {
        'image1': '救援物資運搬ミッション図解',
        'image2': 'マルチコプター部門８の字飛行ミッション図解',
        'image3': 'マーカーコーン',
        'image4': '自動上昇旋回ミッション図解',
        'image5': '物資投下エリア',
        'image6': 'チキンラーメンmini',
        'image7': '識別用紙_正解の台',
        'image8': '自動８の字飛行ミッション図解',
        'image9': '自動水平旋回ビギナー部門水平旋回ミッション図解',
        'image10': '一般部門_自動操縦部門_ユニークデザイン部門競技エリア',
        'image11': '一般部門_自動操縦部門_フィールドレイアウト全体図',
        'image12': 'マルチコプター部門_フィールドレイアウト全体図',
        'image13': '滑走路',
        'image14': 'ポール旋回ミッション図解',
        'image15': 'ミニハードル',
        'image16': 'ミニハードル',
        'image17': '高所物資運搬台',
        'image18': 'チキンラーメン',
        'image19': '自動離着陸ミッション図解'
    }
    
    print("画像番号 | 元ファイルのキャプション | 管理シートの内容 | 一致？")
    print("---------|------------------------|-----------------|-------")
    
    for m in mappings:
        caption = m['caption_after'] if m['caption_after'] else m['caption_before'] if m['caption_before'] else ""
        # キャプションから「図　」を除去して比較
        caption_clean = caption.replace('図　', '').replace('図 ', '') if caption else ""
        sheet_content = sheet_mapping.get(m['image_num'], "")
        
        # 部分一致で判定
        match = "OK" if sheet_content and caption_clean and (sheet_content in caption_clean or caption_clean in sheet_content) else "?"
        
        print(f"{m['image_num']:8} | {caption_clean[:25]:25} | {sheet_content[:25]:25} | {match}")
    
    return mappings

if __name__ == "__main__":
    mappings = analyze_image_caption_mapping()
    print(f"\n総画像数: {len(mappings)}個")