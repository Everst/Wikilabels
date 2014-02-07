def finalize(tokens_path, wiki_titles, wiki_tokens,left):
    import sys,re
    from gensim import corpora
    #from numpy import array
    #from itertools import groupby
    import multiprocessing
    #import numpy
    
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
    
    if titles[0] == "":
        del titles[0]
        del tit_texts[0]

    
    
    
                
    def processing(ver,num1,num2):
        for i in texts_dict.keys()[num1:num2]:
            data = {}
            dato = {}
            index = open('docs/labels/index'+ver+'.txt', 'a')
            grams = open('docs/labels/gram'+ver+'.txt', 'a')
            texts_gram = open('docs/labels/text'+ver+'.txt', 'a')
            match_co = open('docs/labels/match-co'+ver+'.txt', 'a')
            score_f = open('docs/labels/score'+ver+'.txt', 'a')
            print i
            v = texts_dict.get(i)
            v.extend(tit_tok_dict.get(i))
            text = [[w] for w in v]
            dict_titles = corpora.dictionary.Dictionary(w for w in text)
            for n in range(len(titles)):
                tok = tit_texts[n]
                tok = [[w] for w in tok.split(', ') if w]
                class TitleText(object):
                    def __iter__(self):
                        for w in tok:
                            # assume there's one document per line, tokens separated by whitespace
                            yield dict_titles.doc2bow(w)
                texto = list(TitleText())
                texto = [w for w in texto if w]
                dato[titles[n]] = len(texto)
                texty = [c[0][0] for c in texto]
                var50 = len(sorted(set(sorted(texty))))
                data[titles[n]] = var50
                
            
            datum = sorted(dato.items(), key=lambda x: -x[1])
            if datum[0][1] > 11:
                print>>grams,datum[0][0]
                print>>score_f,datum[0][1]
                print>>match_co,float(data.get(datum[0][0]))/float(len(text))
                print>>texts_gram, v
                print>>index, i
                
            if (datum[1][1]>11 and (datum[0][1]-datum[1][1])<5):
                print>>grams,datum[1][0]
                print>>score_f,datum[1][1]
                print>>match_co,float(data.get(datum[1][0]))/float(len(text))
                print>>texts_gram, v
                print>>index, i
                
            if (datum[2][1]>11 and (datum[0][1]-datum[2][1])<5):
                print>>grams,datum[2][0]
                print>>score_f,datum[2][1]
                print>>match_co,float(data.get(datum[2][0]))/float(len(text))
                print>>texts_gram, v
                print>>index, i
                
            if (datum[3][1]>11 and (datum[0][1]-datum[3][1])<5):
                print>>grams,datum[3][0]
                print>>score_f,datum[3][1]
                print>>match_co,float(data.get(datum[3][0]))/float(len(text))
                print>>texts_gram, v
                print>>index, i
                
            index.close()
            grams.close()
            texts_gram.close()
            match_co.close()
            score_f.close()
                            
                    
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        processing("",0,len(texts_dict.keys()))
    else:
        if multiprocessing.cpu_count() == 8:
            multiprocessing.Process(target=processing, args=("1",0,int(len(texts_dict.values())/8),))
            multiprocessing.Process(target=processing, args=("2",int(len(texts_dict.values())/8),int(len(texts_dict.values())/8)*2,))
            multiprocessing.Process(target=processing, args=("3",int(len(texts_dict.values())/8)*2,int(len(texts_dict.values())/8)*3,))
            multiprocessing.Process(target=processing, args=("4",int(len(texts_dict.values())/8)*3,int(len(texts_dict.values())/8)*4,))
            multiprocessing.Process(target=processing, args=("5",int(len(texts_dict.values())/8)*4,int(len(texts_dict.values())/8)*5,))
            multiprocessing.Process(target=processing, args=("6",int(len(texts_dict.values())/8)*5,int(len(texts_dict.values())/8)*6,))
            multiprocessing.Process(target=processing, args=("7",int(len(texts_dict.values())/8)*6,int(len(texts_dict.values())/8)*7,))
            multiprocessing.Process(target=processing, args=("8",int(len(texts_dict.values())/8)*7,len(texts_dict.values()),))
        elif multiprocessing.cpu_count() == 4:
            multiprocessing.Process(target=processing, args=("1",0,int(len(texts_dict.values())/4),))
            multiprocessing.Process(target=processing, args=("2",int(len(texts_dict.values())/4),int(len(texts_dict.values())/4)*2,))
            multiprocessing.Process(target=processing, args=("3",int(len(texts_dict.values())/4)*2,int(len(texts_dict.values())/4)*3,))
            multiprocessing.Process(target=processing, args=("4", int(len(texts_dict.values())/4)*3,len(texts_dict.values()),))
        elif multiprocessing.cpu_count() == 2:
            multiprocessing.Process(target=processing, args=("1",0,int(len(texts_dict.values())/2),))
            multiprocessing.Process(target=processing, args=("2",int(len(texts_dict.values())/2),len(texts_dict.values()),))
        else:
            processing("",0,len(texts_dict.values()))