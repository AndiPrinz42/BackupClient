from os import path as os_path
from os import makedirs as os_makedirs
from shutil import copyfile as shutil_copyfile
import glob
import sys


class Backup:
    def __init__(self, src, dst, recursive):
        self.setSrc(src)
        self.setDst(dst)
        self.setRecursive(recursive)
        self.fileQueue = []

    def setSrc(self, src):
        if(not isinstance(src, str)):
            print("Invalid sourcePath. Must be string.")
            sys.exit(1)
        if(not os_path.exists(src)):
            print("Invalid sourcePath. Path not found.")
            sys.exit(1)
        self.src = src

    def setDst(self, dst):
        if(not isinstance(dst, str)):
            print("Invalid destinationPath. Must be string.")
            sys.exit(1)
        if(not os_path.exists(dst)):
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
        for index, file in enumerate(self.fileQueue):
            print("Updating file(%s/%s): %s                    " % (str(index+1), str(len(self.fileQueue)), str(file)))
            os_makedirs(os_path.dirname(self.dst + file), exist_ok=True)
            try:
                shutil_copyfile(self.src + file, self.dst + file)
            except:
                print("Error copying file: %s" % file)
                pass
            index += 1

        print("Updated %d files                            " % len(self.fileQueue))
        self.clearQueue()

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
                self.pushToQueue(file)
            else:
                srcTime = (int)(os_path.getmtime(self.src + file))
                dstTime = (int)(os_path.getmtime(self.dst + file))
                if srcTime > dstTime:
                    self.pushToQueue(file)
            

    def pushToQueue(self, file):
        self.fileQueue.append(file)

    def clearQueue(self):
        self.fileQueue = []

    def getFiles(self, path):
        files = glob.glob(path+'\**\*.*', recursive=self.recursive)
        for file in files:
            if os_path.isdir(file):
                files.remove(file)
        return files
    
    
if __name__ == "__main__":
    raise Exception("Can't be run as Standalone!")