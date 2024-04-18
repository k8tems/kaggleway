from pytz import timezone
from datetime import datetime
import kaggle
from pathlib import Path


KAGGLE_ROOT = Path('/kaggle/input')


def ls(p):
    return list(p.glob('*'))


def auth():
    kaggle.api.authenticate()


def submit(comp_id, f_name, msg):
    kaggle.api.competition_submit(f_name, msg, comp_id)


def get_latest_submission_score(competition_name):
    submissions = kaggle.api.competitions_submissions_list(id=competition_name)
    return float(submissions[0]['publicScore'])


def get_csv_f_name():
    return datetime.now(timezone("Asia/Tokyo")).strftime("%Y_%m_%d_%H_%M") + ".csv"
