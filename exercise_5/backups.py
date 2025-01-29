from sys import argv as argument
import os
import shutil


#05. Create a program that makes backup copies of directories, to do this it will package them in a file (ZIP
#format) and upload the file to another machine using the FTP protocol.


#   See archives in path
def tree(path):
    if os.path.exists(path):
        files = os.listdir(path)
        for c in sorted(files):
            print(c)
        return True
    else: return False

#   Create backup zip in this folder
def create_backup():
    try:
                         #   file_name           format      directory_to_z   
        archived = shutil.make_archive(argument[3], 'zip', argument[1])
        return archived
    except:
        print("Error doing the ZIP")

#   Main
if len(argument) > 2:
    print("Files to ZIP:")
    if tree(argument[1]):
        create_backup()
        print("Want to move the backup? Y/N")
        response = input(">")
        if response == "Y" or "y":
            directory = input(">")
            try:
                shutil.move("/home/linu/Escritorio/exercise_5"+"/"+argument[2].lower()+".zip", directory) 
            except Exception as e:
                print(f"Can't move the directory. Error. {e}")
        else:
            print("Goodbye!")
    else: print("Path don't exists")
else:
    print("Required Arguments: directory, name_file")