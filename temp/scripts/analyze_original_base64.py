#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元ファイルのBase64画像と[imageN]参照の対応を分析
"""

import re
from pathlib import Path

def analyze_original_file():
    """元ファイルのBase64画像と画像参照を分析"""
    
    # 最初のバックアップファイルを読み込み
    file_path = "21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md.backup_20250910180919"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Base64画像を検出（行番号付き）
    base64_pattern = r'!\[([^\]]*)\]\(data:image/[^;]+;base64,([^)]{50})'  # 最初の50文字だけ取得
    base64_images = []
    
    for i, line in enumerate(lines, 1):
        match = re.search(base64_pattern, line)
        if match:
            base64_images.append({
                'line': i,
                'alt_text': match.group(1),
                'data_preview': match.group(2)[:20] + '...'
            })
    
    # [imageN]参照を検出
    ref_pattern = r'!\[\]\[(image\d+)\]'
    image_refs = []
    
    for i, line in enumerate(lines, 1):
        match = re.search(ref_pattern, line)
        if match:
            image_refs.append({
                'line': i,
                'image_num': match.group(1)
            })
    
    # キャプションも確認
    captions = []
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('図'):
            captions.append({
                'line': i,
                'text': line.strip()
            })
    
    # 結果を出力
    print("=== 元ファイルの画像構造分析 ===")
    print(f"\n検出されたBase64画像: {len(base64_images)}個")
    print(f"検出された[imageN]参照: {len(image_refs)}個")
    print(f"検出されたキャプション: {len(captions)}個")
    
    if base64_images:
        print("\n【Base64画像の位置】")
        for img in base64_images[:10]:  # 最初の10個
            print(f"  Line {img['line']}: alt='{img['alt_text']}', data={img['data_preview']}")
        if len(base64_images) > 10:
            print(f"  ... 他{len(base64_images)-10}個")
    
    if image_refs:
        print("\n【[imageN]参照の位置】")
        for ref in image_refs[:10]:  # 最初の10個
            print(f"  Line {ref['line']}: {ref['image_num']}")
        if len(image_refs) > 10:
            print(f"  ... 他{len(image_refs)-10}個")
    
    # Base64画像と[imageN]参照の関係を分析
    print("\n=== 画像形式の分析 ===")
    
    if base64_images and not image_refs:
        print("✅ Base64画像のみ存在（[imageN]参照なし）")
        print("→ これが元の状態。Base64画像を[imageN]形式に置換する必要がある")
        
        # Base64画像の順序から推定される画像番号
        print("\n【Base64画像の出現順序（推定image番号）】")
        for i, img in enumerate(base64_images, 1):
            # 近くのキャプションを探す
            nearby_caption = None
            for cap in captions:
                if abs(cap['line'] - img['line']) <= 2:
                    nearby_caption = cap['text']
                    break
            
            print(f"  推定image{i}: Line {img['line']}")
            if nearby_caption:
                print(f"    関連キャプション: {nearby_caption}")
    
    elif image_refs and not base64_images:
        print("✅ [imageN]参照のみ存在（Base64画像なし）")
        print("→ すでに置換済みの状態")
    
    elif base64_images and image_refs:
        print("⚠️ Base64画像と[imageN]参照が混在")
        print("→ 部分的に置換された状態（異常）")
    
    else:
        print("❌ 画像が検出されませんでした")
    
    return base64_images, image_refs, captions

if __name__ == "__main__":
    base64_images, image_refs, captions = analyze_original_file()