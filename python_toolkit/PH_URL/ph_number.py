# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
from regex import Regex, UNICODE
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')


class Generizer(object):
    def __init__(self):
        self.__author__ = "Revo"
        self.__date__ = "2017-12-28"
        #self.__date__ = "2017-10-24"
        # email address:
        self.__email_addr = Regex(r'([\w\.-]+@[\w\.-]+)')
        # url address:
        self.__url_addr = Regex(
            r'(?P<url>https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)|[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*))')
        #self.__date_list = ["a.m","p.m","A.M","P.M"]
        # Numbers
        self.__numbers = Regex(r'([+\-]?\d*[\.,]?\d+[\d\.,+\-eE]*)')
        # Replace with add one
        self.__addone = Regex(r'(__(NUM|EMAIL|URL)__)')
        self.__addone_search = Regex(r'(__(NUM|EMAIL|URL)(\d+)__)')
        # double space to single
        self.__spaces = Regex(r'\s+', flags=UNICODE)
        #
        self.__counter = dict({"URL": 0, "EMAIL": 0})
        #
        self.line = 0

    def _add1_NUM(self, match):
        self.__counter += 1
        return " __NUM" + str(self.__counter) + "__ "

    def _add1_EMAIL(self, match):
        self.__counter += 1
        return " __EMAIL" + str(self.__counter) + "__ "

    def _add1_URL(self, match):
        self.__counter += 1
        return " __URL" + str(self.__counter) + "__ "

    def _filter_AM_NUM(self, match):
        # if match.group("url") in self.__date_list or match.group("url").replace(".","").isdigit():
        #    return match.group("url")
        return " __URL__ "

    def _add1(self, match):
        type = match.group(0)[2:-2]
        try:
            self.__counter[type] += 1
        except BaseException:
            self.__counter[type] = 1
        return "__" + type + str(self.__counter[type]) + "__"

    def tokenize(self, text):
        # normalize
        #text = text.replace(" @ ","@")
        #text = text.replace(" . ",".")
        #text = text.replace("http : // ","http://")
        #
        text = self.__email_addr.sub(" __EMAIL__ ", text)
        #" __URL__ "
        text = self.__url_addr.sub(" __URL__ ", text)
        #text = self.__numbers.sub(" __NUM__ ", text)
        text = self.__addone.sub(self._add1, text)
        self.__counter = {}
        # spaces to single space
        #text = self.__spaces.sub(' ', text)
        #
        return text

    def tokenize_two_line(self, source_text, target_text):
        source_text2 = self.__email_addr.sub(" __EMAIL__ ", source_text)
        source_text2 = self.__url_addr.sub(" __URL__ ", source_text2)
        source_text2 = self.__addone.sub(self._add1, source_text2)
        source_counter = self.__counter.copy()
        self.__counter = {"URL": 0, "EMAIL": 0}
        #
        target_text2 = self.__email_addr.sub(" __EMAIL__ ", target_text)
        target_text2 = self.__url_addr.sub(" __URL__ ", target_text2)
        target_text2 = self.__addone.sub(self._add1, target_text2)
        target_counter = self.__counter.copy()
        self.__counter = {"URL": 0, "EMAIL": 0}
        #
        notmatch = False
        if len(target_counter) > 0:
            for key in target_counter:
                if source_counter[key] != target_counter[key]:
                    notmatch = True
                    break
            if not notmatch:
                # matched
                source_text = source_text2
                target_text = target_text2
            #print self.__counter

        return source_text, target_text

    def recover(self, text, ori_line):
        #print text
        self.line += 1
        list_tags = self.__addone_search.findall(text)
        if list_tags:
            print "list_tags:", list_tags
            email_list = self.__email_addr.findall(ori_line)
            url_list = self.__url_addr.findall(ori_line)
            # delete duplicate entities
            for email in email_list:
                for index, url in enumerate(url_list):
                    if email in url:
                        # duplicated
                        del url_list[index]
            # replac start
            for match in list_tags:
                try:
                    if match[1] == "EMAIL":
                        text = text.replace(
                            match[0], email_list[int(match[2]) - 1])
                    elif match[1] == "URL":
                        text = text.replace(
                            match[0], url_list[int(match[2]) - 1][0])
                except BaseException:
                    #print "FUCKED"
                    pass

            # print "LINE:",self.line
            # print "IN,",text
            # print "ORI,",ori_line
            # print "EMAIL,",email_list
            # print "URL,",url_list
            # print "REPLACED:",text
            # print "-----"
        #
        #print text
        return text


if __name__ == '__main__':
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    Real_Generizer = Generizer()
    if sys.argv[1] == '-h':
        print "Usage Recover mode: python ph_number.py [-r] [target_text] [original_text]"
        print "Usage Generalization mode: python ph_number.py [source_file] [original_text]"
        sys.exit()
    #
    if sys.argv[1] == '-r':
        target_file = codecs.open(sys.argv[2], "rb")
        ori_file = codecs.open(sys.argv[3], "rb")
        for line in target_file:
            ori_line = ori_file.readline().strip()
            line = line.strip()
            sys.stdout.write(Real_Generizer.recover(line, ori_line) + "\n")
            # Real_Generizer.recover(line,ori_line)
        sys.exit()
    # generalization
    source_file = codecs.open(sys.argv[1], "rb")
    target_file = codecs.open(sys.argv[2], "rb")
    source_output = codecs.open(
        sys.argv[1][:-3] + ".PH" + sys.argv[1][-3:], "wb")
    target_output = codecs.open(
        sys.argv[2][:-3] + ".PH" + sys.argv[2][-3:], "wb")
    for line in source_file:
        target_line = target_file.readline().strip()
        # sys.stdout.write(Real_Generizer.tokenize(line).strip()+"\n")
        s_output_line, t_output_line = Real_Generizer.tokenize_two_line(
            line, target_line)
        source_output.write(s_output_line.strip() + "\n")
        target_output.write(t_output_line.strip() + "\n")
