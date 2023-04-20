import os
from shutil import copyfile as shutil_copyfile
import glob
import sys

class Backup:
    def __init__(self, src, dst, recursive):
        self.setSrc(src)
        self.setDst(dst)
        self.setRecursive(recursive)
        self.fileSyncQueue = []
        self.fileDeleteQueue = []

    def setSrc(self, src):
        if(not isinstance(src, str)):
            print("Invalid sourcePath. Must be string.")
            sys.exit(1)
        if(not os.path.exists(src)):
            print("Invalid sourcePath. Path not found.")
            sys.exit(1)
        self.src = src

    def setDst(self, dst):
        if(not isinstance(dst, str)):
            print("Invalid destinationPath. Must be string.")
            sys.exit(1)
        if(not os.path.exists(dst)):
            print("Invalid destinationPath. Path not found.")
            sys.exit(1)
        self.dst = dst

    def setRecursive(self, recursive):
        if(not isinstance(recursive, bool)):
            print("Invalid recursive argument. Must be Boolean.")
            sys.exit(1)
        self.recursive = recursive

    def start(self):
        print("Backing up '%s' to '%s'                     " % (self.src, self.dst))
        print("Comparing files...                          ", end="\r")
        self.compare()
        print("")
        print("Updating files...                           ", end="\r")
        index = 1
        for index, file in enumerate(self.fileSyncQueue):
            print("Updating file(%s/%s): %s                    " % (str(index+1), str(len(self.fileSyncQueue)), str(file)))
            os.makedirs(os.path.dirname(self.dst + file), exist_ok=True)
            try:
                shutil_copyfile(self.src + file, self.dst + file)
            except:
                print("Error copying file: %s" % file)
                pass
            index += 1

        print("Updated %d files                            " % len(self.fileSyncQueue))
        self.clearSyncQueue()

        print("Deleting files...                           ", end="\r")
        index = 1
        for index, file in enumerate(self.fileDeleteQueue):
            print("Deleting file(%s/%s): %s                    " % (str(index+1), str(len(self.fileDeleteQueue)), str(file)))
            try:
                os.remove(self.dst + file)
            except:
                print("Error deleting file: %s" % file)
                pass
            index += 1
        print("Deleted %d files                            " % len(self.fileDeleteQueue))
        self.clearDeleteQueue()
        print("Clearing empty directories...               ", end="\r")
        emptyDirs = self.clearEmptyDirectories()
        print("Cleared %d empty directories                " % emptyDirs)

    def compare(self):
        srcFiles = self.getFiles(self.src)
        dstFiles = self.getFiles(self.dst)

        # cut of the src and dst path from the files
        srcFiles = [file.replace(self.src, '', 1) for file in srcFiles]
        dstFiles = [file.replace(self.dst, '', 1) for file in dstFiles]

        # get the files that are in src but not in dst
        for file in srcFiles:
            print("Comparing files... %s                    " % file)
            if file not in dstFiles:
                self.pushToSyncQueue(file)
            else:
                srcTime = (int)(os.path.getmtime(self.src + file))
                dstTime = (int)(os.path.getmtime(self.dst + file))
                if srcTime > dstTime:
                    self.pushToSyncQueue(file)

        # get the files that are in dst but not in src
        for file in dstFiles:
            if file not in srcFiles:
                self.pushToDeleteQueue(file)
            

    def pushToSyncQueue(self, file):
        self.fileSyncQueue.append(file)

    def clearSyncQueue(self):
        self.fileSyncQueue = []

    def pushToDeleteQueue(self, file):
        self.fileDeleteQueue.append(file)

    def clearDeleteQueue(self):
        self.fileDeleteQueue = []

    def getFiles(self, path):
        files = glob.glob(path+'\**\*.*', recursive=self.recursive)
        for file in files:
            if os.path.isdir(file):
                files.remove(file)
        return files
    
    def clearEmptyDirectories(self):
        count = 0
        for root, dirs, files in os.walk(self.dst, topdown=False):
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                    count += 1
                except:
                    pass
        return count
            
    
if __name__ == "__main__":
    raise Exception("Can't be run as Standalone!")