import csv
import myVersion
import os
import subprocess as sp


def checkout(param_dict):
    repository = get_project_repository(param_dict)
    clone_repo(repository, param_dict["output"])
    
    checkout_cmd = None
    if myVersion.is_buggy(param_dict["version"]):
        checkout_cmd = "git checkout tags/Bug-" + str(param_dict["bug-ID"]+"^")
    elif myVersion.is_fixed(param_dict["version"]):
        checkout_cmd = "git checkout tags/Bug-" + str(param_dict["bug-ID"]) + "-full"
    elif myVersion.is_fixed_only_test_change(param_dict["version"]):
        checkout_cmd = "git checkout tags/Bug-" + str(param_dict["bug-ID"]) + "-test"
    else:
        exit()
    sp.call(checkout_cmd, shell=True)


def get_project_repository(param_dict):
    with open("./Projects.csv", 'r') as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for row in reader:
            if str(param_dict["project"]) == str(row["Name"]):
                return row["Repository url"]
    print("I can't find the project in the csv file")
    exit()

def clone_repo(project_repo, folder):
    if os.path.isdir(folder):
        rm_cmd = "rm -R "+str(folder)
        sp.call(rm_cmd, shell=True)
    os.makedirs(folder)

    os.chdir(folder)
    clone_cmd = "git clone "+str(project_repo)
    sp.call(clone_cmd, shell=True)
    os.chdir( os.listdir( "./" )[0] )