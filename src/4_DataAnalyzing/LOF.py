import os
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

all_matrices = []
files = []
path = r'D:\0005_大專生計畫\04_MIE\result\七層鋼構架樓層破壞_7_3_3\MIE'
"""'
# 載入資料並存儲到列表中
for i, file in enumerate(os.listdir(path)):
    if file.endswith(".txt"):
        matrix = np.loadtxt(f'{path}\\{file}')
        files.append(file)
        all_matrices.append(matrix)
data_3d = np.array(all_matrices)
print("資料集的形狀：", data_3d.shape)

# 將三維資料集攤平成二維資料集
num_samples, num_channels, num_scale = data_3d.shape
data_2d = data_3d.reshape((num_samples, num_channels * num_scale))

# 輸出轉換後的資料集形狀
print("轉換後的資料集形狀：", data_2d.shape)
"""

matrix = np.loadtxt(f'{path}\\Mie_4F02.txt')
#matrix = np.transpose(matrix)
print("資料集的形狀：", matrix.shape)

# 創建 LOF 模型
lof_model = LocalOutlierFactor(n_neighbors=7, contamination=0.1)  # 調整參數以滿足你的需求

# 訓練 LOF 模型
lof_model.fit(matrix)  

# 使用 LOF 模型進行異常檢測
outlier_scores = lof_model.negative_outlier_factor_  # 取得 LOF 分數

print(outlier_scores)

# 設定閾值
threshold = -1.5

# 識別異常點
anomalies = np.where(outlier_scores < threshold)[0]
for anomaly in anomalies:
    print("異常點：", [anomaly])

# 使用 argsort 對 LOF 分數的絕對值進行排序，返回排序後的索引
sorted_indices = np.argsort(np.abs(outlier_scores))

# 輸出排序後的 LOF 分數和對應的索引，越前面的索引對應的資料越異常
for i, idx in enumerate(sorted_indices):
    print(f"floor {idx} 的 LOF 分數：{outlier_scores[idx]}")
