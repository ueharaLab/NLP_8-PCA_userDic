import re
import sys
import MeCab
import pandas as pd

def tokenize(sentence):


	csv_input = pd.read_csv('userDic_cooking.csv', encoding='ms932', sep=',',skiprows=0)	
	thesaurus_dict={}
	for key,val in zip(csv_input['key'],csv_input['value']):

		thesaurus_dict[key] = val
	#stopwords_df = pd.read_csv('stopwords.csv', encoding='ms932', sep=',',skiprows=0)

	tagger = MeCab.Tagger("mecabrc -u c:/neologd/NEologd.dic")
	#tagger = MeCab.Tagger("mecabrc")
	node = tagger.parseToNode(sentence)

	tokens = []
	
	while node:            
		
		#features = node.feature.split(',')	
		unique_word=thesaurus_dict.get(node.surface)
		if unique_word != None:	
			tokens.append(unique_word)
		'''	
		if features[0] =='名詞' or features[0] =='形容詞' :
			tokens.append(node.surface)
		elif  features[0] =='動詞' :
			tokens.append(features[6])            
		'''
		node = node.next


	return tokens   
			


