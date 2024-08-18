import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder


COMP_NAME = 'playground-series-s4e8'
TARGET_COL = 'class'


def parse_df(df):
    return df, df.pop('id')


class Competition:
    def __init__(self, name: str, kaggle_root: Path = None):
        self.comp_root = (Path(kaggle_root) or Path('../../kaggle/input')) / name

    @property
    def train_df(self):
        raise NotImplementedError()

    @property
    def parsed_train_df(self):
        raise NotImplementedError()

    @property
    def test_df(self):
        raise NotImplementedError()

    @property
    def parsed_test_df(self):
        raise NotImplementedError()


class GenericPlaygroundCompetition(Competition):
    def __init__(self, comp_name, kaggle_root: Path = None):
        super(GenericPlaygroundCompetition, self).__init__(comp_name, kaggle_root=kaggle_root)

    def read_csv(self, f_name):
        return pd.read_csv(self.comp_root / f_name)

    @property
    def train_df(self):
        return self.read_csv('train.csv')

    @property
    def parsed_train_df(self):
        train_x_df, train_ids = parse_df(comp.train_df)
        train_y_df = train_x_df[TARGET_COL]
        return train_x_df.drop(TARGET_COL, axis=1), train_y_df, train_ids

    @property
    def test_df(self):
        return self.read_csv('test.csv')

    @property
    def parsed_test_df(self):
        return parse_df(self.test_df)


class YEncoder:
    def __init__(self):
        self.enc_ = LabelEncoder()

    def enc(self, x):
        return self.enc_.fit_transform(x)

    def dec(self, x):
        return self.enc_.inverse_transform(x)


comp = GenericPlaygroundCompetition(COMP_NAME, '/kaggle/input')
