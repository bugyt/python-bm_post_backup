#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################################################
# Import
#############################################################
# Import functions file
from bmFunctions import *
# Import config file
from bmConfig import *
# time Python standard library
import time

config()

##############################################################
# Script
#############################################################
actualDate = date(time.time())

emailBody = ""

f = open("/etc/hostname", "r")
if f:
	host = f.read().strip()
else:
	host = "host unknow"

emailSubject = "[" + host + "]";

md5File = archivesDir + "/" + host + "-" + actualDate + ".md5"

checkMd5Ftp = False
print archivesDir
localFiles = getLocalFiles(archivesDir, actualDate)

if not localFiles:
	emailBody += " - Fichiers non présents en local (attention : cela peut venir d'un probleme de droit).\n"
else:
	emailBody += " - Fichiers presents en local :\n\n";
	total_size = 0
	# affichage de la liste des fichiers avec leur taille et un total global
	for file in localFiles:
		emailBody += "   # "+file['name'];
		emailBody += " ("+formatBytes(file["size"])+")";
		emailBody += "\n";
		total_size += file["size"];
	emailBody += "\n   # TOTAL : " + formatBytes(total_size) + "\n\n";

	checkMd5Ftp = verifMd5Ftp(md5File, configFTP)

	if checkMd5Ftp != True:
		emailBody += " - problème d'intégrité dans les fichiers transmis sur le serveur FTP\n";
	else:
		emailBody += " - intégrité des fichiers sur le serveur FTP vérifiés.\n";

if checkMd5Ftp == True:
	emailSubject += " backup ok"
else:
	emailSubject += " backup ko"


# Send mail 
sendMail(emailDest, emailSubject, emailBody)

quit()

##### /Script #####
