import csv

def get_project_info(param_dict):
    csv_file = "./Projects.csv"
    with open(csv_file) as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for row in reader:
            if row["Name"] == param_dict["project"]:
                print("\nProject info:")
                for key, value in row.items():
                    print("\t"+str(key)+": "+str(value))
                print("\n")


def get_bug_info(param_dict):
    csv_file = "./Projects/"+str(param_dict["project"])+"/"+str(param_dict["project"])+"_bugs.csv"
    with open(csv_file) as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for row in reader:
            if int(row["ID"]) == int(param_dict["bug-ID"]):
                print("Bug info:")
                for key, value in row.items():
                    print("\t"+str(key)+": "+str(value))
                print("\n")