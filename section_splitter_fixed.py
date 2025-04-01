# section_splitter_fixed.py
import os
import re
import shutil
from pathlib import Path

def create_section_structure(source_file, target_dir):
    """
    原典ファイルを章・節ごとにセクションファイルに分割して適切なディレクトリに配置
    
    Parameters:
    - source_file: 原典MDファイルのパス
    - target_dir: セクションファイル配置先ディレクトリ
    """
    print(f"Processing file: {source_file}")
    
    # ファイルの存在確認
    if not os.path.exists(source_file):
        print(f"Error: Source file not found: {source_file}")
        return
    
    # ターゲットディレクトリにsectionsフォルダを作成
    sections_dir = os.path.join(target_dir, "sections")
    os.makedirs(sections_dir, exist_ok=True)
    print(f"Created sections directory: {sections_dir}")
    
    # 部門別のサブディレクトリを作成（一般部門のみ）
    if "regular" in target_dir:
        divisions = ["common", "general", "auto-pilot", "unique-design", "multicopter"]
        division_dirs = {}
        for division in divisions:
            division_dir = os.path.join(sections_dir, division)
            os.makedirs(division_dir, exist_ok=True)
            division_dirs[division] = division_dir
        print(f"Created division directories in: {sections_dir}")
    
    # 原典ファイルを読み込み
    try:
        with open(source_file, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"Successfully read file: {source_file}")
        print(f"File size: {len(content)} characters")
    except Exception as e:
        print(f"Error reading file: {e}")
        # UTF-8以外の文字コードを試す
        try:
            with open(source_file, "r", encoding="shift-jis") as f:
                content = f.read()
            print(f"Successfully read file with Shift-JIS encoding: {source_file}")
        except Exception as e:
            print(f"Error reading file with Shift-JIS encoding: {e}")
            return
    
    # 見出しパターンの例を出力
    heading_examples = re.findall(r"^(.{0,20}#.{0,20})$", content, re.MULTILINE)[:5]
    print(f"Heading pattern examples: {heading_examples}")
    
    # 見出しを検索（# から始まる行 または 行の途中に #がある行）
    headings = re.findall(r"^(#{1,3})\s*(.+?)$|^(.{0,10}#{1,3}\s*)(.+?)$", content, re.MULTILINE)
    print(f"Found {len(headings)} potential headings")
    
    # 見出しとその位置を記録
    section_positions = []
    for match in re.finditer(r"^(#{1,3})\s*(.+?)$|^(.{0,10}#{1,3}\s*)(.+?)$", content, re.MULTILINE):
        level = len(match.group(1) if match.group(1) else match.group(3))
        title = match.group(2).strip() if match.group(2) else match.group(4).strip()
        position = match.start()
        if level <= 2:  # H1とH2だけを処理
            section_positions.append((level, title, position))
            print(f"Heading: Level {level}, Title: {title}, Position: {position}")
    
    # 見出しが見つからない場合、別のパターンで試す
    if len(section_positions) == 0:
        print("No headings found with standard pattern, trying alternative patterns...")
        
        # 代替パターン: 数字+ドット+スペースから始まる行
        alt_headings = re.findall(r"^(\d+)\.(\s+.+)$", content, re.MULTILINE)
        print(f"Found {len(alt_headings)} alternative headings with number pattern")
        
        for match in re.finditer(r"^(\d+)\.(\s+.+)$", content, re.MULTILINE):
            num = int(match.group(1))
            title = match.group(2).strip()
            position = match.start()
            # 1桁の数字はH1、2桁の数字はH2と仮定
            level = 1 if num < 10 else 2
            section_positions.append((level, title, position))
            print(f"Alt Heading: Level {level}, Title: {title}, Position: {position}")
    
    # それでも見出しが見つからない場合、空行で区切る
    if len(section_positions) == 0:
        print("No headings found with any pattern, splitting by empty lines...")
        
        # 空行で分割
        paragraphs = re.split(r"\n\s*\n", content)
        curr_pos = 0
        for i, para in enumerate(paragraphs):
            if len(para.strip()) > 0:
                # 段落の最初の行をタイトルとして使用
                title = para.strip().split('\n')[0][:50]  # 最大50文字
                section_positions.append((1, title, curr_pos))
                print(f"Paragraph: Title: {title}, Position: {curr_pos}")
            curr_pos += len(para) + 2  # +2 for the two newlines
    
    # 最後の位置を追加
    section_positions.append((0, "END", len(content)))
    
    # 各セクションの部門を判定する関数
    def determine_division(title, content):
        title_lower = title.lower()
        # 部門判定ロジックを出力
        print(f"Determining division for title: {title}")
        
        if "一般部門" in title or "general" in title_lower:
            return "general"
        elif "自動操縦" in title or "auto" in title_lower or "autonomous" in title_lower:
            return "auto-pilot"
        elif "ユニークデザイン" in title or "unique" in title_lower:
            return "unique-design"
        elif "マルチコプター" in title or "multi" in title_lower:
            return "multicopter"
        else:
            # 内容に基づいて判断（簡易版）
            section_content = content[:1000] if len(content) > 1000 else content
            if "一般部門" in section_content:
                return "general"
            elif "自動操縦" in section_content:
                return "auto-pilot"
            elif "ユニークデザイン" in section_content:
                return "unique-design"
            elif "マルチコプター" in section_content:
                return "multicopter"
            else:
                return "common"  # デフォルトは共通部分
    
    # セクションファイルを作成
    section_info = []  # インデックス生成用の情報
    
    for i in range(len(section_positions) - 1):
        level, title, start = section_positions[i]
        next_position = section_positions[i + 1][2]
        
        # セクションの内容を取得
        section_content = content[start:next_position].strip()
        
        # ファイル名を作成（スラッグ化）
        slug = re.sub(r'\W+', '-', title.lower()).strip('-')
        filename = f"{i:02d}-{slug}.md"
        
        # 部門を判定（regular/一般部門のみ）
        if "regular" in target_dir:
            division = determine_division(title, section_content)
            section_path = os.path.join(sections_dir, division, filename)
        else:
            # ビギナー部門の場合はサブディレクトリなし
            section_path = os.path.join(sections_dir, filename)
        
        # セクションファイルを書き込み
        with open(section_path, "w", encoding="utf-8") as f:
            f.write(section_content)
        
        # インデックス生成用の情報を記録
        section_info.append({
            "level": level,
            "title": title,
            "filename": filename,
            "division": division if "regular" in target_dir else "beginner"
        })
        
        print(f"Created section: {section_path}")
    
    # インデックスファイルを作成
    create_index_file(target_dir, section_info)
    
    print(f"Created index file: {os.path.join(target_dir, 'index.md')}")

