##############################################################
# Required configuration
##############################################################

# Sender email
emailSender = "your@email.com"

# Recipient(s) email
emailRecipients = [
					"first@email.com", 
					"second@email.com"
				  ]

##############################################################
# Automatic configuration with backup-manager.conf
##############################################################

# Active automatic configuration (set to false for manual configuration)
autoConfig = True
# Path to backup-manager configuration file (required if autoConfig = True, default : "/etc/backup-manager.conf")
bmConfDir = "/etc/backup-manager.conf" 


##############################################################
# Manual configuration (need autoConfig = False above)
##############################################################

# Where are store the archives
pLocalArchives = {
					"directory": "/var/archives" # path to local archives (default : "/var/archives")
				}

# Configuration FTP
pConfigFTP = {
				"server": 'ftp.url.net', 
				"user": 'myUser',
 				"password": 'myPassword',
 				"directory": "myDirectory",
 				"passive": True
			}	

