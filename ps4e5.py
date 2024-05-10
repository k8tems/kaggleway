import pandas as pd
from utils import KAGGLE_ROOT, submit, stage_df
from pathlib import Path


target_col = 'FloodProbability'
COMP_ROOT = KAGGLE_ROOT / 'playground-series-s4e5'
SUBMISSION_DIR = Path('/notebooks/ps4e5/submissions')


class Competition:
    def __init__(self, name: str, kaggle_root: Path = None):
        self.comp_root = (Path(kaggle_root) or Path('/kaggle/input')) / name

    def get_train_df(self):
        raise NotImplementedError()

    def get_test_df(self):
        raise NotImplementedError()


def process_feats(df):
    """Default processing function run in all NBs"""


class PS4E5(Competition):
    def __init__(self, kaggle_root: Path = None):
        super(PS4E5, self).__init__('playground-series-s4e5', kaggle_root=kaggle_root)

    def get_train_df(self):
        train_df = pd.read_csv(self.comp_root / 'train.csv')
        train_ids = train_df.pop('id')
        train_y_df = train_df.pop(target_col)
        process_feats(train_df)
        return train_df, train_y_df, train_ids

    def get_test_df(self):
        test_df = pd.read_csv(self.comp_root / 'test.csv')
        process_feats(test_df)
        return test_df, test_df.pop('id')


class PS4E5Submission:
    def __init__(self, d_name):
        self.d_name = d_name

    def stage(self, ids, preds):
        sub_df = pd.DataFrame()
        sub_df['id'] = ids
        sub_df[target_col] = preds
        return stage_df(self.d_name, sub_df)

    def submit(self, msg, f_name=''):
        submit('playground-series-s4e5', msg, d_name=self.d_name, f_name=f_name)
