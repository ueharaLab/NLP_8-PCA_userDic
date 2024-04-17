import re
import sys
import MeCab
import pandas as pd

def tokenize(sentence):


	textures_df = pd.read_csv('./data/texture_ners.csv', encoding='ms932', sep=',',skiprows=0)	
	textures = textures_df['texture'].values.tolist()
	ingred_df = pd.read_csv('./data/ingredient_ners.csv', encoding='ms932', sep=',',skiprows=0)	
	ingredients = ingred_df['ingredient'].values.tolist()

	tagger = MeCab.Tagger("mecabrc -u c:/neologd/NEologd.dic")
	#tagger = MeCab.Tagger("mecabrc")
	node = tagger.parseToNode(sentence)

	tokens = []
	
	while node:            
		
		#features = node.feature.split(',')	
		#unique_word=thesaurus_dict.get(node.surface)
		if node.surface in ingredients:	
			tokens.append(node.surface)
		'''	
		if features[0] =='名詞' or features[0] =='形容詞' :
			tokens.append(node.surface)
		elif  features[0] =='動詞' :
			tokens.append(features[6])            
		'''
		node = node.next


	return tokens   
			


