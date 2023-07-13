import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot
palette = pyplot.get_cmap('Set1')

fort_size = 45

font_dict = {#'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 45,
             }

lengd_font_dict = {#'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : int(45),
             }


def summary(data_list):




    #print(new_df)


    plt.figure(figsize=(15, 10))
    # ax1 = fig.add_subplot(111)



    plt.plot(data_list[0]['episode'], data_list[0]['avg_travel_time'],label='10s', color=palette(1), linewidth=8, linestyle='--',)
    plt.plot(data_list[1]['episode'], data_list[1]['avg_travel_time'],label='30s', color=palette(0), linewidth=8, linestyle='-',)
    plt.plot(data_list[2]['episode'], data_list[2]['avg_travel_time'],label='50s', color=palette(2), linewidth=8, linestyle='--',)
    # plt.plot(df['time'], new_df['weight'], label='weight', color=palette(0), linewidth=8, linestyle='-',)
    # plt.plot(df['time'], new_df['traffic'], label='traffic', color=palette(1), linewidth=8, linestyle='--')
    plt.legend(loc='upper right', prop=lengd_font_dict)
    plt.xlabel('episode', font_dict)
    plt.ylabel('avg travel time', font_dict)
    plt.tick_params(labelsize=fort_size, width=16)
    plt.xlim(0, 50)
    plt.ylim(300, 600)
    plt.grid()
    # file_title = file_name.split('\\')[-1].split('.')[0]
    plt.title('Dataset- Jinan', font_dict)


    plt.tight_layout()
    plt.savefig('interval.png')
    plt.show()




if __name__ == '__main__':

    import matplotlib.font_manager as mfm

    font_path = "times.ttf"
    prop = mfm.FontProperties(fname=font_path)
    data_dir = 'jinan/'




    file_list = ['10.csv', '30.csv',  '50.csv']


    data_list = []
    for file in file_list:
        df = pd.read_csv(data_dir + file, header= 0)
        data_list.append(df)


    summary(data_list)

    print('done')