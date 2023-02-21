import pyPath
import os

USER = os.getlogin()


target_install = f"/home/{USER}/UFT"

def delete_uft_dir():
    for e in os.listdir(target_install):
        os.remove(f"{target_install}/{e}")

if os.path.exists(target_install):
    cmd = input("UFT have been already installed. Do You want to uninstall then enter `y` , if you want to make no change enter `n`  , if you want a update enter `t`. [y/n/t] ?")
    if cmd == "y":
        delete_uft_dir()
        os.rmdir(target_install)
        os.remove("/usr/bin/UFT")
    elif cmd == "n":
        pass
    elif cmd == "t":
        delete_uft_dir()
        os.rmdir(target_install)
        os.remove("/usr/bin/UFT")

        for e in os.listdir():
            try:
                f_p = open(f"{target_install}/{e}", "w")
                f_c = open(f"{e}", "r")
                f_p.write(f_c.read())
                f_p.close()
                f_c.close()
            except:
                pass

        my_path = pyPath.MYPATH()
        my_path.make_redirecting_bashfile(
            "uft",
            target_pyfile=f"/home/{USER}/UFT/main.py",
            allow_args=True,
            max_num_args=1000
        )
        my_path.addfile_to_path(f"{target_install}/uft",
                                "uft",
                                exe=True)

else:
    os.mkdir(target_install)
    for e in os.listdir():

        try:
            f_p = open(f"{target_install}/{e}","w")
            f_c = open(f"{e}","r")
            f_p.write(f_c.read())
            f_p.close()
            f_c.close()
        except:
            pass
    my_path = pyPath.MYPATH()
    my_path.make_redirecting_bashfile(
    "uft",
    target_pyfile=f"/home/{USER}/UFT/main.py",
    allow_args=True,
    max_num_args=5
    )
    my_path.addfile_to_path(f"{target_install}/uft",
                            "uft",
                            exe=True)

print("Thankyou for Installing , From UFT creators.")