def create_index_file(target_dir, section_info):
    """インデックスファイルを作成する"""
    index_content = []
    
    # リポジトリ名から部門名を取得
    repo_type = "一般部門" if "regular" in target_dir else "ビギナー部門"
    
    index_content.append(f"# 第20回飛行ロボットコンテスト {repo_type}ルール\n\n")
    
    if "regular" in target_dir:
        # 一般部門の場合、部門別に目次を作成
        divisions = {
            "common": "共通",
            "general": "一般部門",
            "auto-pilot": "自動操縦部門",
            "unique-design": "ユニークデザイン部門",
            "multicopter": "マルチコプター部門"
        }
        
        for division_key, division_name in divisions.items():
            division_sections = [s for s in section_info if s["division"] == division_key]
            
            if division_sections:
                index_content.append(f"## {division_name}\n\n")
                
                for section in division_sections:
                    if section["level"] == 1:
                        index_content.append(f"- [{section['title']}](sections/{division_key}/{section['filename']})\n")
                
                index_content.append("\n")
    else:
        # ビギナー部門の場合、単純なリスト
        index_content.append("## 目次\n\n")
        
        for section in section_info:
            if section["level"] == 1:
                index_content.append(f"- [{section['title']}](sections/{section['filename']})\n")
    
    with open(os.path.join(target_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write("".join(index_content))

# 実行
if __name__ == "__main__":
    create_section_structure(
        "C:/Users/miyagawa/github/flying-robot-contest-rules-public/20FlyRobo_ip_Regulations.md",
        "C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/regular"
    )
    
    create_section_structure(
        "C:/Users/miyagawa/github/flying-robot-contest-rules-public/20FlyRobo_Beginner_Regulations.md",
        "C:/Users/miyagawa/github/flying-robot-contest-rules-public/docs/beginner"
    )
