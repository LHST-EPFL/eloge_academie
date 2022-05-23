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
    This method looks if the first sentence contains a statement about the birth of the scientist
    Inputs:
        - string (string) : first sentence of the eulogy
        - ls (list) : list of the words indicating birth, by default ['naquit', 'naitre', né']
    Output:
        - boolean : saying if the first sentence contains an indication of birth
    '''
    for word in ls:
        if word in string:
            return True
    return False


def naissance(df, name_col = 'Eloge'):
    '''
    This method adds a column to a dataframe containing a boolean on whether the eulogies' first sentence has a statement about       the birth
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : by default to 'Eloge', name of the column in which the eulogies are
    '''
    df['naissance'] = df[name_col].apply(lambda x : check_naissance(x.split('.')[0]))
    
    
    
def part_of_speech_hist(df, name, name_col = 'Eloge', nbr = False):
    '''
    This method plots an hist of the different part of speech present in the eulogies of an author
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name (string) : name of the author of the eulogies
        - name_col (string) : by default to 'Eloge', name of the column containing the eulogies
        - nbr (number) : by default to False, number of eulogies to norm with
    '''
    #tag the text
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
    '''
    This method's aim is to observe the amount of first person pronouns and to plot a histogram
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies, by default to 'Eloge'
    '''
    #Make a count of all the pronouns
    count = {}
    all_pro = pronom_first.copy()
    all_pro.extend(pronom_suj)
    all_pro.extend(pronom_comp)
    all_pro.extend(pronom_poss)
    for pf in all_pro :
        count[pf] = df[name_col].str.count(pf).sum()


    
    count_plot = dict((k, count[k]) for k in count.keys() if count[k]>0)
    #Sort the pronouns per most appearing
    count_plot = dict(sorted(count_plot.items(), key=lambda item: item[1]))
    count_pf = sum([count_plot[k] for k in count_plot.keys() if k in pronom_first])
    count_op = sum([count_plot[k] for k in count_plot.keys() if k not in pronom_first])
    print('Percentage of first-person pronouns : ' + str((100*count_pf)/(count_pf+count_op)) + '%')
    plt.figure(figsize =(10,6))
    plt.xticks(rotation=90)
    plt.bar(count_plot.keys(), count_plot.values(), color='g')
    plt.title('Most appearing pronouns')
    

def first_person(df, name_col = 'Eloge'):
    '''
    This method aims at plotting the evolution of the use of first-person pronouns
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies, by default to 'Eloge'
    '''
    df['First_Person'] = df[name_col].apply(lambda x : count_fst(x))
    fst_pers = df.groupby('Annee').agg({'First_Person' : 'mean'}).reset_index()
    fst_pers.plot(x = 'Annee', y = 'First_Person', kind = 'bar', figsize = (10,4))
    plt.xlabel('Year')
    plt.title('Evolution of the use of the first person in the eulogies on all pronouns')
    return fst_pers

                                            
def count_fst(string):
    '''
    This method counts the use of first_person pronoun in a eulogy
    Input:
        - string (string) : eulogy
    Output:
        - percentage of first-person pronoun in the eulogy
    '''
    
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
    '''
    This method adds three columns to the dataframe, one containing all the verbs in the eulogy, one containing the count of 
    the past-tense verb, and one the sum of the other verbs
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies, by default to 'tags'
        - past (list) : list containing the tags that correspond to past-tense verbs, by default verbs at the subjunctive 
                        imperfect, the past simple, the past perfect, and imperfect
        - print (boolean) : if to True, prints the overall proportion of past tense verbs and numbers
    '''     
    df['verb'] = df[name_col].apply(lambda x : [elem for elem in x if (len(elem)>1 and elem[1].startswith('VER'))])    
    df['verb_past'] = df['verb'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1] in past)]))
    df['other_verb'] = df['verb'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1] not in past)]))
    if print :
        print('Number of verbs in past tense : ' + str(df['verb_past'].sum()))
        print('Number of verbs not in past tense : ' + str(df['other_verb'].sum()))
        print('Percentage of verbs in past tense : ' + str((100*df['verb_past'].sum())/(df['verb_past'].sum()+df['other_verb'].sum())) + '%')

        

    
def past_tense(df, name_col = 'Eloge'):
    '''
    This method adds a column containing the percentage of verbs at the past tense to the dataframe and plots a hist of it through 
    the years
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies, by default to 'Eloge'
    Outputs:
        - pst (DataFrame) : dataframe that averaged the percentage of past-tense verbs per year
    '''
    #add tags
    add_tags(df, name_col, 'tags')
    #adds verbs, past_verbs and other_verbs columns
    project_back(df)
    df['percent_past'] = df.apply(lambda row : 100*(row['verb_past']/(row['other_verb'] + row['verb_past'])), axis = 1)
    pst = df.groupby(['Annee']).agg({'percent_past' : 'mean'}).reset_index()
    pst.plot(x = 'Annee', y = 'percent_past', kind = 'bar', figsize = (10,4), xlabel='Year', ylabel='Proportion on all verbs used')
    plt.title('Evolution of the use of past tense verbs')
    return pst
    

def cond_imperative(df, name_col = 'Eloge') :
    '''
    This method plots both the proportion of conditional and imperative over the length of the eulogies.
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies, by default to 'Eloge'
    Outputs:
        - pci (DataFrame) : dataframe containing the proportion of imperative and conditional verbs per year
    '''
    if 'tags' not in df.columns :
        add_tags(df, name_col, 'tags')
    df['imp'] = df['tags'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1]== 'VER:impe')]))
    df['cond'] = df['tags'].apply(lambda x : sum([1 for elem in x if (len(elem)>1 and elem[1]== 'VER:cond')]))
    df['imp'] = df.apply(lambda row : row['imp']/len(row[name_col]), axis = 1)
    df['cond'] = df.apply(lambda row : row['cond']/len(row[name_col]), axis = 1)
    pci = df.groupby(['Annee']).agg({'imp' : 'mean', 'cond' : 'mean'}).reset_index()
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize = (10,8.5))
    pci.plot(x='Annee', y='imp', kind ='bar', ax = ax[0], title = 'Use of the imperative throughout the years normed by the length of the eulogy')
    ax[0].set_xlabel('Year')
    pci.plot(x='Annee', y = 'cond', kind = 'bar', ax=ax[1], title = 'Use of the conditionnal throughout the years normed by the length of the eulogy')
    ax[1].set_xlabel('Year')
    plt.subplots_adjust(hspace = 0.5)
    return pci
                                          
        
        
    
def nbr_eulogies(df, name, name_col = 'Annee', fig_size = (10,4)):
    '''
    This methods plots an hist of the number of the eulogies per year from one author
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name (string) : name of the writer of the eulogies
        - name_col (string) : name of the column to print by default to 'Annee'
        - fig_size (tuple) : tuple containing the size of the figure, by default to (10,4)
    '''
    bins = max(df[name_col])-min(df[name_col])
    df[name_col].hist(bins = bins, figsize = fig_size, xrot = 90)
    plt.title('Number of eulogies published by year by ' + name)
    
    
    
    
def nbr_character(df, name_col = 'Eloge', evol = False, year = 'Annee'):
    '''
    This method aims at showing the number of characters per eulogy
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies, by default to 'Eloge'
        - evol (boolean) : if True plots, the evolution of the number of characters by averaging each year, if False just plots
                           a histogram of the number of characters
        - year (string) : name of the column containing the year of publication of the eulogy
    Outputs:
        - nbr_charc (DataFrame) : if evol is True, outputs the dataframe containing the average number of characters per year
    '''
    if not evol :
        df['Eloge'].str.len().hist()
        plt.title('Number of characters per eulogy')
    else :
        df_help = df.copy()
        df_help['Number of characters'] = df_help['Eloge'].apply(lambda x : len(str(x)))

        nbr_charac = df_help.groupby(['Annee']).agg({'Number of characters' : 'mean'}).reset_index()
        nbr_of_years = max(df_help.Annee)-min(df_help.Annee)

        nbr_charac.plot(x= 'Annee', y = 'Number of characters', kind = 'bar')
        plt.xlabel('Annee')
        plt.title('Evolution of number of characters through the years')
        return nbr_charac
        
        
        
def nbr_words(df, name_col = 'Eloge', evol = False, year = 'Annee'):
    '''
    This method aims at showing the number of words per eulogy
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies, by default to 'Eloge'
        - evol (boolean) : if True plots, the evolution of the number of words by averaging each year, if False just plots
                           a histogram of the number of words 
        - year (string) : name of the column containing the year of publication of the eulogy
    Outputs:
        - nbr_words (DataFrame) : if evol is True, outputs the dataframe containing the average number of words per year
    '''
    
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
        plt.xlabel('Year')
        plt.title('Evolution of the average number of words per eulogy through the years')
        return nbr_words
        
        
        
def avg_word_length(df, name_col = 'Eloge', evol = False, year = 'Annee'):
    '''
    This method aims at showing the average length of wordper eulogy
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies, by default to 'Eloge'
        - evol (boolean) : if True plots, the evolution of the average length of words by averaging each year, if False just plots
                           a histogram of the average word length 
        - year (string) : name of the column containing the year of publication of the eulogy
    Outputs:
        - avg_word (DataFrame) : if evol is True, outputs the dataframe containing the average length of words per year
    '''
    if not evol :
        df[name_col].str.split().apply(lambda x : [len(i) for i in x]).map(lambda x : np.mean(x)).hist()
        plt.title('Average word length in the eulogies')
    else :
        df_help = df.copy()
        df_help['Avg Word Length'] = df_help['Eloge'].apply(lambda x : statistics.mean([len(i) for i in x.split()]))
        avg_word = df_help.groupby(['Annee']).agg({'Avg Word Length' : 'mean'}).reset_index()

        avg_word.plot('Annee', 'Avg Word Length', kind = 'bar', figsize = (10,4))
        plt.xlabel('Year')

        plt.title('Evolution of the average word length')
        return avg_word
        
        
        
#https://onecompiler.com/python/3wrds77az

#function to calculate the average sentence length across a piece of text.
def avg_sentence_len(text):
    '''
    This method returns the average length of the sentences in one eulogy
    Input:
        - text(string) : eulogy
    Output:
        - average_sentence_length (number) : average length of the sentences in the eulogy
    '''
    sentences = text.split(".") #split the text into a list of sentences.
    words = text.split(" ") #split the input text into a list of separate words
    if(sentences[len(sentences)-1]==""): #if the last value in sentences is an empty string
        average_sentence_length = len(words) / len(sentences)-1
    else:
        average_sentence_length = len(words) / len(sentences)
    return average_sentence_length #returning avg length of sentence


def avg_sentence(df, name_col = 'Eloge', evol = False, year = 'Annee'):
    '''
    This method aims at observing the average sentence length in the eulogies and plots a hist
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies
        - evol (boolean) : if True, plots the evolution of the average sentence length through the year, if False plots the hist
                           of the average sentence length, by default to False
        - year (string) : name of the column containing the year of publication by default to 'Annee'
    Outputs :
        - avg_sent (DataFrame) : if evol is True, outputs the dataframe containing the average length of sentences per year
    '''
    df_help = df.copy()
    if not evol :
        df_help[name_col].apply(lambda x : avg_sentence_len(x)).hist()
        plt.title('Average length of the sentences in the eulogies')
    else :
        df_help['Avg Sent Length'] = df_help['Eloge'].apply(lambda x : avg_sentence_len(x))

        avg_sent = df_help.groupby(['Annee']).agg({'Avg Sent Length' : 'mean'}).reset_index()

        avg_sent.plot('Annee', 'Avg Sent Length', kind = 'bar', figsize = (10,4))
        plt.title('Evolution of the sentence length through the years')
        plt.xlabel('Year')
        return avg_sent
    
    
    
def get_adverbs(text):
    '''
    This method gets the adverbs in an eulogy
    Input:
        - text (string) : eulogy
    Output:
        - adv (list) : list of the adverbs in the eulogy
    '''
    tags = treetaggerwrapper.make_tags(tagger.tag_text(text))
    tag_idx=0
    adv = []
    #Browse through the words of the eulogies
    while tag_idx<len(tags):
        if len(tags[tag_idx])>1 and tags[tag_idx][1]=='ADV' :
            #if the word is an adverb, then checks if the following word is also one
            if tag_idx < len(tags)-1 :
                if tags[tag_idx+1][1]=='ADV'and len(tags[tag_idx+1])>1:
                    #if two following words are adverbs then add it to the list and move to the next word
                    adv.append(tags[tag_idx][2] + ' ' + tags[tag_idx+1][2])
                    tag_idx += 2
                else :
                    #ads the current word to the adverbs list
                    adv.append(tags[tag_idx][2])
                    tag_idx += 1
            else :
                #add the last word of the eulogy that is an adverb to the list
                adv.append(tags[tag_idx][2])
                tag_idx += 1
        else :
            #move to the following word if the word is not an adverb
            tag_idx += 1
        
    return adv


def keep_adv(df, name_col):
    '''
    This method adds a column to a new dataframe containing the adverbs present in the eulogy
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies
    Outputs :
        - df_help (DataFrame) : outputs a new dataframe containing an additional column that contains the adverbs
    '''
    df_help = df.copy()
    df_help['adverbs'] = df_help[name_col].apply(lambda x : get_adverbs(x))
    return df_help

def count_adverbs(df, name_col = 'Eloge'):
    #https://stackoverflow.com/questions/48707117/count-of-elements-in-lists-within-pandas-data-frame
    '''
    This method counts the number of appearance of all the adverbs throughout the entire eulogies
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : by default to 'Eloge', name of the column containing the eulogies
    Outputs:
        - df_ret (DataFrame) : dataframe containing the adverbs and their number of appearange
        - df_help (DataFrame) : dataframe containing an additionnal column with the list of adverbs
    '''
    
    df_help = keep_adv(df, name_col)
    a = pd.Series([item for sublist in df_help.adverbs for item in sublist])
    df_ret = a.groupby(a).size().rename_axis('Adverb').reset_index(name='Number')
    return df_ret, df_help


def proper_name(df, name_col = 'Eloge', norm = False):
    '''
    This methods' aim is to study the appearance of proper names throughout the eulogies
    Inputs:
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : by default to 'Eloge', name of the column containing the eulogies
        - norm (boolean) : by default to False, if True normed by the length of the eulogy
    '''
    if 'tags' not in df.columns:
        add_tags(df, name_col, 'tags')
    if norm :   
        df['p_name'] = df.apply(lambda x : sum([1 for elem in x['tags'] if len(elem)>1 and elem[1]=='NAM'])/(len(x[name_col])), 
                                axis = 1)
    else :
        df['p_name'] = df.apply(lambda x : sum([1 for elem in x['tags'] if len(elem)>1 and elem[1]=='NAM']), axis = 1)
    p_n = df.groupby('Annee').agg({'p_name' : 'mean'}).reset_index()
    p_n.plot(x = 'Annee', y = 'p_name', kind = 'bar', figsize = (10,4), xlabel='Year')
    if norm :
        plt.title('Evolution of the use of proper names normed by the number of words per eulogy')
    else :
        plt.title('Evolution of the use of proper names')
    return p_n
                            
                               
    
        

    