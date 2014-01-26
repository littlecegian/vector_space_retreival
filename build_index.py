import glob
import os
import re
import sys
import time
import collections
import numpy as np
import math

def get_vector(filename):
	file_pointer = open(filename, 'r')
	file_content = file_pointer.read()
	tokens = re.findall('[a-z0-9]+', file_content.lower())
	tfidf_vector = collections.defaultdict(int)
	for token in tokens:
		tfidf_vector[token] = postings[token][filename]
	return tfidf_vector

def cosine_similarity(query_tf, tfidf_vector):
	nr = 0
	mod_query = 0
	mod_document = 0
	for key in query_tf.keys():
		nr += query_tf[key] * tfidf_vector[key]
		mod_query += query_tf[key] * query_tf[key]

	mod_query = math.sqrt(mod_query)
	for key in tfidf_vector.keys():
		mod_document += tfidf_vector[key] * tfidf_vector[key]
	mod_document = math.sqrt(mod_document)

	cosine = nr/(mod_document*mod_query)
	return cosine

os.chdir("/home/littlecegian/inforetrieval/simple_search_engine/")
postings = {}
idf_values = collections.defaultdict()
query_tf = collections.defaultdict(int)
# nsf_award_abstracts
start = time.time()
output_filenames = []
document_count = 0

for filename in glob.glob("nsf_award_abstracts/*/*/*.txt"):
    file_pointer = open(filename, 'r')
    file_content = file_pointer.read()
    document_count += 1
    tokens = re.findall('[a-z0-9]+', file_content.lower())
    for token in tokens:
    	try:
    		postings[token][filename] += 1
    	except KeyError:
    		if postings.has_key(token):
    			postings[token][filename] = 1
    		else:
    			postings[token] = {}
    			postings[token][filename] = 1
    file_pointer.close()


end = time.time()

print "index has been built successfully"
print "time taken to construct index is " + str(end - start) + " seconds"

print "computing idf for each term . . . . . . ."

start = time.time()

for key in postings.keys():
	idf_values[key] = np.log10(document_count/len(postings[key]))
	for doc_name in postings[key].keys():
		postings[key][doc_name] *= idf_values[key]

end = time.time()

print "tf-idf has been updated for each word in each document"
print "time taken to do that is " + str(end - start) + " seconds"

print "done"

while(1):
	print "Please enter a query"
	query = raw_input().lower()
	if (query == 'exit'):
		break
	tokens = re.findall('[a-z0-9]+', query)
	# print tokens
	if postings.has_key(tokens[0]):
		result_set = set(postings[tokens[0]].keys())
	else:
		print "sorry, no match"
		# result_set = set([])
		continue

	continue_var = 0
	for token in tokens:
		query_tf[token] += 1
		try:
			result_set &= set(postings[token].keys())
		except KeyError:
			print "sorry, no match"
			result_set = set([])
			continue_var = 1
			continue

	if (continue_var == 1):
		continue
	if(len(list(result_set)) == 0):
		print "sorry, no match"
	else:
		# this means that all the tokens are present in certain documents. Now we have to find the cosine similarity
		for filename in list(result_set):
			tfidf_vector = get_vector(filename)
			print re.findall(r"""([a-z0-9]+).txt""", filename, re.VERBOSE)[0], cosine_similarity(query_tf, tfidf_vector)
			# output_filenames.append(re.findall(r"""([a-z0-9]+).txt""", filename, re.VERBOSE)[0])
		# print len(output_filenames)
		# for name in filenames:
		# 	print name + cosine_similarity(query_tf, )