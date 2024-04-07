import os


def rename_files(directory, prefix, old_str, new_str, lastfix):
    for filename in os.listdir(directory):
        if old_str in filename:
            new_filename = prefix + filename.replace(old_str, new_str) + lastfix
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} to {new_filename}")


# 請替換以下變數的值
directory_path = r"C:\Users\dulci\OneDrive - 國立陽明交通大學\桌面\NYCU\0006_大專生計畫\SHM-MIE\result\TCUBA6_交大公教宿舍_濾波_30_3_3\MIE"  # 指定目錄路徑
prefix = ""
old_string = ""  # 要替換的舊字串
new_string = ""  # 新字串
lastfix = ".txt"

# 使用函數進行檔案名稱更改
rename_files(directory_path, prefix, old_string, new_string, lastfix)
