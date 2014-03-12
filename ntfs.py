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

def getVolume():
	return os.listdir("/Volumes");

def choose(vlist):
	for i in range(len(vlist)):
		print str(i+1) +". " + vlist[i]
	x=input()
	return vlist[x-1];

def doWork(vol):
	cmd = "diskutil info /Volumes/" + vol + "| grep UUID"
	cmd2 = "mount | grep " + vol
	fname = "/etc/fstab"

	tmplist = commands.getstatusoutput(cmd2)
	dev = str.split(tmplist[1])[0]
	print "Your Device: " + dev	
	cmdstr = commands.getstatusoutput(cmd)

	uuid = str.split(cmdstr[1])[2]
	print "Your UUID: " + uuid

	line = "UUID="+ uuid + " none ntfs rw,auto,nobrowse"
	find = False;
	if os.path.isfile(fname):
		print fname + " already exists. append command"
		file = open(fname,'a+');
		file.seek(0,0)
		for l in file:
			if line in l:
				find = True
	else:
		print fname + " will be created"
		file = open(fname,"w+")
	
	if not find:
		file.write(line +"\n")
	else:
		print "Already Enabled.."
	file.close()
	print "Eject Drive: " + vol 
	commands.getstatusoutput("diskutil unmount /Volumes/" + vol)
	print "Remount Drive: " + dev
	commands.getstatusoutput("diskutil mount " + dev)

	print "generate Desktop Shortcut for NTFS Drive"
	commands.getstatusoutput("ln -s /Volumes ~/Desktop/Drives")


def bootcamp():
	bc = "BOOTCAMP"
	print "trying BOOTCAMP write ENABLE.."
	vol = getVolume()
	if bc in vol:
		print "found BOOTCAMP partition"
	else:
		print "Choose your BC partition",
		bc = choose(vlist)
	#now we know bc name
	doWork(bc)

# enable NTFS usb drive write
def usb():
	print "Please remove USB NTFS drive and press enter key"
	x = raw_input()
	print "Get Current Volumes ",
	check(1)

#get current volumes
	vol1 = getVolume()
	print "Your current drive lists are: " + str(vol1)
	print "Connect USB NTFS drive and press enter key"
	x = raw_input()

#detect NTFS volumes
	print "Detecting NTFS Volumes ",
	check(10)
	vol2 = getVolume()
	detect = []

	for vstr in vol2:
		if vstr not in vol1:
			detect.append(vstr);
				
	if(len(detect)!=1):
		print "More than 1 volumes are found.. Which one is NTFS drive?"
		ntfs = choose(vol2)
	else:
		ntfs = detect[0]
	doWork(ntfs)
	
#main function
print "********************************************"
print "* 1. Enable BOOTCAMP Partition Write       *"
print "* 2. Enable USB NTFS Drive Write           *"
print "********************************************"
print "Choose function (1-2): ",
x = input()
if x==1:
	bootcamp()
else:
	usb()

print "Well done,thank you."

