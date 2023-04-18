import os
import pickle
import logging

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, validator
from dataclasses import dataclass, field
from colorama import Fore

from datetime import datetime

import uuid

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo


@dataclass(order=True)
class User:
    username: str
    password: str
    email: EmailStr
    active: field(init=False, repr=False)
    admin: field(init=False, repr=False)
    activation_token: field(init=False, repr=str(uuid.uuid4()))
    created_at: field(default_factory=datetime.now, repr=False, init=False, compare=False, hash=False, metadata=None)
    db: field(init=False, repr=False)

    def get_attributes(self) -> str:
        return "".join([f"\nUSER MODEL\n" + Fore.LIGHTBLUE_EX + f"username: {Fore.LIGHTMAGENTA_EX + self.username}\n", Fore.LIGHTBLUE_EX + f"password: {Fore.LIGHTMAGENTA_EX + self.password}\n", \
                       Fore.LIGHTBLUE_EX + f"email: {Fore.LIGHTMAGENTA_EX + self.email}\n", Fore.LIGHTBLUE_EX + f"active: {Fore.LIGHTRED_EX + str(self.active)}\n", \
                       Fore.LIGHTBLUE_EX + f"admin: {Fore.LIGHTRED_EX + str(self.admin)}\n", Fore.LIGHTBLUE_EX + f"activation_token: {Fore.LIGHTCYAN_EX + self.activation_token}\n" + Fore.RESET, \
                Fore.LIGHTBLUE_EX + f"created_at: {Fore.LIGHTYELLOW_EX + str(self.created_at)}\n" + Fore.LIGHTBLUE_EX + f"Database: {Fore.LIGHTGREEN_EX} mongodb+srv://.../database/users" + Fore.RESET])

    def load_user_from_db(self, username: str) -> Optional[dict]:
        user = self.db.users.find_one({"username": username})
        if user is None:
            return None
        self.username = user["username"]
        self.password = user["password"]
        self.email = user["email"]
        self.active = user["status"]
        self.activation_token = user["activation_token"]
        self.created_at = user["created_at"]


@dataclass(order=True)
class Conversation:
    user: User
    messages: field(default_factory=list[dict], repr=False, init=False, compare=False, hash=False, metadata=None)
    database: field(init=False, repr=False)
    id: str

    def __post_init__(self):
        if self.database.db.conversations.find_one({"_id": self.id}) is None:
            self.database.db.conversations.insert_one({"_id": self.id, "user": self.user.username, "messages": self.messages})

    def get_attributes(self) -> str:
        return "".join([f"\nCONVERSATION MODEL\n" + Fore.LIGHTBLUE_EX + f"id: {Fore.LIGHTCYAN_EX + str(self.id)}\n", Fore.LIGHTBLUE_EX + f"user: {Fore.LIGHTMAGENTA_EX + self.user.username}\n", \
                       Fore.LIGHTBLUE_EX + f"messages: {Fore.LIGHTYELLOW_EX + str(self.messages)}\n" + Fore.LIGHTBLUE_EX + f"Database: {Fore.LIGHTGREEN_EX} mongodb+srv://.../database/conversations" + Fore.RESET])

    def add_message(self, message: str, role: str = "user") -> str:
        self.messages.append({"role": role, "content": message})
        self.database.db.users.update_one({"_id": self.id}, {"$set": {"messages": {"role": role, "content": message}}})
        return str(self.messages)


app = Flask(__name__)
CORS(app)
uri = os.getenv("MONGODB_URI").replace("?", "database?")
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)
db_users = mongo.db.users
db_conversations = mongo.db.conversations

id = str(uuid.uuid4())

if not os.path.exists("id.pickle"):
    with open("id.pickle", "wb") as f:
        pickle.dump(id, f)
else:
    with open("id.pickle", "rb") as f:
        id = pickle.load(f)

print(id)

for conversation in db_conversations.find():
    print(conversation)

user = User(username="fuck", password="shit", email="carl", active=False, admin=False, activation_token=str(uuid.uuid4()), created_at=datetime.now(), db=db_users)
convo = Conversation(id=id, user=user, messages=[{"role": "system", "content": "vaschioer"}], database=mongo)

print(user.get_attributes())
convo.add_message(message="vaschier", role="fucker")
print(convo.get_attributes())


logging.basicConfig(level="INFO", format=f"\n{Fore.LIGHTMAGENTA_EX}%(asctime)s - %(name)s - %(levelname)s - %(message)s{Fore.RESET}", datefmt="%d-%b-%y %H:%M:%S")
app.logger = logging.getLogger(__name__)
app.logger.info(f"{Fore.LIGHTBLACK_EX}calisse{Fore.RESET}")
app.logger.warning(f"{Fore.LIGHTYELLOW_EX}calisse{Fore.RESET}")
app.logger.debug(f"{Fore.LIGHTWHITE_EX}calisse{Fore.RESET}")
app.logger.error(f"{Fore.RED}calisse{Fore.RESET}")

user.load_user_from_db("sallePutez")
print(user.get_attributes())
pute = db_users.find_one({"username": "sallePutez"})
print(pute)
new_user = User(username=pute["username"], password=pute["password"], email=pute["email"], active=False, admin=True, activation_token=str(uuid.uuid4()), created_at=pute["createdAt"], db=db_users)
print(new_user.get_attributes())

@app.route("/audio", methods=["POST"])
@cross_origin()
def audio():
    print(request.data)
    return {"message": "success"}, 200


app.run(host='0.0.0.0', port=8000)