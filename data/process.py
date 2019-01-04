#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import scipy.io as scio

# data = scio.loadmat('data.mat')


import h5py
import numpy as np
from collections import OrderedDict

with h5py.File('data.mat', 'r') as f:
    print(dict(f['data']))
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

    result = dict()
    for idx, test in enumerate(perm_test):
        item = OrderedDict()
        test_start, test_end = test_frame_idx[idx].astype(np.int)
        test_binary_code = B_test[test_start-1:test_end]
        test_idx = int(test[0])
        for data_idx, data_frame_idx in enumerate(db_frame_idx):
            if test_idx == data_idx:
                continue
            data_start, data_end = data_frame_idx.astype(np.int)
            data_binary_code = B_db[data_start-1:data_end]
            import pdb
            pdb.set_trace()

# import hdf5storage
# data = hdf5storage.loadmat('data.mat')
