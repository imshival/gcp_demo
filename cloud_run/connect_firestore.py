import firebase_admin
from firebase_admin import credentials, firestore
from collections.abc import Mapping


def get_firestore_data(logged_in_user,logged_in_user_password):

    if not firebase_admin._apps:
        cred = credentials.Certificate("service_account.json")
        default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()  # this connects to our Firestore database
    collection = db.collection('users')  # opens 'places' collection
    doc = collection.document('list1')  # specifies the 'rome' document
    res = doc.get().to_dict()
    if res.get(logged_in_user) is not None:
        firestore_password = res[logged_in_user]
        if logged_in_user_password == firestore_password:
            return "0"
        else:
            return "1"
    else:
        return "2"


