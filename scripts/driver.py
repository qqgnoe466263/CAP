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
    6: "pt6.cmd",        
    7: "pt7.cmd",        
}

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
    if str(result).find(content) > -1:
        print('[*] result    : Read Access\n')
    else:
        print('[*] result    : Read Fail\n')
