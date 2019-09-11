# -*- encoding=utf-8 -*-
import codecs
import numpy as np
from fasttext import FastVector
import sys

# from https://stackoverflow.com/questions/21030391/how-to-normalize-array-numpy
def normalized(a, axis=-1, order=2):
    """Utility function to normalize the rows of a numpy array."""
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def make_training_matrices(source_dictionary, target_dictionary, bilingual_dictionary):
    """
    Source and target dictionaries are the FastVector objects of
    source/target languages. bilingual_dictionary is a list of 
    translation pair tuples [(source_word, target_word), ...].
    """
    source_matrix = []
    target_matrix = []

    for (source, target) in bilingual_dictionary:
        if source in source_dictionary and target in target_dictionary:
            source_matrix.append(source_dictionary[source])
            target_matrix.append(target_dictionary[target])

    # return training matrices
    return np.array(source_matrix), np.array(target_matrix)

def learn_transformation(source_matrix, target_matrix, normalize_vectors=True):
    """
    Source and target matrices are numpy arrays, shape
    (dictionary_length, embedding_dimension). These contain paired
    word vectors from the bilingual dictionary.
    """
    # optionally normalize the training vectors
    if normalize_vectors:
        source_matrix = normalized(source_matrix)
        target_matrix = normalized(target_matrix)

    # perform the SVD
    product = np.matmul(source_matrix.transpose(), target_matrix)
    U, s, V = np.linalg.svd(product)

    # return orthogonal transformation which aligns source language to the target
    return np.matmul(U, V)

def parse_BI(BI):
	BI_DICT = []
	for line in BI:
		en, other, _ = line.split()
		BI_DICT.append((other, en))
	return BI_DICT

def test_word(en_dictionary, other_dictionary, SRC_WORD, TGT_WORD):
	print "Testing WORD[%s->%s]" % (SRC_WORD, TGT_WORD)
	en_vector = en_dictionary[SRC_WORD]
	other_vector = other_dictionary[TGT_WORD]
	print(FastVector.cosine_similarity(en_vector, other_vector))

def write_vec2f(en_dict):
    f = codecs.open("Qe", "w")
    for word in en_dict:
        pro = " ".join(en_dict[word])
        f.write(word + " " + pro + '\n')



print "Readling Dictionary"
BI_DICT = codecs.open("o.s2t_f", "r").readlines()
BI_DICT = parse_BI(BI_DICT)
print "Readling Dictionary (END)"

# SRC_WORD = "昨天"
# TGT_WORD = "yesterday"
SRC_WORD = "钥匙"
TGT_WORD = "keys"
en_dictionary = FastVector(vector_file='en.emb.orig.vec')
other_dictionary = FastVector(vector_file='tizh.emb.orig.vec')

test_word(other_dictionary, en_dictionary, SRC_WORD, TGT_WORD)

# form the training matrices
print "Learning SVD"
source_matrix, target_matrix = make_training_matrices(
    other_dictionary, en_dictionary, BI_DICT)

# learn and apply the transformation
transform = learn_transformation(source_matrix, target_matrix)
other_dictionary.apply_transform(transform)
# zh
test_word(other_dictionary, en_dictionary, SRC_WORD, TGT_WORD)
# ti
SRC_WORD = "กุญ"
test_word(other_dictionary, en_dictionary, SRC_WORD, TGT_WORD)

print "Writing transform Qe out"
other_dictionary.export("Qe")

