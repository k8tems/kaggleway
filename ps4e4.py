import pandas as pd
from .utils import KAGGLE_ROOT, submit, get_csv_f_name
from pathlib import Path


target_col = 'Rings'
COMP_ROOT = KAGGLE_ROOT / 'playground-series-s4e4'
SUBMISSION_DIR = Path('/notebooks/ps4e4/submissions')


def process_feats(df):
    """Default processing function run in all NBs"""
    df['Sex'] = pd.Categorical(df['Sex']).codes


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
    sub_df['Rings'] = preds
    f_name = f'/notebooks/ps4e4/submissions/{get_csv_f_name()}'
    sub_df.to_csv(f_name, index=False)
    return f_name


def submit_ps4e4(msg, f_name=''):
    # f_nameが指定されてなければSUBMISSION_DIRの最新のcsvが採用される
    submit('playground-series-s4e4', msg, d_name=SUBMISSION_DIR, f_name=f_name)
