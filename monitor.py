import subprocess
import pyfiglet
from optparse import OptionParser
from discordwebhook import Discord
import os
import time


parser = OptionParser()

print(pyfiglet.figlet_format("Subdomain Monitor",font='digital'))

parser.add_option('-d',dest='domain',help='Enter domain name')
parser.add_option('-w',dest='webhook',help='Enter webhook url')
parser.add_option('-t',dest='time',help='Time duration')
val,args = parser.parse_args()
domain = val.domain
webhook = val.webhook
second = val.time

def send_notification(message):
        return Discord(url=webhook).post(content=message)

def exec(cmd):
        subprocess.call(cmd,shell=True)

def amass(output='.amass'):
        exec(f'amass enum -d {domain} -o {output}')

def subfinder(output='.subfinder'):
        exec(f'subfinder -d {domain} -o {output}')

def sort(output='.sorted',compare=['.subfinder','.amass']):
        exec(f'cat {compare[0]} {compare[1]} | sort -u > {output}')

def compare(file1,file2):
        arr = []
        with open(file1,'r') as data1:
                old_subdomains = data1.read().split()
        with open(file2,'r') as data:
                new_subdomains = data.read().split()
        print(old_subdomains)
        print(new_subdomains)
        switch = True
        for subdomain in new_subdomains:
                if subdomain not in old_subdomains:
                        arr.append(subdomain)
                        with open(file1,'a') as data1:
                                #print('Awesome')
                                #send_notificaton(f'Got a new subdomain: {subdomain}')
                                data1.write(f"{subdomain}\n")

        send_notification(f'[+] Got a new subdomain: {subdomain}')
        for subdomain in arr:
                send_notification(f'Subdomain: {subdomain}')

def cmd():
        amass()
        subfinder()
        sort()

#compare('old.txt','new.txt')


if __name__ == "__main__":
        while True:
                if '.sorted_new' in os.listdir():
                        cmd()
                        compare('.sorted_new','.sorted')
                        time.sleep(int(second))
                else:
                        amass()
                        #subfinder()
                        sort('.sorted_new')
                        time.sleep(1)
