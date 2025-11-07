# 醫療事業環境永續資訊管理系統
# Healthcare Environment Sustainability Information Management System

一個完整的醫療機構環境永續數據管理系統，用於追蹤和管理能源消耗、用水量、廢棄物處理和碳排放數據。

## 功能特點

- 🔐 **用戶認證系統** - 安全的用戶註冊和登入功能
- ⚡ **能源管理** - 追蹤電力、天然氣和燃油消耗
- 💧 **用水監控** - 記錄用水量和廢水處理數據
- ♻️ **廢棄物管理** - 管理醫療、一般、可回收和有害廢棄物
- 🌍 **碳排放追蹤** - 計算和監控範疇一、二、三碳排放量
- 📊 **數據分析與報表** - 視覺化永續趨勢和生成報告
- 📱 **響應式設計** - 支援桌面和移動設備

## 系統架構

- **後端**: Python Flask 3.0
- **資料庫**: SQLite (可升級至 PostgreSQL/MySQL)
- **前端**: HTML5, CSS3, Jinja2 模板
- **認證**: Flask-Login
- **ORM**: Flask-SQLAlchemy

## 安裝步驟

### 1. 克隆儲存庫

```bash
git clone https://github.com/lizcococandy/healthcare_environment.git
cd healthcare_environment
```

### 2. 建立虛擬環境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 4. 初始化資料庫

```bash
python run.py init_db
```

### 5. 建立管理員帳號（選用）

```bash
python run.py create_admin
```

### 6. 啟動應用程式

```bash
python run.py
```

應用程式將在 `http://127.0.0.1:5000` 上運行

## 使用說明

### 1. 註冊和登入

- 訪問首頁並點擊「註冊帳號」
- 填寫用戶名、電子郵件和密碼
- 註冊成功後使用帳號登入系統

### 2. 新增數據記錄

登入後，您可以在各個模組中新增記錄：

- **能源消耗**: 記錄電力、天然氣、燃油使用量
- **用水記錄**: 記錄用水量和廢水處理量
- **廢棄物管理**: 記錄各類廢棄物重量
- **碳排放**: 記錄各範疇碳排放數據

### 3. 查看儀表板

儀表板顯示：
- 總體統計數據（總能源、用水、廢棄物、碳排放）
- 最近的記錄列表
- 快速導航到各模組

### 4. 查看報表

報表頁面提供：
- 過去6個月的趨勢分析
- 各類數據的月度統計
- 永續指標追蹤

## 資料庫模型

### User（用戶）
- 用戶名、電子郵件、密碼
- 角色（用戶/管理員）

### EnergyConsumption（能源消耗）
- 設施名稱、測量日期
- 電力、天然氣、燃油消耗量

### WaterUsage（用水記錄）
- 設施名稱、測量日期
- 用水量、廢水量

### WasteManagement（廢棄物管理）
- 設施名稱、測量日期
- 醫療、一般、可回收、有害廢棄物量

### CarbonEmissions（碳排放）
- 設施名稱、測量日期
- 範疇一、二、三排放量

## 專案結構

```
healthcare_environment/
├── app/
│   ├── __init__.py          # 應用程式工廠
│   ├── models.py            # 資料庫模型
│   ├── routes/              # 路由模組
│   │   ├── main.py         # 主要路由
│   │   ├── auth.py         # 認證路由
│   │   ├── energy.py       # 能源路由
│   │   ├── water.py        # 用水路由
│   │   ├── waste.py        # 廢棄物路由
│   │   ├── emissions.py    # 碳排放路由
│   │   └── reports.py      # 報表路由
│   ├── templates/           # HTML 模板
│   └── static/             # 靜態資源
│       └── css/
│           └── style.css
├── config.py               # 配置文件
├── run.py                  # 應用程式入口
├── requirements.txt        # Python 相依套件
└── README.md              # 專案說明
```

## 環境配置

可以通過環境變數配置：

- `SECRET_KEY`: Flask 應用程式金鑰
- `DATABASE_URL`: 資料庫連接 URL
- `FLASK_ENV`: 環境（development/production）

## 安全性考量

- 密碼使用 Werkzeug 進行雜湊加密
- 使用 Flask-Login 進行會話管理
- CSRF 保護（建議在生產環境中啟用）
- 資料庫注入防護（使用 SQLAlchemy ORM）

## 未來擴展

- 數據視覺化圖表（使用 Chart.js）
- Excel/PDF 報表匯出
- 多設施管理
- 自動化數據收集 API
- 永續目標設定和追蹤
- 電子郵件通知
- 多語言支援

## 貢獻

歡迎提交 Pull Request 或 Issue！

## 授權

本專案採用 MIT 授權條款。

## 聯絡方式

如有問題或建議，請透過 GitHub Issues 聯絡。
