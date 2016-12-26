import os


def secretkey(path=None):
    """
    Return secret key in default path
    Accept 'path=' as different path to key file
    """
    if path is None:
        path = os.path.join(os.path.dirname(os.getcwd()), 'semisklad/key/key.txt')
    with open(path, 'r') as key_file:
        key = key_file.readline()
        return key
