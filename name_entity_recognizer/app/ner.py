# -*- coding: utf-8 -*-
#import fastai
#from fastai.text import *
#from fastai.lm_rnn import *
#from sebastian.eval import eval_ner
from .fastai_seq_utilities import *
from . import utilities_tgdd as utilities
from pathlib import Path
from torch.autograd import Variable
from functools import partial
from .util import PreprocessClass

import torch
import pickle
import collections
import torch.optim as optim
import sys
import os



class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class NERTAG(metaclass=Singleton):
        
    # Define constant
    START_TAG = "<START>"
    STOP_TAG = "<STOP>"
    LM_PATH = "models/lm"
    PRINT_FLAG = False
    
    dir_path = Path(LM_PATH)
    id2token = pickle.load(open('./name_entity_recognizer/models/itos.pkl', 'rb'))
    token2id = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(id2token)})
    
    id2label = ['_pad_', '_xbos_', '_xfld_', '_1_', 'O', 'B-feature', 'I-feature', 'B-product', 'I-product', 'B-app', 'I-app', '<START>', '<STOP>']
    tag_to_idx = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(id2label)})
    tagset_size = len(id2label)
    def __init__(self):
        
        self.model = load_model_seq(self.LM_PATH, \
      lm_id='', train_file_id='', tag_to_idx=self.tag_to_idx, tagset_size=self.tagset_size, clas_id=None, bs=64, cl=1, backwards=False, bidir=False, \
      startat=0, unfreeze=True, lr=0.01, dropmult=1, pretrain=True, bpe=False, \
      use_clr=False, use_regular_schedule=False, use_discriminative=True, last=False, \
      chain_thaw=True, from_scratch=False, freeze_word2vec=False, \
      n_cycle=4, cycle_len=1, cycle_mult=2, linear_decoder_dp=0.2, \
      id2token=self.id2token, id2label=self.id2label, classifier_filename="clas_seqforward.h5")
        
    def predict_raw(self, raw):
        return self._predict_single(raw)
        
    # def predict(self, mentions):
    #     if not isinstance(mentions, list):
    #         mentions = [mentions]
    #     input_text = []
    #     results = []
    #     for doc in mentions:
    #         input_text.append(doc.content)
    #
    #     result_predicted = list(map(lambda x: self._predict_single(x), input_text))
    #
    #     for index, result_value in enumerate(result_predicted):
    #         result = rest_api_pb2.PredictResult()
    #         result.id = mentions[index].id
    #         result.tags.extend(result_value)
    #         results.append(result)
    #
    #     return results

    def predict_products(self, name_list):
        if not isinstance(name_list, list):
            name_list = [name_list]

        result_predicted = list(map(lambda x: self._predict_single(x), input_text))
        result_predicted = [self.predict_product(name) for name in name_list]

        return results

    def predict_product(self, name):
        result = []
        scores, processed_text = predict_text(self.token2id, self.model, name)

        predicted = scores

        # Print result
        for word, tag in zip(processed_text, predicted):
            result.append(self.id2label[tag])
        return self._extract_product_name(result, name)

    def _extract_product_name(self, id2label_sequence, name):
        prefix_lst = ['_pad_', '_xbos_', '_xfld_', '_1_']
        res_sequence = [x for x in id2label_sequence if x not in prefix_lst]
        name_to_list = name.lower().split(" ")
        id_name_zip = zip(res_sequence, name_to_list)
        product_name, count = "", 0

        for id_tag, name_ele in id_name_zip:
            if id_tag in ["B-product", "I-product"] and name_ele not in ['điện', 'thoại', 'hàng', 'chính', 'hãng']:
                if id_tag == "B-product":
                    count += 1
                if id_tag == "I-product":
                    if 'gb' in name_ele:
                        continue
                if name_ele in ['-']:
                    break
                product_name += " %s" % name_ele

                if count == 2:
                    break
        if product_name is "":
            product_name = "Sản phẩm chung"
        print(product_name)
        print(name_to_list)
        print(res_sequence)
        print('-----------------------')
        return product_name


    # def _predict_single(self, mention):
    #
    #     result = []
    #     scores, processed_text = predict_text(self.token2id, self.model, mention)
    #
    #     predicted = scores
    #
    #     # Print result
    #     for word, tag in zip(processed_text, predicted):
    #         result.append(self.id2label[tag])
    #     return result
    
