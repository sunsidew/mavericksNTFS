#!/usr/bin/python

import os
import time
import sys
import commands

def check(i):
	for i in range(i):
		print ".",
		sys.stdout.flush()
		time.sleep(1)
	print "OK"

print "Please remove USB NTFS drive and press enter key"
x = raw_input()
print "Get Current Volumes ",
check(1)

#get current volumes
vol1 = os.listdir("/Volumes")
print "Your current drive lists are: " + str(vol1)
print "Connect USB NTFS drive and press enter key"
x = raw_input()

#detect NTFS volumes
print "Detect NTFS Volumes ",
check(1)
vol2 = os.listdir("/Volumes");
clist = []
detect = []

for i in range(len(vol2)):
	clist.append(False)
	for name1 in vol1:
		if vol2[i] == name1:
			clist[i] = True
			
for i in range(len(vol2)):
	if (clist[i] == False):
		detect.append(vol2[i])

if(len(detect)!=1):
	print "More than 1 volumes are found.. Which one is NTFS drive?"
	for i in range(len(vol2)):
		print str(i+1) + ". " + vol2[i]
	choice = input()
	ntfs = vol2[choice-1]
else:
	ntfs = detect[0]

cmd = "diskutil info /Volumes/"+ntfs +"| grep UUID"
cmdstr = commands.getstatusoutput(cmd)
uuid = str.split(cmdstr[1])[2]
print "Your UUID: " + uuid

line = "UUID="+ uuid + " none ntfs rw,auto,nobrowse\n"
fname = "/etc/fstab"
if os.path.isfile(fname):
	print fname + " already exists. append command"
	file = open(fname,"a")
else:
	print fname + " will be created"
	file = open(fname,"w+")

file.write(line)
file.close()

print "Well done. Test it!!"
