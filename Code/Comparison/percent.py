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
    This method creates a dictionnary with the topics contained in each part of the text and returns it
    Input:
        - df_try (DataFrame) : dataframe to split into part of text
    Output:
        - dic_perc (dict) : dictionnary containing as keys the part of text, and as values the number of mentions of each topic
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



def plot_stack_bar(df, name_col = 'Topic_Ordered', date = 1793, color_plot = {'outlier' : 'grey', 'Sciences' : 'red', 'Personne' : 'pink', 'Société' : 'orange' ,
             'Postérité' : 'purple', 'Méthode' : 'black', 'Voyage' : 'grey'}, keep_outliers = False, norm = False, norm_by_tot = False):
    
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
    title="Nombre de mentions des topics par partie du texte"
    
    if norm :
        perc.loc[:,:] = perc.loc[:,:].div(perc.sum(axis=1), axis=0)
        perc_pre.loc[:,:] = perc_pre.loc[:,:].div(perc_pre.sum(axis=1), axis=0)
        perc_post.loc[:,:] = perc_post.loc[:,:].div(perc_post.sum(axis=1), axis=0)
        title="Proportion de chaque topic par rapport à tous les topics utilisés dans cette partie"
        for col in perc.columns:
            perc[col] = 100*perc[col]
            perc_pre[col] = 100*perc_pre[col]
            perc_post[col] = 100*perc_post[col]
    
    if not keep_outliers :
        perc.pop('outlier')
        perc_pre.pop('outlier')
        perc_post.pop('outlier')
        
             
    if norm_by_tot :
        title = "Proportion de chaque topic dans chaque partie par rapport à l'utilisation totale de ce topic"
        for col in perc.columns:
            perc[col] = perc[col]/perc[col].sum()
            perc_pre[col] = perc_pre[col]/perc_pre[col].sum()
            perc_post[col] = perc_post[col]/perc_post[col].sum()
            perc[col] = 100*perc[col]
            perc_pre[col] = 100*perc_pre[col]
            perc_post[col] = 100*perc_post[col]

    
    perc['Percent'] =['0-10', '10-20','20-30', '30-40','40-50', '50-60','60-70', '70-80',
                                                '80-90', '90-100']   
    perc_pre['Percent'] =['0-10', '10-20','20-30', '30-40','40-50', '50-60','60-70', '70-80',
                                                '80-90', '90-100']
    perc_post['Percent'] =['0-10', '10-20','20-30', '30-40','40-50', '50-60','60-70', '70-80',
                                                '80-90', '90-100']
    
    
        
        
    
    fig, ax = plt.subplots(nrows = 3, figsize = (10, 15))
    perc.plot.bar(x='Percent', stacked=True, title=title,
             color = color_plot, ax = ax[0], ylabel = 'Proportions (en%)', xlabel = "Partie de l'éloge")
    perc_pre.plot.bar(x='Percent', stacked=True, title=title +' pre Revolution',
                 color = color_plot, ax = ax[1], ylabel = 'Proportions (en%)', xlabel = "Partie de l'éloge")
    perc_post.plot.bar(x='Percent', stacked=True, title=title+' post Revolution',
                  color=color_plot, ax = ax[2], ylabel = 'Proportions (en%)', xlabel = "Partie de l'éloge")
    
    plt.subplots_adjust(hspace = 0.4)
    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].get_legend().remove()
    ax[1].get_legend().remove()
    ax[2].get_legend().remove()
    fig.legend(handles, labels, bbox_to_anchor=(1.5, 0.5))
    return perc, perc_pre, perc_post


