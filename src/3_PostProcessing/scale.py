import os
import numpy as np

for i in range(2,16):
        
    # 資料夾路徑
    path = r'..\..\result\七層鋼構架樓層破壞_濾波_9601-13600_15_3_3\MIE'
    output_path = fr'..\..\result\七層鋼構架樓層破壞_濾波_9601-13600_{i}_3_3\MIE'

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
        np.savetxt(output_file, data_matrix, fmt='%.6f')
