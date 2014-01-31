import glob
import os
import re
import sys
import time
import collections
import numpy as np
import math


def boolean_retrieval(tokens):
	if postings.has_key(tokens[0]):
		result_set = set(postings[tokens[0]].keys())
	else:
		print "sorry, no match"
		return

	no_match = 0
	for token in tokens:
		try:
			result_set &= set(postings[token].keys())
		except KeyError:
			result_set = set([])
			no_match = 1
			break

	if (no_match == 1 or len(list(result_set)) == 0):
		print "sorry, no match"
	else:
		for filename in list(result_set):
			print re.findall(r"""([a-z0-9]+).txt""", filename, re.VERBOSE)[0]

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


def vector_retrieval(tokens):
	filenames = []
	for token in tokens:
		query_tf[token] += 1
		filenames.extend(postings[token].keys())
	filenames = list(set(filenames))
	for filename in filenames:
		cosine_similarities[filename] =	cosine_similarity(flipped[filename], query_tf)
	ranked_results = sorted(cosine_similarities.items(), key=lambda x: x[1], reverse=True)
	for result in ranked_results[:50]:
		print re.findall(r"""([a-z0-9]+).txt""", result[0], re.VERBOSE)[0], result[1]

os.chdir("/home/littlecegian/inforetrieval/simple_search_engine/")
postings = collections.defaultdict(dict)
flipped = collections.defaultdict(dict)
idf_values = collections.defaultdict()
query_tf = collections.defaultdict(int)
cosine_similarities = collections.defaultdict(int)
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

# print "document_count is " + str(document_count)
end = time.time()

print "index has been built successfully"
print "time taken to construct index is " + str(end - start) + " seconds"

print "computing idf for each term . . . . . . ."

start = time.time()

for key in postings.keys():
	idf_values[key] = np.log10(document_count/len(postings[key]))
	for doc_name in postings[key].keys():
		postings[key][doc_name] = (1 + np.log10(postings[key][doc_name])) * (idf_values[key])

for key, val in postings.items():
    for subkey, subval in val.items():
        flipped[subkey][key] = subval


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
	retrieval_mode = tokens.pop(0)
	if(retrieval_mode == "bool"):
		boolean_retrieval(tokens)
	elif(retrieval_mode == "vector"):
		vector_retrieval(tokens)