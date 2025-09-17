#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像管理シートと各ファイルの画像定義を比較
"""

import csv
from pathlib import Path

def compare_definitions():
    """画像管理シートと実際の定義を比較"""
    
    # 画像管理シートを読み込み
    sheet_mapping = {}
    with open('temp/image_management_sheet.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # パスとファイル名を結合
            full_path = row['path'] + row['file_name']
            sheet_mapping[row['image_number']] = full_path
    
    # 現在のファイルの画像定義を読み込み
    current_definitions = {}
    with open('21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('[image'):
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    img_num = parts[0][1:-1]  # [image1] -> image1
                    file_path = parts[1]
                    current_definitions[img_num] = file_path
    
    # 比較結果を出力
    print("=== 画像管理シートと現在の定義の比較 ===\n")
    print("画像番号 | 管理シート | 現在の定義 | 一致")
    print("---------|-----------|-----------|------")
    
    discrepancies = []
    
    for i in range(1, 20):
        img_num = f"image{i}"
        sheet_path = sheet_mapping.get(img_num, "未定義")
        current_path = current_definitions.get(img_num, "未定義")
        
        # 一致判定
        match = "OK" if sheet_path == current_path else "NG"
        
        if sheet_path != current_path:
            discrepancies.append({
                'image': img_num,
                'sheet': sheet_path,
                'current': current_path
            })
        
        # 長いパスは省略表示
        sheet_display = sheet_path.split('/')[-1] if '/' in sheet_path else sheet_path
        current_display = current_path.split('/')[-1] if '/' in current_path else current_path
        
        print(f"{img_num:8} | {sheet_display:30} | {current_display:30} | {match}")
    
    # 不一致の詳細
    if discrepancies:
        print("\n=== 不一致の詳細 ===")
        for disc in discrepancies:
            print(f"\n{disc['image']}:")
            print(f"  管理シート: {disc['sheet']}")
            print(f"  現在の定義: {disc['current']}")
    else:
        print("\nOK: すべての定義が管理シートと一致しています")
    
    return len(discrepancies)

if __name__ == "__main__":
    discrepancy_count = compare_definitions()
    print(f"\n不一致数: {discrepancy_count}個")