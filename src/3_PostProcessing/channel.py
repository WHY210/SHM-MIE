import os
import numpy as np

selected_channels = [1, 2, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20]
selected_channels = [x - 1 for x in selected_channels] 

# 資料夾路徑
path = r'D:\0005_大專生計畫\04_MIE\result\TCUBA6_交大公教宿舍_15_3_3\MIE'
output_path = fr'D:\0005_大專生計畫\04_MIE\result\TCUBA6_交大公教宿舍特定頻道_15_3_3\MIE'

# 確保新資料夾路徑存在
os.makedirs(output_path, exist_ok=True)

# 讀取資料夾內所有檔案，並按照檔名排序
files = sorted(os.listdir(path))

for file in files:
    # 讀取檔案中的數據
    data_matrix = np.loadtxt(os.path.join(path, file))

    # 擷取指定的通道
    selected_matrix = data_matrix[selected_channels, :]

    # 將修改後的數據存儲到新的檔案中
    output_file = os.path.join(output_path, f'{file}')
    np.savetxt(output_file, selected_matrix)
