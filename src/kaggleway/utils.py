import os
import pandas as pd
import torch
from torch import nn
import random
import pickle
import numpy as np
from pytz import timezone
from datetime import datetime
import kaggle
from pathlib import Path
from sklearn.preprocessing import StandardScaler


KAGGLE_ROOT = Path('../../kaggle/input')


def ls(p):
    return list(p.glob('*'))


def auth():
    kaggle.api.authenticate()


def get_latest_submission_f_name(d_name):
    return sorted(os.listdir(d_name), reverse=True)[0]


def submit(comp_id, msg, f_name='', d_name: Path = ''):
    kaggle.api.competition_submit(f_name or (Path(d_name) / get_latest_submission_f_name(d_name)), msg, comp_id)


def get_latest_submission_score(competition_name):
    submissions = kaggle.api.competitions_submissions_list(id=competition_name)
    return float(submissions[0]['publicScore'])


def get_csv_f_name():
    return datetime.now(timezone("Asia/Tokyo")).strftime("%Y_%m_%d_%H_%M") + ".csv"


def stage_df(sub_dir, df):
    f_name = f'{sub_dir}/{get_csv_f_name()}'
    df.to_csv(f_name, index=False)
    return f_name


class Competition:
    def __init__(self, name: str, kaggle_root: Path = None):
        self.comp_root = (Path(kaggle_root) or Path('../../kaggle/input')) / name

    def get_train_df(self):
        raise NotImplementedError()

    def get_test_df(self):
        raise NotImplementedError()


def set_seed(seed_value):
    torch.manual_seed(seed_value)
    np.random.seed(seed_value)
    random.seed(seed_value)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed_value)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def normalize_all(X):
    return pd.DataFrame(StandardScaler().fit_transform(X), index=X.index, columns=X.columns)


def df_to_tensor(df):
    return torch.from_numpy(df.values).float()


def get_n_iters(X, bs):
    return X.shape[0]//bs-1


def gen_batch_indices(max_idx, bs=128, shuffle=True):
    indices = list(range(max_idx))
    if shuffle:
        random.shuffle(indices)
    for i in range(len(indices) // bs + 1):
        yield indices[i*bs:(i+1)*bs]


def gen_batch(X, y=None, bs=128, shuffle=True):
    for indices in gen_batch_indices(len(X), bs=bs, shuffle=shuffle):
        x_batch = X.iloc[indices]
        if y is not None:
            yield x_batch, y.iloc[indices]
        else:
            yield x_batch


def gen_batch_t(X, y=None, device='cuda', bs=128, shuffle=True):
    """テンソルのバッチを生成する"""
    for batch in gen_batch(X, y, bs=bs, shuffle=shuffle):
        if y is not None:
            yield df_to_tensor(batch[0]).to(device), df_to_tensor(batch[1]).to(device)
        else:
            yield df_to_tensor(batch).to(device)


def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.normal_(m.weight, mean=0, std=0.02)
        if m.bias is not None:
            nn.init.constant_(m.bias, 0)


def get_device(model):
    return next(model.parameters()).device


def negative_r2_score_t(y_pred, y_true):
    ss_res = torch.sum((y_true - y_pred) ** 2)
    ss_tot = torch.sum((y_true - torch.mean(y_true)) ** 2)
    return -(1 - ss_res / ss_tot)


def dump_pickle(f_name, data):
    with open(f_name, 'wb') as f:
        pickle.dump(data, f)


def load_pickle(f_name):
    with open(f_name, 'rb') as f:
        return pickle.load(f)
