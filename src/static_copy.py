import os, shutil

def copy_files(source, destination, clear=True):
    if os.path.exists(destination) and clear == True:
        shutil.rmtree(destination)
    if not os.path.exists(destination):
        os.mkdir(destination)
    files_in_path = os.listdir(source)
    path = ""
    for file in files_in_path:
        path = os.path.join(source, file)
        if os.path.isfile(path):
            shutil.copy(path, destination)
        if os.path.isdir(path):
            copy_files(path, os.path.join(destination, file), clear=False)

