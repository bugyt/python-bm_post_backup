# Python script for backup-manager post command with automatic configuration
##### (for BM_POST_BACKUP_COMMAND) 

### Why?

This python script is executed at the end of a backup with [backup-manager](https://github.com/sukria/Backup-Manager), a command line backup tool for GNU/Linux.
For the moment, this script is only available for backup-manager FTP upload.

Actions of the script :
* Get the list of local archive files created by backup-manager
* Get the size of the files
* Check integrity of remote FTP files with local md5 file
* Send email with : 
  *  List of backup files with their size
  *   Result of integrity test

### Configuration

#### bmConfig.py
* Set **emailSender** with your email
* Set **emailRecipients** with your recipients email
* FTP Configuration
  * Automatic FTP configuration
    * **autoConfig** should be *True*
    * Set **bmConfDir** with the path of backup-manager.conf file
  * OR Manual FTP configuration 
    * **autoConfig** should be *False*
    *  Set **pLocalArchives.directory** with the path of the local archives (default : *"/var/archives"*)
    *  Set **pConfigFTP**
      *  **server** : the FTP url 
      *  **user** : the FTP user
      *  **password** : the FTP password
      *  **directory** : the path to archive files on the FTP server
      *  **passive** : passive connection to FTP (*TRUE* or *FALSE* )
