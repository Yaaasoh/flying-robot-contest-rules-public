# update_image_references.py
import os
import re

# 通常部門の画像マッピング
regular_division_image_mapping = {
    "image1.png": "../images/field/field-マルチコプター部門競技エリア-20Fl.png",
    "image2.png": "../images/equipment/equipment-滑走路-20Fl.png",
    "image3.png": "../images/equipment/equipment-チキンラーメン-20Fl.png",
    "image4.png": "../images/equipment/equipment-チキンラーメンmini-20Fl.png",
    "image5.png": "../images/missions/missions-マルチコプター部門８の字飛行ミッション図解-20Fl.png",
    "image6.png": "../images/field/field-マルチコプター部門自動離着陸競技エリア-20Fl.png",
    "image7.png": "../images/equipment/equipment-高所物資運搬台-20Fl.png",
    "image8.png": "../images/field/field-物資投下エリア-20Fl.png",
    "image9.png": "../images/missions/missions-ポール旋回ミッション図解-20Fl.png",
    "image10.png": "../images/missions/missions-自動水平旋回ビギナー部門水平旋回ミッション図解-20Fl.png",
    "image11.png": "../images/equipment/equipment-ミニハードル-20Fl.png",
    "image12.png": "../images/missions/missions-救援物資運搬ミッション図解-20Fl.png",
    "image13.png": "../images/field/field-一般部門_自動操縦部門_フィールドレイアウト全体図-20Fl.png",
    "image14.png": "../images/field/field-自動操縦部門自動離着陸競技エリア-20Fl.png",
    "image15.png": "../images/field/field-一般部門_自動操縦部門_ユニークデザイン部門競技エリア-20Fl.png",
    "image16.png": "../images/equipment/equipment-マーカーコーン-20Fl.png",
    "image17.png": "../images/missions/missions-自動８の字飛行ミッション図解-20Fl.png",
    "image18.png": "../images/field/field-マルチコプター部門_フィールドレイアウト全体図-20Fl.png",
    "image19.png": "../images/missions/missions-自動離着陸ミッション図解-20Fl.png",
    "image20.png": "../images/equipment/equipment-識別用紙_正解の台-20Fl.png",
    "image21.png": "../images/equipment/equipment-識別用紙_不正解の台-20Fl.png",
    "image22.png": "../images/missions/missions-自動上昇旋回ミッション図解-20Fl.png"
}

# ビギナー部門の画像マッピング
beginner_division_image_mapping = {
    "image1.png": "../images/equipment/equipment-マーカーコーン-20Fl.png",
    "image2.png": "../images/equipment/equipment-滑走路-20Fl.png",
    "image3.png": "../images/field/field-ビギナー部門競技エリア.png",
    "image4.png": "../images/field/field-ビギナー部門フィールドレイアウト図.png",
    "image5.png": "../images/field/field-物資投下エリア-20Fl.png",
    "image6.png": "../images/equipment/equipment-チキンラーメン-20Fl.png",
    "image7.png": "../images/equipment/equipment-ミニハードル-20Fl.png",
    "image8.png": "../images/missions/missions-自動水平旋回ビギナー部門水平旋回ミッション図解-20Fl.png"
}

def update_image_references_in_file(file_path, image_mapping):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 画像参照パターンを検索
        updated_content = content
        for old_name, new_path in image_mapping.items():
            # Markdownの画像参照パターン
            pattern = r'!\[(.*?)\]\([^)]*' + re.escape(old_name) + r'\)'
            replacement = r'![\1](' + new_path + r')'
            updated_content = re.sub(pattern, replacement, updated_content)
        
        # 変更があれば保存
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated references in {file_path}")
        else:
            print(f"No changes in {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory, image_mapping):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                update_image_references_in_file(file_path, image_mapping)

# 通常部門セクションファイルの画像参照を更新
process_directory('docs/regular/sections', regular_division_image_mapping)

# ビギナー部門セクションファイルの画像参照を更新
process_directory('docs/beginner/sections', beginner_division_image_mapping)

print("Image reference update completed.")
