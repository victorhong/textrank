"""
This code was inspired by Alex Kessinger's (http://github.com/voidfiles) textrank.py code.

It is base on this paper: http://acl.ldc.upenn.edu/acl2004/emnlp/pdf/Mihalcea.pdf 

"""
import nltk
import itertools
from operator import itemgetter

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.pagerank import pagerank
from pygraph.classes.exceptions import AdditionError


def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP', 'NNS']):
    return [item for item in tagged if item[1] in tags]

def normalize(tagged):
    skip_list = ['[', ']', '(', ')']
    return [(item[0].replace('.', ''), item[1]) for item in tagged if item[0] not in skip_list]

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element



def co_occurence_edge(graph, window_size=2):
    window_start = 0
    window_end = window_size
    while 1:
        window_words = tagged[window_start:window_end]
        if len(window_words) == 2:
            print window_words
            try:
                graph.add_edge((window_words[0][0], window_words[1][0]))
            except AdditionError, e:
                print 'already added %s, %s' % ((window_words[0][0], window_words[1][0]))
        else:
            break

        window_start += 1
        window_end += 1


def isTag(w, keywordList):
    if w in keywordList:
        return 1
    else:
        return 0


# if keywords are next to each other, they will be collapsed into one tag
def collaps_keywords(marked_text):
    keyword_list = set()
    pos = 0
    text_len = len(marked_text)
    while pos < text_len:
        if marked_text[pos][1] == 1:
            keyword = marked_text[pos][0]
            next_pos = pos+1
            while next_pos < text_len and marked_text[next_pos][1] == 1:
                keyword = " ".join([keyword, marked_text[next_pos][0]])
                next_pos += 1
            if keyword not in keyword_list:
                keyword_list.add(keyword)
            pos = next_pos + 1
        else:
            pos +=1
    return keyword_list

infile_name = "/tmp/inputfile"

with open(infile_name, 'r') as f:
  text = f.read()
f.closed

text = nltk.word_tokenize(text)
tagged = nltk.pos_tag(text)

tagged = filter_for_tags(tagged)
tagged = normalize(tagged)
unique_word_set = unique_everseen([x[0] for x in tagged])

gr = digraph()
gr.add_nodes(list(unique_word_set))
co_occurence_edge(gr)

calculated_keyword_rank = pagerank(gr)
sorted_keyword_rank = sorted(calculated_keyword_rank.iteritems(), key=itemgetter(1), reverse=True)

# first 20 keywords
keywordlist = [k[0] for k in sorted_keyword_rank[0:20]]
print  keywordlist

# mark text with keyword candidates
marked_text = [(w, isTag(w, keywordlist)) for w in text]
print marked_text

final_keywords = collaps_keywords(marked_text)
print final_keywords
