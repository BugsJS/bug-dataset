import csv
import json
import myGit
import os
import subprocess as sp

#================= get commands =======================

def get_command(param_dict, command_type):
    path, filename = os.path.split(os.path.realpath(__file__))
    csv_file = str(path)+"/Projects/"+str(param_dict["project"])+"/"+str(param_dict["project"])+"_commands.csv"
    with open(csv_file) as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for row in reader:
            if int(row["ID"]) == int(param_dict["bug-ID"]):
                return row[command_type]


#================= set node version and pre- post command =======================

def set_node_version(node_version_str):
    if len(node_version_str) > 0:
        sp.call( "n "+str(node_version_str), shell=True)
    else:
        sp.call( "n 8.0.0", shell=True)


#================= get test statistics =======================

def get_test_stat_from_god_json(json_data):
    test_stat = {}
    test_stat["tests"] = json_data["stats"]["tests"]
    test_stat["passes"] = json_data["stats"]["passes"]
    test_stat["pending"] = json_data["stats"]["pending"]
    test_stat["failures"] = json_data["stats"]["failures"]
    return test_stat


def get_test_stat_from_bad_json(json_name):
    test_stat = {}
    jsonfile = open(json_name, 'r', encoding='utf-8')
    lines = jsonfile.readlines()
    for line in lines:
        if line.count("\"tests\": ") and line.count("[")==0 :
            test_stat["tests"] = int(line.split(",")[0].split(": ")[1])
        elif line.count("\"passes\": ") and line.count("[")==0 :
            test_stat["passes"] = int(line.split(",")[0].split(": ")[1])
        elif line.count("\"pending\": ") and line.count("[")==0 :
            test_stat["pending"] = int(line.split(",")[0].split(": ")[1])
        elif line.count("\"failures\": ") and line.count("[")==0 :
            test_stat["failures"] = int(line.split(",")[0].split(": ")[1])
    jsonfile.close()
    return test_stat


def test_stat_dump(test_stat):
    print("Number of tests: "+str(test_stat["tests"]))
    print("\tpasses: "+str(test_stat["passes"]))
    print("\tfailures: "+str(test_stat["failures"]))
    print("\tpending: "+str(test_stat["pending"]))


def get_test_stat():
    try:
        json_data = json.load( open("./test_results.json") )
        test_stat = get_test_stat_from_god_json(json_data)
        test_stat_dump(test_stat)
        return test_stat
    except:
        test_stat = get_test_stat_from_bad_json("./test_results.json")
        test_stat_dump(test_stat)
        return test_stat



#================= get coverage statistics =======================

def cov_stat_dump(cov_stat):
    cov_granularity = ["lines", "statements", "functions", "branches"]
    for gr in cov_granularity:
        print("Number of "+str(gr)+": "+str(cov_stat[gr]["total"]))
        print("\tcovered:\t"+str(cov_stat[gr]["covered"]))
        print("\tcovered (%):\t"+str(cov_stat[gr]["pct"]))
        print("\tskipped (%):\t"+str(cov_stat[gr]["skipped"]))


def get_cov_stat_from_god_json(json_data, type):
    cov_stat_of_type = {}
    cov_stat_of_type["total"] = json_data["total"][type]["total"]
    cov_stat_of_type["covered"] = json_data["total"][type]["covered"]
    cov_stat_of_type["skipped"] = json_data["total"][type]["skipped"]
    cov_stat_of_type["pct"] = json_data["total"][type]["pct"]
    return cov_stat_of_type


def _get_cov_stat(json_data):
    cov_stat = {}
    cov_stat["lines"] = get_cov_stat_from_god_json(json_data, "lines")
    cov_stat["statements"] = get_cov_stat_from_god_json(json_data, "statements")
    cov_stat["functions"] = get_cov_stat_from_god_json(json_data, "functions")
    cov_stat["branches"] = get_cov_stat_from_god_json(json_data, "branches")
    return cov_stat


def get_cov_stat():
    try:
        json_data = json.load( open("./coverage/coverage-summary.json") )
        cov_stat = _get_cov_stat(json_data)
        cov_stat_dump(cov_stat)
    except:
        pass


# ====================== tests write into a file =================

def write_test_names_into_file():
    tests = set()
    jsonfile = open("./test_results.json", 'r', encoding='utf-8')
    lines = jsonfile.readlines()
    for line in lines:
        if line.count("\"fullTitle\""):
            test = line.split("\": \"")[1].split("\",\n")[0]
            tests.add(test)
    jsonfile.close()

    jsonfile = open("./tests.json", 'w')
    jsonfile.write("[\n")
    for x in range(len(tests)-1):
        jsonfile.write("  \""+list(tests)[x]+"\",\n")
    jsonfile.write("  \""+list(tests)[len(list(tests))-1]+"\"\n")
    jsonfile.write("]")
    jsonfile.close()


# ======================= run commands =============

def run_pre_and_post_command(pre_and_post_command):
    if len(pre_and_post_command):
        sp.call(pre_and_post_command, shell=True)


def run_test_command(test_command):
    sp.call(str(test_command)+" > ./test_results.json", shell=True)


def run_coverage_command(coverage_command):
    sp.call(coverage_command, shell=True)


def run_pertest_command(coverage_command):
    sp.call("/work/pertest.js -t ./tests.json -r perTest_results.txt -c \""+str(coverage_command)+"\"", shell=True)


def run_npm_install():
    sp.call("npm install", shell=True)


# ======================= tests =============

def test(param_dict):
    myGit.checkout(param_dict)
    set_node_version(get_command(param_dict, "Node version"))

    if get_command(param_dict, "Pre-command").count(".sh")==0:
       run_pre_and_post_command(get_command(param_dict, "Pre-command"))
    run_npm_install()
    run_pre_and_post_command(get_command(param_dict, "Pre-command"))
    run_test_command(get_command(param_dict, "Test command"))
    get_test_stat()

    run_coverage_command(get_command(param_dict, "Coverage command"))
    get_cov_stat()
    run_pre_and_post_command(get_command(param_dict, "Post-command"))


def per_test(param_dict):
    myGit.checkout(param_dict)
    set_node_version(get_command(param_dict, "Node version"))

    run_pre_and_post_command(get_command(param_dict, "Pre-command"))
    run_npm_install()

    run_test_command(get_command(param_dict, "Test command"))
    get_test_stat()

    write_test_names_into_file()
    run_pertest_command(get_command(param_dict, "Coverage command"))
    run_pre_and_post_command(get_command(param_dict, "Post-command"))
