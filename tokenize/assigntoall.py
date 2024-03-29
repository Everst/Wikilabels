def assign(tokens_path, wiki_titles, wiki_tokens, var6, var7, var8, var9, var10, left, first=False):
    import re,sys
    from gensim import corpora
    import math
    from itertools import groupby
    import multiprocessing
    from nltk.stem.wordnet import WordNetLemmatizer
    
    stemmer = WordNetLemmatizer()
    
    from time import strftime
    
    
    def clean2(myList):    # function to remove duplicates from the list of links generated by mechanize    
        try:              
            last = myList[-1]
            for i in range(len(myList)-2, -1, -1):
                if last == myList[i]:
                    del myList[i]
                else:   
                    last = myList[i]
        
        except IndexError:
            pass
    
    tokens_file = open(tokens_path+'tokens.txt').read()
    str678 = re.compile('\.\.')
    tokens_file = str678.sub('', tokens_file)
    tokens_file = re.sub('/', ', ', tokens_file)
    
    texts_all = tokens_file.split('\n')
    
    
    texts_dict = {}
    
    if left:
        left = [int(l) for l in left]
        for l in left:
            texts_dict[l] = [w for w in texts_all[l].split(', ')]
    else:
        lefto = range(len(texts_all))
        for l in lefto:
            texts_dict[l] = [w for w in texts_all[l].split(', ')]
        
    
    tit_tok_file = open(tokens_path+'title-tokens.txt').read()
    tit_tok_file = re.sub('/', ', ', tit_tok_file)
    tit_tok_all = tit_tok_file.split('\n')
    
    tit_tok_dict = {}
    
    if left:
        left = [int(l) for l in left]
        for l in left:
            tit_tok_dict[l] = [w for w in tit_tok_all[l].split(', ')]    
    else:
        lefto = range(len(tit_tok_all))
        for l in lefto:
            tit_tok_dict[l] = [w for w in tit_tok_all[l].split(', ')]
        
    
    if texts_dict[max(texts_dict.keys())][0] == "" and tit_tok_dict[max(texts_dict.keys())][0] == "":
        del texts_dict[len(texts_all)-1]
        del tit_tok_dict[len(tit_tok_all)-1]
    
    titles = open(wiki_titles).read()
    tit_texts = open(wiki_tokens).read()
    tit_texts = re.sub('/', ', ', tit_texts)
    
    titles = titles.split('\n')
    tit_texts = tit_texts.split('\n')
    if titles[-1] == "" and tit_texts[-1] == "":
        del titles[-1]
        del tit_texts[-1]
    #print len(titles)
    #print len(tit_texts)

    if titles[0] == "":
        del titles[0]
        del tit_texts[0]
    
    #titles = [[w.lower()] for w in titles]
    
    
    
    def clean(myList):    # function to remove duplicates from the list of links generated by mechanize    
        myList2 = []
        for m in myList:
            myList2.append(m)
        try:              
            myList2.sort(key=lambda x: x, reverse=True)
            last = myList2[-1]
            for i in range(len(myList2)-2, -1, -1):
                        if last == myList2[i]:
                            del myList2[i]
                        else:   
                            last = myList2[i]
                
        except IndexError:
            pass
        return myList2
    
    def clean3(myList):    # function to remove duplicates from the list of links generated by mechanize    
        try:              
            myList.sort(key=lambda x: x, reverse=True)
            last = myList[-1]
            for i in range(len(myList)-2, -1, -1):
                        if last == myList[i]:
                            del myList[i]
                        else:   
                            last = myList[i]
                
        except IndexError:
            pass
    
    
    
    def second_largest(numbers):
        m1, m2 = 1, None
        for x in numbers:
            if x >= m1:
                m1, m2 = x, m1
            elif x > m2:
                m2 = x
        return m2
    

    if first is True:
        for nj in range(len(titles)):
            gram = titles[nj]
            if len(gram) > 2:
                data = {}
                index = open('docs/labels/index.txt', 'a')
                grams = open('docs/labels/gram.txt', 'a')
                texts_gram = open('docs/labels/text.txt', 'a')
                match_co = open('docs/labels/match-co.txt', 'a')
                score_f = open('docs/labels/score.txt', 'a')
                gram_index = open('docs/labels/gram_index_for_check.txt', 'a')
                print nj
                print>>gram_index, nj
                for numb in texts_dict.keys():
                    text = texts_dict.get(numb)
                    tok = tit_tok_dict.get(numb)
                    #print numb
                
                    if len(tok) >= 3:
                            if re.search('\+|\?|\!|\"|\'|\*|^\W|\(|\)|\=', gram):
                                gramu = "ABRACADABRA"
                            else:
                                gramu = gram
                            
                            searc = re.search('^'+gramu+'\W|\W'+gramu+'\W|\W'+gramu+'$|^'+gramu+'$', ' '.join(tok), re.I)
                            if searc:
                                print text
                                print gram
                                print tok
                                print "+++++"
                                print>>index, numb
                                print>>grams, gram
                                print>>texts_gram, ', '.join(texts_dict.get(numb))
                                print>>match_co, "None"
                                print>>score_f, "None"
                
    
    def processing(ver,num1,num2):
        for nj in range(num1,num2):
            gram = titles[nj]
            if len(gram) > 2:
                data = {}
                index = open('docs/labels/index'+ver+'.txt', 'a')
                grams = open('docs/labels/gram'+ver+'.txt', 'a')
                texts_gram = open('docs/labels/text'+ver+'.txt', 'a')
                match_co = open('docs/labels/match-co'+ver+'.txt', 'a')
                score_f = open('docs/labels/score'+ver+'.txt', 'a')
                gram_index = open('docs/labels/gram_index_for_check'+ver+'.txt', 'a')
                print nj
                print>>gram_index, nj
                gram_list = [[w.lower()] for w in re.sub('_', ' ', gram).split(' ')]
                content = [[t] for t in tit_texts[nj].split(', ') if t]
                content.extend(gram_list)
                dict_titles = corpora.dictionary.Dictionary(w for w in content)
                diction = sorted([dict_titles.doc2bow(t) for t in content])
                diction = [c[0][0] for c in diction]
                diction_scores = [len(list(group)) for key, group in groupby(diction)]
                diction_clean = list(sorted(set(sorted(diction))))
                for nu in range(len(diction_clean)):
                    data[diction_clean[nu]] = diction_scores[nu]  
                gram_dict = sorted([dict_titles.doc2bow(t) for t in gram_list])
                gram_dict = [c[0][0] for c in gram_dict]
                gram_clean = list(sorted(set(sorted(gram_dict))))
                for na in range(len(gram_clean)):
                    data[gram_clean[na]]+=data.get(gram_clean[na])
                #print ids4words_titles
                for numb in texts_dict.keys():
                    text = texts_dict.get(numb)
                    tok = tit_tok_dict.get(numb)
                    text2 = []
                    if int(var10) == 1:
                        text2.extend(text)
                        text2.extend(text)
                        text = text2
                    #print numb
                    if int(var6) == 1:
                        if len(tok) >= 3:
                                tok = [[stemmer.lemmatize(w)] for w in tok]
                                
                                class TitleBigrams(object):
                                        def __iter__(self):
                                            for t in tok:
                                                # assume there's one document per line, tokens separated by whitespace
                                                yield dict_titles.doc2bow(t)
                                
                                sample_titlecorp = list(TitleBigrams())
                                #print sample_titlecorp
                                sample_titlecorp = [w for w in sample_titlecorp if w]
                                title_ratio = len(sample_titlecorp) / len(tok)
                                if title_ratio > 0.34:
                                    #print title_ratio
                                    if len(text) >= 2:
                                        if int(var7) == 1:                            
                                            clean3(text)
                                        
                                        text = [[w] for w in text]
                                        class TextMatch(object):
                                            def __iter__(self):
                                                for w in text:
                                                    # assume there's one document per line, tokens separated by whitespace
                                                    yield dict_titles.doc2bow(w)
                                        
                                        text_corp = list(TextMatch())
                                        text_corp = [w[0][0] for w in text_corp if w]
                                        text_corp = sorted(text_corp)
                                        result = []
                                        for k in text_corp:
                                            result.append(data.get(k)+1)
                                        for n in range(len(text)-len(result)):
                                            result.append(1)
                                        second_l = second_largest(clean(result))
                                        if (max(result) <= second_l * 2 and max(result) > var8):
                                            match_coef = sum([math.sqrt(s) for s in result]) / len(text)
                                            if (match_coef > var9 and len(text_corp) > len(result) / 3):
                                                print text
                                                print result
                                                print gram
                                                print match_coef
                                                print "+++++"
                                                print>>index, numb
                                                print>>grams, gram
                                                print>>texts_gram, ', '.join(texts_dict.get(numb))
                                                print>>match_co, match_coef
                                                print>>score_f, sum(result) / len(text)
                                                
                        else:
                            if len(text) >= 2:
                                if int(var7) == 1:                            
                                    clean3(text)
                                
                                text = [[w] for w in text]
                                class TextMatch(object):
                                    def __iter__(self):
                                        for w in text:
                                            # assume there's one document per line, tokens separated by whitespace
                                            yield dict_titles.doc2bow(w)
                                
                                text_corp = list(TextMatch())
                                text_corp = [w[0][0] for w in text_corp if w]
                                text_corp = sorted(text_corp)
                                result = []
                                for k in text_corp:
                                    result.append(data.get(k)+1)
                                for n in range(len(text)-len(result)):
                                    result.append(1)
                                second_l = second_largest(clean(result))
                                if (max(result) <= second_l * 2 and max(result) > var8):
                                    match_coef = sum([math.sqrt(s) for s in result]) / len(text)
                                    if (match_coef > var9 and len(text_corp) > len(result) / 3):
                                        print text
                                        print result
                                        print gram
                                        print match_coef
                                        print "+++++"
                                        print>>index, numb
                                        print>>grams, gram
                                        print>>texts_gram, ', '.join(texts_dict.get(numb))
                                        print>>match_co, match_coef
                                        print>>score_f, sum(result) / len(text)
                            
                                    
                    
                    else:
                        if len(text) >= 2:
                            if int(var7) == 1:                            
                                clean3(text)
                            
                            text = [[w] for w in text]
                            class TextMatch(object):
                                def __iter__(self):
                                    for w in text:
                                        # assume there's one document per line, tokens separated by whitespace
                                        yield dict_titles.doc2bow(w)
                            
                            text_corp = list(TextMatch())
                            text_corp = [w[0][0] for w in text_corp if w]
                            text_corp = sorted(text_corp)
                            result = []
                            for k in text_corp:
                                result.append(data.get(k)+1)
                            for n in range(len(text)-len(result)):
                                result.append(1)
                            second_l = second_largest(clean(result))
                            if (max(result) <= second_l * 2 and max(result) > var8):
                                match_coef = sum([math.sqrt(s) for s in result]) / len(text)
                                if (match_coef > var9 and len(text_corp) > len(result) / 3):
                                    print text
                                    print result
                                    print gram
                                    print match_coef
                                    print "+++++"
                                    print>>index, numb
                                    print>>grams, gram
                                    print>>texts_gram, ', '.join(texts_dict.get(numb))
                                    print>>match_co, match_coef
                                    print>>score_f, sum(result) / len(text)
                            
                index.close()
                grams.close()
                texts_gram.close()
                match_co.close()
                score_f.close()
                gram_index.close()
                
    
    
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        processing("",0,len(titles))
    else:
        if multiprocessing.cpu_count() == 8:
            multiprocessing.Process(target=processing, args=("1",0,int(len(titles)/8),))
            multiprocessing.Process(target=processing, args=("2",int(len(titles)/8),int(len(titles)/8)*2,))
            multiprocessing.Process(target=processing, args=("3",int(len(titles)/8)*2,int(len(titles)/8)*3,))
            multiprocessing.Process(target=processing, args=("4",int(len(titles)/8)*3,int(len(titles)/8)*4,))
            multiprocessing.Process(target=processing, args=("5",int(len(titles)/8)*4,int(len(titles)/8)*5,))
            multiprocessing.Process(target=processing, args=("6",int(len(titles)/8)*5,int(len(titles)/8)*6,))
            multiprocessing.Process(target=processing, args=("7",int(len(titles)/8)*6,int(len(titles)/8)*7,))
            multiprocessing.Process(target=processing, args=("8",int(len(titles)/8)*7,len(titles),))
        elif multiprocessing.cpu_count() == 4:
            multiprocessing.Process(target=processing, args=("1",0,int(len(titles)/4),))
            multiprocessing.Process(target=processing, args=("2",int(len(titles)/4),int(len(titles)/4)*2,))
            multiprocessing.Process(target=processing, args=("3",int(len(titles)/4)*2,int(len(titles)/4)*3,))
            multiprocessing.Process(target=processing, args=("4", int(len(titles)/4)*3,len(titles),))
        elif multiprocessing.cpu_count() == 2:
            multiprocessing.Process(target=processing, args=("1",0,int(len(titles)/2),))
            multiprocessing.Process(target=processing, args=("2",int(len(titles)/2),len(titles),))
        else:
            processing("",0,len(titles))