#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import nltk,json,sys,re,collections
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

verbConst = 1.35
raw = " ".join(sys.argv[1:])

f = open('./suggestions/counts.txt', 'r')
counts = json.loads(f.read())
f.close()

f = open('./suggestions/averages.txt', 'r')
averages = json.loads(f.read())
f.close()


counts_list = []

for c in counts.keys():
	counts_list.append([counts[c],c])

counts_list = sorted(counts_list)
text = nltk.word_tokenize(raw)
recommendations = []

sents = sent_tokenizer.tokenize(raw)

tagged_text = nltk.pos_tag(text)
verbs = [w for (w,tag) in tagged_text if len(re.findall(r'V.*', tag)) > 0]
total_words = len(text)

if total_words < 200:
	recommendations.append("Your text is too small to analyze.")
	print recommendations
	quit()


tag_freqs = dict(collections.Counter([tag for (w,tag) in tagged_text]))
newTag_freqs = {}


tag_dictionary = nltk.defaultdict(str)
tag_dictionary['NN'] = "nouns"
tag_dictionary['VBZ'] = "third person singular verbs"
tag_dictionary['DT'] = "singular pronouns and determiners"
tag_dictionary['WDT'] = "determiners starting with wh such as which, who, what"
tag_dictionary['VBD'] = "verbs of past tense"
tag_dictionary['VBN'] = "past participle verbs"
tag_dictionary['CD'] = "numerals"
tag_dictionary['WRB'] = "adverbs"
tag_dictionary['PPSS'] = "personal pronouns"
tag_dictionary['TO'] = "word to"
tag_dictionary['PP'] = "possesive determiners"
tag_dictionary['VBG'] = "verbs"
tag_dictionary['PPS'] = "third person personal pronouns"
tag_dictionary['CS'] = "conjunctions"
tag_dictionary['NP'] = "singular nouns"
tag_dictionary['RB'] = "adverbs"
tag_dictionary['NNS'] = "plural nouns"
tag_dictionary['JJ'] = "adjectives"
tag_dictionary['AT'] = "articles"
tag_dictionary['IN'] = "prepositions"
tag_dictionary['MD'] = "modal verbs"
tag_dictionary['PPO'] = "personal accusative pronouns"
tag_dictionary['BEDZ'] = "word was"
tag_dictionary['BEZ'] = " word is"

#tag_dictionary[''] = ""

if len(verbs)/len(sents) > 2.6:

	recommendations.append("It seems like your sentences are overloaded with closes, break long sentences into simpler ones.")

for tag in tag_freqs.keys():
	newTag_freqs[tag] =  tag_freqs [tag] / total_words

for tag in tag_freqs.keys():

	try:
		if (newTag_freqs[tag] / counts[tag]) > 2.4:
			if (tag_dictionary[tag] != ""):
				recommendations.append("Try to use less of " + tag_dictionary[tag])
			
			#nltk.help.brown_tagset(tag)

		if (newTag_freqs[tag] / counts[tag]) < 0.6 :
			if (tag_dictionary[tag] != ""):
				recommendations.append("Try to use more of " + tag_dictionary[tag])
			
			
			#nltk.help.brown_tagset(tag)
	except Exception as e:
		1

print recommendations

