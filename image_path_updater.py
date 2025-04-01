# image_path_updater.py
import os
import re
import json

def load_metadata(metadata_file):
    """メタデータファイルを読み込む"""
    with open(metadata_file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_image_mapping():
    """画像マッピング情報を読み込む"""
    mapping_dict = {}
    
    # 画像対応表（TSVファイル）を読み込み
    tsv_path = "C:\\Users\\miyagawa\\Downloads\\20FlyRobo_Regulations_images.tsv"
    try:
        with open(tsv_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        ip_section_start = False
        beginner_section_start = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "20FlyRobo_ip_Regulations" in line and not ip_section_start:
                ip_section_start = True
                beginner_section_start = False
                continue
                
            if "20FlyRobo_Beginner_Regulations" in line and not beginner_section_start:
                ip_section_start = False
                beginner_section_start = True
                continue
                
            parts = line.split('\t')
            if len(parts) >= 3 and parts[0] == "image":
                image_num = parts[1]
                ext = parts[2]
                desc = parts[3] if len(parts) > 3 else ""
                
                if ip_section_start:
                    key = f"regular_image_{image_num}{ext}"
                    mapping_dict[key] = {
                        "description": desc,
                        "section": "regular"
                    }
                elif beginner_section_start:
                    key = f"beginner_image_{image_num}{ext}"
                    mapping_dict[key] = {
                        "description": desc,
                        "section": "beginner"
                    }
    except Exception as e:
        print(f"Error loading TSV: {e}")
        print(f"File path: {tsv_path}")
    
    # 同一画像マッピング情報
    same_images = {
        "マーカーコーン": {"regular": "image 16.png", "beginner": "image 1.png"},
        "滑走路": {"regular": "image 2.png", "beginner": "image 2.png"},
        "物資投下エリア": {"regular": "image 8.png", "beginner": "image 5.png"},
        "チキンラーメンmini": {"regular": "image 4.png", "beginner": "image 6.png"},
        "水平旋回ミッション": {"regular": "image 10.png", "beginner": "image 8.png"},
        "ミニハードル": {"regular": "image 11.png", "beginner": "image 7.png"}
    }
    
    # 同一画像情報をマッピング辞書に追加
    for desc, images in same_images.items():
        regular_key = f"regular_{images['regular']}"
        beginner_key = f"beginner_{images['beginner']}"
        
        if regular_key in mapping_dict and beginner_key in mapping_dict:
            mapping_dict[regular_key]["same_as"] = beginner_key
            mapping_dict[beginner_key]["same_as"] = regular_key
    
    return mapping_dict

def update_image_references(file_path, metadata, image_mapping):
    """ファイル内の画像参照を更新する"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    # ファイルが属するセクション（regularまたはbeginner）を特定
    section_type = "regular" if "regular" in file_path else "beginner"
    
    # 相対パスのレベルを決定
    # 例: regular/sections/general/01-file.md なら3レベル上（../../../）
    # 例: beginner/sections/01-file.md なら2レベル上（../../）
    path_parts = os.path.normpath(file_path).split(os.sep)
    sections_index = path_parts.index("sections") if "sections" in path_parts else -1
    
    if sections_index >= 0:
        # sectionsディレクトリからの相対位置
        levels_up = len(path_parts) - sections_index
        path_prefix = "../" * levels_up
    else:
        # インデックスファイルなど
        path_prefix = "../"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 画像参照を探す
    image_refs = re.findall(r"!\[(.*?)\]\((.*?)\)", content)
    updated = False
    
    if image_refs:
        print(f"Found {len(image_refs)} image references in {file_path}")
        
        for alt_text, old_path in image_refs:
            # 画像ファイル名を取得
            old_filename = os.path.basename(old_path)
            
            # image番号を取得（例：image 1.png → 1）
            image_num_match = re.search(r'image\s+(\d+)\.png', old_filename)
            image_num = image_num_match.group(1) if image_num_match else None
            
            # 新しいファイル名を検索
            new_filename = None
            new_category = None
            
            # 画像番号が取得できた場合、マッピング情報から該当する画像を探す
            if image_num:
                image_key = f"{section_type}_image_{image_num}.png"
                if image_key in image_mapping:
                    desc = image_mapping[image_key].get("description", "")
                    
                    # カテゴリを推測
                    if "field" in desc.lower() or "layout" in desc.lower() or "エリア" in desc:
                        new_category = "field"
                    elif any(kw in desc.lower() for kw in ["cone", "marker", "hurdle", "チキン", "滑走路"]):
                        new_category = "equipment"
                    else:
                        new_category = "missions"
                    
                    # 新しいファイル名を構築
                    new_filename = f"{new_category}-{desc.replace(' ', '_')}-20Fl.png"
            
            # メタデータから該当する画像を検索（上記で見つからなかった場合）
            if not new_filename and metadata:
                for key, data in metadata.items():
                    if old_filename.lower() in key.lower() or any(tag.lower() in old_filename.lower() for tag in data.get("tags", [])):
                        new_filename = data["filename"]
                        new_category = data["categories"][0] if data["categories"] else "unknown"
                        break
            
            # 見つからない場合はファイル名から推測
            if not new_filename:
                # カテゴリを推測
                if "field" in old_filename.lower() or "layout" in old_filename.lower() or "エリア" in old_filename:
                    new_category = "field"
                elif any(kw in old_filename.lower() for kw in ["cone", "marker", "hurdle", "equipment", "チキン", "滑走"]):
                    new_category = "equipment"
                else:
                    new_category = "missions"
                
                # 新しいファイル名を構築
                base, ext = os.path.splitext(old_filename)
                desc = base.replace("image", "").strip()
                new_filename = f"{new_category}-image{desc}-20Fl{ext}"
            
            # 相対パスを構築
            new_path = f"{path_prefix}images/{new_category}/{new_filename}"
            
            # 置換
            old_ref = f"![{alt_text}]({old_path})"
            new_ref = f"![{alt_text}]({new_path})"
            content = content.replace(old_ref, new_ref)
            updated = True
    
    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated image references in {file_path}")
    else:
        print(f"No image references found or updated in {file_path}")

def main():
    # メタデータを読み込む
    metadata_file = "C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/metadata/images_metadata.json"
    try:
        metadata = load_metadata(metadata_file)
        print(f"Loaded metadata with {len(metadata)} entries")
    except Exception as e:
        print(f"Error loading metadata: {e}")
        metadata = {}
    
    # 画像対応マッピングを読み込む
    image_mapping = load_image_mapping()
    print(f"Loaded image mapping with {len(image_mapping)} entries")
    
    # 一般部門のセクションファイルを更新（部門別サブディレクトリ対応）
    divisions = ["common", "general", "auto-pilot", "unique-design", "multicopter"]
    for division in divisions:
        sections_dir = f"C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/regular/sections/{division}"
        if os.path.exists(sections_dir):
            for filename in os.listdir(sections_dir):
                if filename.endswith(".md"):
                    update_image_references(os.path.join(sections_dir, filename), metadata, image_mapping)
    
    # ビギナー部門のセクションファイルを更新
    sections_dir = "C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/beginner/sections"
    if os.path.exists(sections_dir):
        for filename in os.listdir(sections_dir):
            if filename.endswith(".md"):
                update_image_references(os.path.join(sections_dir, filename), metadata, image_mapping)
    
    # インデックスファイルを更新
    update_image_references("C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/regular/index.md", metadata, image_mapping)
    update_image_references("C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/beginner/index.md", metadata, image_mapping)

if __name__ == "__main__":
    main()
