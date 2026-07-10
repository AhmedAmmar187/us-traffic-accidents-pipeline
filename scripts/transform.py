import os
import pandas as pd
import numpy as np

def run_transformations(input_dir="data/processed", output_dir="data/processed"):
    print("🔮 جاري البدء في عملية تنظيف ونمذجة البيانات (Star Schema)...")

    acc_df = pd.read_csv(os.path.join(input_dir,"all_years_acc.csv"), dtype={"CASENUM": str}, encoding='ISO-8859-1', low_memory=False)
    veh_df = pd.read_csv(os.path.join(input_dir,"all_years_veh.csv"), dtype={"CASENUM": str}, encoding='ISO-8859-1', low_memory=False)

    print("📍 بناء جدول (Dim_Location)...")

    location_cols = ['PSU', 'PJ', 'STRATUM']
    dim_location = acc_df[location_cols].drop_duplicates().reset_index(drop=True)
    dim_location['Location_ID'] = dim_location.index + 1
    dim_location = dim_location[['Location_ID'] + location_cols]

    print("📅 بناء جدول (Dim_Date)...")

    date_cols = ['YEAR', 'MONTH', 'DAY_WEEK']
    dim_date = acc_df[date_cols].drop_duplicates().reset_index(drop=True)
    dim_date['Date_ID'] = dim_date.index + 1
    dim_date = dim_date[['Date_ID'] + date_cols]

    print("🚗 بناء جدول (Dim_Vehicles)...")

    veh_cols = ['VEH_NO']
    if 'MOD_YEAR' in veh_df.columns:
        veh_cols.append('MOD_YEAR')

    dim_vehicles = veh_df[['CASENUM'] + veh_cols].copy()
    dim_vehicles['Vehicles_ID'] = dim_vehicles.index + 1
    dim_vehicles = dim_vehicles[['Vehicles_ID', 'CASENUM'] + veh_cols]

    print("📊 بناء جدول (Fact_Accidents)...")

    fact_df = pd.merge(acc_df, dim_location, on=location_cols, how='left')
    
    fact_df = pd.merge(fact_df, dim_date, on=date_cols, how='left')
    
    fact_metrics = ['VE_TOTAL', 'VE_FORMS', 'PEDS', 'PERMVIT', 'PERNOTMVIT']
    fact_metrics = [col for col in fact_metrics if col in fact_df.columns]
    
    fact_accidents = fact_df[['CASENUM', 'Location_ID', 'Date_ID'] + fact_metrics].copy()
    
    dim_location.to_csv(os.path.join(output_dir, "dim_location.csv"), index=False)
    dim_date.to_csv(os.path.join(output_dir, "dim_date.csv"), index=False)
    dim_vehicles.to_csv(os.path.join(output_dir, "dim_vehicles.csv"), index=False)
    fact_accidents.to_csv(os.path.join(output_dir, "fact_accidents.csv"), index=False)
    
    print("✅ تم الانتهاء من النمذجة وحفظ جميع جداول الـ Star Schema بنجاح!\n")

if __name__ == "__main__":
    run_transformations()