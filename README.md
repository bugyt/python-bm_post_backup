# Python script for backup-manager post command with automatic configuration
##### (for BM_POST_BACKUP_COMMAND) 

### Why?

This python script is executed at the end of a backup with [backup-manager](https://github.com/sukria/Backup-Manager), a command line backup tool for GNU/Linux.
Actions of the script :
* Get the list of local archive files created by backup-manager
* Get the size of the files
* Check integrity of remote FTP files with local md5 file
* Send email with : 
  *  List of backup files with their size
  *   Result of integrity test

### Configuration

#### bmConfig.py

* TODO
