# MP3-Manager
* This is currently just a python script to search for MP3s in a given directory, put non duplicate files in a new folder, utilize 7zip to add these files to an archive. This will probably change soon to something a little more sophisticated.

* In order to run this script, you should have p7zip installed. This script should be portable to Linux and Mac OS X.  This has not been tested on Windows, however, it may work if the installed version of 7zip has a commandline utility.

* This script works with any type of file, but I designed it to find my MP3s.  If you desire, you can give the script a different extension, like .txt, .jpeg, .jpg, .png, etc, as the 5th commandline argument. If you run the script without the 5th commandline argument it defaults to .mp3.

* To run it execute the following from the command line:
  $ python mp3-manager.py [Source Folder] [Destination Folder] [Archive Name] ([file extension])

* For example:
  $ python mp3-manager.py  /home/users/Music /home/users/NewFolder myArchive.7z .mp3

* OR
  $ python mp3-manager.py  /home/users/Music /home/users/NewFolder myArchive.7z 

* OR
  $ python mp3-manager.py  /home/users/files /home/users/NewFolder myArchive.7z .txt 
