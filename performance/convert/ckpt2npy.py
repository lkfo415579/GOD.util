import sys
import numpy as np
import tensorflow as tf
from tensorflow.python import pywrap_tensorflow
print "Usage: py x.py model_step[82000] lang[en2zh]"


def display_first_ELE(t):
    if len(t.shape) == 2:
        v = "%s, %s" % (t[0][0], t[0][1])
    else:
        v = "%s, %s" % (t[0], t[1])
    return v


checkpoint_path = 'model.ckpt-%s' % sys.argv[1]
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()

lang = sys.argv[2]
WB = {"matrix": "kernel", "bias": "bias"}
NEW_MODEL_DICT = {}

MODEL_NUM = 0
for key in var_to_shape_map:
    if key.find("Adam") == -1 and key.find("MultiStepOptimizer") == -1:
        t = reader.get_tensor(key)
        if len(t.shape) != 0:
            MODEL_NUM += 1
            v = display_first_ELE(t)
            print key, t.shape, v
            # replacement
            tk = key.split("/")
            tk[0] = "%s/body" % lang
            CONVERTED = False
            # FFN
            if len(tk) > 4 and tk[4] == "ffn_layer":
                tk[3] = "conv_hidden_relu"
                if tk[5] == "input_layer":
                    layer_id = "1"
                else:
                    layer_id = "2"
                tk[4] = ""
                tk[5] = ""
                tk[6] = "conv%s_single" % layer_id
                tk[-1] = WB[tk[-1]]
                CONVERTED = True
            # self-attention
            if len(tk) > 4 and tk[4] == "multihead_attention":
                if tk[3] == "self_attention":
                    tk[3] = tk[1] + "_" + tk[3]
                tk[4] = ""
                tk[5] = tk[5] + "_single"
                tk[-1] = WB[tk[-1]]
                CONVERTED = True
            # layer_normalization
            if len(tk) > 4 and tk[4] == "layer_norm":
                l_id = ""
                if tk[1] == "decoder" and tk[3] == "feed_forward":
                    l_id = "_2"
                if tk[1] == "encoder" and tk[3] == "feed_forward":
                    l_id = "_1"
                if tk[3] == "encdec_attention":
                    l_id = "_1"
                tk[3] = ""
                tk[4] = tk[4] + l_id
                tk[-1] = "layer_norm_bias" if tk[-1] == "offset" else "layer_norm_scale"
                CONVERTED = True
            # input & output embed
            if len(tk) == 2:
                tk[0] = "%s/symbol_modality" % lang
                if tk[1] == "target_embedding":
                    tk[1] = "target_emb"
                if tk[1] == "source_embedding":
                    tk[1] = "input_emb"
                # last
                if tk[-1] != "bias":
                    tk.append("weights_0")
                else:
                    # input bias
                    tk[1] = "input_emb"
                    tk.append("bias_0")
                # softmax
                if tk[1] == "softmax":
                    tk[-1] += "_V"
                # softmax_U
                if tk[1] == "softmax_U":
                    tk[1] = "softmax"
                    tk[-1] += "_U"
                CONVERTED = True
            # kernel scale of emb
            if tk[1].find("emb") != -1:
                tk[0] = "%s/symbol_modality" % lang
                CONVERTED = True
            # matrix do transpose, exception : scalar and embedding matrix
            # the god damn transpose only swap axis, mother fucker you need to do copy call. DAMN!
            if len(t.shape) > 1 and tk[-1] != "weights_0":
                t = np.transpose(t, (1, 0)).copy()
            #
            tk = [x for x in tk if x != ""]
            tk = "/".join(tk)
            v = display_first_ELE(t)
            print "Replace [%s]: %s|||%s|||%s|||" % (
                CONVERTED, tk, t.shape, t.dtype),
            print v
            NEW_MODEL_DICT[tk] = t
            print "=" * 100

# file to npz
# basic parameters
NEW_MODEL_DICT["%s/dec_heads" % lang] = np.array([[8.8888]], dtype=np.float32)
NEW_MODEL_DICT["%s/enc_heads" % lang] = np.array([[8.8888]], dtype=np.float32)
NEW_MODEL_DICT["%s/dec_layers" %
               lang] = np.array([[3.3333333]], dtype=np.float32)
NEW_MODEL_DICT["%s/enc_layers" %
               lang] = np.array([[4.44444444444]], dtype=np.float32)
print NEW_MODEL_DICT["%s/dec_heads" %
                     lang], NEW_MODEL_DICT["%s/dec_heads" % lang].dtype
#
np.savez("s.model.npz", **NEW_MODEL_DICT)
print "Converted Total layer: %d" % MODEL_NUM
