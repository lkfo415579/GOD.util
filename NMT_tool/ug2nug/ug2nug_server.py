#!/usr/bin/env python
# -*- coding: utf8 -*-
from tornado.concurrent import run_on_executor
import concurrent.futures
'''
   @Brief : UG2NUG server...
   @Modify : 2017/12/11 Edited By Revo, tornado server
   @Version :
            @1.0

   @CopyRight : newtranx
'''
import os
import sys
import time
import json
import uuid
import logging
import argparse
import validictory
import socket

from configobj import ConfigObj

import multiprocessing
import tornado.httpserver

from threading import Lock
from threading import Thread

from multiprocessing import Queue, Process

import tornado.ioloop
import tornado.web
import tornado.gen

import shlex
import subprocess
import codecs

parser = argparse.ArgumentParser()
parser.add_argument(
    '--port',
    type=str,
    required=True,
    help="language detector server listener port")
parser.add_argument(
    '--process',
    type=int,
    required=False,
    help="processes number")
args = parser.parse_args()
#-- parser args from input --#

# -------------------------------------------------------------------------------
#-- task --#
# -------------------------------------------------------------------------------


def build_task(params):
    task = params
    text = task.get("text", None)
    if text.strip() == "":
        task["text"] = None

    return task
# --> end->Func: build_task


# -------------------------------------------------------------------------------
# --@brief: NMT server class...
# --
# --@param: logfile, ...
# -------------------------------------------------------------------------------
class Server(tornado.web.RequestHandler):
    executor = concurrent.futures.ThreadPoolExecutor(int(256))

    def initialize(self, server_ctx):
        self.logger = server_ctx['logger']
        self.task_id = tornado.process.task_id()
        pass
    #-- end->Func: Server: __init__ --#

    @run_on_executor
    def ug2nug(self, task):
        sentence = task['text']
        write_file = "tmp" + str(self.task_id)
        output_file = "tmp.latin" + str(self.task_id)
        file_tmp = codecs.open(write_file, "w", "utf-8")
        file_tmp.write(sentence)
        file_tmp.close()
        subprocess.call(
            "cat " +
            write_file +
            " | ./uygur2latin.pl > " +
            output_file,
            shell=True)
        # dont with converting
        lines = codecs.open(output_file, "rb", "utf-8").readlines()

        #"cat test.uy | ./uygur2latin.pl > test.uy.latin"
        # ---
        # languages_result = Detector(sentence,True).languages
        # detected = {}
        # for lang_result in languages_result:
        #     detected[lang_result.code[:2]] = lang_result.confidence * float(lang_result.read_bytes)
        # detected_MAX = [max(detected, key=detected.get)]
        # #Log
        # self.logger.info( "Detected:%s:%s" % (str(detected_MAX),sentence) )
        # for lang in languages_result:
        #     self.logger.info( lang )
        # self.logger.info( '---' )

        # create json format
        lines = [line.strip().replace(u"↵", ". ").replace(",.", ".")
                 for line in lines]
        #print lines
        json_result = dict({"translation":
                            [{"translated": [{
                                "src_text": sentence,
                                "text": " ".join(lines),
                                "line_num": 0,
                                "ret_code": 0,
                                "rank": 0,
                                "src-tokenized": sentence,
                                "score": 888
                            }], "translatedId": "a09bd26c1fd5497ab53a96960c967107"}]})
        # json_result['predicted'] = detected_MAX[0]
        # json_result['data'] = []
        # for ele in languages_result:
        #     tmp = {}
        #     tmp_ele = str(ele).replace("  "," ").split(" ")
        #     tmp_ele = [item for item in tmp_ele if item != '']
        #     #
        #     tmp['name'] = tmp_ele[1]
        #     tmp['code'] = tmp_ele[3][:2]
        #     tmp['score'] = float(detected[tmp['code']])
        #     tmp['bytes'] = tmp_ele[8]
        #     json_result['data'].append(tmp)

        return json.dumps(json_result)
    #-- end->Func: translate --#

    #-- The inside function: Server:translate --#

    @tornado.gen.coroutine
    def post(self):
        #print self.request.headers["Content-Type"]
        task = None
        if "application/json" in self.request.headers["Content-Type"]:
            try:

                task = json.loads(self.request.body)
                #print task
                task = build_task(task)
            except BaseException:
                task = None
        elif "application/x-www-form-urlencoded" in self.request.headers["Content-Type"]:
            task = {
                'text': self.get_argument('text')
            }
            task = build_task(task)

        try:
            task_schema = {
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
            }
            validictory.validate(task, task_schema)
        except BaseException:
            task = None

        if (task is not None) and 'text' in task:
            #-- Initiazation --#
            # concurrent,use future.result()
            result = self.ug2nug(task).result(300)
            ###
            retCode = 0
            self.set_header("Content-Type", "application/jsoncharset=utf-8")
            self.write(result)
            self.finish()
        else:
            self.set_status(400)
            self.write("Invalid request data, please check it.")
            self.finish()
    #--end->Func: Server:translate --#


#--end->Class: Server --#


# -------------------------------------------------------------------------------
# --@biref: Server process instance...
# -------------------------------------------------------------------------------
def main():
    #-- set up logging --#
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s[%(process)d] - %(name)s - %(message)s",
                        filename="ug2nug" + '_' + args.port + '.log'
                        )
    logger = logging.getLogger('NMTSERVER')
    SERVER_PROCESS = args.process if args.process is not None else 0
    ##
    server_ctx = dict({'logger': logger})
    app = tornado.web.Application([
        (r"/translate", Server, dict(server_ctx=server_ctx)),
    ])
    logger.info("Started Language detector server.")
    http_ctx = tornado.httpserver.HTTPServer(app)
    http_ctx.bind(int(args.port), '0.0.0.0', socket.AF_INET, int(256))
    http_ctx.start(SERVER_PROCESS)
    tornado.ioloop.IOLoop.current().start()
#--end->Func: main --#


# -------------------------------------------------------------------------------
# -- The Server process main instance, do there and running...
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
