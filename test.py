import firebase_admin
from firebase_admin import credentials, firestore
from collections.abc import Mapping
users = []







class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

def get_firestore_data():

    if not firebase_admin._apps:
        cred = credentials.Certificate("service_account.json")
        default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()  # this connects to our Firestore database
    collection = db.collection('users')  # opens 'places' collection
    doc = collection.document('list1')  # specifies the 'rome' document
    res = doc.get().to_dict()
    print(res)
    l=[]
    id1 =0
    for key,val in res.items():
        usernam = key
        passwrd = val
        id1= id1+1
        users.append(User(id=id1, username=usernam, password=passwrd))


get_firestore_data()

users.append(User(id=1, username='mohit', password='moj'))
print("users")
print(users)

