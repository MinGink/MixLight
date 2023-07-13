import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot
palette = pyplot.get_cmap('Set1')

fort_size = 40

font_dict = {#'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 16,
             }

lengd_font_dict = {#'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 12,
             }


def summary(file_name):

    df = pd.read_csv(file_name, header= 0)
    new_df = pd.DataFrame(columns=['time','weight','traffic'])


    for i in range(len(df)):
        time = df['time'][i]
        weight_list = [df['action_1'][i],df['action_2'][i],df['action_3'][i],df['action_4'][i]]
        weight_max = max(weight_list)
        traffic_list = [df['state_1'][i],df['state_2'][i],df['state_3'][i],df['state_4'][i]]
        traffic = traffic_list.index(max(traffic_list))
        if weight_list[traffic] == weight_max or weight_list[traffic] == 2 or weight_list[traffic] == 1:
            weight = traffic
        else:
            weight = weight_list.index(weight_max)


        new_df.loc[i] = [time, weight, traffic]

    #print(new_df)




    fig = plt.figure(figsize=(24, 14))
    file_title = file_name.split('\\')[-1].split('.')[0]
    plt.title(file_title, font_dict)
    ax1 = fig.add_subplot(211)
    plt.scatter(new_df['time'], new_df['traffic'], s=80, color='b', marker='.', label='traffic', alpha=1.0)
    plt.legend(loc = 'upper right',  prop=lengd_font_dict, markerscale=3)
    #plt.xlabel('time', font_dict)
    plt.ylabel('weight', font_dict)
    plt.tick_params(labelsize=40, width=16)
    plt.xticks([])
    #plt.xlim(0, 3600)



    ax2 = fig.add_subplot(212)
    plt.scatter(new_df['time'], new_df['weight'], s=80,color='r', marker='.', label='weight',alpha=1.0)
    plt.legend(loc = 'upper right',  prop=lengd_font_dict, markerscale=3)
    plt.xlabel('time', font_dict)
    plt.ylabel('direction', font_dict)
    plt.tick_params(labelsize=40, width=16)
    plt.xlim(0, 3600)
    plt.yticks([0, 1, 2, 3, ], [ r'$S$', r'$E$', r'$N$', r'$W$',])




    plt.tight_layout()
    plt.savefig(file_name.split('.')[0] + '.png',bbox_inches='tight', pad_inches=0.05)
    plt.show()
    plt.close()


def final():


    df_0 = pd.read_csv('Hangzhou/inter_0.csv', header= 0)
    df_13 = pd.read_csv('Hangzhou/inter_13.csv', header= 0)

    new_df_0 = pd.DataFrame(columns=['time','weight','traffic'])
    new_df_13 = pd.DataFrame(columns=['time','weight','traffic'])


    for i in range(len(df_0)):
        time = df_0['time'][i]
        weight_list = [df_0['action_1'][i],df_0['action_2'][i],df_0['action_3'][i],df_0['action_4'][i]]
        weight_max = max(weight_list)
        traffic_list = [df_0['state_1'][i],df_0['state_2'][i],df_0['state_3'][i],df_0['state_4'][i]]
        traffic = traffic_list.index(max(traffic_list))
        if weight_list[traffic] == weight_max or weight_list[traffic] == 2 or weight_list[traffic] == 1:
            weight = traffic
        else:
            weight = weight_list.index(weight_max)


        new_df_0.loc[i] = [time, weight, traffic]

    for i in range(len(df_13)):
        time = df_13['time'][i]
        weight_list = [df_13['action_1'][i],df_13['action_2'][i],df_13['action_3'][i],df_13['action_4'][i]]
        weight_max = max(weight_list)
        traffic_list = [df_13['state_1'][i],df_13['state_2'][i],df_13['state_3'][i],df_13['state_4'][i]]
        traffic = traffic_list.index(max(traffic_list))
        if weight_list[traffic] == weight_max or weight_list[traffic] == 2 or weight_list[traffic] == 1:
            weight = traffic
        else:
            weight = weight_list.index(weight_max)

        new_df_13.loc[i] = [time, weight, traffic]




    x = new_df_0['time']
    y1 = new_df_0['weight']
    y2 = new_df_13['weight']
    y3 = new_df_0['traffic']
    y4 = new_df_13['traffic']

    fig, axs = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(8, 3))


    axs[0, 0].scatter(x, y1,s=1,color='r', marker='.', label='weight',alpha=1.0)
    axs[0, 0].set_xlim(0, 3600)
    axs[0, 0].set_xticks([0, 1800, 3600])
    axs[0, 0].set_ylim(-0.5, 3.5)
    axs[0, 0].set_yticks([0, 1, 2, 3, ])
    axs[0, 0].set_yticklabels([ r'$S$', r'$E$', r'$N$', r'$W$',])
    axs[0, 0].set_ylabel('weight', font_dict)
    axs[0, 0].set_title('Hangzhou intersection 0', font_dict)
    #axs[0, 0].legend(loc = 'upper right',  prop=lengd_font_dict, markerscale=3)

    axs[0, 1].scatter(x, y2, s=1,color='r', marker='.', label='weight',alpha=1.0)
    axs[0, 1].set_xlim(0, 3600)
    axs[0, 1].set_xticks([0, 1800, 3600])
    axs[0, 1].set_ylim(-0.5, 3.5)
    axs[0, 1].set_yticks([0, 1, 2, 3, ])
    axs[0, 1].set_yticklabels(['S', 'E', 'N', 'W'])
    axs[0, 1].set_title('Hangzhou intersection 13', font_dict)

    axs[1, 0].scatter(x, y3, s=1, color='b', marker='.', label='traffic', alpha=1.0)
    axs[1, 0].set_xlim(0, 3600)
    axs[1, 0].set_xticks([0, 1800, 3600])
    axs[1, 0].set_ylim(-0.5, 3.5)
    axs[1, 0].set_yticks([0, 1, 2, 3, ])
    axs[1, 0].set_yticklabels(['S', 'E', 'N', 'W'])
    axs[1, 0].set_ylabel('traffic', font_dict)
    axs[1, 0].set_xlabel('time', font_dict)

    axs[1, 1].scatter(x, y4, s=1, color='b', marker='.', label='traffic', alpha=1.0)
    axs[1, 1].set_xlim(0, 3600)
    axs[1, 1].set_xticks([0, 1800, 3600])
    axs[1, 1].set_ylim(-0.5, 3.5)
    axs[1, 1].set_yticks([0, 1, 2, 3, ])
    axs[1, 1].set_yticklabels(['S', 'E', 'N', 'W'])
    axs[1, 1].set_xlabel('time', font_dict)


    plt.tight_layout()
    plt.savefig('weight_traffic.png', bbox_inches='tight', dpi=300)
    plt.show()
    print('done')



if __name__ == '__main__':

    import matplotlib.font_manager as mfm

    font_path = "times.ttf"
    prop = mfm.FontProperties(fname=font_path)
    # data_dir = 'Hangzhou/'
    #
    # #file_list = os.listdir(data_dir)
    # file_list = ['inter_0.csv','inter_13.csv']
    #
    # for file in file_list:
    #     #test = data_dir+file
    #     try:
    #         summary(data_dir+file)
    #     except:
    #          print(file)

    final()




