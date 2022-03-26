import pandas as pd
import matplotlib.pyplot as plt
import treetaggerwrapper
from pandas import Series
from tqdm import tqdm 
tqdm.pandas()

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR = './../Treetagger')
pos_tags = pd.read_csv('./../../Data/POS-tags.csv', header=None, index_col=0, squeeze=True).to_dict()


def check_naissance(string, ls = ['naquit','naitre', 'né']):
    for word in ls:
        if word in string:
            return True
    return False


def naissance(df, name_col = 'Eloge'):
    df['naissance'] = df[name_col].apply(lambda x : check_naissance(x))
    
    
    
def part_of_speech_hist(df, name, name_col = 'Eloge', nbr = False):
    df['pos'] = df[name_col].apply(lambda x : tagger.tag_text(x))
    df['pos'] = df['pos'].apply(lambda x : treetaggerwrapper.make_tags(x))
    df['pos'] = df['pos'].apply(lambda x : [elem[1] for elem in x if len(elem)>2])
    df['pos'] = df['pos'].apply(lambda x : [pos_tags[elem] if elem in pos_tags.keys() else elem for elem in x])
    if nbr :
        df['pos'].apply(Series).stack().value_counts(ascending = False).apply(lambda x : x/nbr).plot(kind ='bar',figsize = (10,4))
        plt.title("Nature des mots apparaissant dans les éloge de ' + name + ' normée par le nombre d'éloges")
        plt.xlabel('Nature des mots')
        plt.ylabel("Nombre d'apparition")
    else :
        df['pos'].apply(Series).stack().value_counts(ascending = False).plot(kind ='bar', figsize = (10, 4))
        plt.title('Nature des mots apparaissant dans les éloge de ' + name)
        plt.xlabel('Nature des mots')
        plt.ylabel("Nombre d'apparition")
        
        
        
pronom_suj = [ "tu", "il", "elle", "on", "nous", "vous", "ils","elles"]
pronom_comp = [ "te", "le", "lui", "la", "les", "leur", "eux",  "toi"]
pronom_poss = ["le nôtre", "la nôtre", "les nôtres","le tien", "la tienne", "les tiens", 
               "les tiennes", "le vôtre", "la vôtre",  "les vôtres", "le sien", "la sienne", "les siens", "les siennes", "le leur", "la leur", 
               "les leurs"]
pronom_first = ['je', "j'","me","moi","le mien", "la mienne", "les miens", "les miennes"]


def self_disclosure(df, name_col = 'Eloge'):
    count = {}
    all_pro = pronom_first.copy()
    all_pro.extend(pronom_suj)
    all_pro.extend(pronom_comp)
    all_pro.extend(pronom_poss)
    for pf in all_pro :
        count[pf] = df[name_col].str.count(pf).sum()


    count_plot = dict((k, count[k]) for k in count.keys() if count[k]>0)
    count_plot = dict(sorted(count_plot.items(), key=lambda item: item[1]))
    count_pf = sum([count_plot[k] for k in count_plot.keys() if k in pronom_first])
    count_op = sum([count_plot[k] for k in count_plot.keys() if k not in pronom_first])
    print('Percentage of first-person pronouns : ' + str((100*count_pf)/(count_pf+count_op)) + '%')
    plt.figure(figsize =(10,6))
    plt.xticks(rotation=90)
    plt.bar(count_plot.keys(), count_plot.values(), color='g')
    plt.title('Most appearing pronouns')
    
    
    
def project_back(df, name_col = 'tags', past = ['VER:subi', 'VER:simp', 'VER:pper', 'VER:impf']):
    df['verb'] = df[name_col].progress_apply(lambda x : [elem for elem in x if (len(elem)>1 and elem[1].startswith('VER'))])    
    df['verb_past'] = df['verb'].progress_apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1] in past)]))
    df['other_verb'] = df['verb'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1] not in past)]))
    print('Number of verbs in past tense : ' + str(df['verb_past'].sum()))
    print('Number of verbs not in past tense : ' + str(df['other_verb'].sum()))
    print('Percentage of verbs in past tense : ' + str((100*df_cond['verb_past'].sum())/(df_cond['verb_past'].sum()+df_cond['other_verb'].sum())) + '%')
    