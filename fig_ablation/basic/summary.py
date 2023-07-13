import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot
# plt.style.use('seaborn-')
palette = pyplot.get_cmap('Set1')

fort_size = 40

font_dict = {#'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 40,
             }

lengd_font_dict = {#'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 36,
             }






def summary(folder,mix,y):

    if folder == '3x4':
        city = 'jinan'
    elif folder == '4x4':
        city ='Hangzhou'
    elif folder == '6x6_1':
        city ='syn_1'
    elif folder == '6x6_2':
        city ='syn_2'
    elif folder == '6x6_3':
        city ='syn_3'
    elif folder == '6x6_4':
        city ='syn_4'
    elif folder == '6x6_5':
        city ='syn_5'
    elif folder == '6x6_6':
        city ='syn_6'
    elif folder == '6x6_7':
        city ='syn_7'
    elif folder == '6x6_8':
        city ='syn_8'
    elif folder == '16x3':
        city ='newyork'
    else:
        raise Exception ('Wrong City')


    if mix:
        mix = 'mix'
    else:
        mix = 'same'


    label_list = ['MixLight', 'Basic', ]
    final_result = pd.DataFrame(columns=['average','std'], index=label_list)

    result_list = []


    # method_data = []
    # for suffix in ['_200.csv', '_1234.csv', '_5678.csv']:
    #     file = mix + '_' + 'mixlight' + '_' + city + suffix
    #     df = pd.read_csv(os.path.join(folder, file), header= 0)
    #     result = df['avg_travel_time'].values[:100]
    #
    #     assert len(result) == 100, [file, 'Wrong length']
    #
    #     method_data.append(result)
    # result_list.append(method_data)



    method_list = ['mixlight','basic']

    for method in method_list:
        method_data = []
        for suffix in ['_200.csv','_1234.csv','_5678.csv']:
            file = mix + '_' + method   + '_'  + city + suffix
            df = pd.read_csv(os.path.join(folder, file), header= 0)
            result = df['avg_travel_time'].values[:100]
            method_data.append(result)

            assert len(result) == 100, [file, 'Wrong length']
            #print(file, len(result))
        result_list.append(method_data)
        #print(method, 'done!')


    #print('mixlight', 'done!')
    #print(len(result_list))




    fig = plt.figure(figsize=(10, 6))
    iters = list(range(1,101))


    ax = fig.add_subplot(1, 1, 1)
    for index, result in enumerate(result_list):
        color = palette(index)  # 算法1颜色
        avg = np.mean(result, axis=0)
        std = np.std(result, axis=0)
        r1 = list(map(lambda x: x[0] - x[1], zip(avg, std)))  # 上方差
        r2 = list(map(lambda x: x[0] + x[1], zip(avg, std)))  # 下方差
        ax.plot(iters, avg, color=color, label=label_list[index], linewidth=3.0)
        ax.fill_between(iters, r1, r2, color=color, alpha=0.2)
        final_avg = np.mean(avg[-5:])
        final_std = np.mean(std[-5:])
        final_result.loc[label_list[index]] = [final_avg, final_std]


    ax.legend(loc=1, prop=lengd_font_dict)
    ax.set_xlabel('episode', fontdict=font_dict)
    ax.set_ylabel('avg travel time', fontdict=font_dict)
    # ax.set_yticks([0, 500, 1000, 1500, 2000])
    plt.ylim(y[0], y[1])
    plt.xlim(0, 100)

    plt.tick_params(labelsize=fort_size/2)
    # labels = ax.get_xticklabels() + ax.get_yticklabels()
    # [label.set_fontname('Times New Roman') for label in labels]
    # [label.set_fontstyle('italic') for label in labels]

    plt.grid(visible=True, which='major', axis='both', linewidth=2, linestyle='-',color = 'k', alpha = 0.2)




    if mix == 'mix':
        fig_title = 'fig_mix_env_'+ city + '.png'

    else:
        fig_title = 'fig_same_env_' + city + '.png'



    if city == 'jinan':
        plt_title = 'Jinan'
    elif city == 'Hangzhou':
        plt_title = 'Hangzhou'
    else:
        plt_title ='none'



    plt.title(plt_title, fontdict=font_dict,loc='center')
    print(plt_title)
    plt.subplots_adjust(bottom=0.2,left=0.15)
    plt.tight_layout()
    plt.show()

    log_dir = os.path.join(fig_title)
    fig.savefig(log_dir)
    final_result.to_csv(os.path.join(plt_title + '.csv'))




if __name__ == '__main__':

    import matplotlib.font_manager as mfm

    font_path = "times.ttf"
    prop = mfm.FontProperties(fname=font_path)

    folder_list = ['3x4','4x4',]
    y_list = [[250, 900], [250, 750]]

    mix = False


    for index in range(len(folder_list)):
        summary(folder_list[index],mix = mix, y = y_list[index])


    print('All Finished!')

