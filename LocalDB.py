import json
import os


class DB:
    def __init__(self,name="main.json"):
        self.name = name
        try:
            self.file = open(name,"x")
            self.file.write('[{"users":[]}]')
            self.file.close()
            print("DB Created")
        except:
            print("DB is already found")
    def user_num(self):
        self.file = open(self.name,"r")
        self.raw_data = self.file.read()
        self.file.close()
        self.data = json.loads(self.raw_data)
        return len(self.data[0]["users"])
    def user_exists(self, user_name):
        self.file = open(self.name,"r")
        self.data = self.file.read()
        self.file.close()
        self.data = json.loads(self.data)
        no = 0
        for user in self.data[0]["users"]:
            if user["user"] == user_name:
                return True , no
            no+=1
        return False , no
    def add_user(self,username,password):
        a , b = self.user_exists(username)
        if a == False:
            self.file = open(self.name, "r")
            self.data = self.file.read()
            self.file.close()
            self.data = json.loads(self.data)
            self.user = {"user": username, "password": password,}
            self.data[0]["users"].append(self.user)
            self.new_data = json.dumps(self.data)
            self.file = open(self.name, "w")
            self.file.write(self.new_data)
            self.file.close()
            return True
        else:
            return False
    def delete_user(self,user_name):
        self.file = open(self.name, "r")
        self.data = self.file.read()
        self.file.close()
        self.data = json.loads(self.data)
        self.count = 0
        for user in self.data[0]["users"]:
            if user.get("user") == user_name:
                self.data[0]["users"].pop(self.count)
                file = open(self.name, "w")
                file.write(json.dumps(self.data))
                file.close()
                break
            self.count += 1

    def get_user_password(self,id):
        if True:
            self.file = open(self.name, "r")
            self.data = self.file.read()
            self.file.close()
            self.data = json.loads(self.data)
            for user in self.data[0]["users"]:
                if user.get("user") == id:
                    return [user.get("password")]
        return False
    def edit_user_password(self,id,password):
        a  = self.user_exists(id)
        if a:
            # print("found")
            self.file = open(self.name, "r")
            self.data = self.file.read()
            self.file.close()
            self.data = json.loads(self.data)
            self.count = 0
            for user in self.data[0]["users"]:
                if user.get("user") == id:
                    break
            self.data[0]["users"][self.count]["password"] = password
            file = open(self.name, "w")
            file.write(json.dumps(self.data))
            file.close()
            return True
        else:
            return False
    def confirm_password(self,id,password):
        a = self.get_user_password(id)
        if a == password:
            return True
        else:
            return False
