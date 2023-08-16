from datetime import datetime
import sys
from pathlib import Path


PJ_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PJ_DIR))


from utils.path_manager import create_dir
from utils.run_cmd import run_cmd2
from utils.encrypt_tool import encrypt


def backup_db():
    print("start backup db")

    create_dir('dbback')
    curtime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file = f'dbback/db{curtime}.json'
    cmd = f'/www/server/pyporject_evn/94d7bd8179533c59aca987c718472328_venv/bin/python3 manage.py dumpdata > {file} --indent=4'

    stdout, stderr = run_cmd2(cmd)
    print(stdout, stderr)
    print(f'file: {file}')
    return file


def print_hl():
    print('hl')


if __name__ == '__main__':
    file = backup_db()
    # add enctypt
    encrypt('keys\pj_sys_2023-08-16-12-45-43.key', file)
    # print_hl()

