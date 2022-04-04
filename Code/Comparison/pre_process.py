from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
import re
import treetaggerwrapper


def rmv_sw(df, name_col='Eloge'):
    fr_stop.update({'plus', 'ce', 'cette', 'encore', 'alors', 'qu', "qu'"})
    df['no_sw'] = df[name_col].apply(lambda x : ' '.join([elem for elem in x.split() if (elem not in fr_stop and len(elem)>2)]))
    
def rmv_punkt(df, name_col = 'no_sw'):
    df['no_sw_no_punkt'] = df[name_col].apply(lambda x : re.sub(r'[^\w\s]', ' ', x))

def rmv_digit(df, name_col = 'Eloge_lem'):
    df[name_col] = df[name_col].apply(lambda x : ' '.join([i for i in x.split() if not i.isdigit()]))
    

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGDIR = './../Treetagger')
    
def add_tags(df, name_col, new_name):
    df[new_name] = df[name_col].apply(lambda x : tagger.tag_text(x))
    df[new_name] = df[new_name].apply(lambda x : treetaggerwrapper.make_tags(x))
    
def lemmatize(df, name_col, new_name):
    add_tags(df, name_col, new_name)
    df['Eloge_lem'] = df[new_name].apply(lambda x : ' '.join([elem[2] for elem in x if len(elem)>2]))
    
    
def nouns_verbs(df, name_col):
    add_tags(df, name_col, 'n_v')
    df['n_v'] = df['n_v'].progress_apply(lambda x : ' '.join([elem[2] for elem in x if(elem[1] =='NOM' or elem[1].startswith('VER'))]))
    #df['n_v'] = df['n_v'].progress_apply(lambda x : ' '.join([word for word in x.split() if ((word not in fr_stop) and (len(word)>2))]))
    
    
    
def side_info(df, name_col = 'Eloge'):
    df['Side_Info'] = df[name_col].apply(lambda x : re.findall('\[(.*?)\]', x))
    df[name_col] = df[name_col].apply(lambda x : re.sub('\[(.*?)\]','', x))