def merger():
    import os,re,sys
    
    direct = 'docs/labels'
    files = [direct+'/'+f for f in os.listdir(direct)]
    
    index = open(direct+'/'+'index.txt', 'a')
    labels = open(direct+'/'+'gram.txt', 'a')
    text = open(direct+'/'+'text.txt', 'a')
    match_coef = open(direct+'/'+'match-co.txt', 'a')
    score = open(direct+'/'+'score.txt', 'a')
    
    
    for f in files:
        if re.search('index\d', f):
            print>>index, open(f).read()
            os.remove(f)
        if re.search('gram\d', f):
            print>>labels, open(f).read()
            os.remove(f)
        if re.search('text\d', f):
            print>>text, open(f).read()
            os.remove(f)
        if re.search('match-co\d', f):
            print>>match_coef, open(f).read()
            os.remove(f)
        if re.search('score\d', f):
            print>>score, open(f).read()
            os.remove(f)
            
    
    index.close()
    labels.close()
    text.close()
    match_coef.close()
    score.close()
    
