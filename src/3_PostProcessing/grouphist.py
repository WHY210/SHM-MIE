from collections import OrderedDict
import matplotlib.pyplot as plt
import os 
import numpy as np

plt.style.use("ggplot")  # 使用 ggplot 樣式


def plot(path,channel, scale):
    files = os.listdir(path)
    # 設置子圖排列
    fig, axes = plt.subplots(2, 4, figsize=(13, 7), dpi=100)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    
    legend_labels = set()  # 存儲圖例標籤

    end_index = min(len(axes.flat), channel - 8) if channel != 8 else len(axes.flat)

    for i, ax in enumerate(axes.flat[:end_index]):
        for file in files:
            data = np.loadtxt(os.path.join(path, file))
            data_matrix = data.reshape((channel, scale))

            if file.startswith('UD'):
                color = 'cyan'  # 指定的綠色
                alpha = 0.9 # 透明度為 1
                label = 'Undamaged'  # 圖例標籤
                linewidth = 1.1
            else:
                color = 'red'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = 'Damaged'  # 圖例標籤
                linewidth = 0.5
            """
            if file.startswith('1994'):
                color = '#EF5350'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '1994'  # 圖例標籤
            elif file.startswith('1995'):
                color = '#E53935'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '1995'  # 圖例標籤
            elif file.startswith('1996'):
                color = '#C62828'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '1996'  # 圖例標籤
            elif file.startswith('1997'):
                color = '#FFA726'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '1997'  # 圖例標籤
            elif file.startswith('1998'):
                color = '#FB8C00'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '1998'  # 圖例標籤
            elif file.startswith('1999'):
                color = '#EF6C00'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '1999'  # 圖例標籤
            elif file.startswith('2000'):
                color = '#FFEE58'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2000'  # 圖例標籤
            elif file.startswith('2001'):
                color = '#FDD835'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2001'  # 圖例標籤
            elif file.startswith('2002'):
                color = '#FFFF00'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2002'  # 圖例標籤
            elif file.startswith('2003'):
                color = '#9CCC65'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2003'  # 圖例標籤
            elif file.startswith('2004'):
                color = '#7CB342'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2004'  # 圖例標籤
            elif file.startswith('2005'):
                color = '#1B5E20'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2005'  # 圖例標籤            
            elif file.startswith('2006'):
                color = '29B6F6'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2006'  # 圖例標籤
            elif file.startswith('2007'):
                color = '#039BE5'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2007'  # 圖例標籤
            elif file.startswith('2008'):
                color = '#0288D1'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2008'  # 圖例標籤
            elif file.startswith('2009'):
                color = '#3F51B5'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2009'  # 圖例標籤
            elif file.startswith('2010'):
                color = '#3949AB'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2010'  # 圖例標籤
            elif file.startswith('2011'):
                color = '#1A237E'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2011'  # 圖例標籤
            elif file.startswith('2012'):
                color = '#7E57C2'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2012'  # 圖例標籤
            elif file.startswith('2013'):
                color = '#5E35B1'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2013'  # 圖例標籤
            elif file.startswith('2014'):
                color = '#4527A0'  # 指定的紅色
                alpha = 0.9 # 透明度為 0.05
                label = '2014'  # 圖例標籤
            """
            linewidth = 0.2
            ax.plot(np.arange(1, scale+1), data_matrix[i, :], '-o', markersize=0.75, label=label, color=color, alpha=alpha, linewidth=linewidth)

            # 添加圖例標籤到集合中
            legend_labels.add(label)

        ax.grid(True)
        ax.set_xlabel('Scale', fontsize=7)
        ax.set_ylabel('DMIE', fontsize=7)
        ax.set_title(f'channel {i+1}', fontsize=7)
        ax.tick_params(axis='both', which='major', labelsize=7)
        ax.set_ylim(0.9, 4.3)
        

    # 僅顯示兩個圖例標籤
    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(), fontsize=9, loc='lower center', bbox_to_anchor=(0.5, -0.0), ncol=4)
    fig.suptitle('1994~2014', fontsize=10) #Damaged V.S. Undamaged
    # plt.text(0.90, 0.015, 'N= 4000 points (', fontsize=9, ha='right', va='bottom', transform=plt.gcf().transFigure, color='black')
    # plt.text(0.92, 0.015, 'min', fontsize=10, ha='right', va='bottom', transform=plt.gcf().transFigure, color='blue')
    plt.text(0.857, 0.015, 'N= 4000 points (', fontsize=9, ha='right', va='bottom', transform=plt.gcf().transFigure, color='black')
    plt.text(0.9175, 0.015, ' 9601:13600', fontsize=9, ha='right', va='bottom', transform=plt.gcf().transFigure, color='blue')
    plt.text(0.98, 0.015, '), m=3, R=3', fontsize=9, ha='right', va='bottom', transform=plt.gcf().transFigure)
    # plt.savefig(fr'D:\SHM-MIE\plot\UDD.png')
    plt.show()
    print("filninsh UDD")
   
    #plt.tight_layout()
    #plt.show()

    # 分類不同類型的檔案
    categories = {
        "UD": [],
        "1F": [],
        "2F": [],
        "3F": [],
        "4F": [],
        "5F": [],
        "6F": [],
        "7F": [],
        "12F": [],
        "34F": [],
        "56F": [],
        "123F": [],
        "456F": [],
        "1234F": [],
        "4567F": [],
        "AD": [],
    }



    # 逐一處理每個子圖
    # 遍歷所有檔案
    for file in files:
        for category in categories.keys():
            if file.startswith(category):
                categories[category].append(file)
                break


    total_files = 0
    sum_data = np.zeros((channel))
    for r, (category, files_list) in enumerate(categories.items()):
        if category == "UD":
            for j, file in enumerate(files_list):
                data = np.loadtxt(os.path.join(path, file))
                data_matrix = data.reshape((channel, scale))
                summed_data = np.sum(data_matrix, axis=1) 
                sum_data += summed_data
                total_files += 1
            average_data = sum_data / total_files


    # 逐一處理每個子圖
    for newscale in range(1,1+scale):
        fig, axs = plt.subplots(4, 4, figsize=(32, 22), dpi=500)
        c=0
        for r, (category, files_list) in enumerate(categories.items()):
            for j, file in enumerate(files_list):
                data = np.loadtxt(os.path.join(path, file))
                data_matrix = data.reshape((channel, scale))
                data_matrix = data_matrix[:, :newscale]
                #data_matrix = np.diff(data_matrix, axis=0)
                summed_data = np.sum(data_matrix, axis=1) / scale
                #summed_data = np.sum(np.where(data_matrix < 0, data_matrix, 0), axis=1)
                #sum_DI = summed_data - average_data
                #sum_DI = np.diff(sum_DI, axis=0)
                if channel == 8:
                    axs[int(r/4), int(c%4)].set_xticklabels(['0F', '1F', '2F', '3F', '4F', '5F', '6F', '7F'], fontsize=20)
                    axs[int(r/4), int(c%4)].bar(np.arange(1, 1+channel) -0.2 + 0.1 * (j%5), summed_data, width=0.1, label=file)  
                elif channel == 4:
                    #axs[int(r/4), int(c%4)].set_xticklabels(['1F~3F', '3F~5F', '5F~7F'], fontsize=20)  
                    axs[int(r/4), int(c%4)].set_xticklabels(['1F', '3F', '5F', '7F'], fontsize=20) # 
                    axs[int(r/4), int(c%4)].bar(np.arange(1, 1+channel) -0.2 + 0.1 * (j%5), summed_data, width=0.1, label=file)  
                else:
                    axs[int(r/4), int(c%4)].set_xticklabels(['1F', '2F', '3F', '4F', '5F', '6F', '7F'], fontsize=20)
                    axs[int(r/4), int(c%4)].bar(np.arange(0.5, 0.5+channel) -0.2 + 0.1 * (j%5), summed_data, width=0.1, label=file)  
                axs[int(r/4), int(c%4)].grid(True)
                axs[int(r/4), int(c%4)].tick_params(axis='both', which='major', labelsize=15)
                axs[int(r/4), int(c%4)].set_ylim(-0.25, 0.25)
                axs[int(r/4), int(c%4)].set_title(f'{category}', fontsize=23)
                #axs[int(r/4), int(c%4)].set_xlabel('Channel', fontsize=20)
                axs[int(r/4), int(c%4)].set_ylabel('DDI', fontsize=20) #
                axs[int(r/4), int(c%4)].set_xticks(np.arange(1, channel+1)) #, fontsize=20)
            c+=1
        fig.suptitle(f'DDI (scale = 1 ~ {newscale})', fontsize=28) #
        #plt.text(0.97, 0.04, 'N= 4000 points (9601:13600), m=3, R=3', fontsize=22, ha='right', va='bottom', transform=plt.gcf().transFigure)
        plt.text(0.90, 0.04, 'N= 4000 points (', fontsize=22, ha='right', va='bottom', transform=plt.gcf().transFigure, color='black')
        plt.text(0.92, 0.04, ' min', fontsize=24, ha='right', va='bottom', transform=plt.gcf().transFigure, color='blue')
        plt.text(0.98, 0.04, '), m=3, R=3', fontsize=22, ha='right', va='bottom', transform=plt.gcf().transFigure)
        plt.savefig(fr'.\result\min微振段_七層鋼構架樓層破壞_30_3_3\plot\DDI_{newscale}.png') #
        print(f'scale {newscale}')

        

# 載入資料
        
path = r".\result\min微振段_七層鋼構架樓層破壞_30_3_3\DI_Minus_floor1th_scale0th"

plot(path,7,30)