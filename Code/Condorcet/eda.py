import pandas as pd
import matplotlib.pyplot as plt
import treetaggerwrapper
from pandas import Series
from tqdm import tqdm 
import numpy as np
import statistics
import re
from pre_process import *
tqdm.pandas()

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR = './../Treetagger')
pos_tags = pd.read_csv('./../../Data/POS-tags.csv', header=None, index_col=0, squeeze=True).to_dict()


def check_naissance(string, ls = ['naquit','naitre', 'né']):
    '''
    This method checks if the first sentence of an eulogy contains a statement about the birth
    Inputs:
        - string(string) : first sentence of the eulogy
        - ls (list) : list of words that desccribe the birth by default to ['naquit', 'naitre', 'ne']
    '''
    for word in ls:
        if word in string:
            return True
    return False


def naissance(df, name_col = 'Eloge'):
    df['naissance'] = df[name_col].apply(lambda x : check_naissance(x.split('.')[0]))
    
    
    
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
    

def first_person(df, name_col = 'Eloge'):
    df['First_Person'] = df[name_col].apply(lambda x : count_fst(x))
    fst_pers = df.groupby('Annee').agg({'First_Person' : 'mean'}).reset_index()
    fst_pers.plot(x = 'Annee', y = 'First_Person', kind = 'bar', figsize = (10,4))
    plt.title('Evolution of the use of the first person in the eulogies on all pronouns')
    return fst_pers

                                            
def count_fst(string):
    count = {}
    all_pro = pronom_first.copy()
    all_pro.extend(pronom_suj)
    all_pro.extend(pronom_comp)
    all_pro.extend(pronom_poss)
    for pf in all_pro :
        count[pf] = string.count(pf)
    count_plot = dict((k, count[k]) for k in count.keys() if count[k]>0)
    count_plot = dict(sorted(count_plot.items(), key=lambda item: item[1]))
    count_pf = sum([count_plot[k] for k in count_plot.keys() if k in pronom_first])
    count_op = sum([count_plot[k] for k in count_plot.keys() if k not in pronom_first]) 
    return (100*count_pf)/(count_pf+count_op)
                                            
def project_back(df, name_col = 'tags', past = ['VER:subi', 'VER:simp', 'VER:pper', 'VER:impf'], print = False):
    df['verb'] = df[name_col].apply(lambda x : [elem for elem in x if (len(elem)>1 and elem[1].startswith('VER'))])    
    df['verb_past'] = df['verb'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1] in past)]))
    df['other_verb'] = df['verb'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1] not in past)]))
    if print :
        print('Number of verbs in past tense : ' + str(df['verb_past'].sum()))
        print('Number of verbs not in past tense : ' + str(df['other_verb'].sum()))
        print('Percentage of verbs in past tense : ' + str((100*df['verb_past'].sum())/(df['verb_past'].sum()+df['other_verb'].sum())) + '%')

        

    
def past_tense(df, name_col = 'Eloge'):
    add_tags(df, name_col, 'tags')
    project_back(df)
    df['percent_past'] = df.apply(lambda row : 100*(row['verb_past']/(row['other_verb'] + row['verb_past'])), axis = 1)
    ## TODO DROP OLD COLUMNS
    pst = df.groupby(['Annee']).agg({'percent_past' : 'mean'}).reset_index()
    pst.plot(x = 'Annee', y = 'percent_past', kind = 'bar', figsize = (10,4))
    plt.title('Evolution of the use of past tense verbs')
    return pst
    

def cond_imperative(df, name_col = 'Eloge') :
    if 'tags' not in df.columns :
        add_tags(df, name_col, 'tags')
    df['imp'] = df['tags'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1]== 'VER:impe')]))
    df['cond'] = df['tags'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1]== 'VER:cond')]))
    df['imp'] = df.apply(lambda row : row['imp']/len(row[name_col]), axis = 1)
    df['cond'] = df.apply(lambda row : row['cond']/len(row[name_col]), axis = 1)
    pci = df.groupby(['Annee']).agg({'imp' : 'mean', 'cond' : 'mean'}).reset_index()
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize = (10,8.5))
    pci.plot(x='Annee', y='imp', kind ='bar', ax = ax[0], title = 'Use of the imperative through the years')
    pci.plot(x='Annee', y = 'cond', kind = 'bar', ax=ax[1], title = 'Use of the conditionnal throught the years')
    plt.subplots_adjust(hspace = 0.5)
    return pci
                                          
        
    
def nbr_eulogies(df, name, name_col = 'Annee', fig_size = (10,4)):
    bins = max(df[name_col])-min(df[name_col])
    df[name_col].hist(bins = bins, figsize = fig_size, xrot = 90)
    plt.title('Number of eulogies published by year by ' + name)
    
    
    
    
def nbr_character(df, name_col = 'Eloge', evol = False, year = 'Annee'):
    if not evol :
        df['Eloge'].str.len().hist()
        plt.title('Number of characters per eulogy')
    else :
        df_help = df.copy()
        df_help['Number of characters'] = df_help['Eloge'].apply(lambda x : len(str(x)))

        nbr_charac = df_help.groupby(['Annee']).agg({'Number of characters' : 'mean'}).reset_index()
        nbr_of_years = max(df_help.Annee)-min(df_help.Annee)

        nbr_charac.plot(x= 'Annee', y = 'Number of characters', kind = 'bar')
        plt.title('Evolution of number of characters through the years')
        return nbr_charac
        
        
        
