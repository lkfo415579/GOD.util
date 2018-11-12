#!/usr/bin/env python
# -*- coding: utf8 -*-
from tornado.concurrent import run_on_executor
import concurrent.futures
'''
   @Brief : Language detect server...
   @Modify : 2017/12/07 Edited By Revo, tornado server
   @Version :
            @1.0
            @1.1
                - fixed top3 bug, if it has two zh it will count the lowerest score ones

   @CopyRight : newtranx
'''

import json

import logging
import argparse
import validictory
import socket

import tornado.httpserver


import tornado.ioloop
import tornado.web
import tornado.gen

from polyglot.detect import Detector

# DetectorFactory.seed = 0
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=str, required=True,
                    help="language detector server listener port")
parser.add_argument('--process', type=int, required=False,
                    help="processes number")
args = parser.parse_args()
# -- parser args from input --#

# -------------------------------------------------------------------------------
# -- task --#
# -------------------------------------------------------------------------------


def build_task(params):
    task = params
    text = task.get("text", None)
    if text.strip() == "":
        task["text"] = None
    top = task.get("top", None)
    try:
        if top.strip() == "":
            task["top"] = None
    except BaseException:
        pass
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
        pass
    #-- end->Func: Server: __init__ --#

    @run_on_executor
    def lang_detect(self, task):
        sentence = task['text']
        languages_result = Detector(sentence, True).languages
        detected = {}
        for lang_result in languages_result:
            code = lang_result.code[:2]
            if code in detected:
                detected[code] += lang_result.confidence * \
                    float(lang_result.read_bytes)
            else:
                detected[code] = lang_result.confidence * \
                    float(lang_result.read_bytes)
        detected_MAX = [max(detected, key=detected.get)]
        # Log
        self.logger.info("Detected:%s:%s" % (str(detected_MAX), sentence))
        for lang in languages_result:
            self.logger.info(lang)
        self.logger.info('---')
        # create json format
        json_result = dict()
        json_result['predicted'] = detected_MAX[0]
        json_result['data'] = []
        for ele in languages_result:
            tmp = {}
            tmp_ele = str(ele).replace("  ", " ").split(" ")
            tmp_ele = [item for item in tmp_ele if item != '']
            #
            tmp['name'] = tmp_ele[1]
            tmp['code'] = tmp_ele[3][:2]
            tmp['score'] = float(detected[tmp['code']])
            tmp['bytes'] = tmp_ele[8]
            json_result['data'].append(tmp)

        return json.dumps(json_result)
    #-- end->Func: translate --#

    #-- The inside function: Server:translate --#
    @tornado.gen.coroutine
    def post(self):
        # print self.request.headers["Content-Type"]
        task = None
        if "application/json" in self.request.headers["Content-Type"]:
            try:
                #task = json.loads( self.request.body.encode('utf-8'))
                task = json.loads(self.request.body)
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
            result = self.lang_detect(task).result(300)
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
                        filename="lang" + '_' + args.port + '.log'
                        )
    logger = logging.getLogger('NMTSERVER')
    SERVER_PROCESS = args.process if args.process is not None else 0
    ##
    server_ctx = dict({'logger': logger})
    app = tornado.web.Application([
        (r"/lang", Server, dict(server_ctx=server_ctx)),
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
