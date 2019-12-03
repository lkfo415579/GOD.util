#coding:utf-8
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy
import re
from matplotlib import font_manager
from mpl_toolkits.axes_grid1 import make_axes_locatable

# 指定默认字体
fontP = font_manager.FontProperties()
fontP.set_family('SimHei')
fontP.set_size(9.5)

fontname = "Times New Roman"


def parse_numpy(string):
    string = string.replace('[', ' ').replace(']', ' ').replace(',', ' ')
    string = re.sub(' +', ' ', string)
    result = numpy.fromstring(string, sep=' ')
    return result


# with open(sys.argv[2], 'r') as fsrc:
#     src_lines = fsrc.readlines()
#     max_len_s = max(map(len, map(lambda x: x.split(), src_lines)))+1
#     print(max_len_s)
#
# with open(sys.argv[3], 'r') as ftgt:
#     tgt_lines = ftgt.readlines()
#     max_len_t = max(map(len, map(lambda x: x.split(), tgt_lines)))+1
#     print(max_len_t)

# parse from text
pattern = re.compile(r'(.*?) DEBUG (.*?)\n')
fr = open(sys.argv[1], 'r')
head = 8
matrices = []
for line in fr:
    matrix = parse_numpy(line)
    print matrix.shape
    # matrix = numpy.reshape(matrix, [samples, head, max_len_s, max_len_t])
    matrix = numpy.reshape(matrix, [1, head, -1, 1])
    print matrix.shape
    matrices.append(matrix)
    # sobj = pattern.search(line)
    # if sobj:
    #     print sobj
    #
    #     matrix_str = sobj.group(2)


def draw_n_weights(index, layers=15):
    # src_line = src_lines[index].decode('utf-8')
    # tgt_line = tgt_lines[index].decode('utf-8')
    # src_words = "sugelan huangjia yinhang jiang buzai wei sugelan yiwai kehufuwu <eos> <zero> R@@ BS will no longer serve outside Scotland".split()
    src_words = "sugelan huangjia yinhang jiang buzai wei sugelan yiwai kehufuwu <eos> <zero> R@@ BS will no longer serve outside".split()
    # tgt_words = "".split()
    len_s = len(src_words)
    # len_t = len(tgt_words)
    max_len_s = len(src_words)

    fig, axs = plt.subplots(nrows=1, ncols=5, figsize=(8, 10))
    x=0
    for l in [1,4,8,13,15]:
        rlv = matrices[x][index, :, :max_len_s, :1]
        # rlv = numpy.sum(rlv, axis=1, keepdims=False)
        rlv = numpy.reshape(rlv, [8, max_len_s])
        rlv = numpy.transpose(rlv)
        print rlv.shape
        maximum = numpy.max(numpy.abs(rlv))

        im = axs[x].matshow(rlv, cmap="OrRd", vmin=0, vmax=maximum)
        axs[x].set_yticks([])
        axs[x].tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
        axs[x].set_title("Layer " + str(l), fontsize=10, loc="left")
        axs[x].set_xticklabels(range(9))

        if x == 0:
            axs[x].set_yticks(range(len_s))
            axs[x].tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
            axs[x].set_yticklabels(src_words, fontsize=10)

        x+=1

    # axs[-1].set_yticks(range(len_s))
    # axs[-1].tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
    # axs[-1].set_yticklabels(src_words, fontsize=8, rotation='vertical')

    # ax = plt.gca()
    # divider = make_axes_locatable(ax1)
    # cax = divider.append_axes("right", size="2%", pad=0.05)
    fig.subplots_adjust(right=0.85)
    fig.subplots_adjust(top=0.9)

    # cbar_ax = fig.add_axes([0.9, 0.5, 0.03, 0.7])
    # cbar_ax.tick_params(labelsize='small')
    # fig.colorbar(im, cax=cbar_ax)

    matplotlib.rcParams['font.family'] = "Times New Roman"
    plt.savefig(sys.argv[1]+'.pdf', format="pdf", bbox_inches='tight')


def draw_weights(index, layers=15):
    # src_line = src_lines[index].decode('utf-8')
    # tgt_line = tgt_lines[index].decode('utf-8')
    # src_words = "sugelan huangjia yinhang jiang buzai wei sugelan yiwai kehufuwu <eos> <zero> R@@ BS will no longer serve outside Scotland".split()
    src_words = "sugelan huangjia yinhang jiang buzai wei sugelan yiwai kehufuwu <eos> <zero> R@@ BS will no longer serve outside".split()
    # tgt_words = "".split()
    len_s = len(src_words)
    # len_t = len(tgt_words)
    max_len_s = len(src_words)


    fig, axs = plt.subplots(nrows=3, ncols=5,figsize=(8, 10))

    for l in range(layers):
        x = l/5
        y = l%5
        print x,y
        rlv = matrices[l][index, :, :max_len_s, :1]
        # rlv = numpy.sum(rlv, axis=1, keepdims=False)
        rlv=numpy.reshape(rlv,[8,max_len_s])
        rlv=numpy.transpose(rlv)
        print rlv.shape
        maximum = numpy.max(numpy.abs(rlv))

        im = axs[x][y].matshow(rlv, cmap="OrRd", vmin=0, vmax=maximum)
        axs[x][y].set_yticks([])
        axs[x][y].tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
        axs[x][y].set_title("Layer "+str(l+1),fontsize=10,loc="left")
        axs[x][y].set_xticklabels(range(9))

        if y==0:
            axs[x][y].set_yticks(range(len_s))
            axs[x][y].tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
            axs[x][y].set_yticklabels(src_words, fontsize=10)

    
    # axs[-1].set_yticks(range(len_s))
    # axs[-1].tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
    # axs[-1].set_yticklabels(src_words, fontsize=8, rotation='vertical')

    # ax = plt.gca()
    # divider = make_axes_locatable(ax1)
    # cax = divider.append_axes("right", size="2%", pad=0.05)
    fig.subplots_adjust(right=0.85)
    fig.subplots_adjust(top=0.9)

    # cbar_ax = fig.add_axes([0.9, 0.5, 0.03, 0.7])
    # cbar_ax.tick_params(labelsize='small')
    # fig.colorbar(im, cax=cbar_ax)


    matplotlib.rcParams['font.family'] = "Times New Roman"
    plt.savefig(sys.argv[1]+'.pdf',format="pdf",bbox_inches='tight')

    # plt.show()

for i in range(1):
    draw_n_weights(i)