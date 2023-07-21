import subprocess


def run_cmd(cmd):
    """执行命令"""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')


def run_cmd2(cmd):
    """执行命令"""

    print('cmd:', cmd)
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.stdout, p.stderr
