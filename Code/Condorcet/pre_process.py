from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
import re
import treetaggerwrapper


def rmv_sw(df, name_col='Eloge'):
    '''
    Removing the stop words using spacy list
    Inputs :
        - df (DataFrame) : DataFrame containing the documents
        - name_col (string) : name of the column from which to remove stop words by default to 'Eloge'
    '''
    #update list with our own stop words
    fr_stop.update({'plus', 'ce', 'cette', 'encore', 'alors', 'qu', "qu'"})
    #adding column to dataframe
    df['no_sw'] = df[name_col].apply(lambda x : ' '.join([elem for elem in x.split() if (elem not in fr_stop and len(elem)>2)]))
    
def rmv_punkt(df, name_col = 'no_sw'):
    '''
    Removing punctuation
    Inputs :
        - df (DataFrame) : DataFrame containing the documents
        - name_col (string) : name of the column from which to remove punctuation by default to 'no_sw'
    '''
    df['no_sw_no_punkt'] = df[name_col].apply(lambda x : re.sub(r'[^\w\s]', ' ', x))

def rmv_digit(df, name_col = 'Eloge_lem'):
    '''
    Removing digits
    Inputs :
        - df (DataFrame) : DataFrame containing the documents
        - name_col (string) : name of the column from which to remove digits by default to 'Eloge_lem'
    '''
    df[name_col] = df[name_col].apply(lambda x : ' '.join([i for i in x.split() if not i.isdigit()]))
    

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR = './../Treetagger')
    
def add_tags(df, name_col, new_name):
    '''
    Adds part-of-speech tags to documents
    Inputs :
        - df (DataFrame) : dataframe containing the documents
        - name_col (string) : name of the column where to tag text
        - new_name (string) : name to give to the column containing the tags
    '''
    df[new_name] = df[name_col].apply(lambda x : tagger.tag_text(x))
    df[new_name] = df[new_name].apply(lambda x : treetaggerwrapper.make_tags(x))
    
def lemmatize(df, name_col, new_name):
    '''
    Lemmatizes the documents using treetagger
    Inputs :
        - df (DataFrame) : dataframe containing the documents
        - name_col (string) : name of the column where to lemmatize
        - new_name (string) : name to give to the column containing the tags
    '''
    add_tags(df, name_col, new_name)
    df['Eloge_lem'] = df[new_name].apply(lambda x : ' '.join([elem[2] for elem in x if len(elem)>2]))
    
    
def nouns_verbs(df, name_col, adj = False):
    '''
    This method only keeps nouns, verbs and adjectives for the topic modeling
    Inputs :
        - df (DataFrame) : dataframe containing the documents
        - name_col (string) : name of the column containing the tags
        - adj (boolean) : to keep or not the adjectives in the pre-processing, by default to False
    '''
    add_tags(df, name_col, 'n_v')
    if adj :
        df['n_v'] = df['n_v'].apply(lambda x : ' '.join([elem[2] for elem in x if(elem[1] =='NOM' or elem[1].startswith('VER')
                                                                                 or elem[1]=='ADJ')]))
    else :
        df['n_v'] = df['n_v'].apply(lambda x : ' '.join([elem[2] for elem in x if(elem[1] =='NOM' or elem[1].startswith('VER'))]))
    #df['n_v'] = df['n_v'].apply(lambda x : ' '.join([word for word in x.split() if ((word not in fr_stop) and (len(word)>2))]))
    
    
    
def side_info(df, name_col = 'Eloge'):
    '''
    This method removes the information contained in the brackets that is not part per-say of the eulogy and puts it in another
    columns
    Inputs :
        - df (DataFrame) : dataframe containing the eulogies
        - name_col (string) : name of the column containing the eulogies by default to 'Eloge'
    '''
    df['Side_Info'] = df[name_col].apply(lambda x : re.findall('\[(.*?)\]', x))
    df[name_col] = df[name_col].apply(lambda x : re.sub('\[(.*?)\]','', x))