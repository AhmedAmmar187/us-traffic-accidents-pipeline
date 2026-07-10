import os
import sqlite3
import pandas as pd

def load_data_to_warehouse(input_dir="data/processed", db_name="data/processed/traffic_warehouse.db"):
    print("📥 جاري البدء في مرحلة التحميل (Load) إلى مستودع البيانات المحلي...")
    
    
    conn = sqlite3.connect(db_name)
    
    
    tables_to_load = {
        'fact_accidents': 'Fact_Accidents',
        'dim_location': 'Dim_Location',
        'dim_date': 'Dim_Date',
        'dim_vehicles': 'Dim_Vehicles'
    }
    
    for file_name, table_name in tables_to_load.items():
        file_path = os.path.join(input_dir, f"{file_name}.csv")
        
        if os.path.exists(file_path):
            print(f"شحن الجدول {table_name} إلى مستودع البيانات...")
            df = pd.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        else:
            print(f"⚠️ تحذير: الملف {file_name}.csv غير موجود في المسار المحدد.")
            
    conn.close()
    print(f"✅ تم تحميل جميع الجداول بنجاح داخل مستودع البيانات: {db_name}\n")

if __name__ == "__main__":
    load_data_to_warehouse()