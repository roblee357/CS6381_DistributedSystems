import csv
from subprocess import Popen, PIPE
import os              # OS level utilities
import sys
import argparse   # for command line parsing

from signal import SIGINT
from time import time, sleep

import subprocess, random

# These are all Mininet-specific
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.util import pmonitor

# This is our topology class created specially for Mininet
from ps_topology import PS_Topo



class SystemTest():
    def __init__(self, net):

        for host in net.hosts:
            print('host.name',host.name)

        commands = []
        with open('commands.txt','r') as fin:
            for line in fin:
                commands.append(line.strip())

        with open('System_Test.csv','r') as fin:
            spamreader = csv.reader(fin, delimiter=',', quotechar='|')
            for row in spamreader:
                i = 0
                for i in range(len(row)):
                    host_name = commands[i].split(' ')[0]
                    if '1' in row[i]:
                        cmd_str = ' '.join(commands[i].split(' ')[1:])
                        print('start',host_name,cmd_str)
                        net.host(host_name).sendCmd('ifconfig &> log_broker/' + host_name + '.out &', printPid = True)
                        print('PID', net.host(host_name).sendCmd(cmd_str, printPid = True))

                    if '0' in row[i]:
                        print(net.host(host_name).name, 'stopping')
                        # net.host(host_name).cmd(cmd_str)
                        net.host(host_name).stop
                sleep(1)
                print('the test continues...')

        # i = 1
        # print('net.hosts',net.host('s1h1').cmd)
        # for host in net.hosts:
        #     host.cmd( 'python3 dsorb.py ' + str(i)  +  ' -b broker_on &> log_discovery_server_OR_broker.out & ')
        #     i += 1
        # print('we will wait a bit then destroy the brokers')
        # sleep(10)
        # for host in net.hosts:
        #     host.cmd( 'kill %' + 'python3')
        #     i += 1





