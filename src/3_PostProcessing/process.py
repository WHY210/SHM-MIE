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
        self.path_MIE =  f'..\\result\\{building_type}\\MIE'
        self.path_DI =  f'..\\result\\{building_type}\\DI'
        self.path_mean = f'..\\result\\{building_type}\\MM'
        self.channel = channel
        self.scale = scale

    def path(self):
        os.makedirs(f'..\\result\\{self.building_type}\\MIE', exist_ok=True)
        os.makedirs(f'..\\result\\{self.building_type}\\DI', exist_ok=True)
        os.makedirs(f'..\\result\\{self.building_type}\\MM', exist_ok=True)
        print("finish path")

    def calculate_MinusMean(self):
        os.makedirs(fr'{self.path_mean}', exist_ok=True)

        ## MEAN ##
        average_matrix = np.zeros((self.channel, self.scale))
        for i, file in enumerate(os.listdir(self.path_MIE)):
            matrix = np.loadtxt(f'{self.path_MIE}\\{file}')
            average_matrix += matrix
        average_matrix /= (i+1)
        np.savetxt(fr'{self.path_mean}\MEAN.txt', average_matrix, fmt='%f', delimiter=' ')

        ## MINUS ##
        for i, file in enumerate(os.listdir(self.path_MIE)):
            matrix = np.loadtxt(f'{self.path_MIE}\\{file}')
            matrix -= average_matrix
            np.savetxt(fr'{self.path_mean}\MinusMean_{file}', matrix, fmt='%f', delimiter=' ')
        print("finish calculate MinusMean")

    def calculate_DI(self):
        os.makedirs(fr'{self.path_DI}', exist_ok=True)


        for i, file in enumerate(os.listdir(self.path_MIE)):
              
            ## REFERENCE ##
            if "七層鋼構架樓層破壞" in self.building_type:

                UD001 = np.loadtxt(self.path_MIE + r'.\Mie_UD001.txt')
                UD01 = np.loadtxt(self.path_MIE + r'.\Mie_UD01.txt')
                UD002 = np.loadtxt(self.path_MIE + r'.\Mie_UD002.txt')
                UD02 = np.loadtxt(self.path_MIE + r'.\Mie_UD02.txt')
                UD003 = np.loadtxt(self.path_MIE + r'.\Mie_UD003.txt')
                UD03 = np.loadtxt(self.path_MIE + r'.\Mie_UD03.txt')
                UD04 = np.loadtxt(self.path_MIE + r'.\Mie_UD04.txt')

                reference = (UD001 + UD01 + UD002 + UD02 + UD003 + UD03 + UD04) / 7

            elif "TCUBA6_交大公教宿舍" in self.building_type:
                reference = (np.loadtxt(f'{self.path_MIE}\\Mie_1994060600.txt'))

            ## EVALUATE ##
            evaluate = np.loadtxt(f'{self.path_MIE}\\{file}')
            damage_index = evaluate - reference

            with open(f'{self.path_DI}\\DI_{file}', 'w') as output_file:
                for row in damage_index:
                    np.savetxt(output_file, row, newline=' ')
                    output_file.write('\n')
                    
        print("finish calculate DI")

    def scatter_plot(self, type, bottom, top):
        
         
        if type == "MIE":
            path = self.path_MIE
            os.makedirs(fr'{path}_scatterplot', exist_ok=True)
            ylabel = "MIE (haven't summed up)"
            channel = self.channel
        elif type == "DI":
            path = self.path_DI
            os.makedirs(fr'{path}_scatterplot', exist_ok=True)
            ylabel = "DI (haven't summed up)"
            channel = self.channel
        elif type == "Mean":
            path = self.path_mean
            os.makedirs(fr'{path}_scatterplot', exist_ok=True)
            ylabel = "Minus mean (haven't summed up)"
            channel = self.channel
        elif type == "Minus":
            path = self.path_minus
            os.makedirs(fr'{path}_scatterplot', exist_ok=True)
            ylabel = "Minus (haven't summed up)"
            channel = self.channel - 1

        for i, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')
        
            # 將數據變形為與網格相對應的矩陣
            data_matrix = data.reshape((channel, self.scale))

            plt.figure(figsize=(8, 4), dpi=150)

            for i in range(1, channel+1):
                plt.plot(np.arange(1, self.scale + 1), data_matrix[i - 1, :], label=f"{i}", marker='o', markersize='3')

            # 設置標籤
            plt.xlabel("Scale", fontsize=8)
            plt.xticks(range(1, self.scale+1), fontsize=7)
            plt.ylabel(ylabel, fontsize=8)
            plt.yticks(fontsize=7)
            plt.ylim(bottom, top)
            plt.title(file, fontsize=10)
            plt.legend(loc='upper right', fontsize=6)
            plt.grid("MIE", linestyle = "--",color = 'grey' ,linewidth = '0.3',axis='both', alpha=0.5)

            # 保存圖片
            plt.savefig(f'{path}_scatterplot\\{file}.png')
            #plt.show()
        print(f'finish scatter - {type}')

    def sum_up(self, type):
         
        if type == "MIE":
            path = self.path_MIE
            os.makedirs(fr'{self.path_MIE}_SummedUp', exist_ok=True)
            channel = self.channel
        elif type == "DI":
            path = self.path_DI
            os.makedirs(fr'{self.path_DI}_SummedUp', exist_ok=True)
            channel = self.channel
        elif type == "Mean":
            path = self.path_mean
            os.makedirs(fr'{self.path_mean}_SummedUp', exist_ok=True)
            channel = self.channel
        elif type == "Minus":
            path = self.path_minus
            os.makedirs(fr'{self.path_minus}_SummedUp', exist_ok=True)
            channel = self.channel - 1

        for i, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')

            # 將數據變形為與網格相對應的矩陣
            data_matrix = data.reshape((channel, self.scale))

            # 將相同scale的數據相加
            summed_data = np.sum(data_matrix, axis=1)

            # 將相加後的數據保存為txt檔
            np.savetxt(f'{path}_SummedUp\\{file}', summed_data)
        
        print(f'finish sum up - {type}')

    def minus(self, type):
         
        if type == "MIE":
            path = self.path_MIE
            os.makedirs(fr'{path}_minus', exist_ok=True)
        elif type == "DI":
            path = self.path_DI
            os.makedirs(fr'{path}_minus', exist_ok=True)
        elif type == "Mean":
            path = self.path_mean
            os.makedirs(fr'{path}_minus', exist_ok=True)

        self.path_minus = f'{path}_minus'

        for i, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')

            # 將數據變形為與網格相對應的矩陣
            data_matrix = data.reshape((self.channel, self.scale))

            # 後一個channel減前一個channel
            data_matrix = np.diff(data_matrix, axis=0)

            # 將相加後的數據保存為txt檔
            np.savetxt(f'{path}_minus\\{file}', data_matrix)
        
        print(f'finish calculate minus - {type}')

    def histogram(self, type, bottom, top):
        
        if type == "MIE":
            path = self.path_MIE
            os.makedirs(fr'{path}_histogram', exist_ok=True)
            ylabel = "MIE (summed up)"
            channel = self.channel
        elif type == "DI":
            path = self.path_DI
            os.makedirs(fr'{path}_histogram', exist_ok=True)
            ylabel = "DI (summed up)"
            channel = self.channel
        elif type == "Mean":
            path = self.path_mean
            os.makedirs(fr'{path}_histogram', exist_ok=True)
            ylabel = "Minus mean (summed up)"
            channel = self.channel
        elif type == "Minus":
            path = self.path_minus
            os.makedirs(fr'{path}_histogram', exist_ok=True)
            ylabel = "Minus (summed up)"
            channel = self.channel - 1

        for i, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')

            # 將數據變形為與網格相對應的矩陣
            data_matrix = data.reshape((channel, self.scale))

            # 將相同scale的數據相加
            summed_data = np.sum(data_matrix, axis=1)

            plt.figure(figsize=(8, 4), dpi=150)

            # 繪製直方圖
            plt.bar(range(1, channel + 1), summed_data, alpha=0.7, align='center')

            # 設置標籤
            plt.xlabel("Channel", fontsize=8)
            plt.xticks(range(1, channel + 1), fontsize=7)
            plt.ylabel(ylabel, fontsize=8)
            plt.yticks(fontsize=7)
            plt.ylim(bottom, top)
            plt.title(file, fontsize=10)
            plt.grid("MIE", linestyle="--", color='grey', linewidth='0.5', axis='both', alpha=0.5)

            # 保存圖片
            plt.savefig(f'{path}_histogram\\{file}.png')
            #plt.show()

        print(f'finish histogram - {type}')

    def threeD(self, type, bottom, top):
        
        if type == "MIE":
            path = self.path_MIE
            os.makedirs(fr'{path}_3D', exist_ok=True)
            channel = self.channel
            channel_range = range(channel)
        elif type == "DI":
            path = self.path_DI
            os.makedirs(fr'{path}_3D', exist_ok=True)
            channel = self.channel
            channel_range = range(channel)
        elif type == "Mean":
            path = self.path_mean
            os.makedirs(fr'{path}_3D', exist_ok=True)
            channel = self.channel
            channel_range = range(channel)
        elif type == "Minus":
            path = self.path_minus
            os.makedirs(fr'{path}_3D', exist_ok=True)
            channel = self.channel - 1
            channel_range = range(1, channel+1)

        # 創建一個meshgrid
        x, y = np.meshgrid(range(1, self.scale+1), channel_range)

        for i, file in enumerate(os.listdir(path)):

            data = np.loadtxt(f'{path}\\{file}')

            # 將數據變形為與網格相對應的矩陣
            data_matrix = data.reshape((channel, self.scale))

        

            # 繪製3D圖
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(x, y, data, cmap='viridis')

            # 加入顏色條
            fig.colorbar(surf, shrink=0.5, aspect=5)

            ax.view_init(elev=15, azim=145)  # 設置仰角和方位角
            ax.set_zlim(bottom, top) 
            ax.grid(True)

            # 設置軸標籤
            ax.set_xlabel('scale')
            ax.set_ylabel('channel')
            ax.set_zlabel('Damage Index between floors')

            # 保存圖片
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
#     # TCUBA6.scatter_plot("Mean", -3, 3)
#     # TCUBA6.sum_up("Mean")
#     # TCUBA6.histogram("Mean", -25, 10)
#     # TCUBA6.threeD("Mean")
#     print(f'交大公教宿舍 finish{i}')

for i in range(2,3):
    NCREE = DataProcessor(f'七層鋼構架樓層破壞_{i}_3_3', 8, i)
    # NCREE.path()
    # NCREE.calculate_DI()
    # NCREE.calculate_MinusMean()
     
    # NCREE.scatter_plot("MIE", -5, 5)
    # NCREE.scatter_plot("DI", -3, 3)
    # NCREE.scatter_plot("Mean", -3, 3)
    # NCREE.scatter_plot("Minus", -3, 3)
    # NCREE.sum_up("MIE")
    # NCREE.sum_up("DI")
    # NCREE.sum_up("Mean")
    # NCREE.sum_up("Minus")
    # NCREE.histogram("MIE", -0, 100)
    # NCREE.histogram("DI", -25, 50)
    # NCREE.histogram("Mean", -25, 10)
    # NCREE.histogram("Minus", -20, 50)
    NCREE.minus("DI")  
    NCREE.threeD("MIE", 2.5, 5)
    NCREE.threeD("DI", -2, 2)
    NCREE.threeD("Minus", -2, 2)
    NCREE.threeD("Mean", -2, 2)
    
    
    
    
    print(f'七層鋼構架樓層破壞 finish{i}')

