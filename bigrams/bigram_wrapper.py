def bigraming(data):
	import nltk
	import bigram_finder
	
	
	# Note: this assumes a file already tokenized
	
	# This function is here for the sake of compatibility, please leave it alone
	def normalize (word):
		return word
	
	
	# Read file
	#print "Searching all bigrams"
	#data=open(corpus).read()
	
	# Obtain bigrams with Jordan's code
	if len(data.split('\n'))*0.001 < 5 and len(data.split('\n'))*0.001 > 2:
		bf = bigram_finder.BigramFinder('topicmod/data/stop',[],[],len(data.split('\n'))*0.001,len(data.split('\n'))*0.001)
	elif len(data.split('\n'))*0.001 <= 2:
		bf = bigram_finder.BigramFinder('topicmod/data/stop',[],[],3,3)
	else:
		bf = bigram_finder.BigramFinder('topicmod/data/stop',[],[],5,5)
	bf.create_counts(data.split(', '))
	bf.find_ngrams(data.split(', '))
	big = bf.real_ngrams(0.01)
	
	bigrs = [b[0]+'_'+b[1] for b in big.keys()]
		
	
	return bigrs
	
	