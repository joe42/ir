# -*- coding: utf-8 -*-
#!/bin/python
'''
Created on 13.11.2011

@author: joe
'''
#n_k anzahl der dokumente die begriff k enthalten
#tf_dk = 1 (vorkommenshäufigkeit des begriffs k in dokument d)
#w_dk = wortgewicht des terms k für dokument (oder die anfrage d)
#Dokumentenvektor = (w_d1; w_d2...w_dt)
#Anfragevektor= (w_q1; w_q2...w_qt)
#mit t termen im vokabular
#tf = term frequency
#idf inverse document frequency: je seltener der begriff je höher idf
import re
from collections import defaultdict
from ordereddict import OrderedDict

IDF = 0
DOCUMENTS = 2

def get_file_content_between(file, start, end):
    line_cnt = 0;
    ret = ""
    for line in open(file):
        line_cnt += 1;
        if line_cnt >= start:
            ret += line
        if line_cnt >= end:
            break
    return ret

def text_to_list_db(text_db):
    """:return: list of triples containing a keyword its single idf for all documents and a list of documents it occurs in: (idf, word, document_list)"""
    text_vocabulary = get_file_content_between( text_db,3,70 )
    ret = {}
    for line in text_vocabulary.splitlines():
        columns = line.split()
        try:
            first_index_in_line = int(columns[0])
            ret[first_index_in_line] = (float(columns[1]), columns[2], []) 
            second_index_in_line = int(columns[3])
            ret[second_index_in_line] = (float(columns[4]), columns[5], [])  
            third_index_in_line = int(columns[6])
            ret[third_index_in_line] = (float(columns[7]), columns[8], [])  
        except IndexError:
            pass
    text_document_vectors = get_file_content_between( text_db,74,111 )
    document_cnt = 0
    for line in text_document_vectors.splitlines():
        document_cnt += 1
        vacabulary_indices = re.findall('\\b\\d+\\b', line)
        for id in vacabulary_indices:
            ret[int(id)][DOCUMENTS].append(document_cnt)
    return ret

def text_to_query_db(text_query_db):
    ret = {}
    query_cnt = 0
    for line in text_query_db.splitlines():
        query_cnt += 1
        ret[query_cnt] = []
        query_keyword_ids = re.findall('\\b\\d+\\b', line)
        for id in query_keyword_ids:
            ret[query_cnt].append(int(id))
    return ret

def text_to_relevant_documents_db(text_relevant_document_db):
    ret = {}
    relevant_document_cnt = 0
    for line in text_relevant_document_db.splitlines():
        relevant_document_cnt += 1
        ret[relevant_document_cnt] = []
        relevant_document_ids = re.findall('\\b\\d+\\b', line)
        for id in relevant_document_ids:
            ret[relevant_document_cnt].append(int(id))
    return ret

TEXT_DB = "text_db"
list_db = text_to_list_db(TEXT_DB)
text_queries = get_file_content_between( TEXT_DB,115,119 )
query_db = text_to_query_db(text_queries)
answers = []

for query in query_db.values():
    answer = defaultdict(float)
    answers.append(answer)
    for keyword_id in query:
        for document_id in list_db[keyword_id][DOCUMENTS]:
            answer[document_id] += list_db[keyword_id][IDF]    
    answer = OrderedDict(sorted(answer.items(), key=lambda t: -t[1]))
    print repr(answer)
text_relevant_documents_db = get_file_content_between( TEXT_DB,135,139 )
relevant_documents_db = text_to_relevant_documents_db(text_relevant_documents_db)

for i in range( 1, len(query_db)+1 ):
    answer = answers[i-1]
    relevant_documents = relevant_documents_db[i]
    max_nr_of_hits = len(relevant_documents)
    nr_of_retrieved_documents =0
    nr_of_hits = 0.0
    precision =  0
    recall = 0
    print "\nAnswer "+str(i)
    for document_id in answer:
        nr_of_retrieved_documents += 1
        if document_id in relevant_documents:
            nr_of_hits += 1 
        precision =  nr_of_hits/nr_of_retrieved_documents
        recall = nr_of_hits/max_nr_of_hits
        if precision != 0 and recall != 0:
            F_recall_precision = 2.0/(1/precision+1/recall)
            print "nr_of_retrieved_documents: %s F: %s"%(nr_of_retrieved_documents,F_recall_precision)
























