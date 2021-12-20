import os
import subprocess

path = "/Users/AD/data/bitbucket"
dir_list = os.listdir(path)
# print(dir_list)

for i in dir_list:
    command = f"cd {path}/{i}; git checkout master; git rebase && git pull -f"
    # print(command)
    ret = subprocess.run(command, capture_output=True, shell=True)
    # print(ret.stdout.decode())
    file_object = open('/tmp/sample.txt', 'a')
    file_object.write(ret.stdout.decode())
print("Repo clonning done")
file_object.close()
