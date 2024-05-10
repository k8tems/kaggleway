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


class PS4E5(Competition):
    def __init__(self, kaggle_root: Path = None):
        super(PS4E5, self).__init__('playground-series-s4e5', kaggle_root=kaggle_root)

    def get_train_df(self):
        train_df = pd.read_csv(self.comp_root / 'train.csv')
        train_ids = train_df.pop('id')
        train_y_df = train_df.pop(target_col)
        process_feats(train_df)
        return train_df, train_y_df, train_ids


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
