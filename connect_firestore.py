import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("/Users/pratik/Desktop/gcp_personal/GCP_PROJECT/service_account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()  # this connects to our Firestore database
collection = db.collection('users')  # opens 'places' collection
doc = collection.document('list1')  # specifies the 'rome' document
res = doc.get().to_dict()
print(res)
print(res['pratik'])