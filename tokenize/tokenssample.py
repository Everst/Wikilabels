def tokenize(source, source2, listbox):    
    import re
    import nltk
    from gensim import corpora
    from numpy import array
    import numpy
    import listboxmes
    
    from nltk.stem.wordnet import WordNetLemmatizer
    
    stemmer = WordNetLemmatizer()
    
    from time import strftime
    
    dict_titles = corpora.dictionary.Dictionary.load('docs/corpora/stopwords-full.dict')
    dict_titles_list = sorted(dict_titles.items(), key=lambda x: x[0])
    
    dtype = [('a',int), ('b',object)]
    
    ids4words_titles = array([(k[0],k[1]) for k in dict_titles_list], dtype=dtype)
    
    dict_titles2 = corpora.dictionary.Dictionary.load('docs/corpora/stopwords-short.dict')
    dict_titles_list2 = sorted(dict_titles2.items(), key=lambda x: x[0])
    
    
    ids4words_titles2 = array([(k[0],k[1]) for k in dict_titles_list2], dtype=dtype)
    
    
    abstract_file = open(source).read()
    abstracts = abstract_file.split('\n')
    if abstracts[-1] == "":
        del abstracts[-1]
        
    print len(abstracts)
    
    texts_file = open('docs/provisional/sample/tokens.txt', 'a')
    
    line = listbox.get(3)
    
    for n in range(len(abstracts)):
        if (n == int(len(abstracts)*0.2) or n == int(len(abstracts)*0.4) or n == int(len(abstracts)*0.6) or n == int(len(abstracts)*0.8) or n == int(len(abstracts)-1)):
            listboxmes.listboxmsg_1half(n,len(abstracts),line,listbox,3)
        abstract = abstracts[n]
        text = nltk.word_tokenize(abstract)
        for t in text:
            loc = text.index(t)
            dotword = re.search('(\w+)\.$', t)
            if dotword:
                text[loc] = dotword.group(1)
        for w in text:
            loca = text.index(w)
            theword = re.search('(\w+)the$', w)
            if theword:
                text[loca] = theword.group(1)
        for w in text:
            loca = text.index(w)
            dotdotword = re.search('([A-Za-z]+)\.([A-Za-z]+)', w)
            if dotdotword:
                text[loca] = dotdotword.group(1)
                text.append(dotdotword.group(2))
        text = [w.lower() for w in text]
        texto = [[w.lower()] for w in text]
        class TitleText(object):
            def __iter__(self):
                for w in texto:
                    # assume there's one document per line, tokens separated by whitespace
                    yield dict_titles.doc2bow(w)
        
        texto = list(TitleText())
        texto = [w for w in texto if w]
        texto = array([(c[0][0],c[0][1]) for c in texto], dtype=dtype)
        words_bad = numpy.intersect1d(texto['a'], ids4words_titles['a'], assume_unique=True)
        words_bad = [int(bi) for bi in words_bad]
        baddy = []
        for bi in words_bad:
            baddy.append(ids4words_titles['b'][bi])
        text = [word for word in text if word not in baddy]
        text = [w for w in text if len(w) >= 3] # remove all tokens less than 3 letters/symbols long
        text = [w for w in text if re.search('[A-Za-z]', w)]
        text = [stemmer.lemmatize(w) for w in text]
        print>>texts_file, ', '.join(text)
                        
    texts_file.close()
    
    abstract_file = open(source2).read()
    abstracts = abstract_file.split('\n')
    if abstracts[-1] == "":
        del abstracts[-1]
    print len(abstracts)
    
    texts_file = open('docs/provisional/sample/title-tokens.txt', 'a')
    
    for n in range(len(abstracts)):
        if (n == int(len(abstracts)*0.2) or n == int(len(abstracts)*0.4) or n == int(len(abstracts)*0.6) or n == int(len(abstracts)*0.8) or n == int(len(abstracts)-1)):
            listboxmes.listboxmsg_2half(n, len(abstracts), line, listbox, 3)
        abstract = abstracts[n]
        text = nltk.word_tokenize(abstract)
        for t in text:
            loc = text.index(t)
            dotword = re.search('(\w+)\.$', t)
            if dotword:
                text[loc] = dotword.group(1)
        for w in text:
            loca = text.index(w)
            theword = re.search('(\w+)the$', w)
            if theword:
                text[loca] = theword.group(1)
        for w in text:
            loca = text.index(w)
            dotdotword = re.search('([A-Za-z]+)\.([A-Za-z]+)', w)
            if dotdotword:
                text[loca] = dotdotword.group(1)
                text.append(dotdotword.group(2))
        text = [w.lower() for w in text]
        texto = [[w.lower()] for w in text]
        class TitleText(object):
            def __iter__(self):
                for w in texto:
                    # assume there's one document per line, tokens separated by whitespace
                    yield dict_titles2.doc2bow(w)
        
        texto = list(TitleText())
        texto = [w for w in texto if w]
        texto = array([(c[0][0],c[0][1]) for c in texto], dtype=dtype)
        words_bad = numpy.intersect1d(texto['a'], ids4words_titles2['a'], assume_unique=True)
        words_bad = [int(bi) for bi in words_bad]
        baddy = []
        for bi in words_bad:
            baddy.append(ids4words_titles2['b'][bi])
        text = [word for word in text if word not in baddy]
        text = [w for w in text if len(w) >= 3] # remove all tokens less than 3 letters/symbols long
        text = [w for w in text if re.search('[A-Za-z]', w)]
        #text = [stemmer.lemmatize(w) for w in text]
        print>>texts_file, ', '.join(text)
                        
    texts_file.close()

