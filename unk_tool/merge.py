#/usr/bin/env python
# -*- coding:utf-8 -*-

__author__  = 'liangss'
__version__ = '0.0.1'

import sys, re, getopt,codecs

DELIMTER='@@@@@@@@@@'

def merge(srclf, tgtlf, output, ranksize):
    try:
        fin1 = open(srclf, 'r'); 
        fin2 = open(tgtlf, 'r');

        fout = open(output, "w+") if output is not None else sys.stdout;

        lines = []
        line1 = fin1.readline();
        line2 = fin2.readline();
        while line1 and line2:
            lines.append(line1.split('\n')[0]+DELIMTER+line2);
            line1 = fin1.readline();
            line2 = fin2.readline();
        lines = list(set(lines));
        lines.sort();
        fout.writelines(lines[ranksize:len(lines)-ranksize]);

    except IOError as e:
        print e
    finally:
        fin1.close();
        fin2.close();
        if fout is not sys.stdout:
            fout.close();

def _usage():
    print >>sys.stderr, '''
    Description:
        Merge source input file and target input file to outputfile.
    USAGE:
        python merge.py -s srclfile -t tgtfile -o outputfile -r rank size
    OPTIONS:
        -s srcl inputfile, no inputfile will read lines from stdin
        -t tgtl inputfile, no inputfile will read lines from  
        -o output file name
        -r rank the head lines and tail lines
        -h show help info
    '''
if __name__ == "__main__":

    task = { };
    try:
        opts,args=getopt.getopt(sys.argv[1:],'s:t:o:h', ['srclf=','tgtlf=','output=', 'h'])
        for o, a in opts:
            if o in ('-h', '--help'):
                _usage();
                sys.exit();
            elif o in ('-s', '--srclf'):
                task['srclf'] = a;
            elif o in ('-t', '--tgtlf'):
                task['tgtlf'] = a;
            elif o in ('-o', '--output'):
                task['output'] = a;
            elif o in ('-r', '--ranksize'):
                task['ranksize'] = a;
            else:
                _usage();
                sys.exit();
    except getopt.GetoptError:
        _usage();
        sys.ext();

    merge(
            task['srclf'],
            task['tgtlf'],
            task['output'] if task.has_key('output') else None,
            task['ranksize'] if task.has_key('ranksize') else 0
        ) ;
