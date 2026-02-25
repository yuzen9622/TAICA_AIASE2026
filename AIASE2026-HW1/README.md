# Markdown 渲染作業 - README

> **作業目標**: 使用 Markdown 撰寫內容，並透過開源工具渲染為 PDF 和 HTML 格式

---

## 1. 專案簡介

### 內容主題

本專案的 `content.md` 為**個人履歷（CV）**，展示個人基本資料、學歷、工作經驗、技能與專案經驗等資訊。

內容包含：

- 基本資料表格
- 多層級標題結構
- 有序與無序清單
- 程式碼區塊（含語法高亮）
- 引用區塊
- 任務清單
- 超連結

### 選用渲染工具

本專案使用 **Pandoc** 作為主要渲染工具，並支援多種 PDF 產生方式：

1. **Pandoc + XeLaTeX**（主要方案）：
   - 完美支援中文字型
   - 產生高品質 PDF
   - 適合學術文件與履歷

2. **WeasyPrint**（備選方案）：
   - Python 套件，易於安裝
   - 支援 CSS 樣式
   - 適合網頁風格文件

#### 選擇理由

- **Pandoc** 是業界標準文件轉換工具，支援豐富的 Markdown 語法
- **XeLaTeX** 提供專業的排版品質，完美支援中文
- **自動化腳本**（render.py）智能選擇可用工具，提高成功率
- 同時產生 **HTML** 和 **PDF** 兩種格式，滿足不同需求

---

## 2. 環境需求

### 作業系統

- **支援**: macOS、Linux (Ubuntu/Debian)
- **測試環境**:
  - macOS 14.x (Sonoma)
  - Ubuntu 22.04 LTS

### 所需軟體版本

| 軟體       | 最低版本 | 用途             |
| ---------- | -------- | ---------------- |
| Python     | 3.8+     | 執行渲染腳本     |
| Pandoc     | 2.0+     | Markdown 轉換    |
| XeLaTeX    | 任意版本 | PDF 產生（推薦） |
| WeasyPrint | 60.0+    | PDF 產生（備選） |

---

## 3. 安裝步驟

### 完整安裝流程（適用於乾淨環境）

以下指令可在全新的 macOS 或 Ubuntu 環境中直接執行：

#### 方案 A：macOS 環境（推薦使用 Homebrew）

```bash
# 步驟 1: 安裝 Pandoc
brew install pandoc

# 步驟 2: 安裝 BasicTeX（輕量版 LaTeX，約 100MB）
brew install --cask basictex

# 步驟 3: 更新 PATH 環境變數
eval "$(/usr/libexec/path_helper)"

# 步驟 4: 驗證安裝
pandoc --version
xelatex --version
python3 --version

# 步驟 5: 執行渲染（無需額外 Python 套件）
python3 render.py
```

**注意**：如果步驟 3 執行後 `xelatex --version` 仍找不到指令，請**重新開啟終端機**或執行：

```bash
export PATH="/Library/TeX/texbin:$PATH"
```

#### 方案 B：Ubuntu/Debian 環境

```bash
# 步驟 1: 更新套件清單
sudo apt-get update

# 步驟 2: 安裝 Pandoc
sudo apt-get install -y pandoc

# 步驟 3: 安裝 XeLaTeX 和中文字型
sudo apt-get install -y texlive-xetex texlive-fonts-recommended fonts-noto-cjk

# 步驟 4: 驗證安裝
pandoc --version
xelatex --version
python3 --version

# 步驟 5: 執行渲染
python3 render.py
```

#### 方案 C：使用 WeasyPrint（若 LaTeX 安裝失敗）

如果 LaTeX 安裝失敗或不可用，可改用 WeasyPrint：

**macOS**:

```bash
# 安裝系統依賴
brew install pandoc cairo pango gdk-pixbuf libffi

# 安裝 Python 套件
pip3 install -r requirements.txt

# 執行渲染
python3 render.py
```

**Ubuntu/Debian**:

```bash
# 安裝 Pandoc
sudo apt-get update
sudo apt-get install -y pandoc

# 安裝 WeasyPrint 系統依賴
sudo apt-get install -y python3-dev python3-pip libcairo2 libpango-1.0-0 \
    libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# 安裝 Python 套件
pip3 install -r requirements.txt

# 執行渲染
python3 render.py
```

### 最小化安裝（僅產生 HTML）

如果只需要 HTML 輸出，只需安裝 Pandoc：

