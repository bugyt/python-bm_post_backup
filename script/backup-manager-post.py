#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################################################
# Import
#############################################################

# Config file
from bmConfig import *

# Functions file
from bmFunctions import *

# Time Python standard library
import time

##############################################################
# Main
#############################################################

# Configuration initialization
init()

# Variable
actualDate = date(time.time())
host = hostName()
emailSubject = "[" + host + "]";
emailBody = ""
checkMd5Ftp = False

if not localArchives["directory"]:
	emailBody += " - bm_post_backup configuration error : invalid archivesDir.\n"
	localFiles = None
else:
	localFiles = getLocalFiles(localArchives["directory"], actualDate)
	md5File = localArchives["directory"] + "/" + host + "-" + actualDate + ".md5"

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
sendMail(emailSender, emailRecipients, emailSubject, emailBody)
