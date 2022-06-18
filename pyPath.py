import os
import stat
import shutil

# MYPATH IS A MODULE MADE FOR LINUX. IT CAN BE USED TO
# PERFORM PATH RELATED FUNCTIONS.
# AUTHOR : MERWIN

class MYPATH:
    def __init__(self,):
        pass
    def make_redirecting_bashfile(self,filename,target_pyfile="",content_edited=None,allow_args=False,max_num_args=0):
        if not allow_args:
            default_command = f"""
#!/bin/bash
python3  {target_pyfile}
        """
        else:
            sub = ""
            for e in range(0,max_num_args):
                sub += ' ${'
                sub += f'args[{e}]'
                sub += '} '
            default_command = f"""
#!/bin/bash
args=("$@")
python3  {target_pyfile} {sub}
                    """
        try:
            file = open(filename, "x")
            if content_edited != None:
                file.write(content_edited)
            else:
                file.write(default_command)
            file.close()
        except:
            file = open(filename, "w")
            if content_edited != None:
                file.write(content_edited)
            else:
                file.write(default_command)
            file.close()
    def addfile_to_path(self,path,file_name,exe=False,permissions=None):
        target = rf'/usr/bin/{file_name}'
        if os.path.isfile(path):
            print(True)
            shutil.copyfile(path,target)
            os.system("cd /usr/bin")
            if exe:
                print(True)
                os.chmod(file_name,0o755)
            if permissions != None:
                os.system(f"sudo chmod {permissions} {file_name}") #SET Permissions
            return True
        else:
            return False
    def seek_to_path(self):
        return os.environ.get("PATH")
    def path_var_exists(self,path):
        path_vars = self.seek_to_path()
        path_vars = path_vars.split(":")
        for each in path_vars:
           if each == path:
               return True
        return False
    def add_dir_to_path_TEMP(self,path):
        if os.path.isdir(path):
            os.system(f'PATH="$PATH:{path}"')
            return True
        return False
    def add_dir_to_path_PERMANENT(self,path,path_to_bashrc):
        if os.path.isdir(path):
            bashrc = open(path_to_bashrc,"a")
            bashrc.write(f'PATH="$PATH:{path}"')
            return True
        return False

    def reparsed_path(self,path):
        path_final = ""
        for each in str(path):
            if each == " ":
                path_final += "\ "
            elif each == "(":
                path_final += "\("
            elif each == ")":
                path_final += "\)"
            else:
                path_final += each
        return path_final
if __name__ == '__main__':
    my_path = MYPATH()
    # print(my_path.addfile_to_path("/home/merwin/programming/MYPATH/test_123_2.sh","test_123_2.sh",exe=True))
    # print(my_path.seek_to_path())
    # print(my_path.path_var_exists("/usr/bin"))
