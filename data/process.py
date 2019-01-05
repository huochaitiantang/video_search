#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import scipy.io as scio

# data = scio.loadmat('data.mat')


import h5py
import numpy as np
from collections import OrderedDict
import gmpy


def count_diff_code(q_codes, g_codes):
    cnt = 0
    assert len(q_codes) == 4
    assert len(g_codes) == 4
    for i in range(len(q_codes)):
        cnt += gmpy.popcount(int(q_codes[i]^g_codes[i]))
    return cnt

def similarity(query, gallery):
    s = 0.0
    for q_code in query:
        for g_code in gallery:
            if count_diff_code(q_code, g_code) <= 3:
                s += 1
    return s
    # return s/len(gallery)

with h5py.File('data.mat', 'r') as f:
    data = f['data']

    db_num = np.array(data['db_num'][()])
    test_num = np.array(data['test_num'][()])
    perm_test = np.array(data['perm_test'][()])
    db_labels = np.array(data['db_labels'][()]).T
    test_labels = np.array(data['test_labels'][()]).T
    B_db = np.array(data['B_db'][()]).T
    B_test = np.array(data['B_test'][()]).T
    db_frame_idx = np.array(data['db_frame_idx'][()]).T
    test_frame_idx = np.array(data['test_frame_idx'][()]).T

    result = OrderedDict()
    with open('rank_opt.txt', 'w') as res_f:
        for query_idx, query in enumerate(db_frame_idx):
            print('Query video:{}'.format(query_idx))
            item = OrderedDict()
            query_start, query_end = db_frame_idx[query_idx].astype(np.int)
            query_binary_code = B_db[query_start-1:query_end]
            res_f.write('({} {}) '.format(query_idx, db_labels[query_idx].argmax()))
            for data_idx, data_frame_idx in enumerate(db_frame_idx):
                if query_idx == data_idx:
                    continue
                data_start, data_end = data_frame_idx.astype(np.int)
                data_binary_code = B_db[data_start-1:data_end]
                sim = similarity(query_binary_code, data_binary_code)
                item[data_idx] = sim
                # sort by sim
            item = sorted(item.items(), key=lambda obj:obj[1], reverse=True)
            result[query_idx] = item
            for idx in item:
                res_f.write('({} {} {}) '.format(idx[0], idx[1], db_labels[idx[0]].argmax()))
            res_f.write('\n')
            res_f.flush()
    # print(result)

    # process for 50 test video
    # for idx, test in enumerate(perm_test):
    #     item = OrderedDict()
    #     test_start, test_end = test_frame_idx[idx].astype(np.int)
    #     test_binary_code = B_test[test_start-1:test_end]
    #     test_idx = int(test[0])
    #     for data_idx, data_frame_idx in enumerate(db_frame_idx):
    #         if test_idx == data_idx:
    #             continue
    #         data_start, data_end = data_frame_idx.astype(np.int)
    #         data_binary_code = B_db[data_start-1:data_end]

# import hdf5storage
# data = hdf5storage.loadmat('data.mat')
