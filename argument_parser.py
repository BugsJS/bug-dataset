import argparse
import sys
import os

def arg_parser():
    parser = argparse.ArgumentParser(description = '   ')
    parser.add_argument('-p', '--project',  required = True, choices= get_projects(), help = '')
    parser.add_argument('-b', '--bug-ID',   required = True, help = '')
    parser.add_argument('-t', '--task',     required = True, choices = ['info', 'checkout', 'test', 'per-test'], help='')
    parser.add_argument('-v', '--version',  required = True, choices = ['buggy', 'fixed', 'fixed-only-test-change'], help='')

    parser.add_argument('-o', '--output', help='output (clone, checkout etc) folder')

    param_dict = {}
    args = parser.parse_args()
    param_dict["project"] = args.project
    param_dict["bug-ID"] = args.bug_ID
    param_dict["version"] = args.version
    param_dict["task"] = args.task
    param_dict["output"] = args.output
    return param_dict


def get_projects():
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    projects_set = set()
    projects_file = open(os.path.join(SCRIPTDIR, "Projects.csv"), "r")
    lines = projects_file.read().splitlines()
    for x in range(1, len(lines)):
        projects_set.add(lines[x].split(";")[0])
    projects_file.close()
    return list(projects_set)

