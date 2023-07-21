from datetime import datetime
import sys
from pathlib import Path


PJ_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PJ_DIR))


from utils.path_manager import create_dir
from utils.run_cmd import run_cmd2


def backup_db():
    print("start backup db")

    create_dir('dbback')
    curtime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    cmd = f'/www/server/pyporject_evn/94d7bd8179533c59aca987c718472328_venv/bin/python3 manage.py dumpdata > dbback/db{curtime}.json --indent=4'

    stdout, stderr = run_cmd2(cmd)
    print(stdout, stderr)


def print_hl():
    print('hl')


if __name__ == '__main__':
    backup_db()
    # print_hl()

