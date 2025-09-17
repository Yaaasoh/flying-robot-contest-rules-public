#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飛行ロボコン21 画像マッピング検証スクリプト
タスク3: 画像管理シートとの整合性確認
"""

import re
import csv
from pathlib import Path
from datetime import datetime

def validate_image_mapping():
    """画像管理シートと現在のファイルの整合性を確認"""
    
    # ファイルパス設定
    current_file = Path("21FlyRobo_GeneralAutoUniqueMulti_Regulations_text.md")
    mapping_sheet = Path("temp/image_management_sheet.csv")
    
    # 画像管理シートを読み込み
    correct_mapping = {}
    with open(mapping_sheet, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            correct_mapping[row['image_number']] = {
                'file_name': row['file_name'],
                'category': row['category'],
                'description': row['description'],
                'path': row['path']
            }
    
    # 現在のファイルから画像定義を抽出
    with open(current_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 画像定義部分（ファイル末尾）を抽出
    current_definitions = {}
    definition_pattern = r'^\[image(\d+)\]:\s*(.+)$'
    
    for match in re.finditer(definition_pattern, content, re.MULTILINE):
        image_num = f"image{match.group(1)}"
        file_path = match.group(2).strip()
        current_definitions[image_num] = file_path
    
    # 整合性チェック
    validation_results = []
    errors = []
    
    for img_num in sorted(correct_mapping.keys(), key=lambda x: int(x.replace('image', ''))):
        correct_info = correct_mapping[img_num]
        correct_path = correct_info['path'] + correct_info['file_name']
        current_path = current_definitions.get(img_num, 'NOT DEFINED')
        
        is_correct = current_path == correct_path
        
        validation_results.append({
            'image_number': img_num,
            'correct_path': correct_path,
            'current_path': current_path,
            'status': 'OK' if is_correct else 'ERROR',
            'description': correct_info['description']
        })
        
        if not is_correct:
            errors.append({
                'image_number': img_num,
                'error': f"期待値: {correct_path}, 実際: {current_path}",
                'description': correct_info['description']
            })
    
    # image_mapping_validation.csv 作成
    with open('temp/image_mapping_validation.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ImageNumber', 'Status', 'CorrectPath', 'CurrentPath', 'Description'])
        
        for result in validation_results:
            writer.writerow([
                result['image_number'],
                result['status'],
                result['correct_path'],
                result['current_path'],
                result['description']
            ])
    
    # mapping_errors.txt 作成
    with open('temp/mapping_errors.txt', 'w', encoding='utf-8') as f:
        f.write("=== 画像マッピングエラー一覧 ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        f.write(f"総画像数: {len(validation_results)}\n")
        f.write(f"エラー数: {len(errors)}\n")
        f.write("\n")
        
        if errors:
            f.write("【エラー詳細】\n")
            for error in errors:
                f.write(f"\n{error['image_number']}:\n")
                f.write(f"  エラー: {error['error']}\n")
                f.write(f"  説明: {error['description']}\n")
        else:
            f.write("エラーはありません。すべての画像定義が正しく設定されています。\n")
        
        # 重複チェック（image15とimage16）
        f.write("\n")
        f.write("=== 重複チェック ===\n")
        if correct_mapping['image15']['file_name'] == correct_mapping['image16']['file_name']:
            f.write("警告: image15とimage16が同じファイルを参照しています\n")
            f.write(f"  ファイル名: {correct_mapping['image15']['file_name']}\n")
    
    # correct_image_definitions.txt 作成
    with open('temp/correct_image_definitions.txt', 'w', encoding='utf-8') as f:
        f.write("=== 正しい画像定義 ===\n")
        f.write(f"作成日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
        f.write("\n")
        f.write("以下の形式でファイル末尾に定義すべき内容：\n")
        f.write("\n")
        
        for img_num in sorted(correct_mapping.keys(), key=lambda x: int(x.replace('image', ''))):
            info = correct_mapping[img_num]
            correct_path = info['path'] + info['file_name']
            f.write(f"[{img_num}]: {correct_path}\n")
    
    print(f"完了: 画像マッピング検証ファイルを作成しました")
    print(f"総画像数: {len(validation_results)}")
    print(f"エラー数: {len(errors)}")
    
    return len(validation_results), len(errors)

if __name__ == "__main__":
    validate_image_mapping()