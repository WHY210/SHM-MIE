import os


def rename_files(directory, old_str, new_str):
    for filename in os.listdir(directory):
        if old_str in filename:
            new_filename = filename.replace(old_str, new_str)
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} to {new_filename}")


# 請替換以下變數的值
directory_path = r"D:\SHM-MIE\result\七層鋼構架樓層破壞_20_3_3\MIE"  # 指定目錄路徑
old_string = "Mie_"  # 要替換的舊字串
new_string = ""  # 新字串

# 使用函數進行檔案名稱更改
rename_files(directory_path, old_string, new_string)
