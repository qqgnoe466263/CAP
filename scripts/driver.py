#!/usr/bin/env python3
import sys
import os
import subprocess
from subprocess import PIPE, Popen

test_case = {
    0: "pt0.cmd",        
    1: "pt1.cmd",        
    2: "pt2.cmd",        
    3: "pt5.cmd",        
    4: "pt6.cmd",        
    5: "pt7.cmd",        
}

RED = '\033[91m'
GREEN = '\033[92m'
WHITE = '\033[0m'

def printInColor(res, t):
    print(f"[*] result : ", end='')
    if t == "Normal Test":
        if res > -1:
            print(f"{GREEN} PASS{WHITE}")
        else:
            print(f"{RED} FAIL{WHITE}")
    elif t == "Security Test":
        if res > -1:
            print(f"{RED} ILLEGAL ACCESS{WHITE}")
        else:
            print(f"{GREEN} PASS{WHITE}")

for i in range(len(test_case)):
    f = open("traces/" + test_case[i], "r")
    testing_type = f.readline()
    testing_cmd = f.readline()
    content = f.readline()[:-1]

    s = (testing_cmd.split('\n')[0]).split(' ')
    proc = subprocess.Popen(s, stdout=subprocess.PIPE) 
    result = proc.stdout.readline()
    print('[+] Test type : {}'.format(testing_type[:-1]))
    print('[+] Test      : {}'.format(testing_cmd[:-1]))
    printInColor(str(result).find(content), format(testing_type[:-1]))
    # if str(result).find(content) > -1:
        # # print('[*] result    : Read Access\n')
    # else:
    #     print('[*] result    : Read Fail\n')
