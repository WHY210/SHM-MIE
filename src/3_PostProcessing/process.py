import numpy as np
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use("ggplot")  # classic bmh Solarize_Light2 seaborn default fivethirtyeight dark_background ggplot
plt.rcParams['figure.max_open_warning'] = 1000

class DataProcessor:
    def __init__(self, building_type, channel, scale):
        self.building_type = building_type
        self.path = f'..\\..\\result\\{building_type}'
        self.path_MIE =  f'..\\..\\result\\{building_type}\\MIE'
        self.path_DI =  f'..\\..\\result\\{building_type}\\DI'
        self.path_MM = f'..\\..\\result\\{building_type}\\MM'
        self.path_Minus_MIE = f'..\\..\\result\\{building_type}\\MIE_Minus'
        self.path_Minus_DI = f'..\\..\\result\\{building_type}\\DI_Minus'
        self.path_Minus_MM = f'..\\..\\result\\{building_type}\\MM_Minus'
        self.channel = channel
        self.scale = scale

    def calculate_MinusMean(self):
        os.makedirs(fr'{self.path_MM}', exist_ok=True)

        ## MEAN ##
        average_matrix = np.zeros((self.channel, self.scale))
        for i, file in enumerate(os.listdir(self.path_MIE)):
            matrix = np.loadtxt(f'{self.path_MIE}\\{file}')
            average_matrix += matrix
        average_matrix /= (i+1)
        np.savetxt(fr'{self.path_MM}\mean.txt', average_matrix, fmt='%f', delimiter=' ')

        ## MINUS ##
        for i, file in enumerate(os.listdir(self.path_MIE)):
            matrix = np.loadtxt(f'{self.path_MIE}\\{file}')
            matrix -= average_matrix
            np.savetxt(fr'{self.path_MM}\MM_{file}', matrix, fmt='%f', delimiter=' ')
        print("finish calculate MM")

    def calculate_DI(self):
        
        os.makedirs(fr'{self.path_DI}', exist_ok=True)

        for _, file in enumerate(os.listdir(self.path_MIE)):
              
            ## REFERENCE ##
            if "七層鋼構架樓層破壞" in self.building_type:

                UD001 = np.loadtxt(self.path_MIE + r'\UD001.txt')
                UD01 = np.loadtxt(self.path_MIE + r'\UD01.txt')
                UD002 = np.loadtxt(self.path_MIE + r'\UD002.txt')
                UD02 = np.loadtxt(self.path_MIE + r'\UD02.txt')
                UD003 = np.loadtxt(self.path_MIE + r'\UD003.txt')
                UD03 = np.loadtxt(self.path_MIE + r'\UD03.txt')
                UD04 = np.loadtxt(self.path_MIE + r'\UD04.txt')

                reference = (UD001 + UD01 + UD002 + UD02 + UD003 + UD03 + UD04) / 7

            elif "TCUBA6_交大公教宿舍" in self.building_type:
                reference = (np.loadtxt(f'{self.path_MIE}\\Mie_1994060600.txt'))

            ## EVALUATE ##
            evaluate = np.loadtxt(f'{self.path_MIE}\\{file}')
            damage_index = evaluate - reference

            with open(f'{self.path_DI}\\{file}', 'w') as output_file:
                for row in damage_index:
                    np.savetxt(output_file, row, newline=' ')
                    output_file.write('\n')
                    
        print("finish calculate DI")

    def scatter_plot(self, type, bottom, top):
        
        path = getattr(self, f'path_{type}')
        os.makedirs(fr'{path}_scatterplot', exist_ok=True)

        if type in ['Minus_MIE', 'Minus_DI', 'Minus_MM']:
            channel = self.channel - 1
            ylabel = f"{type}"
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

    def minus(self, type):

        path = getattr(self, f'path_{type}')
        os.makedirs(f'{path}_Minus', exist_ok=True)
        
        for _, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')
            data_matrix = data.reshape((self.channel, self.scale))
            data_matrix = np.diff(data_matrix, axis=0)
            np.savetxt(f'{path}_Minus\\{file}', data_matrix, fmt='%.6f')
        
        print(f'finish calculate minus - {type}')

   
    def totalplot(self, bottom1, top1, bottom2, top2):
        os.makedirs(fr'{self.path}\\totalplot', exist_ok=True)

        for _, file in enumerate(os.listdir(self.path_MIE)):
            
            fig, ax1 = plt.subplots(figsize=(8, 5), dpi=150)  
            ax2 = ax1.twinx()


            for type in ["DI", "Minus_MIE", "Minus_DI"]:
                if type in ['Minus_MIE', 'Minus_DI']:
                    channel = self.channel - 1
                    x_range = np.arange(1, channel + 1)
                    alpha = 1
                else:
                    channel = self.channel
                    x_range = np.arange(channel)
                    alpha = 0.5
                path = getattr(self, f'path_{type}')
                data = np.loadtxt(f'{path}\\{file}')
                data_matrix = data.reshape((channel, self.scale))
                summed_data = np.sum(data_matrix, axis=1)
                ax1.plot(x_range, summed_data, label=type, alpha = alpha)

            ax1.set_xlabel("Channel", fontsize=7)
            ax1.set_ylabel("summed up", fontsize=7)
            ax1.set_ylim(bottom1, top1)
            ax1.set_yticks(np.arange(bottom1, top1, 2))
            ax1.tick_params(axis='y', labelcolor='tab:blue', labelsize=7)
            ax1.legend(loc='upper left')
            
            # MIE
            path_MIE = getattr(self, 'path_MIE')
            data_MIE = np.loadtxt(f'{path_MIE}\\{file}')
            data_matrix_MIE = data_MIE.reshape((self.channel, self.scale))
            summed_data_MIE = np.sum(data_matrix_MIE, axis=1)
            ax2.bar(np.arange(self.channel), summed_data_MIE, label='MIE', color='#F4A7B9', alpha=0.5)
            ax2.set_ylabel("MIE summed up", fontsize=7)
            ax2.set_ylim(bottom2, top2)
            ax2.tick_params(axis='y', labelcolor='tab:red', labelsize=7)
            ax2.legend(loc='upper right')

            ax1.set_xticks(x_range)
            ax1.set_xticklabels(x_range, fontsize=7)
            ax1.set_title(file, fontsize=10)
            ax1.grid(True, linestyle="--", color='grey', linewidth='0.5', axis='both', alpha=0.5)
            ax2.grid(False)
            plt.savefig(fr'{self.path}\totalplot\{file}.png')
            plt.close()

        print(f'finish totalplot')

    def threeD(self, type, bottom, top):
        
        if type in ['Minus_MIE', 'Minus_DI', 'Minus_MM']:
            channel = self.channel - 1
            channel_range = range(1, channel+1)
        else:
            channel = self.channel
            channel_range = range(channel)

        path = getattr(self, f'path_{type}')
        os.makedirs(fr'{path}_3D', exist_ok=True)
        x, y = np.meshgrid(range(1, self.scale+1), channel_range)

        for _, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')
            data_matrix = data.reshape((channel, self.scale))

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(x, y, data, cmap='viridis')

            fig.colorbar(surf, shrink=0.5, aspect=5)

            ax.view_init(elev=15, azim=145)  # 設置仰角和方位角
            ax.set_zlim(bottom, top) 
            ax.grid(True)
            ax.set_xlabel('scale')
            ax.set_ylabel('channel')
            ax.set_zlabel('Damage Index between floors')
            plt.savefig(f'{path}_3D\\{file}.png')
        
        print(f'finish 3D - {type}')


