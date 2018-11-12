# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
from regex import Regex, UNICODE
import codecs


class Replacer(object):
    def __init__(self):
        self.__author__ = "Revo"
        self.__date__ = "2017-10-27"
        # email address:
        self.__email_addr = Regex(r'([\w\.-]+@[\w\.-]+)')
        # url address:
        self.__url_addr = Regex(
            r'(?P<url>https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)|[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*))')
        # Numbers
        self.__numbers = Regex(r'([+\-]?\d*[\.,]?\d+[\d\.,+\-eE]*)')
        # Replace with add one
        self.__addone = Regex(r'(__(NUM|EMAIL|URL)(\d+)__)')
        # double space to single
        self.__spaces = Regex(r'\s+', flags=UNICODE)

        self.line = 0

    def process(self, text, ori_line):
        #print text
        self.line += 1
        list_tags = self.__addone.findall(text)
        if list_tags:
            #print list_tags
            print "LINE:", self.line
            print "IN,", text
            print "ORI,", ori_line
            email_list = self.__email_addr.findall(ori_line)
            num_list = self.__numbers.findall(ori_line)
            url_list = self.__url_addr.findall(ori_line)
            print "EMAIL,", email_list
            print "NUM,", num_list
            print "URL,", url_list
            for match in list_tags:
                try:
                    if match[1] == "URL":
                        text = text.replace(
                            match[0], url_list[int(match[2]) - 1][0])
                    elif match[1] == "EMAIL":
                        text = text.replace(
                            match[0], email_list[int(match[2]) - 1])
                    elif match[1] == "NUM":
                        # eight->problem
                        text = text.replace(
                            match[0], num_list[int(match[2]) - 1])
                except BaseException:
                    print "FUCKED"
                    pass
            print "REPLACED:", text
            print "-----"

            #" __URL__ "
            #text = self.__url_addr.sub(" __URL__ ", text)
            #text = self.__numbers.sub(" __NUM__ ", text)
            #text = self.__addone.sub(self._add1,text)


if __name__ == '__main__':
    #sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    print "Usage python *.py [num_file] [ori_file]"
    num_file = codecs.open(sys.argv[1], "rb")
    ori_file = codecs.open(sys.argv[2], "rb")

    replacer = Replacer()

    for line in num_file:
        ori_line = ori_file.readline().strip()
        line = line.strip()
        replacer.process(line, ori_line)
        #print ori_line

    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
