#!/usr/bin/env python3
import sys
import os
import subprocess
from subprocess import PIPE, Popen


test_case = {
    0: "test_pt8.cmd",        
    1: "test_pt.cmd",        
    2: "test_pt5.cmd",        
    3: "test_pt2.cmd",        
    4: "test_pt1.cmd",        
    5: "test_pt3.cmd",        
    6: "test_pt4.cmd",        
    7: "test_pt6.cmd",        
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
