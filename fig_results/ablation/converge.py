import matplotlib.pyplot as plt
import csv
import pandas as pd
import os



def summary():

    dual_df = pd.read_csv(os.path.join('same_jinan_mixlight.csv'))
    dual_y = dual_df['avg_travel_time'].values.tolist()
    dual_x = [i for i in range(1,len(dual_y)+1)]


    single_df = pd.read_csv(os.path.join('same_jinan_basic.csv'))
    single_y = single_df['avg_travel_time'].values.tolist()
    single_x = [i for i in range(1,len(single_y)+1)]



    plt.plot(dual_x,   dual_y,      color='r',  linewidth=3,  linestyle='-',   label='MixLight')
    plt.plot(single_x, single_y,    color='b',  linewidth=3,  linestyle='--',   label='Basic')


    plt.grid(True)
    plt.axis([0, 200, 290, 450])

    plt.xlabel('episode',fontsize=15)
    plt.ylabel('avg_travel_time',fontsize=15)
    plt.legend(fontsize=15)
    plt.tick_params(labelsize=13)


    fig_title = 'conv_jinan.png'
    plt_title = 'Dataset-jinan'

    plt.title(plt_title,fontsize=18)

    log_dir = os.path.join(fig_title)

    plt.savefig(log_dir)

    print('Finished!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    summary()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
