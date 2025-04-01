import os
import re
import json

def scan_image_references(base_dir):
    """ドキュメント内の画像参照を検索して問題を報告する"""
    results = {
        "total_files": 0,
        "files_with_images": 0,
        "total_image_refs": 0,
        "problematic_refs": [],
        "missing_files": []
    }
    
    # 検索対象のディレクトリ
    search_dirs = [
        os.path.join(base_dir, "docs", "regular"),
        os.path.join(base_dir, "docs", "beginner"),
    ]
    
    # 画像が存在するディレクトリ
    image_dirs = [
        os.path.join(base_dir, "docs", "images", "field"),
        os.path.join(base_dir, "docs", "images", "equipment"),
        os.path.join(base_dir, "docs", "images", "missions")
    ]
    
    # 存在する画像ファイルのリストを作成
    existing_images = []
    for image_dir in image_dirs:
        if os.path.exists(image_dir):
            for file in os.listdir(image_dir):
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
                    existing_images.append(file)
    
    # 画像参照のパターン
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    
    # ファイルを再帰的に検索
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if file.endswith(".md"):
                    results["total_files"] += 1
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        # 画像参照を検索
                        image_refs = re.findall(image_pattern, content)
                        
                        if image_refs:
                            results["files_with_images"] += 1
                            results["total_image_refs"] += len(image_refs)
                            
                            for alt_text, image_path in image_refs:
                                # 画像ファイル名を取得
                                image_filename = os.path.basename(image_path)
                                
                                # 相対パスの形式をチェック
                                path_parts = image_path.split("/")
                                if not image_path.startswith(("../images/", "../../images/", "../../../images/")):
                                    results["problematic_refs"].append({
                                        "file": file_path,
                                        "alt_text": alt_text,
                                        "image_path": image_path,
                                        "issue": "相対パスが正しい形式でない"
                                    })
                                
                                # 画像ファイルが存在するかチェック
                                if image_filename not in existing_images:
                                    results["missing_files"].append({
                                        "file": file_path,
                                        "alt_text": alt_text,
                                        "image_path": image_path,
                                        "issue": "参照画像が存在しない"
                                    })
                    except Exception as e:
                        print(f"エラー: {file_path} - {str(e)}")
    
    return results

def main():
    base_dir = "C:/Users/miyagawa/github/flying-robot-contest-rules-public"
    results = scan_image_references(base_dir)
    
    print("\n画像参照スキャン結果:")
    print(f"総ファイル数: {results['total_files']}")
    print(f"画像参照があるファイル数: {results['files_with_images']}")
    print(f"総画像参照数: {results['total_image_refs']}")
    print(f"問題のある参照: {len(results['problematic_refs'])}")
    print(f"存在しない画像ファイル: {len(results['missing_files'])}")
    
    # 詳細情報を出力
    if results['problematic_refs']:
        print("\n問題のある参照:")
        for i, ref in enumerate(results['problematic_refs'][:10], 1):  # 最初の10件のみ表示
            print(f"{i}. ファイル: {ref['file']}")
            print(f"   画像パス: {ref['image_path']}")
            print(f"   問題: {ref['issue']}")
        
        if len(results['problematic_refs']) > 10:
            print(f"   ... その他 {len(results['problematic_refs']) - 10} 件")
    
    if results['missing_files']:
        print("\n存在しない画像ファイル:")
        for i, ref in enumerate(results['missing_files'][:10], 1):  # 最初の10件のみ表示
            print(f"{i}. ファイル: {ref['file']}")
            print(f"   画像パス: {ref['image_path']}")
        
        if len(results['missing_files']) > 10:
            print(f"   ... その他 {len(results['missing_files']) - 10} 件")
    
    # 結果をJSONとして保存
    with open(os.path.join(base_dir, "image_debug_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n詳細な結果は image_debug_results.json に保存されました")

if __name__ == "__main__":
    main()
