# BackupClient
This is a backup utility written in Python that allows you to easily backup files from a source directory to a destination directory. The program compares the files in the source and destination directories and synchronizes them, copying new or modified files to the destination and deleting files that no longer exist in the source. It also includes a feature to clear empty directories from the destination.

The backup code consists of a single file (backup.py) and is written in object-oriented style. The Backup class is defined with several methods to set the source and destination directories, set whether the program should work recursively, and start the backup process. The compare method is used to find differences between the source and destination directories and populates the appropriate sync or delete queue. The program then iterates through the queues, performing the necessary file operations.

The code includes error handling for invalid source and destination paths and files that can't be copied or deleted. The program also outputs progress messages during the backup process, indicating the number of files updated and deleted, and the number of empty directories cleared.

This utility can be useful for personal or small-scale backup needs, and the code can be easily modified and customized to fit specific requirements.