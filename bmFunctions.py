# -*- coding: utf-8 -*-

##############################################################
# Send a mail
##############################################################
def sendMail( dests, subject, message ) :
	# Import smtplib for the actual sending function
	import smtplib

	# Import the email modules we'll need
	from email.mime.text import MIMEText

	for dest in dests:

		msg = MIMEText(message)
		msg['Subject'] = subject
		msg['From'] = ""
		msg['To'] = dest

		# Send the message via our own SMTP server, but don't include the
		# envelope header.
		s = smtplib.SMTP('localhost')
		s.sendmail(msg['From'], msg['To'], msg.as_string())

	s.quit()

##############################################################
# Date format
##############################################################
def date(unixtime, format = '%Y%m%d'):

	import datetime

	d = datetime.datetime.fromtimestamp(unixtime)

	return d.strftime(format)

##############################################################
# Get local files in archive directory
##############################################################
def getLocalFiles(archivesDir, filtreDate):
	
	from os import listdir
	from os.path import isfile, join, getsize

	files=[]

	for f in listdir(archivesDir):

		if isfile(join(archivesDir, f)) and filtreDate in f:

			file = {}
			file['name'] = f
			file['size'] = getsize(join(archivesDir, f))
			files.append(file)

	files.sort()

	return files

##############################################################
# Size file format
##############################################################
def formatBytes(bytes, precision = 2):

	from math import floor, log, pow

	units = ['B', 'KB', 'MB', 'GB', 'TB']
	bytes = max(bytes, 0);
	vpow = floor((log(bytes) if bytes else 0) / log(1024));
	vpow = min(vpow, len(units) - 1);
	bytes = bytes / pow(1024, vpow);

	return str(round(bytes, precision)) + " " + units[int(vpow)];

##############################################################
# Check FTP files with local md5 file
##############################################################
def verifMd5Ftp(md5File, configFTP):

	import string

	handle = open(md5File, "r")

	if (handle):

		for line in handle:

			md5, filename = string.split(line, "  ")
			filename = filename.strip()

			if filename:

				if (md5 != getMd5OverFtp(filename, configFTP)):

					handle.close()

					return False

		handle.close()

	else:

		return False

	return True

##############################################################
# Connect to FTP and create md5 hash string
##############################################################
def getMd5OverFtp(file, configFTP):

	import hashlib
	from ftplib import FTP 

	ftp  = FTP(configFTP["server"])

	ftp.login(configFTP["user"], configFTP["password"])

	hasher = hashlib.md5()
	
	resp = ftp.retrbinary("RETR " + configFTP["directory"] + file, hasher.update)

	ftp.quit()

	return hasher.hexdigest()