import os
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

# 指定資料夾路徑
path = r'D:\SHM-MIE\result\七層鋼構架樓層破壞_20_3_3\MIE'

# 初始化資料集和文件列表
all_matrices = []
files = []

# 讀取UD開頭的txt檔案，並將資料存儲到列表中
for file in os.listdir(path):
    if file.startswith("UD") and file.endswith(".txt"):
        matrix = np.loadtxt(os.path.join(path, file))
        files.append(file)
        all_matrices.append(matrix)

# 將列表轉換為 NumPy 陣列
data_3d = np.array(all_matrices)

# 輸出資料集的形狀
print("資料集的形狀：", data_3d.shape)

# 攤平資料集成二維
num_samples, num_channels, num_scale = data_3d.shape
data_2d = data_3d.reshape((num_samples, num_channels * num_scale))

# 輸出轉換後的資料集形狀
print("轉換後的資料集形狀：", data_2d.shape)

# 創建 LOF 模型
lof_model = LocalOutlierFactor(n_neighbors=7, contamination=0.1)  # 調整參數以滿足您的需求

# 訓練 LOF 模型
lof_model.fit(data_2d)

# 使用 LOF 模型進行異常檢測
outlier_scores = lof_model.negative_outlier_factor_  # 取得 LOF 分數

# 設定異常閾值
threshold = -1.5

# 識別異常點
anomalies = np.where(outlier_scores < threshold)[0]
print("異常點索引：", anomalies)

# 輸出排序後的 LOF 分數和對應的索引，越前面的索引對應的資料越異常
sorted_indices = np.argsort(np.abs(outlier_scores))
for i, idx in enumerate(sorted_indices):
    print(f"{files[i]} 的 LOF 分數：{outlier_scores[idx]}")
