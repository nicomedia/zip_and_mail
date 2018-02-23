import sys
import os
import zipfile
import smtplib
import os.path, time
from shutil import copyfile
from os.path import basename
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# Observer thread
class detect_changes(PatternMatchingEventHandler):
    patterns = ["*.*", "*.*"]

    def process(self, event):

        print (event.src_path, event.event_type)  # print now only for degug
        # Create and delete file triggers a modification at directory
        if os.path.exists(event.src_path) and event.is_directory == False:
            add_file_to_folder(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

# Add file from source path to new directory
def add_file_to_folder(modified_file):
    recursive_file = modified_file
    while observed_folder != os.path.dirname(recursive_file):
        recursive_file = os.path.dirname(recursive_file)
    recursive_file = os.path.dirname(recursive_file)
    difference = modified_file[len(recursive_file):]

    if not os.path.exists(newpath + difference):
        if not os.path.exists(os.path.dirname(newpath + difference)):
            os.makedirs(os.path.dirname(newpath + difference), 755, exist_ok=True)
        copyfile(modified_file, newpath + difference)
    else:
        os.remove(newpath + difference)
        copyfile(modified_file, newpath + difference)
    return

observed_folder = PATH_TO_OBSERVED_FOLDER
base_folder     = PATH_FOR_BASED_FOLDER
# MFO #
# Program detect the changes in files at the given folder and its subfolders.
if __name__ == "__main__":
    # Create folder to copy changed files
    datestring = datetime.strftime(datetime.now(), '%Y_%m_%d')
    newpath =  base_folder + "mfo_" + datestring
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    # Start observer that detects the changes
    observer = Observer()
    observer.schedule(detect_changes(), observed_folder, recursive=True)
    observer.start()
    # Detect exceptions
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Failed")

    observer.join()

    #main()
