# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
A simple tokenizer for MT preprocessing.

Library usage:

    from util.tokenize import Tokenizer
    t = Tokenizer({'lowercase': True, 'moses_escape': True})
    tokenized = t.tokenize(text)

Command-line usage:

    ./tokenize.py [-h] [-l] [-e ENCODING] [-m] [-f FACTOR-NUM] \\ 
                  [input-file output-file]
    
    -h = display this help
    -l = lowercase everything
    -e = use the given encoding (default: UTF-8)
    -m = escape characters that are special to Moses
    -f = treat input as pre-tokenized factors (separated by `|'), 
         split it further according to the given factor (numbered from 0)
    -t = threads when processing
    
    If no input and output files are given, the tokenizer will read
    STDIN and write to STDOUT.
"""
from __future__ import unicode_literals
from regex import Regex, UNICODE
from fileprocess import process_lines
import sys
import getopt
import threading
#import jieba
#from pattern.en import tag

__author__ = "chao, Tian Liang,Hao Zongs"
__date__ = "2014"

DEFAULT_ENCODING = 'UTF-8'


class Tokenizer(object):
    """\
    A simple tokenizer class, capable of tokenizing given strings.
    """

    # Moses special characters escaping
    ESCAPES = [('&', '&amp;'), # must go first to prevent double escaping!
               ('|', '&bar;'),
               ('<', '&lt;'),
               ('>', '&gt;'),
               ('[', '&bra;'),
               (']', '&ket;')]

    def __init__(self, options={}):
        """\
        Constructor (pre-compile all needed regexes).
        """
        # process options
        self.lowercase = True if options.get('lowercase') else False
        self.moses_escape = True if options.get('moses_escape') else False
        self.ts = options.get('num_t') if options.get('num_t') else 1
        # compile regexes
        self.__spaces = Regex(r'\s+', flags=UNICODE)
        self.__ascii_junk = Regex(r'[\000-\037]')
        self.__special_chars = \
                Regex(r'(([^\p{IsAlnum}\s\.\,−\-])\2*)')
        # email address: 
        self.__email_addr = Regex(r'([\w\.-]+@[\w\.-]+)')
        # url address:
        self.__url_addr = Regex(r'(?P<url>https?://[a-zA-Z0-9:/\.?=!@$#&\*_()]+|www\.\w+\.[a-zA-Z0-9:/\.?=!@$#&\*_()]+|\w+\.\w+)')
        # NEED TO PROTECT THIS EMAIL ADDRESS, EXTRACT IT AND TEHN INSERT BACK

        # single quotes: all unicode quotes + prime
        self.__to_single_quotes = Regex(r'[`‛‚‘’‹›′]')
        # double quotes: all unicode chars incl. Chinese + double prime + ditto
        self.__to_double_quotes = Regex(r'(\'\'|``|[«»„‟“”″〃「」『』〝〞〟])')
        self.__no_numbers = Regex(r'([^\p{N}])([,.])([^\p{N}])')
        self.__pre_numbers = Regex(r'([^\p{N}])([,.])([\p{N}])')
        self.__post_numbers = Regex(r'([\p{N}])([,.])([^\p{N}])')
        # hyphen: separate every time but for unary minus
        self.__minus = Regex(r'([-−])')
        self.__pre_notnum = Regex(r'(-)([^\p{N}])')
        self.__post_num_or_nospace = Regex(r'(\p{N} *|[^ ])(-)')

    def tokenize_factors(self, pretoks, factor_no=0):
        """\
        Further tokenize a list of factored tokens (separated by "|"), 
        separating the given factor and copying the other factor to all its
        parts.
        """
        out = []
        for pretok in pretoks:
            factors = pretok.split('|')
            tokens = ['|'.join(factors[:factor_no] + [token] +
                               factors[factor_no + 1:])
                      for token in
                      self.tokenize(factors[factor_no]).split(' ')]
            out.extend(tokens)
        return out

    def tokenize_factored_text(self, factored_text, factor_no=0):
        """\
        Further tokenize pre-tokenized text composed of several factors
        (separated by `|'). Tokenize further the given factor and copy all
        other factors.
        """
        pretoks = self.__spaces.split(factored_text)
        return ' '.join(self.tokenize_factors(pretoks, factor_no))

    def preserve_email(self, text):
        '''
        Preserve email address with "__email_addr__" for later recovery.
        '''
        self.__emails = self.__email_addr.findall(text)
        return self.__email_addr.sub("__email_addr__", text)

    def recover_email(self, text):
        '''
        Recover email addresses once a time.
        '''
        for i in xrange(len(self.__emails)):
            text = text.replace("__ email _ addr __", self.__emails[i], 1)
        del self.__emails
        return text

    def preserve_url(self, text):
    	'''
    	Preserve url address with "__url_addr__" for later recovery.
    	'''
    	self.__urls = self.__url_addr.findall(text)
    	return self.__url_addr.sub("__url_addr__", text)

    def recover_url(self, text):
        '''
        Recover url addresses once a time.
        '''
        for i in xrange(len(self.__urls)):
            text = text.replace("__ url _ addr __", self.__urls[i], 1)
        del self.__urls
        return text

    def preserve_punc(self, text):
    	self.__puncs = self.__punc_str.findall(text)
    	return self.__punc_str.sub("__punc_str__", text)

    def recover_punc(self, text):
    	for i in xrange(len(self.__puncs)):
            text = text.replace("__ punc _ str __", self.__puncs[i], 1)
        del self.__puncs
        return text

    def tokenize(self, text):
        """\
        Tokenize the given text using current settings.
        """
        # pad with spaces so that regexes match everywhere
        text = ' ' + text + ' '
        # spaces to single space
        text = self.__spaces.sub(' ', text)
        # remove ASCII junk
        text = self.__ascii_junk.sub('', text)

        # preserve
        text = self.preserve_email(text)
        text = self.preserve_url(text)

        # separate punctuation (consecutive items of same type stay together)
        text = self.__special_chars.sub(r' \1 ', text)
        # separate dots and commas everywhere except in numbers
        text = self.__no_numbers.sub(r'\1 \2 \3', text)
        text = self.__pre_numbers.sub(r'\1 \2 \3', text)
        text = self.__post_numbers.sub(r'\1 \2 \3', text)
        # normalize quotes
        text = self.__to_single_quotes.sub('\'', text)
        text = self.__to_double_quotes.sub('"', text)
        # separate hyphen, minus
        text = self.__pre_notnum.sub(r'\1 \2', text)
        text = self.__post_num_or_nospace.sub(r'\1\2 ', text)
        text = self.__minus.sub(r' \1', text)
        # spaces to single space
        text = self.__spaces.sub(' ', text)
        text = text.strip()
        # escape chars that are special to Moses
        if self.moses_escape:
            for char, repl in self.ESCAPES:
                text = text.replace(char, repl)
        # recover
        text = self.recover_email(text)
        text = self.recover_url(text)
        # lowercase
        if self.lowercase:
            text = text.lower()

        return text

def display_usage():
    """\
    Display program usage information.
    """
    print >> sys.stderr, __doc__


if __name__ == '__main__':
    # parse options
    opts, filenames = getopt.getopt(sys.argv[1:], 'hle:mft:')
    options = {}
    help = False
    encoding = DEFAULT_ENCODING
    factor = None
    for opt, arg in opts:
        if opt == '-l':
            options['lowercase'] = True
        elif opt == '-h':
            help = True
        elif opt == '-e':
            encoding = arg
        elif opt == '-m':
            options['moses_escape'] = True
        elif opt == '-f':
            factor = int(arg)
        elif opt == '-t':
            options['num_t'] = int(arg)
    # display help
    if len(filenames) > 2 or help:
        display_usage()
        sys.exit(1)
    # process the input
    tok = Tokenizer(options)
    proc_func = tok.tokenize if factor is None else \
            lambda text: tok.tokenize_factored_text(text, factor)
    process_lines(proc_func, filenames, encoding)
