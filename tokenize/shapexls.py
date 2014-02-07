def record(abstract_source, title_source):
    import re
    import csv
    
    from time import strftime
    
    
    csv_data = open('Final/Result-'+str(strftime("%Y%m%d-%H%M"))+'.csv', 'ab')
    a = csv.writer(csv_data, delimiter=',')
    a.writerow(['Title', 'Abstract', 'Index', 'Label', 'Score', 'Match coefficient'])

    abstract_file = open(abstract_source).read().split('\n')
    titles = open(title_source).read().split('\n')                
    
    index = open('docs/labels/index.txt').read().split('\n')
    score = open('docs/labels/score.txt').read().split('\n')
    unigram = open('docs/labels/gram.txt').read().split('\n')
    match_coef = open('docs/labels/match-co.txt').read().split('\n')
    
    del index[-1]
    del score[-1]
    del unigram[-1]
    del match_coef[-1]   
    
    
    for n in range(len(unigram)):
        a.writerow([titles[int(index[n])], abstract_file[int(index[n])], index[n], unigram[n], score[n], match_coef[n]])
        
    csv_data.close()