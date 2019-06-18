import numpy as np
import yaml
import sys
from sys import getsizeof

lang = "%s" % sys.argv[2]
prefix = "%s/body" % lang
Wemb_prefix = "%s/symbol_modality" % lang
WB = {"b": "bias", "W": "kernel"}
new_model_dict = {}
model = np.load(sys.argv[1])

print "Converting MARIAN MODEL 2 sougou MODEL"
print "LOADED model:%s" % sys.argv[1]

all_s = 0
for key in model:
    print "=" * 100
    #
    name = key
    shape = model[key].shape
    values = model[key]
    print "Name:", name,
    print "Shapes:", shape,
    s = getsizeof(values)
    print "Size:", s, "," + str(s / 1024 ** 2) + "MB"
    all_s += s
    #
    # skip special
    if key.find("special") != -1:
        continue
    # converting
    tokens = name.split("_")
    endec_name = tokens[0]
    try:
        layer_id = str(int(tokens[1][-1]) - 1)
    except:
        layer_id = tokens[1][-1]
    new_name = ""
    # embedding
    if tokens[1] == "Wemb":
        emb_name = "input_emb" if tokens[0] == "encoder" else "target_emb"
        new_name = Wemb_prefix + "/%s/%s" % (emb_name, "weights_0")
    # embeding scale
    if tokens[1] == "scale":
        emb_name = "input_emb" if tokens[0] == "encoder" else "target_emb"
        wb = tokens[-1][-2]
        new_name = Wemb_prefix + \
            "/%s/%s" % (emb_name, "embedding_scale_single/%s" % WB[wb])
    # self_attention
    if tokens[-2] == "self" or tokens[-2] == "context":
        wb = tokens[-1][-2]
        qkv = tokens[-1][-1]
        AXIS = 1
        # if wb == "W":
        #   AXIS = 0
        # else:
        #   AXIS = 1
        # context
        body_str = "%s_self_attention/" % endec_name if tokens[-2] == "self" else "encdec_attention/"
        if qkv == "o":
            new_name = prefix + "/" + endec_name + \
                ("/layer_%s/" % layer_id) + body_str + \
                "output_transform_single/%s" % WB[wb]
        elif qkv == "q" or qkv == "k" or qkv == "v":
            # only convert in each q
            # combine qkv together with bias and weights
            new_name = prefix + "/" + endec_name + \
                ("/layer_%s/" % layer_id) + body_str + \
                "%s_transform_single/%s" % (qkv, WB[wb])
            # if tokens[-2] == "context":
            #   # q
            #   new_name = prefix + "/" + endec_name + ("/layer_%s/" % layer_id) + body_str + "q_transform_single/%s" % WB[wb]
            #   new_model_dict[new_name] = np.transpose(values)
            #   print "REPLACE %s to %s" % (name, new_name)
            #   # kv
            #   new_values = model[key[:-1] + "k"]
            #   new_values = np.concatenate((new_values, model[key[:-1] + "v"]), axis=AXIS)
            #   values = new_values
            #   new_name = prefix + "/" + endec_name + ("/layer_%s/" % layer_id) + body_str + "kv_transform_single/%s" % WB[wb]
            # else:
            #   new_values = np.array(values)
            #   print "Q's shape:", new_values.shape
            #   new_values = np.concatenate((new_values, model[key[:-1] + "k"]), axis=AXIS)
            #   new_values = np.concatenate((new_values, model[key[:-1] + "v"]), axis=AXIS)
            #   print "Qkv's shape:", new_values.shape
            #   values = new_values
            #   new_name = prefix + "/" + endec_name + ("/layer_%s/" % layer_id) + body_str + "qkv_transform_single/%s" % WB[wb]
    # FFN
    if tokens[-2] == "ffn":
        # encoder_l6_ffn_b1
        wb = tokens[-1][-2]
        ele_num = tokens[-1][-1]
        new_name = prefix + "/" + endec_name + \
            ("/layer_%s/" % layer_id) + \
            "conv_hidden_relu/conv%s_single" % ele_num + "/%s" % WB[wb]
    # ff logit out
    if tokens[1] == "ff":
        type = tokens[2]
        if type == "logit":
            wb = tokens[-1][-1]
            type = "V"
        else:
            wb = tokens[-1][-2]
            type = "U"
        wb = "weights_0" if wb == "W" else "bias_0"
        new_name = Wemb_prefix + "/softmax/%s_%s" % (wb, type)

    # layer norm, decoder_l1_ffn_ffn_ln_scale
    if tokens[-2] == "ln":
        if tokens[-4] == "self":
            suffix = ""
        elif tokens[-4] == "context":
            suffix = "_1"
        else:
            # encoder has only one layernorm
            if endec_name == "encoder":
                suffix = "_1"
            else:
                suffix = "_2"
        new_name = prefix + "/" + endec_name + \
            ("/layer_%s/" % layer_id) + \
            "layer_norm%s/layer_norm_%s" % (suffix, tokens[-1])
        # print "REPLACE %s to %s" % (name, new_name)
        # continue

    # write to new_model_dict
    if new_name != "":
        # no transpose only on Emb
        if tokens[1] == "Wemb":
            new_model_dict[new_name] = values
        else:
            new_model_dict[new_name] = np.transpose(values)
        print "REPLACE %s ||| %s ||| dtype:%s" % (name, new_name, values.dtype)
# basic parameters
new_model_dict["%s/dec_heads" % lang] = np.array([[8.8888]], dtype=np.float32)
new_model_dict["%s/enc_heads" % lang] = np.array([[8.8888]], dtype=np.float32)
new_model_dict["%s/dec_layers" %
               lang] = np.array([[3.3333333]], dtype=np.float32)
new_model_dict["%s/enc_layers" %
               lang] = np.array([[4.44444444444]], dtype=np.float32)
print new_model_dict["%s/dec_heads" %
                     lang], new_model_dict["%s/dec_heads" % lang].dtype

np.savez("s.model", **new_model_dict)

print "=" * 100
# Total size
print "Toal Size: %d, %dMB" % (all_s, all_s / 1024 ** 2)
