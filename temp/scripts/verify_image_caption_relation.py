#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像とキャプションの関係を検証
"""

import re
from pathlib import Path

def verify_image_caption_relation():
    """画像タグとキャプションの位置関係を検証"""
    
    files = [
        "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md.backup_20250910180919",
        "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md"
    ]
    
    for file_path in files:
        print(f"\n=== {Path(file_path).name} ===")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 画像タグとキャプションのペアを探す
        for i in range(len(lines)):
            line = lines[i].strip()
            
            # 画像タグを含む行を探す
            if re.search(r'!\[.*?\]\[image\d+\]', line):
                image_match = re.search(r'\[(image\d+)\]', line)
                if image_match:
                    image_num = image_match.group(1)
                    
                    # 前後の行でキャプションを探す
                    caption_before = None
                    caption_after = None
                    
                    if i > 0:
                        before = lines[i-1].strip()
                        if before.startswith('図'):
                            caption_before = before
                    
                    if i < len(lines) - 1:
                        after = lines[i+1].strip()
                        if after.startswith('図'):
                            caption_after = after
                    
                    # レポート出力
                    if caption_before or caption_after:
                        print(f"\nLine {i+1}: {image_num}")
                        if caption_before:
                            print(f"  前の行のキャプション: {caption_before}")
                        print(f"  画像タグ: {line[:50]}...")
                        if caption_after:
                            print(f"  次の行のキャプション: {caption_after}")

if __name__ == "__main__":
    verify_image_caption_relation()