```bash
# macOS
brew install pandoc

# Ubuntu
sudo apt-get update && sudo apt-get install -y pandoc

# 執行（只會產生 HTML，PDF 會顯示警告）
python3 render.py
```

---

## 4. 執行渲染

### 一鍵執行（推薦）

確保你位於專案根目錄（包含 `content.md` 和 `render.py` 的目錄），執行：

```bash
python3 render.py
```

**執行結果**：

- ✅ 自動檢查依賴（Pandoc、content.md）
- ✅ 產生 `output/output.html`
- ✅ 自動選擇最佳方法產生 `output/output.pdf`
- ✅ 顯示輸出檔案資訊

### 執行範例輸出

```
🚀 開始渲染 Markdown 文件...

🔍 檢查依賴...
✅ 依賴檢查通過

📄 正在產生 HTML...
✅ HTML 已產生：output/output.html

📑 正在產生 PDF (使用 Pandoc + LaTeX)...
✅ PDF 已產生：output/output.pdf (使用字型：PingFang TC)

==================================================
🎉 渲染完成！
==================================================

📂 輸出檔案：
   - output.html        (XX.X KB)
   - output.pdf         (XXX.X KB)

💡 檢視方式：
   HTML: open output/output.html
   PDF:  open output/output.pdf
```

### 手動執行（進階使用）

如果需要手動控制渲染流程，可使用以下指令：

#### 僅產生 HTML

```bash
pandoc content.md -o output/output.html --standalone --css=../style.css
```

#### 僅產生 PDF（使用 Pandoc + XeLaTeX）

**macOS**:

```bash
pandoc content.md -o output/output.pdf --pdf-engine=xelatex -V CJKmainfont="PingFang TC"
```

**Ubuntu**:

```bash
pandoc content.md -o output/output.pdf --pdf-engine=xelatex -V CJKmainfont="Noto Sans CJK TC"
```

#### 使用 WeasyPrint 產生 PDF

```bash
# 先產生臨時 HTML
pandoc content.md -o output/temp.html --standalone --css=style.css

# 轉換為 PDF
python3 -c "from weasyprint import HTML; HTML('output/temp.html').write_pdf('output/output.pdf')"

# 清理臨時檔案
rm output/temp.html
```

### 故障排除（自動執行）

如果 `python3 render.py` 執行失敗，腳本會自動顯示錯誤訊息和解決方案。

**常見錯誤及解決方法**：

1. **找不到 Pandoc**

   ```bash
   # macOS
   brew install pandoc

   # Ubuntu
   sudo apt-get install -y pandoc
   ```

2. **找不到 content.md**

   ```bash
   # 確認當前目錄
   ls -la content.md

   # 如果不在正確目錄，切換到專案根目錄
   cd /path/to/AIASE2026-HW1
   ```

3. **無法產生 PDF**
   - 腳本會顯示詳細安裝指引
   - 至少會成功產生 HTML 輸出

---

## 5. 預期輸出

### 輸出檔案結構

執行 `python3 render.py` 成功後，專案目錄結構如下：

```
AIASE2026-HW1/
├── content.md           # 原始 Markdown 內容
├── README.md            # 本說明文件
├── render.py            # 渲染腳本
├── requirements.txt     # Python 依賴清單
├── style.css            # HTML/PDF 樣式表
└── output/              # 輸出目錄
    ├── output.html      # ✓ HTML 格式輸出（必定產生）
    └── output.pdf       # ✓ PDF 格式輸出（若環境支援）
```

### 輸出檔案說明

| 檔案                 | 格式  | 用途      | 特色                                          |
| -------------------- | ----- | --------- | --------------------------------------------- |
| `output/output.html` | HTML5 | 網頁瀏覽  | 含自訂 CSS 樣式、可在瀏覽器開啟、保留所有格式 |
| `output/output.pdf`  | PDF   | 列印/分享 | 高品質排版、支援中文字型、適合正式文件        |

### 檔案內容特色

**HTML 輸出** (`output/output.html`):

- ✅ 響應式設計，支援各種螢幕尺寸
- ✅ 語法高亮的程式碼區塊
- ✅ 美化的表格與清單
- ✅ 可點擊的超連結
- ✅ 自訂字型與配色

**PDF 輸出** (`output/output.pdf`):

- ✅ 專業的文件排版
- ✅ 完整的中文支援（使用 PingFang TC 或 Noto Sans CJK）
- ✅ 適合列印的頁面設定
- ✅ 保留所有 Markdown 格式（標題、列表、程式碼等）
- ✅ 嵌入字型，跨平台顯示一致

