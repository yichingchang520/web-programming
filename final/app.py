from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime
import os

# 明確指定 templates 資料夾的絕對路徑
template_dir = os.path.abspath(os.path.dirname(__file__)) + '/templates'
app = Flask(__name__, template_folder=template_dir)

# 抓取 app.py 所在的資料夾路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 強制將資料庫與 app.py 放在一起
DB_NAME = os.path.join(BASE_DIR, 'justice_bridge.db')

# (下方保留你原本的程式碼)
app = Flask(__name__)

# 1. 初始化資料庫（如果沒有 Table 就建立一個）
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 建立 user_verdicts 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_verdicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            verdict TEXT NOT NULL,
            reflection TEXT,
            submit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 程式啟動時執行資料庫初始化
init_db()

# 2. 建立接收前端資料的 API 路由
@app.route('/api/submit_verdict', methods=['POST'])
def submit_verdict():
    try:
        # 從前端接收 JSON 格式的資料
        data = request.get_json()
        
        # 取出我們需要的欄位
        case_id = data.get('case_id')
        verdict = data.get('verdict')
        reflection = data.get('reflection')

        # 簡單的防呆機制：確保必填欄位有值
        if not case_id or not verdict:
            return jsonify({"status": "error", "message": "案件代號與判決為必填欄位"}), 400

        # 將資料存入 SQLite 資料庫
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # 獲取當下台灣時間 (UTC+8) 作為記錄時間
        submit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO user_verdicts (case_id, verdict, reflection, submit_time)
            VALUES (?, ?, ?, ?)
        ''', (case_id, verdict, reflection, submit_time))
        
        conn.commit()
        conn.close()

        # 回傳成功訊息給前端
        return jsonify({"status": "success", "message": "判決與反思已成功記錄！"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "伺服器發生錯誤，請稍後再試"}), 500

# ======= 網頁路由 (GET 請求) =======

# 1. 首頁
@app.route('/')
def index():
    return render_template('index.html')

# 2. 虐童案：案件詳情頁
@app.route('/case_nanny.html')
def case_nanny():
    return render_template('case_nanny.html')

# 3. 虐童案：虛擬法庭頁
@app.route('/court_nanny.html')
def court_nanny():
    return render_template('court_nanny.html')

# 4. 國中割頸案：案件詳情頁 
@app.route('/case_school.html')
def case_school():
    return render_template('case_school.html')

# 5. 國中割頸案：虛擬法庭頁
@app.route('/court_school.html')
def court_school():
    return render_template('court_school.html')

if __name__ == '__main__':
    # 加上 host='0.0.0.0'，這是雲端環境必備的設定
    app.run(host='0.0.0.0', port=5000, debug=True)