#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飛行ロボットコンテスト ルールファイル分析スクリプト

このスクリプトは以下の分析を行います：
1. ファイルの基本情報（サイズ、行数など）
2. 見出し構造の分析（H1, H2, H3など）
3. 画像参照の分析
4. Base64エンコード画像の検出
5. 文書構造のアウトライン生成
"""

import os
import re
import argparse
import base64
import hashlib
from collections import Counter
from datetime import datetime

def analyze_file(file_path):
    """
    マークダウンファイルを分析し、詳細情報を返す
    
    Args:
        file_path (str): 分析対象のファイルパス
        
    Returns:
        dict: 分析結果
    """
    result = {
        'filename': os.path.basename(file_path),
        'file_path': file_path,
        'file_size': 0,
        'line_count': 0,
        'char_count': 0,
        'headings': {
            'h1': [],
            'h2': [],
            'h3': [],
            'h4': [],
            'h5': [],
            'h6': []
        },
        'heading_count': {
            'h1': 0,
            'h2': 0,
            'h3': 0,
            'h4': 0,
            'h5': 0,
            'h6': 0
        },
        'image_references': [],
        'base64_images': [],
        'outline': [],
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 基本情報
        result['file_size'] = os.path.getsize(file_path)
        result['line_count'] = len(content.split('\n'))
        result['char_count'] = len(content)
        
        # 見出し分析
        heading_patterns = {
            'h1': r'^# (.+?)$',
            'h2': r'^## (.+?)$',
            'h3': r'^### (.+?)$',
            'h4': r'^#### (.+?)$',
            'h5': r'^##### (.+?)$',
            'h6': r'^###### (.+?)$'
        }
        
        for level, pattern in heading_patterns.items():
            headings = re.findall(pattern, content, re.MULTILINE)
            result['headings'][level] = headings
            result['heading_count'][level] = len(headings)
            
            # アウトライン構築のためにレベルと見出しテキストを追加
            for heading in headings:
                result['outline'].append((level, heading))
        
        # アウトラインを見出しレベルと出現順でソート
        result['outline'].sort(key=lambda x: (int(x[0][1]), content.find(f"{'#' * int(x[0][1])} {x[1]}")))
        
        # 画像参照の分析
        image_pattern = r'!\[(.*?)\]\((.*?)\)'
        image_references = re.findall(image_pattern, content)
        
        for alt_text, image_path in image_references:
            # Base64エンコード画像の検出
            if image_path.startswith('data:image'):
                # Base64エンコード画像情報を保存
                image_type = re.search(r'data:image/([^;]+);', image_path)
                image_type = image_type.group(1) if image_type else 'unknown'
                
                # Base64部分を抽出
                base64_data = re.search(r'base64,([^)]+)', image_path)
                base64_data = base64_data.group(1) if base64_data else ''
                
                # ハッシュ化して識別子にする
                image_hash = hashlib.md5(base64_data.encode()).hexdigest()[:8]
                
                result['base64_images'].append({
                    'alt_text': alt_text,
                    'image_type': image_type,
                    'image_hash': image_hash,
                    'data_length': len(base64_data)
                })
            else:
                # 通常の画像参照を保存
                result['image_references'].append({
                    'alt_text': alt_text,
                    'image_path': image_path
                })
        
        return result
        
    except Exception as e:
        print(f"エラー: {file_path} の分析中に問題が発生しました: {e}")
        return result

def generate_analysis_report(analysis_results):
    """
    分析結果からMarkdown形式のレポートを生成
    
    Args:
        analysis_results (list): analyze_file関数から得られた結果のリスト
        
    Returns:
        str: Markdown形式のレポート
    """
    report = f"# 飛行ロボットコンテスト ルールファイル分析レポート\n\n"
    report += f"分析日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n"
    
    # 目次
    report += "## 目次\n\n"
    report += "1. [ファイルの基本情報](#ファイルの基本情報)\n"
    report += "2. [見出し構造の分析](#見出し構造の分析)\n"
    report += "3. [画像参照の分析](#画像参照の分析)\n"
    report += "4. [文書構造のアウトライン](#文書構造のアウトライン)\n"
    report += "5. [分析まとめ](#分析まとめ)\n\n"
    
    # ファイルの基本情報
    report += "## ファイルの基本情報\n\n"
    report += "| ファイル名 | サイズ | 行数 | 文字数 |\n"
    report += "|------------|--------|------|--------|\n"
    
    for result in analysis_results:
        file_size_kb = result['file_size'] / 1024
        report += f"| {result['filename']} | {file_size_kb:.2f} KB | {result['line_count']} | {result['char_count']} |\n"
    
    report += "\n"
    
    # 見出し構造の分析
    report += "## 見出し構造の分析\n\n"
    
    for result in analysis_results:
        report += f"### {result['filename']} の見出し構造\n\n"
        report += "| 見出しレベル | 数 |\n"
        report += "|--------------|----|\n"
        
        for level, count in result['heading_count'].items():
            report += f"| {level.upper()} | {count} |\n"
        
        report += "\n"
        
        # 見出しレベルの分布を表示
        report += "#### 見出しの具体例\n\n"
        
        for level, headings in result['headings'].items():
            if headings:
                report += f"**{level.upper()}レベルの見出し (最大5件):**\n\n"
                for i, heading in enumerate(headings[:5]):
                    report += f"- {heading}\n"
                
                if len(headings) > 5:
                    report += f"- ...他 {len(headings) - 5} 件\n"
                
                report += "\n"
    
    # 画像参照の分析
    report += "## 画像参照の分析\n\n"
    
    for result in analysis_results:
        report += f"### {result['filename']} の画像参照\n\n"
        report += f"- 通常の画像参照: {len(result['image_references'])} 件\n"
        report += f"- Base64エンコード画像: {len(result['base64_images'])} 件\n\n"
        
        if result['image_references']:
            report += "#### 通常の画像参照例 (最大5件)\n\n"
            report += "| 代替テキスト | 画像パス |\n"
            report += "|--------------|----------|\n"
            
            for i, img_ref in enumerate(result['image_references'][:5]):
                report += f"| {img_ref['alt_text']} | {img_ref['image_path']} |\n"
            
            if len(result['image_references']) > 5:
                report += f"\n他 {len(result['image_references']) - 5} 件の画像参照があります。\n"
            
            report += "\n"
        
        if result['base64_images']:
            report += "#### Base64エンコード画像 (最大5件)\n\n"
            report += "| 代替テキスト | 画像タイプ | ハッシュ | データ長 |\n"
            report += "|--------------|------------|---------|----------|\n"
            
            for i, img_ref in enumerate(result['base64_images'][:5]):
                report += f"| {img_ref['alt_text']} | {img_ref['image_type']} | {img_ref['image_hash']} | {img_ref['data_length']} |\n"
            
            if len(result['base64_images']) > 5:
                report += f"\n他 {len(result['base64_images']) - 5} 件のBase64エンコード画像があります。\n"
            
            report += "\n"
    
    # 文書構造のアウトライン
    report += "## 文書構造のアウトライン\n\n"
    
    for result in analysis_results:
        report += f"### {result['filename']} の文書構造\n\n"
        
        if result['outline']:
            for level, heading in result['outline']:
                indent = "  " * (int(level[1]) - 1)
                report += f"{indent}- {heading}\n"
        else:
            report += "アウトラインを生成できませんでした。\n"
        
        report += "\n"
    
    # 分析まとめ
    report += "## 分析まとめ\n\n"
    
    # ファイル間の比較
    if len(analysis_results) > 1:
        report += "### ファイル間の比較\n\n"
        
        # 見出しレベルの分布比較
        report += "#### 見出しレベルの分布比較\n\n"
        report += "| ファイル名 | H1 | H2 | H3 | H4 | H5 | H6 |\n"
        report += "|------------|----|----|----|----|----|----|"
        
        for result in analysis_results:
            report += f"\n| {result['filename']} "
            for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                report += f"| {result['heading_count'][level]} "
        
        report += "|\n\n"
        
        # 画像参照の比較
        report += "#### 画像参照の比較\n\n"
        report += "| ファイル名 | 通常画像参照 | Base64画像 |\n"
        report += "|------------|--------------|------------|\n"
        
        for result in analysis_results:
            report += f"| {result['filename']} | {len(result['image_references'])} | {len(result['base64_images'])} |\n"
    
    # 所見と提案
    report += "\n### 所見と再構成の提案\n\n"
    report += "分析結果に基づく所見と再構成の提案は以下の通りです：\n\n"
    
    # 見出し構造の所見
    report += "#### 見出し構造\n\n"
    report += "- H1見出しは各部門や大セクションを表していると推測されます\n"
    report += "- H2見出しは主要なセクションを表していると推測されます\n"
    report += "- 見出しの階層構造を保持した統合が望ましいと考えられます\n\n"
    
    # 画像参照の所見
    report += "#### 画像参照\n\n"
    report += "- 画像参照のパターンが統一されておらず、標準化が必要です\n"
    report += "- Base64エンコード画像は実際のファイルに変換すべきです\n"
    report += "- 画像のカテゴリ分けと命名規則の確立が望ましいです\n\n"
    
    # 提案
    report += "#### 再構成の提案\n\n"
    report += "1. **部門中心型アプローチ**: 各部門のルールを独立したドキュメントとして整理\n"
    report += "2. **見出し階層の整理**: H1→部門名、H2→主要セクション、H3→サブセクションという構造化\n"
    report += "3. **画像参照の標準化**: `![代替テキスト](../images/カテゴリ/ファイル名.拡張子)` 形式に統一\n"
    report += "4. **相互参照の追加**: 関連する部門やセクションへの参照を追加\n"
    
    return report

def main():
    parser = argparse.ArgumentParser(description='飛行ロボットコンテスト ルールファイル分析スクリプト')
    parser.add_argument('files', nargs='+', help='分析対象のマークダウンファイル')
    parser.add_argument('-o', '--output', help='分析結果を出力するファイル（省略時は標準出力）')
    
    args = parser.parse_args()
    
    analysis_results = []
    
    for file_path in args.files:
        print(f"分析中: {file_path}")
        result = analyze_file(file_path)
        analysis_results.append(result)
    
    report = generate_analysis_report(analysis_results)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"分析レポートを {args.output} に保存しました。")
    else:
        print("\n" + report)

if __name__ == "__main__":
    main()
