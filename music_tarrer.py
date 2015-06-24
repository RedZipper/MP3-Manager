import shutil
import os
import sys
import hashlib
import errno
import tarfile

#http://stackoverflow.com/questions/2032403/how-to-create-full-compressed-tar-file-using-python
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    

def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as excepton:
        if excepton.errno != errno.EEXIST:
            raise

#Music Location
orig_loc = sys.argv[1] 
end_loc = sys.argv[2] 
arch_loc = sys.argv[3]

music_hashes = []
ext = ".mp3"
make_dir(end_loc)

#traverse directory and add music to list
for root, dirs, music_files in os.walk(orig_loc):
    path = root.split('/')
    for mp3 in music_files:
        tmp_ext = os.path.splitext(mp3)[1]
        if tmp_ext == ext:
             #check for duplicates
                m_path = os.path.realpath(os.path.join(root,mp3))
                with open(m_path, "rb") as f:
                    data = f.read()
                    h = hashlib.sha256(data)
                    f.close()

                if h not in music_hashes:
                    shutil.copy(m_path, end_loc) 
                    music_hashes.append(h)
                    print "adding %s to music list" % str(mp3)
                else:
                    print "DUPLICATE FILE %s NOT ADDED." % str(mp3)
        else:   
            print "NOT ADDING file %s with extension:"%str(mp3), tmp_ext
print "added %d files to Directry"% len(music_hashes)

print "Creating ARCHIVE"

make_tarfile(arch_loc, end_loc)