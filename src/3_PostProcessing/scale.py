import os
import numpy as np

for i in range(1,20):
        
    # 資料夾路徑
    path = r'D:\0005_大專生計畫\04_MIE\result\TCUBA6_交大公教宿舍特定頻道_15_3_3\MIE'
    output_path = fr'D:\0005_大專生計畫\04_MIE\result\TCUBA6_交大公教宿舍特定頻道_{i}_3_3\MIE'

    # 確保新資料夾路徑存在
    os.makedirs(output_path, exist_ok=True)

    # 讀取資料夾內所有檔案，並按照檔名排序
    files = sorted(os.listdir(path))

    for _, file in enumerate(files):
        # 讀取檔案中的數據
        data_matrix = np.loadtxt(os.path.join(path, file))
        data_matrix = data_matrix[:, :i]
        
        # 將修改後的數據存儲到新的檔案中
        output_file = os.path.join(output_path, f'{file}')
        np.savetxt(output_file, data_matrix)
