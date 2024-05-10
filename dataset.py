import sys
import csv
import subprocess


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


if __name__ == '__main__':
    csv_data = load_csv(sys.argv[1])
    dst = sys.argv[2]
    for name, data_type in csv_data:
        if data_type == 'c':
            cmd = 'kaggle competitions download -c'
            d_name = name
        else:
            cmd = 'kaggle datasets download'
            d_name = name.split('/')[-1]
        run_cmd(f'{cmd} {name} -p {dst}')
        run_cmd(f'unzip -nd {d_name} {d_name}.zip')
