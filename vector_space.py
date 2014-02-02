import glob
import os
import re
import sys
import time
import collections
import numpy as np
import math


# def get_vector(filename):
# 	file_pointer = open(filename, 'r')
# 	file_content = file_pointer.read()
# 	tokens = re.findall('[a-z0-9]+', file_content.lower())
# 	tfidf_vector = collections.defaultdict(int)
# 	for token in tokens:
# 		tfidf_vector[token] = postings[token][filename]
# 	return tfidf_vector


def boolean_retrieval(tokens):
	if postings.has_key(tokens[0]):
		result_set = set(postings[tokens[0]].keys())
	else:
		print "sorry, no match"
		return

	for token in tokens:
		result_set &= set(postings[token].keys())

	if (len(list(result_set)) == 0):
		print "sorry, no match"
	else:
		for filename in list(result_set):
			print re.findall(r"""([a-z0-9]+).txt""", filename, re.VERBOSE)[0]

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
	cosine_similarities = collections.defaultdict(int)
	query_tf = collections.defaultdict(int)
	ranked_results = []
	for token in tokens:
		query_tf[token] += 1
		filenames.extend(postings[token].keys())
	filenames = list(set(filenames))
	for filename in filenames:
		cosine_similarities[filename] =	cosine_similarity(query_tf, flipped[filename])
	ranked_results = sorted(cosine_similarities.items(), key=lambda x: x[1], reverse=True)
	for result in ranked_results[:50]:
		print re.findall(r"""([a-z0-9]+).txt""", result[0], re.VERBOSE)[0], result[1]

os.chdir("./")
postings = collections.defaultdict(lambda: collections.defaultdict(int))
flipped = collections.defaultdict(lambda: collections.defaultdict(int))
idf_values = collections.defaultdict(int)
start = time.time()
output_filenames = []
document_count = 0

print "building index . . . . . . ."
for filename in glob.glob("nsf_award_abstracts/*/*/*.txt"):
    file_pointer = open(filename, 'r')
    file_content = file_pointer.read()
    document_count += 1
    tokens = re.findall('[a-z0-9]+', file_content.lower())
    for token in tokens:
    	postings[token][filename] += 1
    file_pointer.close()

# print "document_count is " + str(document_count)
end = time.time()

print "index has been built successfully"
print "time taken to construct index is " + str(end - start) + " seconds"

print "computing idf for each term . . . . . . ."

start = time.time()

for key in postings.keys():
	idf_values[key] = math.log(document_count/len(postings[key]))/math.log(10)
	for doc_name in postings[key].keys():
		postings[key][doc_name] = (1 + (math.log(postings[key][doc_name]) / math.log(10))) * (idf_values[key])

print "creating a tf-idf vector for all documents . . . . . . ."

for key, val in postings.items():
    for subkey, subval in val.items():
        flipped[subkey][key] = subval


end = time.time()

print "tf-idf has been updated for each word in each document"
print "time taken is " + str(end - start) + " seconds"

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