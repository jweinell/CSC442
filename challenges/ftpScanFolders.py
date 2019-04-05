#!/usr/bin/python

import argparse
import ftplib
import sys
import StringIO
import re
import pprint
import socket

host = '127.0.0.1'
port = '21'
username = ''
password = ''
startingPath = '/'
depth = 1

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Destination Host")
parser.add_argument("--port", help="Destination port")
parser.add_argument("--path", help="Starting Path")
parser.add_argument("-u","--user", help="Username")
parser.add_argument("-p","--password", help="Password")
parser.add_argument("-d","--depth", help="Maximum depth of search")
args = parser.parse_args()

#print args

if args.host: host = args.host
if args.port: port = args.port
if args.path: startingPath = args.path
if args.user: user = args.user
if args.password: password = args.password
if args.depth: depth = int(args.depth)
#if args.pass: password = args.pass


source = (host,port,username,password)

def getConnection(source):
    ftp = ftplib.FTP()

    # Establish connection
    try:
        ftp.connect(host=host, port=port, timeout = 5)
    except socket.timeout as e:
        print 'Connection has timed out'
        exit()
    except socket.error as e:
        print e
        exit()

    # Attempt to login
    try:
        ftp.login(username,password)
    except ftplib.error_perm as e:
        print e
        exit()

    return ftp

def scanPath(ftpConn, path, depth = 1):
    ftp = ftpConn
    ftp.cwd(path)
    original_stdout = sys.stdout
    filesIO = StringIO.StringIO()
    sys.stdout = filesIO
    ftp.retrlines('LIST -a')
    objects = filesIO.getvalue().split('\n')[2:]
    sys.stdout = original_stdout

    objectDef = re.compile(r'(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\s*(.*)')
    folderDef = re.compile(r'^d.*')
    folders = []
    permissionsSet = set()
    for object in objects:
        objectMatch = objectDef.search(object)
        objectHash = {}
        objectHash['permissions'] = objectMatch.group(1)
        objectHash['owner'] = objectMatch.group(3)
        objectHash['group'] = objectMatch.group(4)
        objectHash['size'] = objectMatch.group(5)
        objectHash['month'] = objectMatch.group(6)
        objectHash['day'] = objectMatch.group(7)
        objectHash['time'] = objectMatch.group(8)
        objectHash['name'] = objectMatch.group(9)

        if folderDef.match(objectHash['permissions']):
            folders.append(objectHash)

        permissionsSet.add(objectHash['permissions'])

    print(" {0:<12} {1:}".format(len(permissionsSet),path))

    if depth == 1:
        for folder in folders:
            pass
            #print(" {0:<12} {1:}".format(folder['permissions'],path + folder['name']))
    else:
        for folder in folders:
            try:
                scanPath(ftpConn,path + folder['name'] + '/', depth - 1)
            except:
                pass
    #print objectHash['permissions']


    #print objectDef.search(objects[0])
    #print objects

scanPath(getConnection(source),startingPath, depth = depth)
