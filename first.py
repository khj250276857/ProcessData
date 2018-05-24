import os

file_path = r'E:\MR Cardiac\new_01\Se1\cycle01'
for root, dirs, files in os.walk(file_path):
    print(root)
    print(dirs)
    print(files)

