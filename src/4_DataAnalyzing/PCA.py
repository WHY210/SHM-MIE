import os
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

all_matrices = []
files = []
path = r'D:\SHM-MIE\result\七層鋼構架樓層破壞_特定樓層_30_3_3\DI_Minus_1_0_x'

# 載入資料並存儲到列表中
for i, file in enumerate(os.listdir(path)):
    if file.endswith(".txt"):
        data = np.loadtxt(f'{path}\\{file}')
        #data = np.transpose(data)
        print("資料集的形狀：", data.shape)

        # 1. 標準化資料
        data_scaled = (data - np.mean(data, axis=0)) / np.std(data, axis=0)

        # 2. 應用 PCA
        pca = PCA(n_components=2)  # 選擇投影到 2 維空間
        data_pca = pca.fit_transform(data_scaled)

        # 3. 可視化結果
        plt.figure(figsize=(8, 6))
        plt.scatter(data_pca[:, 0], data_pca[:, 1], alpha=0.5)

        # 在每個點的附近添加標籤
        for i, (x, y) in enumerate(data_pca):
            plt.text(x, y, str(i), fontsize=10)

        plt.title('PCA Projection of Data with Labels')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.grid(True)
        plt.savefig(f'{path}\\{file}_PCA2D.png')

        # 2. 應用 PCA
        pca = PCA(n_components=3)  # 選擇投影到 3 維空間
        data_pca = pca.fit_transform(data_scaled)

        # 3. 可視化結果
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # 繪製三維散點圖
        ax.scatter(data_pca[:, 0], data_pca[:, 1], data_pca[:, 2], alpha=0.5)

        # 在每個點的附近添加標籤
        for i, (x, y, z) in enumerate(data_pca):
            ax.text(x, y, z, str(i), fontsize=8)

        ax.set_title('PCA Projection of Data in 3D')
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.set_zlabel('Principal Component 3')
        plt.savefig(f'{path}\\{file}_PCA3D.png')

        from sklearn.manifold import TSNE
        import numpy as np
        import matplotlib.pyplot as plt

        # 假設資料儲存在 data 變數中，labels 儲存了每個資料點的標籤
        # data 的形狀應該是 (n_samples, n_features)
        # labels 的形狀應該是 (n_samples,)
        # 在這裡你可以將資料和標籤轉換成你需要的格式

        # 1. 標準化資料
        data_scaled = (data - np.mean(data, axis=0)) / np.std(data, axis=0)

        # 2. 應用 t-SNE
        tsne = TSNE(n_components=2, perplexity=6)  # 選擇投影到 2 維空間，並設置 perplexity
        data_tsne = tsne.fit_transform(data_scaled)

        # 3. 可視化結果
        plt.figure(figsize=(8, 6))

        # 繪製散點圖
        plt.scatter(data_tsne[:, 0], data_tsne[:, 1], alpha=0.5)

        # 在每個資料點的附近添加標籤
        for i, (x, y) in enumerate(data_tsne):
            plt.text(x, y, str(i), fontsize=8)

        plt.title('t-SNE Projection of Data in 2D with Labels')
        plt.xlabel('t-SNE Component 1')
        plt.ylabel('t-SNE Component 2')
        plt.grid(True)
        plt.savefig(f'{path}\\{file}_tSNE2D.png')



        from sklearn.manifold import TSNE
        import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # 用於繪製三維圖形

        # 1. 標準化資料
        data_scaled = (data - np.mean(data, axis=0)) / np.std(data, axis=0)

        # 2. 應用 t-SNE
        tsne = TSNE(n_components=3, perplexity=6)  # 選擇投影到 3 維空間，並設置 perplexity
        data_tsne = tsne.fit_transform(data_scaled)

        # 3. 可視化結果
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # 繪製三維散點圖
        ax.scatter(data_tsne[:, 0], data_tsne[:, 1], data_tsne[:, 2], alpha=0.5)

        # 在每個資料點的附近添加標籤
        for i, (x, y, z) in enumerate(data_tsne):
            ax.text(x, y, z, str(i), fontsize=8)

        ax.set_title('t-SNE Projection of Data in 3D with Labels')
        ax.set_xlabel('t-SNE Component 1')
        ax.set_ylabel('t-SNE Component 2')
        ax.set_zlabel('t-SNE Component 3')
        plt.savefig(f'{path}\\{file}_tSNE3D.png')