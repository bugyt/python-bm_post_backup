
import ConfigParser

# email des destinataires
emailDest = ["first@email.com", "second@email.com"]
# repertoire local de stockage des fichiers de sauvegarde
archivesDir = '/var/archives'
# Configuration FTP
configFTP = {
				"server": 'ftp.url.net', 
				"user": 'myUser',
 				"password": 'myPassword',
 				"directory": "myDirectory",
 				"passive": True
			}		

						
# Path to backup-manager configuration file
bmConfDir = "/etc/backup-manager.conf"




def config():

	##############################################################
	# Get value option
	##############################################################
	def getValue(config, option):
		option = export + option
		if config.has_option(section, option):
			return config.get(section, option)
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

	bmConfig = ConfigParser.SafeConfigParser()

	bmConfig.readfp(FakeSecHead(open(bmConfDir)))

	archivesDir = getValue(bmConfig, "BM_REPOSITORY_ROOT")
	configFTP["server"] = getValue(bmConfig, "BM_UPLOAD_FTP_HOSTS")
	configFTP["user"] = getValue(bmConfig, "BM_UPLOAD_FTP_USER")
	configFTP["password"] = getValue(bmConfig, "BM_UPLOAD_FTP_PASSWORD")
	configFTP["directory"] = getValue(bmConfig, "BM_UPLOAD_DESTINATION")
	configFTP["passive"] = getValue(bmConfig, "BM_UPLOAD_FTP_PASSIVE")
	#else:
		#archivesDir = "error"

	print archivesDir

