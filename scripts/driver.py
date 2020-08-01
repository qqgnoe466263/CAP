#!/usr/bin/env python3
import sys
import os
import subprocess
from subprocess import PIPE, Popen

test_case = {
    0: "pt0.cmd",        
    1: "pt1.cmd",        
    2: "pt2.cmd",        
    3: "pt3.cmd",        
    4: "pt4.cmd",        
    5: "pt5.cmd",        
}

RED = '\033[91m'
GREEN = '\033[92m'
WHITE = '\033[0m'
fail = 0;

def printInColorNor(fl, res):
    print(f"[*] result : ", end='')
    if res > -1 and fl == 'pass':
        print(f"{GREEN} PASS{WHITE}")
    else:
        print(f"{RED} FAIL{WHITE}")
        global fail
        fail = 1

def printInColorSec(fl, con, res):
    print(f"[*] result : ", end='')
    if con[0] == '200' and res > -1:
        print(f"{RED} ILLEGAL ACCESS{WHITE}")
        global fail
        fail = 1
    else:
        print(f"{GREEN} PASS{WHITE}")

for i in range(len(test_case)):
    f = open("traces/" + test_case[i], "r")
    testing_type = f.readline() # type
    testing_cmd = f.readline() # command
    content = f.readline()[:-1] # expected response
    flag = f.readline()[:-1] # pass / fail


    s = (testing_cmd.split('\n')[0]).split(' ')
    proc = subprocess.Popen(s, stdout=subprocess.PIPE) 
    result = proc.stdout.readline()
    print('[+] Test type : {}'.format(testing_type[:-1]))
    print('[+] Test      : {}'.format(testing_cmd[:-1]))

    if testing_type[:-1] == 'Security Test':
        content = content.split(' ')
        printInColorSec(flag, content, str(result).find(content[1]))
    else:
        printInColorNor(flag, str(result).find(content))

if fail == 1:
    os.system("kill `pidof http_server`")
    sys.exit(1)
