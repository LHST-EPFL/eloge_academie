import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
from tqdm import tqdm
tqdm.pandas()


def major_topic(topic, ls):
    '''
    This method affects the higher topic corresponding to the topic
    Inputs :
        - topic (int) : topic to affect
        - ls (dict) : dictionnary containing the name of the higher topic and its value is the list of the corresponding topics
    Outpus :
        - (idx, entri[0]) (tuple) : tuple containing the index of the higher topic and its name
    '''
    for idx, entri in enumerate(ls.items()) :
        if topic in entri[1] :
            return topic ,entri[0]
    return -1, 'outlier'

def rmv_sent(df_try):
    '''
    This method only keeps the topic name in column percent
    Input:
        - df_try (DataFrame) : dataframe where we need to only keep the name of topic
    '''
    df_try['0-10'] = df_try['0-10'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['10-20'] = df_try['10-20'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['20-30'] = df_try['20-30'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['30-40'] = df_try['30-40'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['40-50'] = df_try['40-50'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['50-60'] = df_try['50-60'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['60-70'] = df_try['60-70'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['70-80'] = df_try['70-80'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['80-90'] = df_try['80-90'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    df_try['90-100'] = df_try['90-100'].apply(lambda x : [(key[1], val) for key, val in x.items()])
    
    
    
    
def create_dict_perc(df_try):
    '''
    '''
    dic_perc = {'0-10' : {}, '10-20' : {}, '20-30' : {}, '30-40' : {}, '40-50' : {}, '50-60' : {}, '60-70' : {},
           '70-80' : {}, '80-90' : {}, '90-100' : {}}
    for idx, row in tqdm(df_try.iterrows()):
        for name_col in ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']:
            for tupl in row[name_col]:
                if tupl[0] not in dic_perc[name_col].keys():
                    dic_perc[name_col][tupl[0]] = tupl[1]
                else :
                    dic_perc[name_col][tupl[0]] += tupl[1]
    return dic_perc




def divide_by_percent(ls):
    '''
    This method creates a dictionnary that divides each eulogy by percentage of text
    Input :
        - ls (list) :
    Output :
        - dic (dict) : that contains as keys the percents and as values the sentences corresponding
    '''
    dic = {}
    cent = len(ls)
    count_10 = ls[:(int(cent/10) + 1)]
    count_20 = ls[(int(cent/10) + 1): (2*int(cent/10) + 1)]
    count_30 = ls[(2*int(cent/10) + 1): (3*int(cent/10) + 1)]
    count_40 = ls[(3*int(cent/10) + 1): (4*int(cent/10) + 1)]
    count_50 = ls[(4*int(cent/10) + 1): (5*int(cent/10) + 1)]
    count_60 = ls[(5*int(cent/10) + 1): (6*int(cent/10) + 1)]
    count_70 = ls[(6*int(cent/10) + 1): (7*int(cent/10) + 1)]
    count_80 = ls[(7*int(cent/10) + 1): (8*int(cent/10) + 1)]
    count_90 = ls[(8*int(cent/10) + 1): (9*int(cent/10) + 1)]
    count_100 = ls[(9*int(cent/10) + 1):]
    dic['0-10'] = Counter(count_10)
    dic['10-20'] = Counter(count_20)
    dic['20-30'] = Counter(count_30)
    dic['30-40'] = Counter(count_40)
    dic['40-50'] = Counter(count_50)
    dic['50-60'] = Counter(count_60)
    dic['60-70'] = Counter(count_70)
    dic['70-80'] = Counter(count_80)
    dic['80-90'] = Counter(count_90)
    dic['90-100'] = Counter(count_100)
    return dic



def plot_stack_bar(df, name_col = 'Topic_Ordered', date = 1793, color_plot = {'outlier' : 'grey', 'science' : 'red', 'personne' : 'pink', 'societe' : 'orange' ,
             'posterite' : 'purple', 'theorie' : 'black', 'voyage' : 'grey'}, keep_outliers = False, norm = False, norm_by_tot = False):
    
    '''
    This method plots stack bars of proportion of each category of topic by percentage of text
    Inputs :
        - df (DataFrame)
        - name_col (string) :
        - date (int) :
        - color_plot (dict) :
        - keep_outliers (boolean) :
        - norm (boolean) :
        - norm_by_tot (boolean): norms on the y-axis on the category, to see what proportion of this category is used in this 
                                 percentage of text on all the category used
    Outputs :
        - perc (DataFrame) :
        - perc_pre (DataFrame) :
        - perc_post (DataFrame) :
    '''
    
    #Dividing eulogy by percent
    df['Percent'] = df['Topic_Ordered'].apply(lambda x : divide_by_percent(x))
    
    #Dividing dataframes per date
    df_pre = df[df['Annee']<=date]
    df_post = df[df['Annee']> date]
    
    #Creates a dataframe with as columns 0-10, 10-20,...
    df_try = pd.concat([df.drop(['Percent'], axis=1), df['Percent'].apply(pd.Series)], axis=1)
    df_try_pre = pd.concat([df_pre.drop(['Percent'], axis=1), df_pre['Percent'].apply(pd.Series)], axis=1)
    df_try_post = pd.concat([df_post.drop(['Percent'], axis=1), df_post['Percent'].apply(pd.Series)], axis=1)
    
    #Removing the number of the topics
    rmv_sent(df_try)
    rmv_sent(df_try_pre)
    rmv_sent(df_try_post)
    
    dic_perc = create_dict_perc(df_try)
    dic_perc_pre = create_dict_perc(df_try_pre)
    dic_perc_post = create_dict_perc(df_try_post)
    
    
    perc = pd.DataFrame(dic_perc.values())
    perc_pre = pd.DataFrame(dic_perc_pre.values())
    perc_post = pd.DataFrame(dic_perc_post.values())
    
    if norm :
        perc.loc[:,:] = perc.loc[:,:].div(perc.sum(axis=1), axis=0)
        perc_pre.loc[:,:] = perc_pre.loc[:,:].div(perc_pre.sum(axis=1), axis=0)
        perc_post.loc[:,:] = perc_post.loc[:,:].div(perc_post.sum(axis=1), axis=0)
        for col in perc.columns:
            perc[col] = 100*perc[col]
            perc_pre[col] = 100*perc_pre[col]
            perc_post[col] = 100*perc_post[col]
    
    if not keep_outliers :
        perc.pop('outlier')
        perc_pre.pop('outlier')
        perc_post.pop('outlier')
        
             
    if norm_by_tot :
        for col in perc.columns:
            perc[col] = perc[col]/perc[col].sum()
            perc_pre[col] = perc_pre[col]/perc_pre[col].sum()
            perc_post[col] = perc_post[col]/perc_post[col].sum()

    
    perc['Percent'] =['0-10', '10-20','20-30', '30-40','40-50', '50-60','60-70', '70-80',
                                                '80-90', '90-100']   
    perc_pre['Percent'] =['0-10', '10-20','20-30', '30-40','40-50', '50-60','60-70', '70-80',
                                                '80-90', '90-100']
    perc_post['Percent'] =['0-10', '10-20','20-30', '30-40','40-50', '50-60','60-70', '70-80',
                                                '80-90', '90-100']
    
    
        
        
    
    fig, ax = plt.subplots(nrows = 3, figsize = (10, 15))
    perc.plot.bar(x='Percent', stacked=True, title='Proportion of each topic',
             color = color_plot, ax = ax[0])#, xlabel = 'Proportions', ylabel = 'Percentage in the text')
    perc_pre.plot.bar(x='Percent', stacked=True, title='Proportion of each topic pre Revolution',
                 color = color_plot, ax = ax[1])#, xlabel = 'Proportions', ylabel = 'Percentage in the text')
    perc_post.plot.bar(x='Percent', stacked=True, title='Proportion of each topic post Revolution',
                  color=color_plot, ax = ax[2])#, xlabel = 'Proportions', ylabel = 'Percentage in the text')
    
    plt.subplots_adjust(hspace = 0.4)
    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].get_legend().remove()
    ax[1].get_legend().remove()
    ax[2].get_legend().remove()
    fig.legend(handles, labels, bbox_to_anchor=(1.3, 0.5))
    return perc, perc_pre, perc_post


def sent_rep(topic, df_rep, print_ = True, perc=10):
    '''
    This method aims at outputing the most representative sentences of a topic
    Inputs :
        - topic (int) : number of the topic
        - df_rep(DataFrame) : TODO
        - print_ (boolean) : Whether to print the sentences by default to True
        - perc (int) : Number of sentences to output, by default to 10
    Outputs :
        - df_help (DataFrame) : dataframe containing the most reprensentative sentences
    '''
    #Extracting the sentences with the highest probability of being affected to this topic and shuffling them in case
    #more than the perc have the highest percentage of being affected to this topic
    df_help = df_rep[df_rep['Topic']==topic].sample(frac=1).nlargest(n=perc, keep='first', columns = 'Prob')
    if print_:
        for _,row in df_help.iterrows():
            print(row['Eloge'])
            print('\n')
    return df_help