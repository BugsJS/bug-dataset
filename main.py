import argument_parser
import myGit
import myInfo
import myTask
import myTest

param_dict = argument_parser.arg_parser()

if myTask.is_info(param_dict["task"]):
    myInfo.get_project_info(param_dict)
    myInfo.get_bug_info(param_dict)
elif myTask.is_checkout(param_dict["task"]):
    myGit.checkout(param_dict)
elif myTask.is_test(param_dict["task"]):
    myTest.test(param_dict)
elif myTask.is_per_test(param_dict["task"]):
    myTest.per_test(param_dict)
