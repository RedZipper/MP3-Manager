"""
    mp3-manager.py: Finds MP3s in a given directory, places
    non-duplicates in a new folder and tars them.
    
    Copyright (C) 2015 Christina Ford
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. """

import binascii
import shutil
import os
import sys
import hashlib
import errno
import tarfile

from subprocess import call

#http://stackoverflow.com/questions/2032403/how-to-create-full-compressed-tar-file-using-python
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    print "Creating ARCHIVE in: %s%s", str(archname), str(source_dir)

def make_archive(archive_name, source_dir):
    try:
        call(["7z", "a", "-t7z", archive_name, source_dir, "-mx9"])
    except:
        print "error when attempting to make archive."
        print "Is p7zip installed?"
        sys.exit()

def get_hash(filename):
    with open(filename, "rb") as f:
        data = f.read()
        data = binascii.hexlify(data)
        h =  hashlib.sha256(data).hexdigest()
    return h

def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as excepton:
        if excepton.errno != errno.EEXIST:
            raise


def copy_file(hash, hash_list, dir_from, dir_to, mp3):
    if hash not in hash_list:
        shutil.copy(dir_from, dir_to)
        hash_list.append(hash)
        print "adding %s to music list" % str(mp3)
        return True
    else:
        print "Duplicate file %s not added." %str(mp3)
        return False

#traverse  directories adding mp3's to new folder
#hash the files and add hash to list
#only add the files with given extension (example .mp3)
def traverse_dir(orig_loc, ext):
    music_hashes = []
    for root, dirs, music_files in os.walk(orig_loc):
        path = root.split('/')
        for mp3 in music_files:
            #make sure these are mp3s
            tmp_ext = os.path.splitext(mp3)[1]
            if tmp_ext == ext:
                    m_path = os.path.realpath(os.path.join(root,mp3))
                    h = get_hash(m_path)
                    result = copy_file(h,music_hashes, m_path, end_loc, mp3)
            
            else:
                print "NOT ADDING file %s with extension: "%str(mp3), tmp_ext
    print "added %d files to Directry"% len(music_hashes)

if __name__ == "__main__":
    
    usage = "[Source Folder] [Destination Folder] [Archive Name] ([file extension])"
    
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print usage
        sys.exit()
    
    elif len(sys.argv) == 5:
        
        ext = sys.argv[4] # default .mp3
    else:
        ext = ".mp3"
    
    orig_loc = sys.argv[1]
    end_loc  = sys.argv[2]
    arch_loc = sys.argv[3]

    make_dir(end_loc)
    # should probably check to see if this directory exists

    if os.path.isdir(orig_loc):
        traverse_dir(orig_loc, ext)
        #make_tarfile(arch_loc, end_loc)
        make_archive(arch_loc, end_loc)
    else:
        print "Error, Source Drectory does not exist. Exiting . . ."
        sys.exit()
