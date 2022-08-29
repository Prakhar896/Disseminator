#### THIS IS A TEST SCRIPT TO GENERATE FILES ONLY, DO NOT USE IN PRODUCTION ####

import os, sys, time

numFiles = input("How many files would you like to create: ")
while True:
    if not numFiles.isdigit():
        numFiles = input("Please enter a number: ")
        continue
    break

numFiles = int(numFiles)

deleteExistingFiles = input("Do you want to delete existing files? (y/n): ")
print()
if deleteExistingFiles == "y":
    for file in os.listdir(os.path.join(os.getcwd(), 'targetFiles')):
        os.remove(os.path.join(os.getcwd(), 'targetFiles', file))
        print("Deleted file: " + file)

print()

for i in range(numFiles):
    with open(os.path.join(os.getcwd(), 'targetFiles', 'file' + str(i) + '.txt'), 'w') as f:
        f.write("Auto-generated file. File number: " + str(i))

print()
print("Files created.")