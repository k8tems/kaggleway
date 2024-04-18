import pandas as pd
from .utils import KAGGLE_ROOT
from utils import submit


target_col = 'Rings'
COMP_ROOT = KAGGLE_ROOT / 'playground-series-s4e4'


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


def stage_submission(ids, preds, f_name):
    sub_df = pd.DataFrame()
    sub_df['id'] = ids
    sub_df['Rings'] = preds
    f_name = f'/notebooks/ps4e4/submissions/{f_name}'
    sub_df.to_csv(f_name, index=False)
    return f_name


def submit_ps4e4(f_name, msg):
    submit('playground-series-s4e4', f_name, msg)
