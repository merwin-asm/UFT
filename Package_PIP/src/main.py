########################################################################
# UFT - 2 - CLIENT - CLI - PIP - Package
# Author : Merwin M.M
########################################################################


import socket
import os
import sys
import time
import hashlib

try:
    import rsa
    import requests as r
    from rich import print
    from rich.table import Table
    from rich.progress import track
except:
    os.system("pip install rsa requests rich")
try:
    import rsa
    import requests as r
    from rich import print
    from rich.table import Table
    from rich.progress import track
except:
    os.system("pip3 install rsa requests rich")
try:
    import rsa
    import requests as r
    from rich import print
    from rich.table import Table
    from rich.progress import track
except:
    print("\n\n Error related to the install of the requirements... Try to install rsa , requests and rich.. Then Run..")


table_commands = Table(title="Commands")
table_commands.add_column("Command", style="cyan", no_wrap=True)
table_commands.add_column("Use", style="magenta")
table_commands.add_column("No", justify="right", style="green")
table_commands.add_row("help", "Get info about the commands.", "1")
table_commands.add_row("upload (filename) (password)", "Upload a file.", "2")
table_commands.add_row("download (filename) (output) ", "Download a file.", "3")
table_commands.add_row("delete (filename) (password) ","Delete a file which is present in the server.","4")
table_commands.add_row("replace (filename) (password)","Replace a existing file.","5")

def read_public_key():
    with open("pub_key.txt", "rb") as f:
        pub_key = rsa.PublicKey.load_pkcs1(f.read())
        f.close()
    return pub_key


def encrypt(msg,public_key):
    return rsa.encrypt(msg.encode("ascii"),public_key)

def decrypt(msg,private_key):
    try:
        return rsa.decrypt(msg,private_key).decode("ascii")
    except:
        return False

def send_large(file_path,cli,max_chunk = 65536):
    f = open(file_path,"rb")
    size = os.path.getsize(file_path)
    if int(size) < max_chunk:
        cli.send("1".encode())
        rev = 1
    else:
        rev = size/max_chunk
        if int(rev) < rev:
            rev = int(rev+1)
        cli.send(str(int(rev)).encode())
    cli.recv(1024).decode()
    for step in track(range(int(rev)),description="Uploading..."):
        data = f.read(max_chunk)
        if data == b'':
            cli.send("done".encode())
            f.close()
            break
        else:
            cli.send(data)
            cli.recv(1024).decode()
            step
    while True:
        data = f.read(max_chunk)
        if data == b'':
            cli.send("done".encode())
            f.close()
            break
        else:
            cli.send(data)
            cli.recv(1024).decode()
def recv_large(filename,cli,max_chunk = 65536):
    f = open(filename,"wb")
    rev = cli.recv(1024).decode()
    rev = int(rev)
    cli.send(".".encode())
    data_chunks = b''
    for step in track(range(rev),description="Downloading..."):
        data = cli.recv(max_chunk)
        if data.decode() == "done":
            break
        else:
            data_chunks+=data
            cli.send(".".encode())
            step
    while True:
        data = cli.recv(max_chunk)
        if data.decode() == "done":
            break
        else:
            data_chunks += data
            cli.send(".".encode())
    f.write(data_chunks)
    f.close()
def hash_salt(password):
    dk = hashlib.pbkdf2_hmac('sha512', str(password).encode(), b'asxdjkjkhrafkn.ker//', 10000)
    final =  dk.hex()
    return final.encode()


def get_key():
    os_type = sys.platform.lower()
    if "win" in os_type:
        command = "wmic bios get serialnumber"
    elif "linux" in os_type:
        command = "sudo dmidecode -s system-serial-number"
    elif "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
	
    sn =  os.popen(command).read().replace("\n","").replace("	","").replace(" ","")
    
    key = r.get("https://serververifier.darkmash.repl.co/generatekey",headers={"cpu":sn}).text
    
    if key == "0":
        print("[red]  [-] Server Denied Connection[/red]")
        quit()

    return key
        
def main():

    recv_chunks = []
    send_chunks = []
    # Getting server info
    server_stat_url = "https://raw.githubusercontent.com/darkmash-org/UFT/main/status.txt"
    server_stats = r.get(server_stat_url).text
    server_stats = server_stats.replace("\n","")
    if server_stats == "DOWN":
        print("[bold red] [-] The server is DOWN. Try later..[/bold red]")
        quit()
    # setting connection to server
    server_stats = server_stats.split(":")
    port = int(server_stats[1])
    add = socket.gethostbyname(server_stats[0])
    print(f"[bold green] You are connecting to : {add} [/bold green]")
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    function = sys.argv[1]
    try:
        client.connect((add, port))
        key = get_key()
        client.send(key.encode())
        if client.recv(1024).decode() == "0":
            quit()
        print("[green] Got Connected To Server [/green]")
        if function == "help":
            print(table_commands)
        elif function == "download":
            a = time.time()
            client.send("download".encode())
            client.recv(1024).decode()
            file_name = sys.argv[2]
            new_name = sys.argv[3]
            client.send(file_name.encode())
            res = client.recv(1024).decode()
            if res == "yes":
                client.send(".".encode())
                recv_large(new_name,client)
                b = time.time()-a
                print(f" [blue]Time Taken : {b}s[/blue]")
            else:
                print("[red] File Not Found...[/red]")
        elif function == "upload":
            file_name = sys.argv[2]
            try:
                a = os.path.exists(file_name)
                if a:
                    b = os.path.isfile(file_name)
                    if b:
                        uploadable = True
                    else:
                        uploadable = False
                else:
                    uploadable = False
            except:
                uploadable = False
            if uploadable:
                file_password = sys.argv[3]
                file_password = hash_salt(file_password)
                client.send("upload".encode())
                client.recv(1024).decode()
                client.send(file_name.encode())
                res = client.recv(1024).decode()
                if res == "__++":
                    print("[red] File already exists , Try using other filename. [/red]")
                else:
                    client.send(file_password)
                    client.recv(1024).decode()

                    send_large(file_name,client)

                    print("[green] UPLOADED[/green]")
            else:
                print("[red] File Error[/red]")
        elif function == "delete":
            client.send("delete".encode())
            client.recv(1024).decode()
            filename = sys.argv[2]
            password = sys.argv[3]
            password = hash_salt(password)
            client.send(filename.encode())
            client.recv(1024).decode()
            client.send(password)
            res = client.recv(1024).decode()
            if res == "deleted":
                print("[green] Deleted...[/green]")
            else:
                print("[red] Password Incorrect / File Error...[/red]")
        elif function == "replace":
            file_name = sys.argv[2]
            pwd = sys.argv[3]
            os.system(f"uft delete {file_name} {pwd}")
            time.sleep(4)
            os.system(f"uft upload {file_name} {pwd}")     		
        else:
            print("[red] Command Not Found...[/red]")
        client.close()
        print("[red] Disconnected[/red]")
    except Exception as e:
        print(e)
        print("[red] Connection Error [/red]")

if __name__ == "__main__":
    main()
