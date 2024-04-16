import pandas as pd
from utils import KAGGLE_ROOT


target_col = 'Rings'
COMP_ROOT = KAGGLE_ROOT / 'playground-series-s4e4'


def process_feats(df):
    """Default processing function run in all NBs"""
    df['Sex'] = pd.Categorical(df['Sex']).codes


def get_train_df():
    train_df = pd.read_csv(COMP_ROOT / 'train.csv')
    train_ids = train_df['id']
    train_x_df = train_df.drop(['id', target_col], axis=1)
    train_y_df = train_df[target_col]
    process_feats(train_x_df)
    return train_x_df, train_y_df, train_ids


def get_test_df():
    test_df = pd.read_csv(COMP_ROOT / 'test.csv')
    test_ids = test_df['id']
    process_feats(test_df)
    return test_df.drop('id', axis=1), test_ids
