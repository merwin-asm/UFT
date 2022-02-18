import pyPath
import os
import time

my_path = pyPath.MYPATH()

def reparsed_path(path):
    path_final = ""
    for each in str(path):
        if each == " ":
            path_final+="\ "
        elif each == "(":
            path_final+="\("
        elif each == ")":
            path_final += "\)"
        else:
            path_final+=each
    return path_final
try:
    full_path_main = os.path.abspath("main_ver_2.py")
    full_path_main = reparsed_path(full_path_main)
    my_path.make_redirecting_bashfile("uft",full_path_main,allow_args=True,max_num_args=5)
    full_path = os.path.abspath("uft")
    print(full_path)
    my_path.addfile_to_path(full_path,"uft",exe=True)
    print("INSTALLED...")
except:
    print("Failed or it has been already installed..")
