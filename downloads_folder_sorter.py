"""Downloads folder sorter

This script iterates through the files in a user's downloads folder on Windows and places each file in its appropriate
folder.

This file contains the following functions:

    * move_file - checks if the destination folder exists, creates it if it doesn't, then moves a file into it
    * sort_folder - iterates through the files in the folder
"""

import os.path
import shutil
from pathlib import Path
import json

global destination
user = os.getenv('USERNAME')

downloads_path = Path("/Users/{}/Downloads".format(user))
downloads_path2 = Path("L:/allFirefoxDownloads")
print("download paths: ", downloads_path, downloads_path2, "\n")


with open('config.json', encoding='utf-8') as f:
    CATEGORIES = json.load(f)


def move_file(file, destination):
    """Checks if the destination folder exists, creates it if it doesn't, then moves a file into it
    Parameters
    ----------
    file : Path
        the path to a file
    destination : Path
        the path to the destination folder
    try except: in case the file already exists, it copy and replaces it and deletes the source file.
    """
    try:
        if not destination.exists():
            destination.mkdir(parents=True, exist_ok=True)
        print("file: ", file, "\n")
        print("destination: ", destination, "\n")
        shutil.move(file, destination)
    except shutil.Error as e:
        print("destination path already existing, so replacing: ", file)
        print(e, ", so replacing...")
        shutil.copy2(file, destination)
        os.remove(file)
        print("done!")


def move_folders(folder, destination):
    print("move de folder: " + str(folder))
    print("naar dest: " + str(destination))
    try:
        if not destination.exists():
            destination.mkdir(parents=True, exist_ok=True)
        dest = shutil.move(folder, destination)
    except shutil.Error as e:
        print("destination path already existing, so replacing: ", folder)
        print(e, ", so replacing...")
    #     if os.path.exists(folder):
    #         i, temp = 1, folder
    #         while os.path.exists(temp):
    #             temp = os.path.join(strdest, f"{folder}_{i}.{ext}")
    #             dictfiles[filename] = temp
    #             i += 1
    # shutil.move(filename, dictfiles[filename])
    # dest = shutil.move(folder, destination, copy_function=shutil.copytree)
    # os.remove(folder)
    print("done!")


def sort_folder():
    """Iterates through the files in the folder"""
    for file in downloads_path.iterdir():
        if file.is_file():
            for category in CATEGORIES:
                if file.suffix in category['extensions']:
                    destination = file.parent.joinpath(category['name'])
                    move_file(file, destination)

# Allfirefoxdownloads:
def sort_folder2():
    """Iterates through the files in the folder"""
    for file in downloads_path2.iterdir():
        if file.is_file():
            for category in CATEGORIES:
                if file.suffix in category['extensions']:
                    destination = file.parent.joinpath(category['name'])
                    move_file(file, destination)
        else:
            new_list = []
            for category in CATEGORIES:
                new_list.append(category['name'])
            if file.name not in new_list:
                if file.name != "$RECYCLE.BIN":
                    destination = file.parent.joinpath(category['name'])
                    # print("hiero", file.name)
                    # print(destination)
                    move_folders(file, destination)


if __name__ == '__main__':
    sort_folder()
    sort_folder2()
