def potential(save_path, listbox):
    import re
    import nltk
    import collections
    from nltk.stem.wordnet import WordNetLemmatizer
    from numpy import array
    import numpy
    from gensim import corpora
    from bigrams import bigram_wrapper
    
    from time import strftime
    
    dict_titles = corpora.dictionary.Dictionary.load('docs/wiki-titles/wiki-titles.dict')
    dict_titles_list = sorted(dict_titles.items(), key=lambda x: x[0])
    
    dtype = [('a',int), ('b',object)]
    
    ids4words_titles = array([(k[0],k[1]) for k in dict_titles_list], dtype=dtype)
    
    
    stemmer = WordNetLemmatizer()
    
    #file to write bigrams, trigrams,and unigrams
    
    def potlab(tokversion):
        if save_path is None:
            labels_file = open('docs/provisional/potential-labels.txt', 'a')
        else:
            labels_file = open(str(save_path)+'/potential-labels.txt', 'a')
        filed = open('docs/provisional/tokens'+tokversion+'.txt').read()
        str678 = re.compile('\.\.')
        filed = str678.sub('', filed)
        
        texts = filed.split('\n')
        if texts[-1] == "":
            del texts[-1]
        #print len(texts)
        texts = [[w for w in text.split(', ')] for text in texts]
        
        #analyze bigrams
        bigrams_NSF = bigram_wrapper.bigraming(filed)
        #print len(bigrams_NSF)
        
        
        bigrams_NSF = [[w] for w in bigrams_NSF]
        class TitleBigrams(object):
                def __iter__(self):
                    for text in bigrams_NSF:
                        # assume there's one document per line, tokens separated by whitespace
                        yield dict_titles.doc2bow(text)
        
        bigrams_titlecorp = list(TitleBigrams())
        bigrams_titlecorp = [w for w in bigrams_titlecorp if w]
        bigrams_titlecorp = array([(c[0][0],c[0][1]) for c in bigrams_titlecorp], dtype=dtype)
        bititle_exist = numpy.intersect1d(bigrams_titlecorp['a'], ids4words_titles['a'], assume_unique=True)
        #print len(bititle_exist)
        bititle_exist = [int(bi) for bi in bititle_exist]
        
        for bi in bititle_exist:
            #pass
            print>>labels_file, ids4words_titles['b'][bi]
        
        texts_freq = [list(set(text)) for text in texts]
        #print len(texts_freq)
        
        all_tokens = []
        for text in texts_freq:
            for t in text:
                all_tokens.append(t)
        #print len(all_tokens)
        
        fdist = nltk.FreqDist(all_tokens)
        if len(texts)*0.001 <= 2: 
            freq = [k for k,v in fdist.items() if v > 2]
        else:
            freq = [k for k,v in fdist.items() if v > len(texts)*0.001]
        #print len(freq)
        
        freq = sorted(freq, reverse=True)
        last = freq[-1]
        for i in range(len(freq)-2, -1, -1):
            if stemmer.lemmatize(last) == stemmer.lemmatize(freq[i]):
                del freq[i]
            else:
                last = freq[i]
        #print len(freq)
        
        freq = sorted(freq)
        freq = [[w] for w in freq]
        
        class TitleUnigrams(object):
                def __iter__(self):
                    for text in freq:
                        # assume there's one document per line, tokens separated by whitespace
                        yield dict_titles.doc2bow(text)
        
        unigrams_titlecorp = list(TitleUnigrams())
        unigrams_titlecorp = [w for w in unigrams_titlecorp if w]
        unigrams_titlecorp = array([(c[0][0],c[0][1]) for c in unigrams_titlecorp], dtype=dtype)
        unititle_exist = numpy.intersect1d(unigrams_titlecorp['a'], ids4words_titles['a'], assume_unique=True)
        #print len(unititle_exist)
        unititle_exist = [int(bi) for bi in unititle_exist]
        
        for uni in unititle_exist:
            #pass
            print>>labels_file, ids4words_titles['b'][uni]
        labels_file.close()
    
    line = listbox.get(1)
    potlab("1")
    line+="50%"
    listbox.delete(1)
    listbox.insert(1,line)
    potlab("2")
    line+="...Done!"
    listbox.delete(1)
    listbox.insert(1,line)