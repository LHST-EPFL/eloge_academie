#https://stackoverflow.com/questions/52946332/how-to-print-specific-words-in-colour-on-python#
def get_rep_adv(df, df_sent, df_adv, adverb = 'environ',categorie='Assertivité',  name_col = 'Eloge', 
                adv = None, BOLD = '\033[1m', END = '\033[0m', print_=True):
    '''
        This method prints six sentences from different eulogies, three before the Revolution, three after. Those sentences   are    
        considered the most representative of the adverb. We take the three eulogies that contain the most adverbs of the same 
        categorie and then we take at random in the eulogy one sentence containing the eulogies and prints it in bold
        Inputs:
            - df (DataFrame) : dataframe containing the eulogies
            - df_sent (DataFrame) : dataframe containing the sentences of the eulogies
            - df_adv (DataFrame) : dataframe containing the adverbs and their categories
            - adverb (string) : adverb to highlight, by default to 'environ'
            - categorie (string) : categorie of the adverb we want to study, by default to 'Assertivité'
            - name_col (string) : name of the column containing the eulogy
            - adv (string) : by default to None, else name of the column that contains the list of adverbs for each eulogy
            - BOLD (string) : code of the bold to print, by default to '\033[1m'
            - END (string) : code of the reset to print, by default to '\033[0m'
            - print_ (boolean) : by default to True, whether to print or no the sentences
        Outputs :
            - list_pre (list) : list containing the sentences before the Revolution
            - list_post (list) : list containing the sentences after the Revolution
          
    '''
    
    
    
    #Finds the category of the adverb
    sorte = df_adv[df_adv['Adverb']==adverb].reset_index()[categorie][0]
    #Make a list of all the adverbs that are in this categor
    ls = df_adv[df_adv[categorie]==sorte]['Adverb'].tolist()

    df_help = df.copy()
    if adv != None :
        #Creates a new column with the number of adverbs in the category in the eulogy divided by the number of adverbs in this 
        #eulogy
        df_help['aux'] = df_help[adv].apply(lambda x : [elem for elem in x if elem in ls])
        df_help['adv'] = df_help.apply(lambda x : len(x['aux'])/len(x[adv]), axis=1)
    else :
        # Creates a column with the adverbs for each eulogy
        df_help = keep_adv(df_help, name_col)
        #Creates a new column with the number of adverbs in the category in the eulogy divided by the number of adverbs in this 
        #eulogy
        df_help['aux'] = df_help['adverbs'].apply(lambda x : [elem for elem in x if elem in ls])
        df_help['adv'] = df_help.apply(lambda x : len(x['aux'])/len(x['adverbs']),
                                       axis=1)
    
    #Divides the dataset in pre and post Revolution and then sort them by descending order on proportion of the category in the 
    #eulogy
    df_pre = df_help[df_help['Annee']<=1793].copy().reset_index()
    df_post = df_help[df_help['Annee']>1793].copy().reset_index()
    df_pre.sort_values(ascending = False, by = 'adv', inplace = True)
    df_post.sort_values(ascending = False, by = 'adv', inplace = True)
    
    
    # Pre-Revolution
    #keeps track of the number of sentences with the adverb found
    counter = 0
    #keeps track of the index in the dataframe
    idx = 0
    list_pre = []
    if print_:
        print("\u0332".join('Pre-Revolution : '))
    while counter < 3  and idx<df_pre.shape[0]:
        #if we still haven't found three sentences with the adverb and aren't at the end of the dataframe
        if adverb in df_pre['aux'][idx]:
            #adverb found in the eulogy
            counter +=1
            #find the sentences corresponding to this eulogy
            df_aux = df_sent[(df_sent['Savant'] == df_pre['Savant'][idx]) & (df_sent['Annee'] == df_pre['Annee'][idx])].reset_index()
            #find all the sentences containing the adverb and shuffle it and print the first one
            df_aux['adverbs'] = df_aux['adverbs'].apply(lambda x : ' '.join(x))
            df_aux = df_aux[df_aux['adverbs'].str.contains(adverb)].sample(frac=1).reset_index()

            utterances = df_aux['Eloge'][0].split()
            idxs = [i for i, x in enumerate(utterances) if adverb in x]
                # modify the occurences by wrapping them in ANSI sequences
            for i in idxs:
                utterances[i] = BOLD + utterances[i] + END
            # join the list back into a string and print
            utterances = " ".join(utterances)
            if print_:
                print(utterances)
            list_pre.append(df_aux['Eloge'][0])

        idx+=1
    
    # Pre-Revolution
    #keeps track of the number of sentences with the adverb found
    counter = 0
    #keeps track of the index in the dataframe
    idx = 0
    list_post = []
    if print_:
        print("\u0332".join('Post-Revolution : '))
    while counter < 3  and idx<df_post.shape[0]:
        #if we still haven't found three sentences with the adverb and aren't at the end of the dataframe
        if adverb in df_post['aux'][idx]:
            #adverb found in the eulogy
            counter +=1
            #find the sentences corresponding to this eulogy
            df_aux = df_sent[(df_sent['Savant'] == df_post['Savant'][idx]) & (df_sent['Annee'] == df_post['Annee'][idx])].reset_index()
            #find all the sentences containing the adverb and shuffle it and print the first one
            df_aux['adverbs'] = df_aux['adverbs'].apply(lambda x : ' '.join(x))
            df_aux = df_aux[df_aux['adverbs'].str.contains(adverb)].sample(frac=1).reset_index()
            utterances = df_aux['Eloge'][0].split()
            idxs = [i for i, x in enumerate(utterances) if adverb in x]
                # modify the occurences by wrapping them in ANSI sequences
            for i in idxs:
                utterances[i] = BOLD + utterances[i] + END
            # join the list back into a string and print
            utterances = " ".join(utterances)
            if print_:
                print(utterances)
            list_post.append(df_aux['Eloge'][0])
        idx+=1
        
    return list_pre, list_post