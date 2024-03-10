import os
import numpy as np

path = r"D:\SHM-MIE\result\七層鋼構架樓層破壞_7_3_3\DI"  

# 創建一個空的列表來儲存所有文件的最大值、最小值、平均值、標準差和位置
data = []

for file in os.listdir(path):
    if file.endswith('.txt'):  
        matrix = np.loadtxt(os.path.join(path, file))
        max_value = np.max(matrix)
        min_value = np.min(matrix)
        mean_value = np.mean(matrix)
        std_value = np.std(matrix)
        max_position = np.unravel_index(np.argmax(matrix), matrix.shape)
        min_position = np.unravel_index(np.argmin(matrix), matrix.shape)

        # 將每個文件的統計量儲存到列表中，並將位置索引加1
        data.append([file, 
                     "MAX: ", max_value, (max_position[0]+1, max_position[1]+1), 
                     "MIN: ", min_value, (min_position[0]+1, min_position[1]+1),
                     "MEAN: ", mean_value,
                     "STD: ", std_value])

# 將列表轉換為 NumPy 陣列
data_array = np.array(data, dtype=object)

# 將資料寫入到文本檔中
np.savetxt(r"D:\SHM-MIE\result\七層鋼構架樓層破壞_7_3_3\mixmin.txt", data_array, fmt='%s')
