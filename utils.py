import os
from pytz import timezone
from datetime import datetime
import kaggle
from pathlib import Path


KAGGLE_ROOT = Path('/kaggle/input')


def ls(p):
    return list(p.glob('*'))


def auth():
    kaggle.api.authenticate()


def get_latest_submission_f_name(d_name):
    return sorted(os.listdir(d_name), reverse=True)[0]


def submit(comp_id, msg, f_name='', d_name=''):
    f_name = f_name or get_latest_submission_f_name(d_name)
    print('submitting', f_name)
    kaggle.api.competition_submit(f_name, msg, comp_id)


def get_latest_submission_score(competition_name):
    submissions = kaggle.api.competitions_submissions_list(id=competition_name)
    return float(submissions[0]['publicScore'])


def get_csv_f_name():
    return datetime.now(timezone("Asia/Tokyo")).strftime("%Y_%m_%d_%H_%M") + ".csv"


def stage_df(sub_dir, df):
    f_name = f'{sub_dir}/{get_csv_f_name()}'
    df.to_csv(f_name, index=False)
    return f_name
