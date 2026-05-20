import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/amastour/workspace/terraform_exam/credendials.json'
from firestore_client import get_firestore_client
fs = get_firestore_client()
print('Project:', fs.project)
print('[OK] Firestore connection successful')
