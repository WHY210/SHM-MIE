import numpy as np
import os

# 讀取健康案例中的樓層向矩陣和尺度向矩陣
path = r"D:\SHM-MIE\result\七層鋼構架樓層破壞_7_3_3\MIE"
files = os.listdir(path)
 
max_value_floor = 0
max_value_scale = 0

#'UD003_difference.txt',

for file in ['UD001_difference.txt', 'UD002_difference.txt', 'UD01_difference.txt', 'UD02_difference.txt',  'UD04_difference.txt', 'UD03_difference.txt']:
    data = np.loadtxt(os.path.join(path, file), dtype=float)
    floor_matrix = np.diff(data, axis=1, )
    scale_matrix = np.diff(data, axis=0, )
    max_value_floor = np.maximum(max_value_floor, np.abs(floor_matrix).max())  # 找出絕對值最大的值作為α
    max_value_scale = np.maximum(max_value_scale, np.abs(scale_matrix).max())  # 找出絕對值最大的值作為β
print(max_value_floor, max_value_scale)

floor_base = 1*max_value_floor 
scale_base = 1*max_value_scale  
#floor_base = 0.041001193 * 1.35
#scale_base = 0.060942024 * 1.35

# 處理待測案例中的樓層向矩陣和尺度向矩陣
for file in files:
    if file.endswith("_difference.txt"):
        data = np.loadtxt(os.path.join(path, file), dtype=float)
        floor_matrix = np.diff(data, axis=1, )
        scale_matrix = np.diff(data, axis=0, )

        data_matrix_floor = np.where(floor_matrix > floor_base, 1, 
                                         np.where(floor_matrix < floor_base, -1, 0))  
        data_matrix_scale = np.where(scale_matrix > floor_base, 1, 
                                         np.where(scale_matrix < scale_base, -1, 0))  
        with open(f'{path}\\{file}_floor.txt', 'w') as output_file:
                for row in data_matrix_floor:
                    np.savetxt(output_file, row, newline=' ', fmt='%d')
                    output_file.write('\n')
        with open(f'{path}\\{file}_scale.txt', 'w') as output_file:
                for row in data_matrix_scale:
                    np.savetxt(output_file, row, newline=' ', fmt='%d')
                    output_file.write('\n')