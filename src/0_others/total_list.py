import os
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    # 將經緯度轉換為弧度
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # 地球半徑為6371公里

    return distance

def extract_info(file_path, hx_east_lat, hx_east_lon):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    earthquake_line = next((line.strip() for line in lines if line.startswith("Earthquake")), "")
    sample_rate_line = next((line.strip() for line in lines if line.startswith("RecordLength")), "")

    # 取得地震的經緯度 
    lat_index = earthquake_line.find('N')
    lon_index = earthquake_line.find('E', 15) 
    mag_index = earthquake_line.find('M', 15) 
    
    lat = float(earthquake_line[lat_index + 1:].split()[0])
    lon = float(earthquake_line[lon_index + 1:].split()[0])
    mag = float(earthquake_line[mag_index + 1:].split()[0])

    # 計算震央距離
    distance = haversine(hx_east_lat, hx_east_lon, lat, lon)

    return f"{os.path.basename(file_path)} {earthquake_line} 規模{mag} 震央距離{distance:.2f} {sample_rate_line}"

def merge_info_lines(input_folder, output_file, hx_east_lat, hx_east_lon):
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as output:
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)
                info_line = extract_info(file_path, hx_east_lat, hx_east_lon)
                output.write(info_line + '\n')

# 輸入資料夾的路徑和輸出檔案的路徑
input_folder = r'D:\0005_大專生計畫\04_MIE\data\TCUBA6_交大公教宿舍'
output_file = r'D:\0005_大專生計畫\04_MIE\result\TCUBA6_交大公教宿舍\total.txt'

# 新竹東區的經緯度
hx_east_lat = 24.803
hx_east_lon = 120.995

# 執行合併操作
merge_info_lines(input_folder, output_file, hx_east_lat, hx_east_lon)
