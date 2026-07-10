import os
import glob
import pandas as pd


def merge_yearly_data(data_dir="data/raw", output_dir="data/processed"):
    os.makedirs(output_dir, exist_ok=True)
    file_types = ['acc', 'veh', 'pers']

    for f_type in file_types:
        print(f"جاري البحث عن ملفات من النوع: {f_type} لدمجها...")

        search_pattern = os.path.join(data_dir, f"{f_type}_*.csv")
        all_files = glob.glob(search_pattern)

        if not all_files:
            print(f"⚠️ تحذير: لم يتم العثور على أي ملفات للنوع {f_type} في المسار {data_dir}")
            continue
        df_list = []
        for file in sorted(all_files):
            print(f"قراءة الملف: {os.path.basename(file)}")

            df = pd.read_csv(file, dtype={'CASENUM' : str}, encoding='ISO-8859-1', low_memory=False)
            df_list.append(df)


        merged_df = pd.concat(df_list, ignore_index=True)

        output_file = os.path.join(output_dir, f"all_years_{f_type}.csv")
        merged_df.to_csv(output_file, index =False)
        print(f"✅ تم دمج وحفظ الملف بنجاح في: {output_file} | الحجم: {merged_df.shape}\n")

if __name__ == "__main__":
    merge_yearly_data()