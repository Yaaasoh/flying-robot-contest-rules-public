#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飛行ロボコン21 画像修正 検証ツールキット
Version: 1.0
Date: 2025/01/11

使用方法:
    python verification_toolkit.py <command> <file_path> [options]

コマンド:
    validate    - 完全検証を実行
    check-b64   - Base64画像の検出
    check-refs  - 画像参照の検証
    check-defs  - 画像定義の検証
    check-caps  - キャプションの検証
    compare     - 2ファイルの比較
    report      - 検証レポート生成
"""

import re
import sys
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import hashlib
import difflib

class Colors:
    """コンソール出力用の色定義"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class ImageVerifier:
    """画像修正の検証を行うメインクラス"""
    
    def __init__(self, file_path: str, mapping_path: Optional[str] = None):
        """
        初期化
        
        Args:
            file_path: 検証対象のMarkdownファイルパス
            mapping_path: 画像マッピングCSVファイルパス（オプション）
        """
        self.file_path = Path(file_path)
        self.mapping_path = Path(mapping_path) if mapping_path else None
        self.content = self._read_file()
        self.lines = self.content.split('\n')
        self.mapping = self._load_mapping() if self.mapping_path else {}
        self.errors = []
        self.warnings = []
        self.info = []
        
    def _read_file(self) -> str:
        """ファイルを読み込む"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"{Colors.RED}❌ ファイル読み込みエラー: {e}{Colors.ENDC}")
            sys.exit(1)
    
    def _load_mapping(self) -> Dict:
        """マッピングファイルを読み込む"""
        mapping = {}
        try:
            with open(self.mapping_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    mapping[row['image_number']] = row
        except Exception as e:
            self.warnings.append(f"マッピングファイル読み込みエラー: {e}")
        return mapping
    
    def check_base64_images(self) -> Tuple[int, List[str]]:
        """
        Base64画像の検出
        
        Returns:
            (画像数, 画像リスト)
        """
        pattern = r'!\[([^\]]*)\]\(data:image/[^;]+;base64,([^)]+)\)'
        matches = re.findall(pattern, self.content)
        
        base64_images = []
        for i, (alt_text, base64_data) in enumerate(matches, 1):
            # Base64データのハッシュ値を計算（識別用）
            hash_value = hashlib.md5(base64_data.encode()).hexdigest()[:8]
            base64_images.append({
                'index': i,
                'alt_text': alt_text,
                'hash': hash_value,
                'size': len(base64_data)
            })
        
        if base64_images:
            self.errors.append(f"Base64画像が{len(base64_images)}個検出されました")
            for img in base64_images:
                self.info.append(f"  - Base64画像 #{img['index']}: "
                               f"alt='{img['alt_text']}', "
                               f"hash={img['hash']}, "
                               f"size={img['size']} bytes")
        
        return len(base64_images), base64_images
    
    def check_image_references(self) -> Dict[str, List[int]]:
        """
        画像参照の検証
        
        Returns:
            画像番号と行番号のマッピング
        """
        pattern = r'!\[\]\[(image\d+)\]'
        references = {}
        
        for i, line in enumerate(self.lines, 1):
            matches = re.findall(pattern, line)
            for match in matches:
                if match not in references:
                    references[match] = []
                references[match].append(i)
        
        # 期待される画像番号の確認
        expected_images = set(f"image{i}" for i in range(1, 20))
        found_images = set(references.keys())
        
        missing = expected_images - found_images
        extra = found_images - expected_images
        
        if missing:
            self.warnings.append(f"使用されていない画像番号: {', '.join(sorted(missing))}")
        if extra:
            self.errors.append(f"予期しない画像番号: {', '.join(sorted(extra))}")
        
        # 重複使用の確認
        for img_num, lines in references.items():
            if len(lines) > 1:
                self.info.append(f"{img_num} は{len(lines)}箇所で使用: "
                               f"行 {', '.join(map(str, lines))}")
        
        return references
    
    def check_image_definitions(self) -> Dict[str, str]:
        """
        画像定義の検証
        
        Returns:
            画像番号とファイルパスのマッピング
        """
        pattern = r'^\[(image\d+)\]:\s*(.+)$'
        definitions = {}
        
        for i, line in enumerate(self.lines, 1):
            match = re.match(pattern, line)
            if match:
                img_num, file_path = match.groups()
                if img_num in definitions:
                    self.errors.append(f"{img_num} の定義が重複: "
                                     f"行{i}と既存定義")
                definitions[img_num] = file_path.strip()
        
        # マッピングとの照合
        if self.mapping:
            for img_num, expected in self.mapping.items():
                expected_path = expected['path'] + expected['file_name']
                actual_path = definitions.get(img_num)
                
                if not actual_path:
                    self.errors.append(f"{img_num} の定義がありません")
                elif actual_path != expected_path:
                    self.errors.append(f"{img_num} のパスが不正: "
                                     f"期待値={expected_path}, "
                                     f"実際={actual_path}")
        
        return definitions
    
    def check_captions(self) -> List[Dict]:
        """
        キャプションの検証
        
        Returns:
            キャプション情報のリスト
        """
        captions = []
        
        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if stripped.startswith('図'):
                # 全角スペースか半角スペースかを判定
                space_type = 'fullwidth' if '　' in stripped[1:2] else 'halfwidth'
                
                captions.append({
                    'line': i,
                    'text': stripped,
                    'space_type': space_type
                })
        
        # キャプション数の確認
        expected_count = 19  # 期待されるキャプション数
        actual_count = len(captions)
        
        if actual_count != expected_count:
            self.warnings.append(f"キャプション数が期待値と異なる: "
                               f"期待={expected_count}, 実際={actual_count}")
        
        # スペースの一貫性確認
        space_types = set(cap['space_type'] for cap in captions)
        if len(space_types) > 1:
            self.warnings.append("キャプションのスペース形式が混在しています")
        
        return captions
    
    def check_consistency(self, references: Dict, definitions: Dict) -> None:
        """
        画像参照と定義の整合性確認
        
        Args:
            references: 画像参照のマッピング
            definitions: 画像定義のマッピング
        """
        # 参照されているが定義がない画像
        for img_num in references:
            if img_num not in definitions:
                self.errors.append(f"{img_num} は参照されていますが定義がありません")
        
        # 定義されているが参照されていない画像
        for img_num in definitions:
            if img_num not in references:
                self.warnings.append(f"{img_num} は定義されていますが使用されていません")
    
    def validate_all(self) -> bool:
        """
        完全検証を実行
        
        Returns:
            エラーがない場合True
        """
        print(f"{Colors.HEADER}=== 検証開始: {self.file_path.name} ==={Colors.ENDC}")
        
        # 1. Base64画像チェック
        print(f"\n{Colors.BLUE}1. Base64画像チェック{Colors.ENDC}")
        b64_count, _ = self.check_base64_images()
        print(f"  結果: {b64_count}個のBase64画像")
        
        # 2. 画像参照チェック
        print(f"\n{Colors.BLUE}2. 画像参照チェック{Colors.ENDC}")
        references = self.check_image_references()
        print(f"  結果: {len(references)}種類の画像が参照されています")
        
        # 3. 画像定義チェック
        print(f"\n{Colors.BLUE}3. 画像定義チェック{Colors.ENDC}")
        definitions = self.check_image_definitions()
        print(f"  結果: {len(definitions)}個の画像定義")
        
        # 4. キャプションチェック
        print(f"\n{Colors.BLUE}4. キャプションチェック{Colors.ENDC}")
        captions = self.check_captions()
        print(f"  結果: {len(captions)}個のキャプション")
        
        # 5. 整合性チェック
        print(f"\n{Colors.BLUE}5. 整合性チェック{Colors.ENDC}")
        self.check_consistency(references, definitions)
        print(f"  完了")
        
        # 結果サマリー
        self._print_summary()
        
        return len(self.errors) == 0
    
    def _print_summary(self) -> None:
        """検証結果のサマリーを出力"""
        print(f"\n{Colors.HEADER}=== 検証結果サマリー ==={Colors.ENDC}")
        
        if self.errors:
            print(f"\n{Colors.RED}❌ エラー: {len(self.errors)}件{Colors.ENDC}")
            for error in self.errors:
                print(f"  • {error}")
        else:
            print(f"\n{Colors.GREEN}✅ エラーなし{Colors.ENDC}")
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}⚠️  警告: {len(self.warnings)}件{Colors.ENDC}")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.info:
            print(f"\n{Colors.BLUE}ℹ️  情報:{Colors.ENDC}")
            for info in self.info[:5]:  # 最初の5件のみ表示
                print(f"  • {info}")
            if len(self.info) > 5:
                print(f"  ... 他{len(self.info)-5}件")
    
    def generate_report(self, output_path: str) -> None:
        """
        検証レポートをJSON形式で生成
        
        Args:
            output_path: 出力ファイルパス
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'file': str(self.file_path),
            'summary': {
                'errors': len(self.errors),
                'warnings': len(self.warnings),
                'info': len(self.info)
            },
            'details': {
                'errors': self.errors,
                'warnings': self.warnings,
                'info': self.info
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"{Colors.GREEN}レポートを生成しました: {output_path}{Colors.ENDC}")


