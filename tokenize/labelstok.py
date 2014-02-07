def labelstokenize(source, path, addup, addup_tokens, addup_titles, save_path, listbox):
    import re
    import nltk
    from gensim import corpora
    from numpy import array
    import numpy
    
    import mechanize
    from lxml import etree
    import lxml.html
    import cookielib
    import listboxmes
    
    
    from nltk.stem.wordnet import WordNetLemmatizer
    
    stemmer = WordNetLemmatizer()
    
    from time import strftime
    print "1.  " + strftime("%m-%d-%Y %H:%M:%S")
    
    #open browser for wikipedia
    br = mechanize.Browser()
    br.set_handle_robots(False)  # bypass robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Firefox')]  # Some websites demand a user-agent that isn't a robot
    
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    dict_titles = corpora.dictionary.Dictionary.load('docs/corpora/stopwords-full.dict')
    dict_titles_list = sorted(dict_titles.items(), key=lambda x: x[0])
    
    dtype = [('a',int), ('b',object)]
    
    ids4words_titles = array([(k[0],k[1]) for k in dict_titles_list], dtype=dtype)
    
    titles = open(path).read()
    titles = re.sub(r'\\', '', titles)
    slash = list(re.finditer('([a-z])(/)([a-z])', titles))
    if slash:
        for s in slash:
            titles.replace(s.group(1)+s.group(2)+s.group(3), s.group(1)+", "+s.group(3))
    titles = titles.split('\n')
    #titles = list(sorted(set(sorted(titles))))
    if titles[-1] == "":
        del titles[-1]
    print len(titles)
    print "4.  " + strftime("%m-%d-%Y %H:%M:%S")
    
    
    if save_path is None:
        gramu = open('docs/provisional/wikilabels-precise.txt', 'a')
        texts_file = open('docs/provisional/tokens-wikilabels.txt', 'a')
        real_t = open('docs/provisional/real-titles-wiki.txt', 'a')
    else:
        gramu = open(str(save_path)+'/wikilabels-precise.txt', 'a')
        texts_file = open(str(save_path)+'/tokens-wikilabels.txt', 'a')
        real_t = open(str(save_path)+'/real-titles-wiki.txt', 'a')
    
    
    
    if addup is not None:
        if addup_tokens and addup_titles:
            toks_add = open(addup_tokens).read()
            tit_add = open(addup_titles).read()
            print>>texts_file, toks_add
            print>>real_t, tit_add
            print>>gramu, tit_add 
            titles2 = open(addup).read().split('\n')
            if titles2[-1] == "":
                del titles2[-1]
            tit_good = []
            for t in titles:
                if t not in titles2:
                    tit_good.append(t)
            titles = tit_good
        elif addup_tokens and not addup_titles:
            print>>texts_file, open(addup_tokens).read()
            titles2 = open(addup).read().split('\n')
            if titles2[-1] == "":
                del titles2[-1]
            for t in titles2:
                print>>real_t, t
                print>>gramu, t
            tit_good = []
            for t in titles:
                if t not in titles2:
                    tit_good.append(t)
            titles = tit_good 
        else:
            titles2 = open(addup).read()
            titles2 = re.sub(r'\\', '', titles2)
            slash = list(re.finditer('([a-z])(/)([a-z])', titles2))
            if slash:
                for s in slash:
                    titles2.replace(s.group(1)+s.group(2)+s.group(3), s.group(1)+", "+s.group(3))
            titles2 = titles2.split('\n')
            titles2 = list(sorted(set(sorted(titles2))))
            titles.extend(titles2)
        
    
    titles = [w.lower() for w in titles]
    titles = [re.sub(' ', '_', t) for t in titles]
    if titles[-1] == "":
        del titles[-1]
    titles = list(sorted(set(sorted(titles))))
        
    str888 = re.compile('[\n\t\r\f]+|<.*?>|^[\W_]+?|[\W_]+?$|&.*?;|<!--.*?-->', re.DOTALL)
    str000 = re.compile('<table.*?>.*?</table.*?>|<select.*?>.*?</select.*?>|<script.*?>.*?</script.*?>|{.*}|<noscript>.*?</noscript>', re.DOTALL)
    str123 = re.compile('\[.*?\]')
    str908 = re.compile('&#8211;|&#8212;')
    
    unique = []
    cate = []
    
    line = listbox.get(2)
    
    for nk in range(len(titles)):
        w = titles[nk]
        if (nk == int(len(titles)*0.2) or nk == int(len(titles)*0.4) or nk == int(len(titles)*0.6) or nk == int(len(titles)*0.8) or nk == int(len(titles)-1)):
            listboxmes.listboxmsg_1half(nk,len(titles),line,listbox,2)
        try:
            abstsearch = []
            if re.search('_', w):
                abstsearch.extend([w.lower(), w.upper(), w.title()])
            else:
                abstsearch.extend([w.lower(), w.upper()])
            for gram in abstsearch:
                        print gram
                        try:
                            resp = br.open('http://en.wikipedia.org/wiki/' + gram)
                            resp2 = resp.get_data()
                            doc = lxml.html.document_fromstring(resp2)
                            titles_wiki = doc.cssselect('h1#firstHeading')
                            for t in titles_wiki:
                                title = etree.tostring(t).decode('utf-8')
                                title = str908.sub('-', title)
                                title = str888.sub('', title)
                                title = str000.sub('', title)
                                title = str123.sub('', title)
                                if title not in unique:
                                    unique.append(title)
                                    print>>real_t, title
                                    recs = doc.cssselect('div#mw-content-text')
                                    for r in recs:
                                        content = etree.tostring(r).decode('utf-8')
                                        disa = re.search('page lists articles associated with the same title', content)
                                        if disa:
                                            linko = list(re.finditer('href="/wiki/(.*?)"', content))
                                            if linko:
                                                for li in linko:
                                                    helpy = re.search('File:|Help:', li.group(1))
                                                    if helpy is None:
                                                        cate.append(li.group(1))
                                     
                                        else:
                                            content = str888.sub(' ', content)
                                            content = str000.sub(' ', content)
                                            content = str123.sub(' ', content)
                                            text = nltk.word_tokenize(content)
                                            for numb in range(len(text)):
                                                dotword = re.search('(\w+)\.$', text[numb])
                                                if dotword:
                                                    text[numb] = dotword.group(1)
                                                theword = re.search('(\w+)the$', text[numb])
                                                if theword:
                                                    text[numb] = theword.group(1)
                                                dotdotword = re.search('([A-Za-z]+)\.([A-Za-z]+)', text[numb])
                                                if dotdotword:
                                                    text[numb] = dotdotword.group(1)
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
                                            words_bad = numpy.intersect1d(texto['a'], ids4words_titles['a']) #, assume_unique=True)
                                            words_bad = [int(bi) for bi in words_bad]
                                            baddy = []
                                            for bi in words_bad:
                                                baddy.append(ids4words_titles['b'][bi])
                                            
                                            text = [word for word in text if word not in baddy]
                                            text = [w for w in text if len(w) >= 3] # remove all tokens less than 3 letters/symbols long
                                            text = [w for w in text if re.search('[A-Za-z]', w)]
                                            text = [stemmer.lemmatize(w) for w in text]
                                            text = [str(w) for w in text]
                                            print>>gramu, gram
                                            print>>texts_file, ', '.join(text)
                                else:
                                    pass
                                        
                        except:
                            print "___"
                            print gram
                            print "___"
    
                    
        except:
            print "bad symbols"
    
    
    cate = list(sorted(set(sorted(cate))))
    
    for gram in cate:
        listboxmes.listboxmsg_2half(cate.index(gram),len(cate),line,listbox,2)
        try:
            resp = br.open('http://en.wikipedia.org/wiki/' + gram)
            resp2 = resp.get_data()
            doc = lxml.html.document_fromstring(resp2)
            titles_wiki = doc.cssselect('h1#firstHeading')
            for t in titles_wiki:
                title = etree.tostring(t).decode('utf-8')
                title = str908.sub('-', title)
                title = str888.sub('', title)
                title = str000.sub('', title)
                title = str123.sub('', title)
                if title not in unique:
                    unique.append(title)
                    print>>real_t, title
                    recs = doc.cssselect('div#mw-content-text')
                    for r in recs:
                        content = etree.tostring(r).decode('utf-8')
                        content = str888.sub(' ', content)
                        content = str000.sub(' ', content)
                        content = str123.sub(' ', content)
                        text = nltk.word_tokenize(content)
                        for numb in range(len(text)):
                            dotword = re.search('(\w+)\.$', text[numb])
                            if dotword:
                                text[numb] = dotword.group(1)
                            theword = re.search('(\w+)the$', text[numb])
                            if theword:
                                text[numb] = theword.group(1)
                            dotdotword = re.search('([A-Za-z]+)\.([A-Za-z]+)', text[numb])
                            if dotdotword:
                                text[numb] = dotdotword.group(1)
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
                        words_bad = numpy.intersect1d(texto['a'], ids4words_titles['a']) #, assume_unique=True)
                        words_bad = [int(bi) for bi in words_bad]
                        baddy = []
                        for bi in words_bad:
                            baddy.append(ids4words_titles['b'][bi])
                        
                        text = [word for word in text if word not in baddy]
                        text = [w for w in text if len(w) >= 3] # remove all tokens less than 3 letters/symbols long
                        text = [w for w in text if re.search('[A-Za-z]', w)]
                        text = [stemmer.lemmatize(w) for w in text]
                        text = [str(w) for w in text]
                        print>>gramu, gram
                        print>>texts_file, ', '.join(text)
                else:
                    pass
                        
        except:
            print "___"
            print gram
            print "___"
    
    
            
    gramu.close()
    texts_file.close()
    real_t.close()
                            
