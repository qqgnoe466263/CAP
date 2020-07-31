#!/usr/bin/env python
import sys
import os
import subprocess
from subprocess import PIPE, Popen


test_case = {
    1: "test_pt.cmd",        
    2: "test_pt1.cmd",        
    3: "test_pt2.cmd",        
    4: "test_pt3.cmd",        
    5: "test_pt4.cmd",        
    6: "test_pt5.cmd",        
    7: "test_pt6.cmd",        
}

testList = test_case.keys()

for i in range(len(testList)):
    f = open("traces/" + test_case[testList[i]], "r")
    testing_cmd = f.readline()
    content = f.readline()[:-1]

    s = (testing_cmd.split('\n')[0]).split(' ')
    proc = subprocess.Popen(s, stdout=subprocess.PIPE) 
    result = proc.stdout.readline()
    print '[+] Test   :',testing_cmd[:-1]
    if result.find(content) > -1:
        print '[*] result : pass'
    else:
        print '[*] result : fail'
