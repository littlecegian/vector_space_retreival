import glob
import os
import re
import sys
import time
os.chdir("/home/littlecegian/inforetrieval/simple_search_engine/")
postings = {}
# nsf_award_abstracts
start = time.time()

for filename in glob.glob("nsf_award_abstracts/*/*/*.txt"):
    file_pointer = open(filename, 'r')
    file_content = file_pointer.read()
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
print "time taken to construct index is " + str(end - start) + " seconds"


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
		for filename in list(result_set):
			print re.findall(r"""([a-z0-9]+).txt""", filename, re.VERBOSE)[0] + "  "


print "done"