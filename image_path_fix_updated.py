# image_path_fix_updated.py
import re
import os

# マッピングテーブル（旧参照 -> 新参照）を定義
image_mapping = {
    # 一般部門
    '../images/missions/missions-image28-1-20Fl.md': '../images/field/field-マルチコプター部門競技エリア-20Fl.png',
    '../images/missions/missions-image29-2-20Fl.md': '../images/equipment/equipment-滑走路-20Fl.png',
    '../images/missions/missions-image31-3-20Fl.md': '../images/equipment/equipment-チキンラーメン-20Fl.png',
    '../images/missions/missions-image32-4-20Fl.md': '../images/equipment/equipment-チキンラーメンmini-20Fl.png',
    '../images/missions/missions-image33-6-20Fl.md': '../images/field/field-マルチコプター部門自動離着陸競技エリア-20Fl.png',
    '../images/missions/missions-image34-7-20Fl.md': '../images/equipment/equipment-高所物資運搬台-20Fl.png',
    '../images/missions/missions-image83-13-20Fl.md': '../images/field/field-一般部門_自動操縦部門_フィールドレイアウト全体図-20Fl.png',
    '../images/missions/missions-image88-15-20Fl.md': '../images/field/field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア-20Fl.png',
    '../images/missions/missions-image89-16-20Fl.md': '../images/equipment/equipment-マーカーコーン-20Fl.png',
    '../images/missions/missions-image121-18-20Fl.md': '../images/field/field-マルチコプター部門_フィールドレイアウト全体図-20Fl.png',
    '../images/missions/missions-image124-21-20Fl.md': '../images/equipment/equipment-識別用紙_不正解の台-20Fl.png',
    '../images/missions/missions-image137-22-20Fl.md': '../images/missions/missions-自動上昇旋回ミッション図解-20Fl.png',
    
    # ビギナー部門
    '../images/missions/missions-image28-1-2-20Fl.md': '../images/equipment/equipment-マーカーコーン-20Fl.png',
    '../images/missions/missions-image29-3-20Fl.md': '../images/field/field-ビギナー部門競技エリア.png',
    '../images/missions/missions-image31-4-20Fl.md': '../images/field/field-ビギナー部門フィールドレイアウト図.png',
    '../images/missions/missions-image32-5-20Fl.md': '../images/field/field-物資投下エリア-20Fl.png',
    '../images/missions/missions-image33-6-20Fl.md': '../images/equipment/equipment-チキンラーメン-20Fl.png'
}

# 処理するファイル
files_to_process = [
    'C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/regular/index.md',
    'C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/beginner/index.md'
]

# 各ファイルを処理
for file_path in files_to_process:
    if not os.path.exists(file_path):
        print(f"ファイルが存在しません: {file_path}")
        continue
    
    # ファイルを読み込む
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 画像参照を修正
    updated_content = content
    for old_path, new_path in image_mapping.items():
        # Markdownの画像リンク形式を検索して置換
        pattern = r'!\[(.*?)\]\(' + re.escape(old_path) + r'\)'
        replacement = r'![\1](' + new_path + r')'
        updated_content = re.sub(pattern, replacement, updated_content)
    
    # 変更があれば保存
    if updated_content != content:
        print(f"{file_path} の画像参照を更新します")
        
        # バックアップ作成
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"バックアップを作成しました: {backup_path}")
        
        # 更新内容を保存
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"{file_path} の更新が完了しました")
    else:
        print(f"{file_path} に更新すべき画像参照はありませんでした")

print("画像参照の修正が完了しました。")