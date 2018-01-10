# -*- coding: utf-8 -*-
#!/usr/bin/env python
import jieba_ext_cut
class JIE_Tokenizer(object):
    def __init__(self,path):
        self.tokenizer = jieba_ext_cut.Jieba(path+'/jieba.dict.utf8',
            path+'/hmm_model.utf8',
            path+'/user.dict.utf8',
            path+'/idf.utf8',
            path+'/stop_words.utf8')
    def tokenize(self,sentence):
        return self.tokenizer.jieba_ext_cut(str(sentence))
