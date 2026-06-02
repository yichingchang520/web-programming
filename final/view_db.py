import sqlite3
import pandas as pd
import os
from datetime import datetime

# 抓取 view_db.py 所在的資料夾路徑 (確保路徑正確)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 強制讀取同一層的資料庫
DB_NAME = os.path.join(BASE_DIR, 'justice_bridge.db')

def export_to_excel():
    try:
        # 1. 連線到資料庫並撈取資料
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM user_verdicts", conn)
        conn.close()

        # 2. 檢查是否有資料
        if df.empty:
            print("目前資料庫是空的，還沒有資料可以匯出喔！")
        else:
            # 3. 產生帶有當前時間的檔案名稱 (格式：YYYYMMDD_HHMMSS)
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_filename = f'justice_bridge_data_{current_time}.xlsx'
            
            # 將存檔路徑設定在與這支程式相同的資料夾下
            excel_path = os.path.join(BASE_DIR, excel_filename)

            # 4. 匯出成 Excel (設定 index=False 讓 Excel 不要出現多餘的行號)
            df.to_excel(excel_path, index=False, engine='openpyxl')
            
            print("=== 法感實驗室：數據匯出成功 ===")
            print(f"✅ 總計匯出 {len(df)} 筆判決資料。")
            print(f"📁 檔案已儲存至：{excel_filename}")
            print("你可以直接在左側的檔案總管中點擊下載該檔案！")

    except sqlite3.OperationalError:
        print(f"找不到資料庫檔案 '{DB_NAME}'，請先確認 Flask 伺服器是否已經成功運行並建立資料庫。")
    except ModuleNotFoundError:
        print("缺少處理 Excel 的套件！請在終端機執行：pip install openpyxl")
    except Exception as e:
        print(f"發生錯誤：{e}")

if __name__ == '__main__':
    export_to_excel()