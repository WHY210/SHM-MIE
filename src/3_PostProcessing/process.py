import numpy as np
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use("ggplot")  # classic bmh Solarize_Light2 seaborn default fivethirtyeight dark_background ggplot
plt.rcParams['figure.max_open_warning'] = 1000
from matplotlib.colors import LinearSegmentedColormap

class DataProcessor:
    def __init__(self, building_type, channel, scale):
        self.building_type = building_type
        self.path = f'.\\result\\{building_type}'
        self.path_MIEnotstd =  f'.\\result\\{building_type}\\MIE'
        self.path_MIE =  f'.\\result\\{building_type}\\MIE'
        self.path_DInotstd =  f'.\\result\\{building_type}\\DI'
        self.path_DI =  f'.\\result\\{building_type}\\DI'
        self.path_MM = f'.\\result\\{building_type}\\MM'
        self.channel = channel
        self.scale = scale

    def standerdize(self, flag, old, new):
        path_old = getattr(self, f'path_{old}')
        path_new = getattr(self, f'path_{new}')
        os.makedirs(fr'{path_new}', exist_ok=True)
        if flag:
            for i, file in enumerate(os.listdir(path_old)):
                if file.endswith(".txt"):
                    data = np.loadtxt(f'{path_old}\\{file}')
                    mean = np.mean(data, axis=0)
                    std = np.std(data, axis=0)
                    normalized_data = (data - mean) / std
                    np.savetxt(fr'{path_new}\{file}', normalized_data, fmt='%.6f', delimiter=' ')
        else:
            for i, file in enumerate(os.listdir(path_old)):
                if file.endswith(".txt"):
                    data = np.loadtxt(f'{path_old}\\{file}')
                    np.savetxt(fr'{path_new}\{file}', data, fmt='%.6f', delimiter=' ')
        
        print("finish std", flag)


    def calculate_MinusMean(self):
        os.makedirs(fr'{self.path_MM}', exist_ok=True)

        ## MEAN ##
        average_matrix = np.zeros((self.channel, self.scale))
        for i, file in enumerate(os.listdir(self.path_MIE)):
            matrix = np.loadtxt(f'{self.path_MIE}\\{file}')
            average_matrix += matrix
        average_matrix /= (i+1)
        np.savetxt(fr'{self.path_MM}\mean.txt', average_matrix, fmt='%.6f', delimiter=' ')

        ## MINUS ##
        for i, file in enumerate(os.listdir(self.path_MIE)):
            matrix = np.loadtxt(f'{self.path_MIE}\\{file}')
            matrix -= average_matrix
            np.savetxt(fr'{self.path_MM}\MM_{file}', matrix, fmt='%.6f', delimiter=' ')
        print("finish calculate MM")

    def calculate_DI(self):
        
        os.makedirs(fr'{self.path_DInotstd}', exist_ok=True)

        for _, file in enumerate(os.listdir(self.path_MIE)):
            if file.endswith(".txt"):
              
                ## REFERENCE ##
                if "七層鋼構架樓層破壞" in self.building_type:
                
                    ## EVALUATE ##
                    evaluate = np.loadtxt(f'{self.path_MIE}\\{file}')
                    min_value = np.inf*np.ones((self.channel, self.scale))
                    max_value = np.zeros((self.channel, self.scale))
                    damage_index = np.zeros((self.channel, self.scale))
                    # 讀取七個參考文件的數據並添加到列表中
                    sum_reference = np.zeros_like(evaluate)
                    num_references = 0  # 計算參考文件的總數
                    for reference_file in ['UD001.txt', 'UD002.txt', 'UD01.txt', 'UD02.txt', 'UD003.txt', 'UD04.txt', 'UD03.txt']:
                        reference = np.loadtxt(os.path.join(self.path_MIE, reference_file))
                        sum_reference += reference
                        num_references += 1

                    # 計算每個位置的平均值
                    reference = sum_reference / num_references
                        
                    damage_index = evaluate - reference
                    """ 
                    # 計算 evaluate 和每個參考文件之間的差值，並找出每個位置的最小值
                        differences = evaluate - reference
                        differences = differences.reshape((self.channel, self.scale))
                        for c in range(self.channel):
                            for s in range(self.scale):
                                if file != reference_file:
                                    max_value[c,s] = np.maximum(max_value[c,s], np.abs(differences[c,s]))
                                    if np.abs(differences[c,s]) == max_value[c,s]:
                                        damage_index[c,s] = differences[c,s] 
                                        """
                            

                elif "TCUBA6_交大公教宿舍" in self.building_type:
                    reference = (np.loadtxt(f'{self.path_MIE}\\Mie_1994060600.txt'))

                    ## EVALUATE ##
                    evaluate = np.loadtxt(f'{self.path_MIE}\\{file}')
                    damage_index = evaluate - reference

                with open(f'{self.path_DInotstd}\\{file}', 'w') as output_file:
                    for row in damage_index:
                        np.savetxt(output_file, row, newline=' ', fmt='%.25f')
                        output_file.write('\n')
                        
        print("finish calculate DI")

    def scatter_plot(self, type, bottom, top):
        
        path = getattr(self, f'path_{type}')
        os.makedirs(fr'{path}_scatterplot', exist_ok=True)
        if type in ['MIE_Minus_1_0_1', 'DI_Minus_1_0_1', 'MM_Minus_1_0_1']:
            channel = self.channel - 1
            scale =self.scale - 1
            channel_range = range(1, channel+1)           
            scale_range = range(1, scale+1)
        elif type in ['MIE_Minus_1_1_0', 'DI_Minus_1_1_0', 'MM_Minus_1_1_0']:
            channel = self.channel - 1
            scale =self.scale - 1
            channel_range = range(1, channel+1)
            scale_range = range(1, scale+1)
        elif type in ['MIE_Minus_1_0_x', 'DI_Minus_1_0_x', 'MM_Minus_1_0_x']:
            channel = self.channel - 1
            scale =self.scale
        else:
            channel = self.channel

        ylabel = f"{type}"

        for _, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')
            data_matrix = data.reshape((channel, self.scale))

            plt.figure(figsize=(8, 4), dpi=150)

            for i in range(1, channel+1):
                plt.plot(np.arange(1, self.scale + 1), data_matrix[i - 1, :], label=f"{i-1}", marker='o', markersize='3')

            plt.xlabel("Scale", fontsize=8)
            plt.xticks(range(1, self.scale+1), fontsize=7)
            plt.ylabel(ylabel, fontsize=8)
            plt.yticks(fontsize=7)
            plt.ylim(bottom, top)
            plt.title(file, fontsize=10)
            plt.legend(loc='upper right', fontsize=6)
            plt.grid("MIE", linestyle = "--",color = 'grey' ,linewidth = '0.3',axis='both', alpha=0.5)
            plt.savefig(f'{path}_scatterplot\\{file}.png')
        
        print(f'finish scatter - {type}')

    def sum_up(self, type):

        path = getattr(self, f'path_{type}')
        os.makedirs(fr'{path}_SummedUp', exist_ok=True)

        if type in ['Minus_MIE', 'Minus_DI', 'Minus_MM']:
            channel = self.channel - 1
        else:
            channel = self.channel

        for i, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')
            data_matrix = data.reshape((channel, self.scale))
            summed_data = np.sum(data_matrix, axis=1)
            np.savetxt(f'{path}_SummedUp\\{file}', summed_data)
        
        print(f'finish sum up - {type}')

    def minus(self, type, axis1, time1, axis2, time2):

        path = getattr(self, f'path_{type}')
        folder = f'{path}_Minus_{axis1}{time1}th_{axis2}{time2}th'
        os.makedirs(folder, exist_ok=True)

        for _, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')
            data_matrix = data.reshape((self.channel, self.scale))
            def axis(axistype, axisnumber):
                if axistype == "scale":
                    axisnumber = 1
                elif axistype == "floor":
                    axisnumber = 0
                return axisnumber
            data_matrix = np.diff(data_matrix, n=time1, axis=axis(axis1, time1))
            data_matrix = np.diff(data_matrix, n=time2, axis=axis(axis2, time2))
            np.savetxt(f'{folder}\\{file}', data_matrix, fmt='%.8f')
        
        print(f'finish calculate minus - {type}')

   
    def totalplot(self, bottom1, top1, bottom2, top2):
        os.makedirs(fr'{self.path}\\totalplot', exist_ok=True)

        for _, file in enumerate(os.listdir(self.path_MIE)):
            
            fig, ax1 = plt.subplots(figsize=(8, 5), dpi=150)  
            ax2 = ax1.twinx()

            # MIE
            path_MIE = getattr(self, 'path_MIE')
            data_MIE = np.loadtxt(f'{path_MIE}\\{file}')
            data_matrix_MIE = data_MIE.reshape((self.channel, self.scale))
            summed_data_MIE = np.sum(data_matrix_MIE, axis=1)
            ax1.bar(np.arange(self.channel), summed_data_MIE, label='MIE', color='#86C166', alpha=0.5, zorder=-2)
            ax1.set_ylabel("MIE summed up", fontsize=7)
            ax1.set_ylim(bottom2, top2)
            ax1.tick_params(axis='y', labelcolor='tab:red', labelsize=7)
            ax1.legend(loc='upper right')

            for type, color in zip(["DI", "MIE_Minus_1_0_x", "DI_Minus_1_0_x"], ['#9B90C2', '#0089A7', '#DB4D6D']):
                if type in ['MIE_Minus_1_0_x', 'DI_Minus_1_0_x']:
                    channel = self.channel - 1
                    x_range = np.arange(1, channel + 1)
                    alpha = 1
                else:
                    channel = self.channel
                    x_range = np.arange(channel)
                    alpha = 0.75
                path = f'{self.path}\\{type}'
                data = np.loadtxt(f'{path}\\{file}')
                data_matrix = data.reshape((channel, self.scale))
                summed_data = np.sum(data_matrix, axis=1)
                ax2.plot(x_range, summed_data, label=type, color=color, alpha = alpha, zorder=2)

            ax2.axhline(y=0, color='white', linewidth=1, linestyle='--', zorder=-1)
            ax2.set_xlabel("Channel", fontsize=7)
            ax2.set_ylabel("summed up", fontsize=7)
            ax2.set_ylim(bottom1, top1)
            ax2.set_yticks(np.arange(bottom1, top1, 2))
            ax2.tick_params(axis='y', labelcolor='tab:blue', labelsize=7)
            ax2.legend(loc='upper left')

            ax1.set_xticks(x_range)
            ax1.set_xticklabels(x_range, fontsize=7)
            ax1.set_title(file, fontsize=10)
            ax1.grid(True, linestyle="--", color='grey', linewidth='0.5', axis='both', alpha=0.5)
            ax2.grid(False)
            plt.savefig(fr'{self.path}\totalplot\{file}.png')
            plt.close()

        print(f'finish totalplot')

    def totalplot_2(self, bottom1, top1, bottom2, top2):
        os.makedirs(fr'{self.path}\\totalplot_2', exist_ok=True)

        for _, file in enumerate(os.listdir(self.path_MIE)):
            
            fig = plt.subplots(figsize=(8, 5), dpi=150)  

            for type, color in zip(["Minus_2_MIE", "Minus_2_DI"], ['#9B90C2', '#0089A7', '#DB4D6D']):
                if type in ["Minus_2_MIE", "Minus_2_DI"]:
                    channel = self.channel - 2
                    x_range = np.arange(1.5, channel + 1.5)
                    alpha = 1
                else:
                    channel = self.channel
                    x_range = np.arange(channel)
                    alpha = 0.75
                path = getattr(self, f'path_{type}')
                data = np.loadtxt(f'{path}\\{file}')
                data_matrix = data.reshape((channel, self.scale))
                summed_data = np.sum(data_matrix, axis=1)
                plt.plot(x_range, summed_data, label=type, color=color, alpha = alpha, zorder=2)

            plt.axhline(y=0, color='white', linewidth=1, linestyle='--', zorder=-1)
            plt.xlabel("Channel", fontsize=7)
            plt.ylim(bottom1, top1)
            plt.yticks(np.arange(bottom1, top1, 2))
            plt.legend(loc='upper left')
            plt.xticks(x_range)
            plt.xticks(ticks=x_range, fontsize=7)
            plt.title(file, fontsize=10)
            plt.grid(True, linestyle="--", color='grey', linewidth='0.5', axis='both', alpha=0.5)
            plt.savefig(fr'{self.path}\totalplot_2\{file}.png')
            plt.close()

        print(f'finish totalplot')

    def threeD(self, type, bottom, top):
        for i in range(5):
            if f'floor{i}' in type:
                channel = self.channel - i
            if f'scale{i}' in type:
                scale = self.scale - i
        
        channel_range = range(channel)
        scale_range = range(1, scale+1)

        path = f'{self.path}\\{type}'
        os.makedirs(fr'{path}_3D', exist_ok=True)
        x, y = np.meshgrid(scale_range, channel_range)

        for _, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')
            data_matrix = data.reshape((channel, scale))

            fig = plt.figure(figsize=(7.3, 7.3), dpi=200)
            ax = fig.add_subplot(111, projection='3d')

            surf = ax.plot_surface(x, y, data_matrix, cmap='viridis' ) 
            zero_plane = np.zeros_like(data_matrix)
            ax.plot_surface(x, y, zero_plane, color='gray', alpha=0.5)
            fig.colorbar(surf, shrink=0.5, aspect=5)

            ax.view_init(elev=30, azim=145)  # 設置仰角和方位角15,145
            ax.set_zlim(bottom, top) 
            ax.grid(True)
            ax.set_xlabel('scale')
            ax.set_ylabel('channel')
            ax.set_zlabel('Damage Index between floors')
            plt.savefig(f'{path}_3D\\{file}.png')
        
        print(f'finish 3D - {type}')