def nbr_words(df, name_col = 'Eloge', evol = False, year = 'Annee'):
    if not evol:
        df[name_col].str.split().map(lambda x : len(x)).hist()
        plt.title('Number of words per eulogies')
        plt.xlabel('Number of words')
        plt.ylabel('Number of eulogies')
    else :
        df_help = df.copy()
        df_help['Number of words'] = df_help['Eloge'].apply(lambda x : len(x.split()))

        nbr_words = df_help.groupby(['Annee']).agg({'Number of words' : 'mean'}).reset_index()

        nbr_words.plot(x = 'Annee', y = 'Number of words', kind = 'bar', figsize = (10,4))
        return nbr_words
        
        
        
def avg_word_length(df, name_col = 'Eloge', evol = False, year = 'Annee'):
    if not evol :
        df[name_col].str.split().apply(lambda x : [len(i) for i in x]).map(lambda x : np.mean(x)).hist()
        plt.title('Average word length in the eulogies')
    else :
        df_help = df.copy()
        df_help['Avg Word Length'] = df_help['Eloge'].apply(lambda x : statistics.mean([len(i) for i in x.split()]))
        avg_word = df_help.groupby(['Annee']).agg({'Avg Word Length' : 'mean'}).reset_index()

        avg_word.plot('Annee', 'Avg Word Length', kind = 'bar', figsize = (10,4))

        plt.title('Evolution of the average word length')
        return avg_word
        
        
        
#https://onecompiler.com/python/3wrds77az

#function to calculate the average sentence length across a piece of text.
def avg_sentence_len(text):
    sentences = text.split(".") #split the text into a list of sentences.
    words = text.split(" ") #split the input text into a list of separate words
    if(sentences[len(sentences)-1]==""): #if the last value in sentences is an empty string
        average_sentence_length = len(words) / len(sentences)-1
    else:
        average_sentence_length = len(words) / len(sentences)
    return average_sentence_length #returning avg length of sentence


def avg_sentence(df, name_col = 'Eloge', evol = False, year = 'Annee'):
    df_help = df.copy()
    if not evol :
        df_help[name_col].apply(lambda x : avg_sentence_len(x)).hist()
        plt.title('Average length of the sentences in the eulogies')
    else :
        df_help['Avg Sent Length'] = df_help['Eloge'].apply(lambda x : avg_sentence_len(x))

        avg_sent = df_help.groupby(['Annee']).agg({'Avg Sent Length' : 'mean'}).reset_index()

        avg_sent.plot('Annee', 'Avg Sent Length', kind = 'bar', figsize = (10,4))
        plt.title('Evolution of the sentence length through the years')
        return avg_sent
    
    
    
def get_adverbs(text):
    tags = treetaggerwrapper.make_tags(tagger.tag_text(text))
    tag_idx=0
    adv = []
    while tag_idx<len(tags):
        if len(tags[tag_idx])>1 and tags[tag_idx][1]=='ADV' :
            if tag_idx < len(tags)-1 :
                if tags[tag_idx+1][1]=='ADV'and len(tags[tag_idx+1])>1:
                    adv.append(tags[tag_idx][2] + ' ' + tags[tag_idx+1][2])
                    tag_idx += 2
                else :
                    adv.append(tags[tag_idx][2])
                    tag_idx += 1
            else :
                adv.append(tags[tag_idx][2])
                tag_idx += 1
        else :
            tag_idx += 1
        
    return adv


def keep_adv(df, name_col):
    df_help = df.copy()
    df_help['adverbs'] = df_help[name_col].apply(lambda x : get_adverbs(x))
    return df_help

def count_adverbs(df, name_col = 'Eloge'):
    #https://stackoverflow.com/questions/48707117/count-of-elements-in-lists-within-pandas-data-frame
    
    df_help = keep_adv(df, name_col)
    #df_help['adverbs'] = df_help['adverbs'].apply(lambda x : [word.lower().strip() for word in x])
    #df_help['adverbs'] = df_help['adverbs'].apply(lambda x : [re.sub(r'[^a-zA-Z]', '', word) for word in x])
    a = pd.Series([item for sublist in df_help.adverbs for item in sublist])
    df_ret = a.groupby(a).size().rename_axis('Adverb').reset_index(name='Number')
    return df_ret, df_help


def proper_name(df, name_col = 'Eloge', norm = False):
    if 'tags' not in df.columns:
        add_tags(df, name_col, 'tags')
    if norm :   
        df['p_name'] = df.apply(lambda x : sum([1 for elem in x['tags'] if len(elem)>1 and elem[1]=='NAM'])/(len(x[name_col])), 
                                axis = 1)
    else :
        df['p_name'] = df.apply(lambda x : sum([1 for elem in x['tags'] if len(elem)>1 and elem[1]=='NAM']), axis = 1)
    p_n = df.groupby('Annee').agg({'p_name' : 'mean'}).reset_index()
    p_n.plot(x = 'Annee', y = 'p_name', kind = 'bar', figsize = (10,4))
    if norm :
        plt.title('Evolution of the use of proper names normed by the number of words per eulogy')
    else :
        plt.title('Evolution of the use of proper names')
    return p_n
                            
                               
    
        

    