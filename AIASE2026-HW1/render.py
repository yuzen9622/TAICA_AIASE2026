#!/usr/bin/env python3
"""
Markdown 渲染工具
用途：將 content.md 渲染為 HTML 和 PDF 格式
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


class MarkdownRenderer:
    """Markdown 渲染器"""

    def __init__(self):
        self.content_file = Path("content.md")
        self.output_dir = Path("output")
        self.html_output = self.output_dir / "output.html"
        self.pdf_output = self.output_dir / "output.pdf"
        self.style_file = Path("style.css")

    def check_dependencies(self):
        """檢查必要的依賴"""
        print("🔍 檢查依賴...")

        # 檢查 content.md
        if not self.content_file.exists():
            print(f"❌ 錯誤：找不到 {self.content_file}")
            sys.exit(1)

        # 檢查 Pandoc
        if not shutil.which("pandoc"):
            print("❌ 錯誤：未安裝 Pandoc")
            print("請執行以下指令安裝：")
            print("  macOS:   brew install pandoc")
            print("  Ubuntu:  sudo apt-get install pandoc")
            sys.exit(1)

        print("✅ 依賴檢查通過")

    def create_output_dir(self):
        """確保輸出目錄存在"""
        self.output_dir.mkdir(exist_ok=True)

    def render_html(self):
        """渲染 HTML"""
        print("\n📄 正在產生 HTML...")

        cmd = [
            "pandoc",
            str(self.content_file),
            "-o",
            str(self.html_output),
            "--standalone",
        ]

        # 如果有自訂樣式表，加入 CSS
        if self.style_file.exists():
            cmd.extend(["--css", f"../{self.style_file}"])
            print(f"   使用自訂樣式：{self.style_file}")

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ HTML 已產生：{self.html_output}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ HTML 產生失敗：{e.stderr}")
            return False

    def render_pdf_with_pandoc(self):
        """使用 Pandoc + LaTeX 產生 PDF"""
        print("\n📑 正在產生 PDF (使用 Pandoc + LaTeX)...")

        # 檢查是否有 LaTeX
        has_xelatex = shutil.which("xelatex")
        has_pdflatex = shutil.which("pdflatex")

        if not (has_xelatex or has_pdflatex):
            print("⚠️  未找到 LaTeX 引擎")
            return False

        # 優先使用 XeLaTeX (支援中文)
        if has_xelatex:
            # 嘗試使用中文字型
            fonts = ["PingFang TC", "Heiti TC", "STHeiti", "Arial Unicode MS"]

            for font in fonts:
                cmd = [
                    "pandoc",
                    str(self.content_file),
                    "-o",
                    str(self.pdf_output),
                    "--pdf-engine=xelatex",
                    f"-V",
                    f"CJKmainfont={font}",
                ]

                try:
                    result = subprocess.run(
                        cmd, check=True, capture_output=True, text=True, timeout=60
                    )
                    print(f"✅ PDF 已產生：{self.pdf_output} (使用字型：{font})")
                    return True
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    continue

            # 如果指定字型都失敗，嘗試不指定字型
            try:
                cmd = [
                    "pandoc",
                    str(self.content_file),
                    "-o",
                    str(self.pdf_output),
                    "--pdf-engine=xelatex",
                ]
                subprocess.run(
                    cmd, check=True, capture_output=True, text=True, timeout=60
                )
                print(f"✅ PDF 已產生：{self.pdf_output}")
                return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"⚠️  XeLaTeX 產生失敗")

        # 最後嘗試 pdflatex (不支援中文)
        if has_pdflatex:
            try:
                cmd = [
                    "pandoc",
                    str(self.content_file),
                    "-o",
                    str(self.pdf_output),
                    "--pdf-engine=pdflatex",
                ]
                subprocess.run(
                    cmd, check=True, capture_output=True, text=True, timeout=60
                )
                print(f"✅ PDF 已產生：{self.pdf_output} (中文可能無法正常顯示)")
                return True
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                print("⚠️  PDFLaTeX 產生失敗")

        return False

    def render_pdf_with_weasyprint(self):
        """使用 WeasyPrint 產生 PDF"""
        print("\n📑 正在產生 PDF (使用 WeasyPrint)...")

        try:
            from weasyprint import HTML

            # 先產生臨時 HTML
            temp_html = self.output_dir / "temp.html"
            cmd = [
                "pandoc",
                str(self.content_file),
                "-o",
                str(temp_html),
                "--standalone",
            ]

            if self.style_file.exists():
                cmd.extend(["--css", str(self.style_file)])

            subprocess.run(cmd, check=True, capture_output=True, text=True)

            # 使用 WeasyPrint 轉 PDF
            HTML(str(temp_html)).write_pdf(str(self.pdf_output))

            # 清理臨時檔案
            temp_html.unlink()

            print(f"✅ PDF 已產生：{self.pdf_output}")
            return True

        except ImportError:
            print("⚠️  WeasyPrint 未安裝")
            return False
        except Exception as e:
            print(f"⚠️  WeasyPrint 產生失敗：{e}")
            return False

    def render_pdf(self):
        """產生 PDF (嘗試多種方法)"""
        # 優先使用 Pandoc + LaTeX (較簡單)
        if self.render_pdf_with_pandoc():
            return True

        # 如果失敗，嘗試 WeasyPrint
        if self.render_pdf_with_weasyprint():
            return True

        # 都失敗，顯示安裝建議
        print("\n❌ 無法產生 PDF")
        print("\n請選擇以下任一方案：")
        print("\n  方案1: 安裝 LaTeX (推薦)")
        print("    macOS:  brew install --cask basictex")
        print("    Ubuntu: sudo apt-get install texlive-xetex")
        print("\n  方案2: 安裝 WeasyPrint")
        print("    1. 安裝系統依賴：")
        print("       macOS:  brew install cairo pango gdk-pixbuf libffi")
        print(
            "       Ubuntu: sudo apt-get install python3-dev libcairo2 libpango-1.0-0"
        )
        print("    2. 安裝 Python 套件：")
        print("       pip install -r requirements.txt")

        return False

    def show_results(self):
        """顯示結果"""
        print("\n" + "=" * 50)
        print("🎉 渲染完成！")
        print("=" * 50)
        print("\n📂 輸出檔案：")

        for file in self.output_dir.iterdir():
            if file.name == ".gitkeep":
                continue
            size = file.stat().st_size
            size_str = self._format_size(size)
            print(f"   - {file.name:20s} ({size_str})")

        print("\n💡 檢視方式：")
        if self.html_output.exists():
            print(f"   HTML: open {self.html_output}")
        if self.pdf_output.exists():
            print(f"   PDF:  open {self.pdf_output}")

    @staticmethod
    def _format_size(size):
        """格式化檔案大小"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def run(self):
        """執行渲染流程"""
        print("🚀 開始渲染 Markdown 文件...")
        print()

        # 檢查依賴
        self.check_dependencies()

        # 建立輸出目錄
        self.create_output_dir()

        # 渲染 HTML
        html_success = self.render_html()

        # 渲染 PDF
        pdf_success = self.render_pdf()

        # 顯示結果
        if html_success or pdf_success:
            self.show_results()

        # 返回狀態碼
        if html_success and pdf_success:
            return 0
        elif html_success or pdf_success:
            return 1
        else:
            return 2


def main():
    """主程式"""
    renderer = MarkdownRenderer()
    exit_code = renderer.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
