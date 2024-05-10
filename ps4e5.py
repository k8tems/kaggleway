import pandas as pd
from .utils import KAGGLE_ROOT, submit, stage_df
from pathlib import Path


target_col = 'FloodProbability'
COMP_ROOT = KAGGLE_ROOT / 'playground-series-s4e5'
SUBMISSION_DIR = Path('/notebooks/ps4e5/submissions')


def process_feats(df):
    """Default processing function run in all NBs"""


def get_train_df():
    train_df = pd.read_csv(COMP_ROOT / 'train.csv')
    train_ids = train_df.pop('id')
    train_y_df = train_df.pop(target_col)
    process_feats(train_df)
    return train_df, train_y_df, train_ids


def get_test_df():
    test_df = pd.read_csv(COMP_ROOT / 'test.csv')
    process_feats(test_df)
    return test_df, test_df.pop('id')


def stage_submission(ids, preds):
    sub_df = pd.DataFrame()
    sub_df['id'] = ids
    sub_df[target_col] = preds
    return stage_df(SUBMISSION_DIR, sub_df)


def submit_ps4e5(msg, f_name=''):
    # f_nameが指定されてなければSUBMISSION_DIRの最新のcsvが採用される
    submit('playground-series-s4e5', msg, d_name=SUBMISSION_DIR, f_name=f_name)
