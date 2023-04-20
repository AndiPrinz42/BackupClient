from os import path as os_path
import sys
import backup

def main():
    args = sys.argv
    src = ""
    dst = ""
    recursive = False

    if len(sys.argv) == 1:
        src, dst, recursive = interactiveInput()
    elif len(sys.argv) == 2 and (args[1] == "-h" or args[1] == "--help"):
        help(args)
        sys.exit(1)
    elif len(sys.argv) == 4:
        src = args[1]
        dst = args[2]
        if(src == dst):
            print("Invalid arguments. Source and destination must be different.")
            sys.exit(1)
        recursive = args[3]
        if recursive == "True":
            recursive = True
        elif recursive == "False":
            recursive = False
        else:
            print("Invalid recursive argument. Must be Boolean.")
            sys.exit(1)
    else:
        print("Invalid arguments. Use -h or --help for help.")
        sys.exit(1)

    backupHandler = backup.Backup(src, dst, recursive)

    backupHandler.start()

def interactiveInput():
    src = ""
    dst = ""
    recursive = ""

    while(not os_path.exists(src)):
        emptyLine()
        src = input("Source path: ")
        print("Validating source path...                  ", end="\r")
        if not os_path.exists(src):
            print("Validating source path... Invalid path     ")
    print("Validating source path... Done             ")
    print("")

    while(not os_path.exists(dst) or src == dst):
        emptyLine()
        dst = input("Destination path: ")
        print("Validating destination path...             ", end="\r")
        if (not os_path.exists(dst) or src == dst):
            print("Validating destination path... Invalid path")
    print("Validating destination path... Done        ")
    print("")

    while(recursive != "y" and recursive != "n"):
        emptyLine()
        recursive = input("Recursive? (y/n): ")
        if recursive != "y" and recursive != "n":
            print("Invalid recursive argument.")
    if recursive == "y":
        recursive = True
    else:
        recursive = False

    return src, dst, recursive

def help(args):
    print(f"Usage: {args[0]} <sourcePath> <destinationPath> <recursive?>")

def emptyLine():
    print(" " * 100, end="\r")

if __name__ == "__main__":
    main()