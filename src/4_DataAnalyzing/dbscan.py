from sklearn.cluster import DBSCAN
import numpy as np
import os

all_matrices = []
files = []
path = r'D:\0005_大專生計畫\04_MIE\result\七層鋼構架樓層破壞_20_3_3\DI' # D:\0005_大專生計畫\04_MIE\data\real_data(V)_七層鋼構架樓層破壞' #

"""
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

matrix = np.loadtxt(f'{path}\\DI_Mie_4F02.txt')
# matrix = np.transpose(matrix)
print("資料集的形狀：", matrix.shape) # (n_features, n_samples)


# 初始化 DBSCAN 模型
dbscan_model = DBSCAN(eps=0.5, min_samples=5)

# 使用 DBSCAN 模型進行訓練和異常檢測
labels = dbscan_model.fit_predict(matrix)

# 根據標籤將資料分為群集0和異常值-1
print(labels!= -1)
normal_matrix = matrix[labels != -1]
anomalies = matrix[labels == -1]

# 輸出結果
#print("群集中的資料：", normal_matrix)
#print("異常值：", anomalies)