### 檢視輸出

執行完成後，可使用以下指令檢視結果：

```bash
# 在瀏覽器中開啟 HTML
open output/output.html           # macOS
xdg-open output/output.html       # Linux

# 開啟 PDF
open output/output.pdf             # macOS
xdg-open output/output.pdf         # Linux
evince output/output.pdf           # Linux (替代)
```

### 成功指標

✅ **最低要求**（通過 CI）:

- `output/` 目錄存在
- 至少包含一個輸出檔案（HTML 或 PDF）

✅ **完整成功**:

- 同時產生 `output.html` 和 `output.pdf`
- 兩個檔案都可正常開啟
- 內容完整呈現，無亂碼

---

## 6. 參考資料

### 官方文件

- **Pandoc**: https://pandoc.org/MANUAL.html
  - 安裝指南: https://pandoc.org/installing.html
  - Markdown 語法: https://pandoc.org/MANUAL.html#pandocs-markdown

- **XeLaTeX / TeX Live**:
  - BasicTeX (macOS): https://www.tug.org/mactex/morepackages.html
  - TeX Live (Linux): https://www.tug.org/texlive/
  - XeTeX: https://tug.org/xetex/

- **WeasyPrint**: https://doc.courtbouillon.org/weasyprint/
  - 安裝指南: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
  - 故障排除: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#troubleshooting

- **Markdown 指南**: https://www.markdownguide.org/
  - 基本語法: https://www.markdownguide.org/basic-syntax/
  - 擴展語法: https://www.markdownguide.org/extended-syntax/

### 工具倉庫

- Pandoc GitHub: https://github.com/jgm/pandoc
- WeasyPrint GitHub: https://github.com/Kozea/WeasyPrint
- Markdown-it: https://github.com/markdown-it/markdown-it

### 字型資源

- **macOS 內建字型**:
  - PingFang TC（蘋方-繁體中文）
  - Heiti TC（黑體-繁體中文）

- **Linux 開源字型**:
  - Noto Sans CJK: https://www.google.com/get/noto/
  - 文泉驛微米黑: http://wenq.org/wqy2/index.cgi

---

## 附錄：完整執行範例

### 情境 1：全新 macOS 環境（推薦）

```bash
# 假設已安裝 Homebrew 和 Python 3

# 1. 安裝依賴
brew install pandoc
brew install --cask basictex
eval "$(/usr/libexec/path_helper)"

# 2. 進入專案目錄
cd AIASE2026-HW1

# 3. 執行渲染
python3 render.py

# 4. 檢視結果
open output/output.html
open output/output.pdf
```

### 情境 2：全新 Ubuntu 環境

```bash
# 1. 安裝依賴
sudo apt-get update
sudo apt-get install -y pandoc texlive-xetex texlive-fonts-recommended fonts-noto-cjk

# 2. 進入專案目錄
cd AIASE2026-HW1

# 3. 執行渲染
python3 render.py

# 4. 檢視結果
xdg-open output/output.html
xdg-open output/output.pdf
```

### 情境 3：僅安裝 Pandoc（最小化）

```bash
# 1. 僅安裝 Pandoc
brew install pandoc  # macOS
# 或
sudo apt-get install -y pandoc  # Ubuntu

# 2. 執行渲染（僅產生 HTML）
cd AIASE2026-HW1
python3 render.py

# 3. 輸出結果
# ✅ output/output.html (成功)
# ⚠️  PDF 產生失敗（顯示安裝指引）
```

---

## 快速故障排除

| 問題                  | 解決方法                                                                                |
| --------------------- | --------------------------------------------------------------------------------------- |
| 找不到 `pandoc` 指令  | `brew install pandoc` (macOS) 或 `sudo apt-get install pandoc` (Ubuntu)                 |
| 找不到 `xelatex` 指令 | `brew install --cask basictex` (macOS) 或 `sudo apt-get install texlive-xetex` (Ubuntu) |
| PDF 中文顯示為方塊    | 確保已安裝 XeLaTeX 和中文字型（PingFang TC / Noto Sans CJK）                            |
| `content.md` 不存在   | 確認已在正確目錄：`ls -la content.md`                                                   |
| WeasyPrint 導入錯誤   | 安裝系統依賴後重新安裝：`brew install cairo pango` → `pip3 install -r requirements.txt` |

---

## 授權

本專案為學術作業，僅供學習使用。

---

_最後更新：2026年2月25日_