def sent_rep(topic, df_rep, print_ = True, perc=10):
    '''
    This method aims at outputing the most representative sentences of a topic
    Inputs :
        - topic (int) : number of the topic
        - df_rep(DataFrame) : dataframe containing sentences their first topic and probabilities
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


def get_rep_aux_topic(df, topic,  perc=3, print_=True, scd=True):
    '''
    This method gets the most representative sentences for the second and third topic inside a topic
    Inputs:
        - df (DataFrame) : dataframe containing sentences information about first, second and third topics and their probabilities
        - topic (int) : topic we want to study
        - perc (int) : number of sentences to print, by default to 3
        - print_ (Boolean) : by default to True, to print or not the most representative sentences
        - scd (Boolean) : by default set to True, if True prints phrases about the second topic, to False about the third one
    Output:
        - df_help (DataFrame) : dataframe containing the most representative sentences for second or third topic
    '''
    if scd :
        string='Second topic '
        name_col = 'Scd_Topic'
        prob_col = 'Scd_Prob'
    else :
        string = 'Third topic '
        name_col = 'Third_Topic'
        prob_col = 'Third_Prob'
        
    df_aux = df[df['Topic']==topic]
    scd_top = df_aux[name_col].unique()
    for top in scd_top:
        print("\u0332".join(string + str(top) +' :'))
        df_help = df_aux[df_aux[name_col]==top].sample(frac=1).nlargest(n=perc, keep='first', columns = prob_col)
        if print_:
            for _,row in df_help.iterrows():
                print(row['Eloge'])
                print('\n')
    return df_help




#from https://github.com/MaartenGr/BERTopic/blob/master/bertopic/plotting/_topics_over_time.py

import pandas as pd
from typing import List
import plotly.graph_objects as go
from sklearn.preprocessing import normalize

#This method reuses the one implemented by MaartenGr for BERTopic but adds the posssibility to change the title or the 
#name of the axis

def visualize_topics_over_time(topic_model,
                               topics_over_time: pd.DataFrame,
                               top_n_topics: int = None,
                               topics: List[int] = None,
                               normalize_frequency: bool = False,
                               width: int = 1250,
                               height: int = 450, 
                               title='Topics Au cours du Temps', 
                               yaxis="Nombre de topics divisé par le nombre d'éloges",
                              xaxis="Année") -> go.Figure:
    """ Visualize topics over time
    Arguments:
        topic_model: A fitted BERTopic instance.
        topics_over_time: The topics you would like to be visualized with the
                          corresponding topic representation
        top_n_topics: To visualize the most frequent topics instead of all
        topics: Select which topics you would like to be visualized
        normalize_frequency: Whether to normalize each topic's frequency individually
        width: The width of the figure.
        height: The height of the figure.
        title: The title of the plot.
        yaxis : The title of the yaxis
        xaxis : The title of the xaxis
    Returns:
        A plotly.graph_objects.Figure including all traces
    Usage:
    To visualize the topics over time, simply run:
    ```python
    topics_over_time = topic_model.topics_over_time(docs, topics, timestamps)
    topic_model.visualize_topics_over_time(topics_over_time)
    ```
    Or if you want to save the resulting figure:
    ```python
    fig = topic_model.visualize_topics_over_time(topics_over_time)
    fig.write_html("path/to/file.html")
    ```
    <iframe src="../../getting_started/visualization/trump.html"
    style="width:1000px; height: 680px; border: 0px;""></iframe>
    """
    colors = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#D55E00", "#0072B2", "#CC79A7"]

    # Select topics
    if topics:
        selected_topics = topics
    elif top_n_topics:
        selected_topics = topic_model.get_topic_freq().head(top_n_topics + 1)[1:].Topic.values
    else:
        selected_topics = topic_model.get_topic_freq().Topic.values

    # Prepare data
    topic_names = {key: value[:40] + "..." if len(value) > 40 else value
                   for key, value in topic_model.topic_names.items()}
    topics_over_time["Name"] = topics_over_time.Topic.map(topic_names)
    data = topics_over_time.loc[topics_over_time.Topic.isin(selected_topics), :]

    # Add traces
    fig = go.Figure()
    for index, topic in enumerate(data.Topic.unique()):
        trace_data = data.loc[data.Topic == topic, :]
        topic_name = trace_data.Name.values[0]
        words = trace_data.Words.values
        if normalize_frequency:
            y = normalize(trace_data.Frequency.values.reshape(1, -1))[0]
        else:
            y = trace_data.Frequency
        fig.add_trace(go.Scatter(x=trace_data.Timestamp, y=y,
                                 mode='lines',
                                 marker_color=colors[index % 7],
                                 hoverinfo="text",
                                 name=topic_name,
                                 hovertext=[f'<b>Topic {topic}</b><br>Words: {word}' for word in words]))

    # Styling of the visualization
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(
        yaxis_title=yaxis,
        xaxis_title=xaxis,
        title={
            'text': "<b>" + title,
            'y': .95,
            'x': 0.40,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=22,
                color="Black")
        },
        template="simple_white",
        width=width,
        height=height,
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        legend=dict(
            title="<b>Global Topic Representation",
        )
    )
    return fig