class FileComparator:
    """ファイル比較ツール"""
    
    @staticmethod
    def compare_files(file1: str, file2: str, output_html: bool = False) -> None:
        """
        2つのファイルを比較
        
        Args:
            file1: 比較元ファイル
            file2: 比較先ファイル
            output_html: HTML形式で出力するか
        """
        with open(file1, 'r', encoding='utf-8') as f:
            lines1 = f.readlines()
        
        with open(file2, 'r', encoding='utf-8') as f:
            lines2 = f.readlines()
        
        if output_html:
            # HTML差分を生成
            differ = difflib.HtmlDiff()
            html = differ.make_file(lines1, lines2, file1, file2)
            output_path = 'comparison.html'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"HTML差分を生成しました: {output_path}")
        else:
            # コンソールに差分を表示
            differ = difflib.unified_diff(
                lines1, lines2,
                fromfile=file1,
                tofile=file2,
                lineterm=''
            )
            
            for line in differ:
                if line.startswith('+'):
                    print(f"{Colors.GREEN}{line}{Colors.ENDC}")
                elif line.startswith('-'):
                    print(f"{Colors.RED}{line}{Colors.ENDC}")
                elif line.startswith('@'):
                    print(f"{Colors.BLUE}{line}{Colors.ENDC}")
                else:
                    print(line)


