import sys
import csv
import subprocess
import argparse


def load_csv(f_name):
    with open(f_name, 'r', encoding='utf8') as f:
        return list(csv.reader(f))


def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{cmd}':", e.stderr)
        return None


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_path', type=str, default='dataset.csv',
                        help='Location of csv file containing the list of datasets to download')
    parser.add_argument('dst_path', type=str, default='/kaggle/input',
                        help='Directory where the unzipped folder will be saved at')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    csv_data = load_csv(args.csv_path)
    for name, data_type in csv_data:
        if data_type == 'c':
            cmd = 'kaggle competitions download -c'
            d_name = name
        else:
            cmd = 'kaggle datasets download'
            d_name = name.split('/')[-1]
        run_cmd(f'{cmd} {name} -p {args.dst_path}')
        run_cmd(f'unzip -nd {d_name} {d_name}.zip')
