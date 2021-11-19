import subprocess
import shlex
command = "/home/sliti-wassim/anaconda3/envs/map4/bin/python Mp4.py --option1 -dir /path/to/dir"
args = shlex.split(command)
my_subprocess = subprocess.Popen(args)
