#!/usr/bin/python3

import os
import subprocess


def hello(project_dir):
    os.chdir(project_dir)
    subprocess.call(["echo $(date '+%s')>> /tmp/crontab.txt"], shell=True)
    subprocess.call(["echo $(pwd) >> /tmp/crontab.txt"], shell=True)
    print('hello, crontab')


def cleandb(project_dir):
    os.chdir(project_dir)
    subprocess.call(["echo $(date '+%s')>> /tmp/crontab.txt"], shell=True)
    subprocess.call(["echo cleandb >> /tmp/crontab.txt"], shell=True)
    subprocess.call(["cd {} && echo $(pwd) >> /tmp/crontab.txt && python3 manage.py cleandb".format(project_dir)], shell=True)