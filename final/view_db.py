import sqlite3
import pandas as pd

# 定義資料庫檔案名稱
DB_NAME = 'justice_bridge.db'

def view_data():
    try:
        # 連線到資料庫
        conn = sqlite3.connect(DB_NAME)
        
        # 使用 Pandas 讀取整個資料表，這會讓資料排版變得非常漂亮
        # SQL 指令：選取 user_verdicts 表格中的所有資料
        df = pd.read_sql_query("SELECT * FROM user_verdicts", conn)
        
        # 關閉連線
        conn.close()

        # 檢查是否有資料
        if df.empty:
            print("目前資料庫是空的，還沒有人提交判決喔！")
        else:
            print("=== 法感實驗室：最新民意數據 ===")
            # 設定 Pandas 印出時不要省略欄位
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(df)
            print("\n總計收到 {} 筆判決。".format(len(df)))

    except sqlite3.OperationalError:
        print(f"找不到資料庫檔案 '{DB_NAME}'，請確認 Flask 伺服器是否已經成功運行並建立資料庫。")
    except Exception as e:
        print(f"發生錯誤：{e}")

if __name__ == '__main__':
    view_data()