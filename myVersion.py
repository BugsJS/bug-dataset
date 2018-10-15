
def is_buggy(version):
    if version == "buggy":
        return True
    return False

def is_fixed(version):
    if version == "fixed":
        return True
    return False

def is_fixed_only_test_change(version):
    if version == "fixed-only-test-change":
        return True
    return False
