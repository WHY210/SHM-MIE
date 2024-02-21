import os
import matplotlib.pyplot as plt
import numpy as np

# 資料夾路徑
print(os.getcwd())
path = r'..\..\result\TCUBA6_交大公教宿舍_2_3_3\MIE_SummedUp'

# 讀取資料夾內所有檔案，並按照檔名排序
files = sorted(os.listdir(path))

# 產生年份列表，從檔名中提取年份部分
years = [file.split('.')[0][:6] for file in files]

# 建立一個空的24x21的NumPy陣列，用於存儲所有檔案的數據
data_matrix = np.zeros((24, len(years)))

# 迭代處理每個檔案
for i, file in enumerate(files):
    # 讀取檔案中的24個數字
    with open(os.path.join(path, file), 'r') as f:
        data = np.loadtxt(f)
    
    # 將數據存儲到數據矩陣中
    data_matrix[:, i] = data

# 繪製趨勢圖
plt.figure(figsize=(10, 6))
for i in range(data_matrix.shape[0]):
    plt.plot(years, data_matrix[i, :], label=f'Channel {i+1}')

plt.title('Trends Over the Years')
plt.xlabel('Year')
plt.xticks(fontsize=3)
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()
