def count():
    import re
    
    corpus = open('docs/provisional/sample/title-tokens.txt').read().split('\n')
    if corpus[-1] == "":
        del corpus[-1]
    full = range(len(corpus))
    
    
    index = open('docs/labels/index.txt').read().split('\n')
    index = [int(i) for i in index if i]
            
    left = []
    
    index = list(sorted(set(sorted(index))))
    
    for i in full:
        if i not in index:
            left.append(i)
    
    match_coef = open('docs/labels/match-co.txt').read().split('\n')
    for n in range(len(index)):
        if match_coef[n] == "None":
            if index[n] not in left:
                left.append(index[n])
    
    left = list(sorted(set(sorted(left))))
    
    
    return left