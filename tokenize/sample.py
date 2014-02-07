def tokenize(abstracts):    
    import re
    import nltk
    from gensim import corpora
    from numpy import array
    import numpy
    
    from nltk.stem.wordnet import WordNetLemmatizer
    
    stemmer = WordNetLemmatizer()
    
    
    dict_titles = corpora.dictionary.Dictionary.load('docs/corpora/stopwords-full.dict')
    dict_titles_list = sorted(dict_titles.items(), key=lambda x: x[0])
    
    dtype = [('a',int), ('b',object)]
    
    ids4words_titles = array([(k[0],k[1]) for k in dict_titles_list], dtype=dtype)
    
    texts_file = []
    
    for n in range(len(abstracts)):
        #print n
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
        texts_file.append( ', '.join(text))
                        
    return texts_file