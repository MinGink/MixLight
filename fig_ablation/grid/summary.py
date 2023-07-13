import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot
# plt.style.use('seaborn-')
palette = pyplot.get_cmap('Set1')

fort_size = 80

font_dict = {#'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 80,
             }

lengd_font_dict = {#'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : int(56),
             }






def summary(folder,mix,y):


    if folder == '4x5_2':
        city ='452'
    elif folder == '5x5_1':
        city = '551'
    else:
        raise Exception ('Wrong City')


    if mix:
        mix = 'mix'
    else:
        mix = 'same'


    label_list = ['MixLight', 'CoLight', 'FRAP', 'MpLight', ]
    final_result = pd.DataFrame(columns=['average','std'], index=label_list)

    result_list = []


    method_data = []
    for suffix in ['_1234.csv', '_5678.csv']:
        file = mix + '_' + 'mixlight' + '_' + city + suffix
        df = pd.read_csv(os.path.join(folder, file), header= 0)
        result = df['avg_travel_time'].values[:100]

        assert len(result) == 100, [file, 'Wrong length']

        method_data.append(result)
    result_list.append(method_data)



    method_list = ['colight', 'frap', 'mplight']

    for method in method_list:
        method_data = []
        for suffix in ['_1234.csv','_5678.csv']:
            file = mix + '_' + method   + '_'  + city + suffix
            df = pd.read_csv(os.path.join(folder, file), names=['episode', method,'nan'])
            result = df[method].values[:100]
            method_data.append(result)

            assert len(result) == 100, [file, 'Wrong length']
            #print(file, len(result))
        result_list.append(method_data)
        #print(method, 'done!')


    #print('mixlight', 'done!')
    #print(len(result_list))




    fig = plt.figure(figsize=(20, 15))
    iters = list(range(1,101))


    ax = fig.add_subplot(1, 1, 1)
    for index, method_list in enumerate(result_list):
        color = palette(index)  # 算法1颜色
        avg = np.mean(method_list, axis=0)
        std = np.std(method_list, axis=0)
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
        plt_title = 'mixed-type agent environment - ' + city
    else:
        fig_title = 'fig_same_env_' + city + '.png'
        plt_title = 'single-type agent environment - ' + city



    #plt.title(plt_title, fontdict=font_dict, pad=50,loc='center')
    print(plt_title)
    plt.subplots_adjust(bottom=0.2,left=0.15)
    plt.show()


    log_dir = os.path.join(fig_title)
    fig.savefig(log_dir)
    final_result.to_csv(os.path.join(plt_title + '.csv'))




if __name__ == '__main__':

    import matplotlib.font_manager as mfm

    font_path = "times.ttf"
    prop = mfm.FontProperties(fname=font_path)

    folder_list = ['4x5_2','5x5_1']
    same_y_list = [[100, 1500], [250, 1200]]
    mix_y_list = [[200, 1200], [250, 1000]]
    mix_list = [True, False]




    # index = 10
    # summary(folder_list[index], mix=mix, y=y_list[index])


    for mix in mix_list:
        if mix == False:
            y_list = same_y_list
        else:
            y_list = mix_y_list
        for index in range(len(folder_list)):
            summary(folder_list[index],mix = mix, y = y_list[index])


    print('All Finished!')

