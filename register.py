#!/usr/bin/env python

import os
import sys
import json
import subprocess
from os import path



def get_pwd():
    res = subprocess.run('pwd',capture_output=True,shell=True,text=True)
    pres_dir = res.stdout.split('\n')[0] # remove line feed
    return pres_dir
    
def int_or_not(value):
    try:
    	int(value)
    	return True
    except ValueError:
    	return False

def get_list(dir_path):
    if path.exists('st_dict.json'):
        file1 = open('st_dict.json','r')
        dc = json.load(file1)

    else:
        file1 = open('st_dict.json','w')
        ls_files_only = 'ls -p | grep -E \'.mkv$|.webm$|.flv$|.gif$|.mov$|.avi$|.mpg$|.mpeg$|.mp4$|.m4p$|.m4v$|.wmv|.ogg|.ogv\''
        ls_cmnd = 'cd '+"\'"+dir_path+"\'"+' && '+ls_files_only
        p = subprocess.run(ls_cmnd, shell=True, capture_output=True, text=True)
        file_list = (p.stdout).split('\n')
        if file_list[len(file_list)-1]=='':
            file_list = file_list[:len(file_list)-1]
        status = [False]*len(file_list)
        dc = dict(zip(file_list,status))
        json.dump(dc,file1)
    
    return dc

def reset_record(dir_path):
    if path.exists('st_dict.json'):
        st = 'rm st_dict.json'
        subprocess.run(st,shell=True)
    return get_list(dir_path)

def set_true(khata, key):
    file1 = open('st_dict.json','w')
    khata[key] = True
    json.dump(khata,file1)

def run_next(khata,dir_path):
    i = 0;
    dir_path = get_pwd()
    for key in khata :
        if khata[key]==False:
            set_true(khata,key)
            file_path = dir_path+'/'+key
            if not path.exists(file_path):
                print('Video not found at ',file_path)
            else:
                cmnd = 'vlc '+'\"'+file_path+'\"'
                subprocess.run(cmnd,shell=True,capture_output=True)
            break
    first_screen(khata,dir_path)



def run_this_one(khata,dir_path,serial_no):
    i = 0
    for key in khata:
        i+=1
        if i>serial_no or serial_no<=0 or serial_no>len(khata):
            print('wrong entry')
            break
        elif i==serial_no:
            set_true(khata,key)
            file_path = dir_path+'/'+key
            if not path.exists(file_path):
                print('Video not found at ',file_path)
            else:
                cmnd = 'vlc '+'\"'+file_path+'\"'
                subprocess.run(cmnd,shell=True,capture_output=True)
            break
    subprocess.run('clear')
    first_screen(khata,dir_path)


def display_records(khata):
    # subprocess.run('clear',shell=True)
    i = 1
    print(' { ">>" means watched, "--" means not watched }\n')
    tru = '(>>)'
    fls = '(--)'
    for key in khata:
        if khata.get(key):
            print(tru,'[',i,']',key)
        else:
            print(fls,'[',i,']',key)
        i+=1

def statistics(khata):
    # subprocess.run('clear',shell=True)
    t=f=0
    for key in khata:
        if khata[key]:
            t+=1
        else:
            f+=1
    tot = t+f
    if tot>0:
        per = int((t/tot)*100)
    else:
    	per = 0
    print('-----------------------------------'.center(term_wid))
    print('    TOTAL VIDEOS       --> %d'.center(term_wid)%(tot))
    print('-----------------------------------'.center(term_wid))
    print('    VIDEOS WATCHED     --> %d'.center(term_wid)%(t))
    print('-----------------------------------'.center(term_wid))
    print('    PERCENTAGE WATCHED --> %d '.center(term_wid)%(per))
    print('-----------------------------------'.center(term_wid))

def print_menu():
    # subprocess.run('clear',shell=True)
    print('__________________Enter A Choice________________'.center(term_wid))
    print('|   |                                           |'.center(term_wid))
    print('| 1 | LIST THE VIDEOS                           |'.center(term_wid))
    print('|---|-------------------------------------------|'.center(term_wid))
    print('| 2 | PLAY the NEXT VIDEO                       |'.center(term_wid))
    print('|---|-------------------------------------------|'.center(term_wid))
    print('| 3 | PLAY A PARTICULAR VIDEO                   |'.center(term_wid))
    print('|---|-------------------------------------------|'.center(term_wid))
    print('| 4 | RESET STATUS of all videos TO UNWATCHED   |'.center(term_wid))
    print('|---|-------------------------------------------|'.center(term_wid))
    print('| 5 | DISPLAY STATISTICS                        |'.center(term_wid))
    print('|---|-------------------------------------------|'.center(term_wid))
    print('|                                               |'.center(term_wid))
    print('|       ------ enter SPACE TO EXIT ------       |'.center(term_wid))
    print('|_______________________________________________|\n'.center(term_wid))
    choice = str(input('--> '))
    return choice

def first_screen(khata,dir_path):
    # subprocess.run('clear',shell=True)
    choice = '1'
    while choice != ' ' or choice != '\n':
        # subprocess.run('clear')
        choice = print_menu()
        if choice == ' ':
            subprocess.run('clear')
            sys.exit()
        elif choice == '1':
            subprocess.run('clear')
            display_records(khata)
        elif choice == '2':
            subprocess.run('clear')
            run_next(khata,dir_path)
        elif choice == '3':
            subprocess.run('clear')
            display_records(khata)
            print('______________________________________________________'.center(term_wid))
            print('|  enter the serial number of the file you wanna play |'.center(term_wid))
            serial_no = (input('|_____________________________________________________|'.center(term_wid)))
            if int_or_not(serial_no):
            	serial_no = int(serial_no)
            	run_this_one(khata,dir_path,serial_no)
            else:
            	print('Wrong Input')
        elif choice == '4':
            subprocess.run('clear')
            khata = reset_record(dir_path)
            statistics(khata)
        elif choice == '5':
            subprocess.run('clear')
            statistics(khata)
        else:
            subprocess.run('clear')
            print('invalid choice')

term_wid = os.get_terminal_size().columns
subprocess.run('clear')
dir_path = get_pwd()
khata = get_list(dir_path)
statistics(khata)
print('\n')
first_screen(khata,dir_path)