# for i in range(15,16):
#     TCUBA6 = DataProcessor(f'TCUBA6_交大公教宿舍特定頻道_{i}_3_3', 12, i)
#     TCUBA6.calculate_DI()
#     TCUBA6.minus(1, 0, False, "x", "DI")
#     # TCUBA6.threeD("DI", -2, 2)
#     TCUBA6.threeD("DI_Minus_1_0_x", -2, 2)



for i in range(30, 31):
    NCREE = DataProcessor(f'min微振段_七層鋼構架樓層破壞_特定樓層_{i}_3_3', 5, i)
    NCREE.standerdize(False, "MIEnotstd", "MIE")
    NCREE.calculate_DI()
    # NCREE.standerdize(False, "DInotstd", "DI")
    NCREE.minus("MIE", "floor", 1, "scale", 0)  
    NCREE.minus("DI", "floor", 1, "scale", 0)  
    # NCREE.totalplot(-15, 15, 0, 75)
    # NCREE.scatter_plot("MIE", -5, 5)
    # NCREE.scatter_plot("DI", -5, 5)
    # NCREE.threeD("MIE", 0, 5)
    # NCREE.threeD("DI", -2, 2)
    # NCREE.threeD("MIE_Minus_floor1_sclae0", -2, 2)
    # NCREE.threeD("DI_Minus_floor1_sclae0", -2, 2)
    print(f'七層鋼構架樓層破壞 finish{i}')