def load_model_seq(dir_path="", lm_id='', train_file_id='', tag_to_idx='', tagset_size='', clas_id=None, bs=64, cl=1, \
              backwards=False, bidir=False, startat=0, unfreeze=True, lr=0.01, dropmult=1.0, \
              pretrain=True, bpe=False, use_clr=True, use_regular_schedule=False, \
              use_discriminative=True, last=False, chain_thaw=False, from_scratch=False, \
              freeze_word2vec=False, n_cycle=3, cycle_len=1, cycle_mult=2, linear_decoder_dp=0.1, \
              id2token={}, id2label={}, classifier_filename="clas_seqforward.h5"):
     
    PRE = 'bwd_' if backwards else ''
    PRE = 'bpe_' + PRE if bpe else PRE

    train_file_id = train_file_id if train_file_id == '' else f'_{train_file_id}'

    dir_path = "./name_entity_recognizer/%s" % dir_path

    dir_path = Path(dir_path)
    lm_id = lm_id if lm_id == '' else f'{lm_id}_'
    clas_id = lm_id if clas_id is None else clas_id
    clas_id = clas_id if clas_id == '' else f'{clas_id}_'

    lm_file = f'{PRE}{lm_id}fwd_lm_tgdd_lm_enc'

    lm_path = dir_path / f'{lm_file}.h5'
    assert lm_path.exists(), f'Error: {lm_path} does not exist.'
    
    """hyperaparameter settings"""
    bptt,em_sz,nh,nl = 70,400,1150,3
    dps = np.array([0.4,0.5,0.05,0.3,0.4])*dropmult
    opt_fn = partial(optim.Adam, betas=(0.8, 0.99))
    
    """load datasets"""
    c = len(id2label)

    if bpe:
        vs=30002
    else:
        vs = len(id2token)
    
    m = get_rnn_seq_tagger(bptt, 70, c, vs, emb_sz=em_sz, n_hid=nh, n_layers=nl, pad_token=1,
                  layers=[em_sz, 50, c], drops=[dps[4], 0.1],
                  dropouti=dps[0], wdrop=dps[1], dropoute=dps[2], dropouth=dps[3], \
                  linear_decoder_dp=linear_decoder_dp, tag_to_idx=tag_to_idx, tagset_size=tagset_size)
    m.load_state_dict(torch.load(dir_path / classifier_filename, map_location=lambda storage, loc: storage))
    m.reset()
    m.eval()
    
    return m

def predict_text(stoi, model, text):
    prefix_str = ['\nxbos', 'xfld', '1']

    texts = [text]

#    tok = list(map(lambda x: x.split(), texts))
    tok = [PreprocessClass.convert(s).split() for s in texts]

    preprocessed = tok[0]
    preprocessed = [utilities.map_number_and_punct(p.lower()) for p in tok[0]]
    preprocessed = prefix_str + preprocessed
    
    
    # turn into integers for each word
    encoded = [stoi[p] for p in preprocessed]

    ary = np.reshape(np.array(encoded),(-1,1))

    # turn this array into a tensor
    tensor = torch.from_numpy(ary)

    # wrap in a torch Variable
    variable = Variable(tensor)

    # do the predictions
    predictions = model((variable, []))

    return predictions[1], preprocessed

def predict_processed(model, encoded):
    ary = np.reshape(np.array(encoded),(-1,1))

    tensor = torch.from_numpy(ary)

    variable = Variable(tensor)

    # do the predictions
    predictions = model((variable, []))

    return predictions[1]

#model = load_model_seq(LM_PATH, \
#      lm_id='', train_file_id='', clas_id=None, bs=64, cl=1, backwards=False, bidir=False, \
#      startat=0, unfreeze=True, lr=0.01, dropmult=1, pretrain=True, bpe=False, \
#      use_clr=False, use_regular_schedule=False, use_discriminative=True, last=False, \
#      chain_thaw=True, from_scratch=False, freeze_word2vec=False, \
#      n_cycle=4, cycle_len=1, cycle_mult=2, linear_decoder_dp=0.2, \
#      id2token=id2token, id2label=id2label, classifier_filename="clas_seqforward.h5")
#text = "ip6 với ss7 cái nào nhanh hơn"
#ner_model = NERTAG()
#ner_model.predict_raw(text)



