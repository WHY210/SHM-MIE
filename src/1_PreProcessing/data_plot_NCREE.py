import numpy as np
import matplotlib.pyplot as plt
import os

file_path = r'.\data\real_data(V)_七層鋼構架樓層破壞'

for i, file in enumerate(os.listdir(file_path)):
    if file.endswith("txt"):
        data_matrix = np.loadtxt(os.path.join(file_path, file))
        num_timesteps,  num_channels = data_matrix.shape
        fig, axs = plt.subplots(8, 1, figsize=(7.3, 7.3), dpi=200)  
        for i in range(num_channels):
            axs[i].plot(range(num_timesteps), data_matrix[:, i], label=f'Channel {i}')
            axs[i].set_title(f'Channel {i}', fontsize=7)
            axs[i].set_ylim(-0.02, 0.02)  
            axs[i].axvspan(9601, 13600, color='gray', alpha=0.2)  # MIE段落
        plt.tight_layout()  
        plt.savefig(f'{file_path}\\{file}.png') 