def main():
    """メイン関数"""
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    file_path = sys.argv[2]
    
    if command == 'validate':
        # 完全検証
        mapping_path = sys.argv[3] if len(sys.argv) > 3 else None
        verifier = ImageVerifier(file_path, mapping_path)
        success = verifier.validate_all()
        sys.exit(0 if success else 1)
    
    elif command == 'check-b64':
        # Base64画像チェックのみ
        verifier = ImageVerifier(file_path)
        count, images = verifier.check_base64_images()
        print(f"Base64画像: {count}個")
        sys.exit(0 if count == 0 else 1)
    
    elif command == 'check-refs':
        # 画像参照チェックのみ
        verifier = ImageVerifier(file_path)
        refs = verifier.check_image_references()
        print(f"画像参照: {len(refs)}種類")
        for img, lines in sorted(refs.items()):
            print(f"  {img}: 行 {', '.join(map(str, lines))}")
    
    elif command == 'check-defs':
        # 画像定義チェックのみ
        mapping_path = sys.argv[3] if len(sys.argv) > 3 else None
        verifier = ImageVerifier(file_path, mapping_path)
        defs = verifier.check_image_definitions()
        print(f"画像定義: {len(defs)}個")
        for img, path in sorted(defs.items()):
            print(f"  {img}: {path}")
    
    elif command == 'check-caps':
        # キャプションチェックのみ
        verifier = ImageVerifier(file_path)
        caps = verifier.check_captions()
        print(f"キャプション: {len(caps)}個")
        for cap in caps:
            print(f"  Line {cap['line']}: {cap['text']} ({cap['space_type']})")
    
    elif command == 'compare':
        # ファイル比較
        if len(sys.argv) < 4:
            print("使用方法: compare <file1> <file2> [--html]")
            sys.exit(1)
        file2 = sys.argv[3]
        output_html = '--html' in sys.argv
        FileComparator.compare_files(file_path, file2, output_html)
    
    elif command == 'report':
        # レポート生成
        mapping_path = sys.argv[3] if len(sys.argv) > 3 else None
        output_path = sys.argv[4] if len(sys.argv) > 4 else 'verification_report.json'
        verifier = ImageVerifier(file_path, mapping_path)
        verifier.validate_all()
        verifier.generate_report(output_path)
    
    else:
        print(f"不明なコマンド: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()