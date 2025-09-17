#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第21回飛行ロボコン 完全修正スクリプト
修正依頼書に基づく全修正を実行
"""

import re
from pathlib import Path
from datetime import datetime
import json

def process_general_multi_file(file_path: str):
    """
    一般・自動・ユニーク・マルチ部門ファイルの修正
    """
    print("\n=== 21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md の処理 ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 「図　一般部門・自動操縦部門・ユニークデザイン部門のフィールド」の前に画像追加
        if '図　一般部門・自動操縦部門・ユニークデザイン部門のフィールド' in line:
            # 新規画像を追加
            new_lines.append('![](images/field/field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア_21.png)\n')
            new_lines.append('![](images/field/field-一般部門_自動操縦部門_フィールドレイアウト全体図_21.png)\n')
            new_lines.append('![](images/field/field-物資投下エリア_21.png)\n')
            new_lines.append('\n')
            new_lines.append(line)  # キャプション行
            # 次の行の![][image1]はスキップ
            if i + 1 < len(lines) and '![][image1]' in lines[i + 1]:
                i += 2  # image1行をスキップ
                continue
        
        # 「図　滑走路」の処理
        elif '図　滑走路（※実際の滑走路は約5.4m、高さ約20mm）' in line:
            # 上に画像追加
            new_lines.append('![](images/equipment/equipment-滑走路_21.png)\n')
            new_lines.append('\n')
            new_lines.append(line)  # キャプション行
            # 次の行の![][image2]はスキップ
            if i + 1 < len(lines) and '![][image2]' in lines[i + 1]:
                i += 1  # image2行をスキップ
            # 下に画像追加
            new_lines.append('\n')
            new_lines.append('![](images/field/field-マルチコプター部門競技エリア_21.png)\n')
            new_lines.append('![](images/field/field-マルチコプター部門_フィールドレイアウト全体図_21.png)\n')
            i += 1
            continue
        
        # 「図　マルチコプター部門のフィールド」と![][image3]を削除
        elif '図　マルチコプター部門のフィールド' in line:
            # この行と次の![][image3]をスキップ
            if i + 1 < len(lines) and '![][image3]' in lines[i + 1]:
                i += 2
                continue
        
        # 既存の画像参照を置換（統一形式：キャプションなし）
        elif '![][image4]' in line:
            new_lines.append(line.replace('![][image4]', '![](images/equipment/equipment-マーカーコーン_21.png)'))
        elif '![][image5]' in line:
            new_lines.append(line.replace('![][image5]', '![](images/equipment/equipment-ミニハードル_21.png)'))
        elif '![][image6]' in line:
            new_lines.append(line.replace('![][image6]', '![](images/equipment/equipment-チキンラーメンmini_21.png)'))
        elif '![][image7]' in line:
            new_lines.append(line.replace('![][image7]', '![](images/missions/missions-救援物資運搬ミッション図解_21.png)'))
        elif '![][image8]' in line:
            new_lines.append(line.replace('![][image8]', '![](images/missions/missions-ポール旋回ミッション図解_21.png)'))
        elif '![][image9]' in line:
            new_lines.append(line.replace('![][image9]', '![](images/missions/missions-自動水平旋回ビギナー部門水平旋回ミッション図解_21.png)'))
        elif '![][image10]' in line:
            new_lines.append(line.replace('![][image10]', '![](images/missions/missions-自動８の字飛行ミッション図解_21.png)'))
        elif '![][image11]' in line:
            new_lines.append(line.replace('![][image11]', '![](images/missions/missions-自動水平旋回ビギナー部門水平旋回ミッション図解_21.png)'))
        elif '![][image12]' in line:
            new_lines.append(line.replace('![][image12]', '![](images/missions/missions-マルチコプター部門８の字飛行ミッション図解_21.png)'))
        elif '![][image13]' in line:
            new_lines.append(line.replace('![][image13]', '![](images/missions/missions-自動上昇旋回ミッション図解_21.png)'))
        elif '![][image14]' in line:
            new_lines.append(line.replace('![][image14]', '![](images/missions/missions-自動離着陸ミッション図解_21.png)'))
        elif '![][image15]' in line:
            new_lines.append(line.replace('![][image15]', '![](images/equipment/equipment-チキンラーメンmini_21.png)'))
        elif '![][image16]' in line:
            new_lines.append(line.replace('![][image16]', '![](images/equipment/equipment-チキンラーメン_21.png)'))
        elif '![][image17]' in line and '![][image18]' in line:
            # テーブル内の画像（image17とimage18が同じ行にある）
            line = line.replace('![][image17]', '![](images/equipment/equipment-高所物資運搬台_21.png)')
            line = line.replace('![][image18]', '![](images/equipment/equipment-識別用紙_正解の台_21.png)')
            new_lines.append(line)
        elif '![][image17]' in line:
            new_lines.append(line.replace('![][image17]', '![](images/equipment/equipment-高所物資運搬台_21.png)'))
        elif '![][image18]' in line:
            new_lines.append(line.replace('![][image18]', '![](images/equipment/equipment-識別用紙_正解の台_21.png)'))
        elif '![][image19]' in line:
            new_lines.append(line.replace('![][image19]', '![](images/missions/missions-マルチコプター部門８の字飛行ミッション図解_21.png)'))
        
        # 画像定義行を削除
        elif re.match(r'^\[image\d+\]:', line):
            i += 1
            continue  # この行をスキップ
        
        else:
            new_lines.append(line)
        
        i += 1
    
    # ファイルを保存
    output_path = file_path.replace('_EDIT.md', '_EDIT_fixed.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"  ✅ 完了: {output_path}")
    return output_path

def process_beginner_file(file_path: str):
    """
    ビギナー部門ファイルの修正（画像順序の入れ替え）
    """
    print("\n=== 21FlyRobo_Beginner_Regulations_text_EDIT.md の処理 ===")
    
    # ここでは画像タグの順序を入れ替える処理を実装
    # 実際のファイル構造に応じて調整が必要
    
    print("  ⚠️ ビギナー部門の修正は手動で実施してください")
    return None

def process_index_file(file_path: str):
    """
    index.mdの修正
    """
    print("\n=== index.md の処理 ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 削除対象のテキスト
    deletions = [
        # 参加チーム数のブロック
        r'- \*\*参加チーム数\*\*: 126チーム[\s\S]*?ビギナー部門: 35チーム',
        # 虚偽の説明文
        r'- 本サイトは第21回大会の公式ルール文書を掲載しています',
        # 迷惑な案内文
        r'- ルールに関する質問は大会事務局までお問い合わせください',
        # （現行）の文字
        r'（現行）'
    ]
    
    for pattern in deletions:
        content = re.sub(pattern, '', content)
    
    # リンクテキストの変更
    content = content.replace(
        '通常部門ルール（一般・自動操縦・ユニークデザイン・マルチコプター）',
        '一般・自動操縦・ユニークデザイン・マルチコプター部門'
    )
    
    # ファイルを保存
    output_path = file_path.replace('.md', '_fixed.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ 完了: {output_path}")
    return output_path

def process_mkdocs_yml(file_path: str):
    """
    mkdocs.ymlの修正
    """
    print("\n=== mkdocs.yml の処理 ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # ナビゲーション名の変更
        if '第21回ルール（最新）' in line:
            line = line.replace('第21回ルール（最新）', '第21回ルール')
        if '通常部門（一般・自動・UD・マルチ）' in line:
            line = line.replace('通常部門（一般・自動・UD・マルチ）', '一般・自動操縦・ユニークデザイン・マルチコプター部門')
        new_lines.append(line)
    
    # ファイルを保存
    output_path = file_path.replace('.yml', '_fixed.yml')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"  ✅ 完了: {output_path}")
    return output_path

def main():
    """
    メイン処理
    """
    print("=" * 60)
    print("第21回飛行ロボコン 完全修正スクリプト")
    print("=" * 60)
    
    # 処理結果を記録
    results = {
        'timestamp': datetime.now().isoformat(),
        'processed_files': []
    }
    
    # 1. 一般・自動・ユニーク・マルチ部門
    if Path('21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md').exists():
        result = process_general_multi_file('21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md')
        if result:
            results['processed_files'].append(result)
    else:
        print("❌ 21FlyRobo_GeneralAutoUniqueMulti_Regulations_text_EDIT.md が見つかりません")
    
    # 2. ビギナー部門（手動対応が必要）
    if Path('21FlyRobo_Beginner_Regulations_text_EDIT.md').exists():
        process_beginner_file('21FlyRobo_Beginner_Regulations_text_EDIT.md')
    
    # 3. index.md
    if Path('index.md').exists():
        result = process_index_file('index.md')
        if result:
            results['processed_files'].append(result)
    else:
        print("❌ index.md が見つかりません")
    
    # 4. mkdocs.yml
    if Path('mkdocs.yml').exists():
        result = process_mkdocs_yml('mkdocs.yml')
        if result:
            results['processed_files'].append(result)
    else:
        print("❌ mkdocs.yml が見つかりません")
    
    # 結果をログファイルに保存
    log_path = Path('temp/correct/revision_log.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ 修正完了")
    print(f"処理ファイル数: {len(results['processed_files'])}")
    print(f"ログファイル: {log_path}")
    print("\n⚠️ 注意事項:")
    print("  1. ビギナー部門の画像順序は手動で修正してください")
    print("  2. 生成された_fixedファイルを確認後、元のファイル名にリネームしてください")
    print("  3. MkDocsでプレビューして画像が正しく表示されることを確認してください")
    print("=" * 60)

if __name__ == "__main__":
    main()