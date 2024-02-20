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
directory_path = r"D:\0005_大專生計畫\04_MIE\result\TCUBA6_交大公教宿舍_15_3_3\MIE_SummedUp"  # 指定目錄路徑
old_string = "Mie_"  # 要替換的舊字串
new_string = ""  # 新字串

# 使用函數進行檔案名稱更改
rename_files(directory_path, old_string, new_string)


###################################

"""
original_numbers = [
    
]

# 加上 "20" 並轉換成整數格式
modified_numbers = [int("20" + number) for number in original_numbers]

print(modified_numbers)
"""