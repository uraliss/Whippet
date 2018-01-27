#####################################################
# Whippet
#
# removes duplicate files using comparison of
# hashes
#
# Alan Oliver (c) 2018
# alan.oliver@squarebots.com
#
#####################################################

#####################################################
# imports
#####################################################

import hashlib, os, csv, sys
from pathlib import Path

#####################################################
# global variables
#####################################################

blocksize = 65536
root_dir = input("Type directory you wish to scan ")

capture = []
duplicates = []
deletions = []

#####################################################
# functions
#####################################################

def hash_file(file_name):
    hasher = hashlib.sha1()
    my_hash = ""
    with open(file_name, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            sys.stdout.write('.')
            sys.stdout.flush()
            hasher.update(buf)
            buf = afile.read(blocksize)

            my_hash = (hasher.hexdigest())
    print ()


    return my_hash

def is_duplicate(hash1, hash2):
    if (hash1 == hash2):
        return True
    else:
        return False

def print_records(records):
    for record in records:
        current_hash = record[1]
        print(record)
        print(current_hash)

def plist(list):
    for item in list:
        print (item)

#####################################################
# main program
#####################################################

os.system('cls')

# get files and get hash

print("Finding and hashing files.")

for root, dirs, files in os.walk(root_dir, topdown=False):
    for name in files:
        file_name = (os.path.join(root, name))

        p = Path(file_name).resolve()
        print (p)


        # get hash of file
        #print (p)
        my_hash = hash_file(file_name)
        #print(my_hash)

        capture.append([file_name, my_hash])


############## locate duplicates

print ("Finding duplicates")


iter1 = 0
while (iter1 <= len(capture)-1):
    iter2 = iter1 + 1
    while (iter2 <= len(capture)-1):
        record1 = capture[iter1]
        record2 = capture[iter2]
        # print(iter1, iter2)
        if (record1[1] == record2[1]):
            duplicates.append(record2)

        iter2 = iter2 + 1

    iter1 = iter1 + 1


for record in duplicates:
    if record not in deletions:
        print("duplicate found " + record[0])
        deletions.append(record)


if len(deletions) == 0:
    print("No Duplicates Found")
    sys.exit()

os.system('cls')


print()
print("The following files are duplicates and can be deleted")
plist(deletions)

answer = input("Do you want to delete these files? Y/N ")

if answer == "Y":
    for record in deletions:
        os.remove(record[0])
        print (record[0] + " REMOVED")

else:
    print("You chose not to delete these files")


print ("Finished")