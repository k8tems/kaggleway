import pandas as pd
from utils import submit, stage_df, Competition
from pathlib import Path


TARGET_COL = 'FloodProbability'
COMP_NAME = 'playground-series-s4e5'


def process_feats(df):
    """Default processing function run in all NBs"""


class PS4E5(Competition):
    def __init__(self, kaggle_root: Path = None):
        super(PS4E5, self).__init__(COMP_NAME, kaggle_root=kaggle_root)

    def read_csv(self, f_name):
        return pd.read_csv(self.comp_root / f_name)

    def get_train_df(self):
        train_df = self.read_csv('train.csv')
        train_ids = train_df.pop('id')
        train_y_df = train_df.pop(TARGET_COL)
        process_feats(train_df)
        return train_df, train_y_df, train_ids

    def get_test_df(self):
        test_df = self.read_csv('test.csv')
        process_feats(test_df)
        return test_df, test_df.pop('id')


class PS4E5Submission:
    def __init__(self, d_name):
        self.d_name = d_name

    def stage(self, ids, preds):
        sub_df = pd.DataFrame()
        sub_df['id'] = ids
        sub_df[TARGET_COL] = preds
        return stage_df(self.d_name, sub_df)

    def submit(self, msg, f_name=''):
        submit(COMP_NAME, msg, d_name=self.d_name, f_name=f_name)