# for i in range(9,16):
#     TCUBA6 = DataProcessor(f'TCUBA6_交大公教宿舍特定頻道_{i}_3_3', 12, i)
#     TCUBA6.path()
#     TCUBA6.calculate_DI()
#     # TCUBA6.calculate_MinusMean()
#     # TCUBA6.scatter_plot("MIE", 0, 5)
#     # TCUBA6.sum_up("MIE")
#     # TCUBA6.histogram("MIE", -0, 100)
#     TCUBA6.threeD("MIE", 2.5, 5)
#     # TCUBA6.scatter_plot("DI", -3, 3)
#     # TCUBA6.sum_up("DI")
#     # TCUBA6.histogram("DI", -25, 50)
#     TCUBA6.threeD("DI", -2, 2)
#     TCUBA6.minus("DI")
#     # TCUBA6.scatter_plot("Minus", -3, 3)
#     # TCUBA6.sum_up("Minus")
#     # TCUBA6.histogram("Minus", -20, 50)
#     TCUBA6.threeD("Minus", -2, 2)
#     # TCUBA6.scatter_plot("MM", -3, 3)
#     # TCUBA6.sum_up("MM")
#     # TCUBA6.histogram("MM", -25, 10)
#     # TCUBA6.threeD("MM")
#     print(f'交大公教宿舍 finish{i}')

for i in range(2, 21):
    NCREE = DataProcessor(f'七層鋼構架樓層破壞_{i}_3_3', 8, i)
    NCREE.calculate_DI()
    NCREE.minus("MIE") 
    NCREE.minus("DI")  
    NCREE.totalplot(-10, 10, 0, 50)
    NCREE.threeD("MIE", 0, 5)
    NCREE.threeD("DI", -2, 2)
    NCREE.threeD("Minus_MIE", -2, 2)
    NCREE.threeD("Minus_DI", -2, 2)
    
    print(f'七層鋼構架樓層破壞_濾波 finish{i}')

