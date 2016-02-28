# -*- coding: utf-8 -*-
from bmConfig import *
localArchives = {}
configFTP = {}

##############################################################
# Send a mail
##############################################################
def sendMail( sender, recipients, subject, message ) :
	# Import smtplib for the actual sending function
	import smtplib

	# Import the email modules we'll need
	from email.mime.text import MIMEText

	for recipient in recipients:

		msg = MIMEText(message)
		msg['Subject'] = subject
		msg['From'] = sender
		msg['To'] = recipient

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
	from os.path import join

	ftp  = FTP(configFTP["server"])
	ftpDirectory = configFTP["directory"]
	pathToFile = join(ftpDirectory,file)

	ftp.login(configFTP["user"], configFTP["password"])

	hasher = hashlib.md5()

	if pathToFile in ftp.nlst(ftpDirectory) :
		resp = ftp.retrbinary("RETR " + pathToFile, hasher.update)

	ftp.quit()
	return hasher.hexdigest()
	

##############################################################
# Initialization
##############################################################
def hostName():
	f = open("/etc/hostname", "r")
	if f:
			return f.read().strip()
	else:
		return "host unknow"

##############################################################
# Initialization
##############################################################
def init():
	if autoConfig:
		automaticConfiguration()
	else:
		localArchives = pLocalArchives
		configFTP = pConfigFTP		

##############################################################
# Autoconfig with back-manager configuration file
##############################################################
def automaticConfiguration():
	import ConfigParser

	##############################################################
	# Get value option
	##############################################################
	def getValue(config, option):
		option = export + option
		if config.has_option(section, option):
			return config.get(section, option)[1:-1]
		else: 
			return None

	##############################################################
	# To parse a configuration file without section
	##############################################################
	class FakeSecHead(object):

		def __init__(self, fp):
			self.fp = fp
			self.sechead = "[" + section + "]\n"

		def readline(self):
			if self.sechead:
				try: 
					return self.sechead
				finally: 
					self.sechead = None
			else: 
				return self.fp.readline()

	section = "asection"
	export = "export "

	bmConfig = ConfigParser.SafeConfigParser(allow_no_value=True)

	bmConfig.readfp(FakeSecHead(open(bmConfDir)))

	localArchives["directory"] = getValue(bmConfig, "BM_REPOSITORY_ROOT")
	configFTP["server"] = getValue(bmConfig, "BM_UPLOAD_FTP_HOSTS")
	configFTP["user"] = getValue(bmConfig, "BM_UPLOAD_FTP_USER")
	configFTP["password"] = getValue(bmConfig, "BM_UPLOAD_FTP_PASSWORD")
	configFTP["directory"] = getValue(bmConfig, "BM_UPLOAD_DESTINATION")
	configFTP["passive"] = getValue(bmConfig, "BM_UPLOAD_FTP_PASSIVE")
