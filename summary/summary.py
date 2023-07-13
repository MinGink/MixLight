import matplotlib.pyplot as plt
import csv
import pandas as pd
import os



def summary(folder,mix):

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

    single =    mix + '_' + 'basic'     + '_' + city + '_200.csv'
    colight =   mix + '_' + 'colight'   +'_'  + city + '_159.csv'
    frap =      mix + '_' + 'frap'      + '_' + city + '_200.csv'
    mixlight =  mix + '_' + 'mixlight'  + '_' + city + '_200.csv'
    mplight =   mix + '_' + 'mplight'   + '_' + city + '_200.csv'





    colight_df = pd.read_csv(os.path.join(folder,colight), header= None, names=['episode', 'time','NAN'])
    colight_y = colight_df['time'].values.tolist()
    colight_x = [i for i in range(1,len(colight_y)+1)]

    frap_df = pd.read_csv(os.path.join(folder,frap), header= None, names=['episode', 'time','NAN'])
    frap_y = frap_df['time'].values.tolist()
    frap_x = [i for i in range(1,len(frap_y)+1)]

    mplight_df = pd.read_csv(os.path.join(folder,mplight), header= None, names=['episode', 'time','NAN'])
    mplight_y = mplight_df['time'].values.tolist()
    mplight_x = [i for i in range(1,len(mplight_y)+1)]

    mixlight_df = pd.read_csv(os.path.join(folder,mixlight))#header= None, names=['episode','time','total','complete','ratio','stops'])
    mixlight_y = mixlight_df['avg_travel_time'].values.tolist()
    mixlight_x = [i for i in range(1,len(mixlight_y)+1)]


    single_df = pd.read_csv(os.path.join(folder,single))#header= None, names=['episode','time','total','complete','ratio','stops'])
    single_y = single_df['avg_travel_time'].values.tolist()
    single_x = [i for i in range(1,len(single_y)+1)]



    plt.plot(colight_x, colight_y,    color='C1', linewidth=1.5, linestyle='--',   label='CoLight')
    plt.plot(frap_x, frap_y,          color='b',  linewidth=1.5,  linestyle='-',   label='FRAP')
    plt.plot(mplight_x, mplight_y,    color='c',  linewidth=1.5,  linestyle='--',    label='MPLight')
    plt.plot(mixlight_x, mixlight_y,  color='r',  linewidth=1.5,  linestyle='-',    label='MixLight')
    plt.plot(single_x, single_y,      color='g',  linewidth=1.5,  linestyle='--',label='Baisc')

    plt.grid(True)
    plt.axis([0, 100, 1000, 1500])

    plt.xlabel('episode')
    plt.ylabel('avg_travel_time')
    plt.legend()

    if mix == 'mix':
        fig_title = 'fig_mix_env_'+ city + '.png'
        plt_title = 'Mixed type agent environment -' + city
    else:
        fig_title = 'fig_same_env_' + city + '.png'
        plt_title = 'Single type agent environment -' + city

    plt.title(plt_title)

    log_dir = os.path.join(fig_title)

    plt.savefig(log_dir)

    print('Finished!')


if __name__ == '__main__':

    folder = '16x3'
    mix = True

    summary(folder,mix)

