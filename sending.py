import os
import cv2
import firebase_admin
from firebase_admin import credentials, db, storage
import urllib.request

class Sending:
    def __init__(self, user_id):
        self.user_id = user_id
        self.cred = credentials.Certificate('library/doggy-dine-firebase-adminsdk-6tcsx-e66d564d1b.json')
        if not firebase_admin._apps:
            firebase_admin.initialize_app(self.cred, {
                'databaseURL': "https://doggy-dine-default-rtdb.firebaseio.com/",
                'storageBucket': "doggy-dine.appspot.com"
            })
        self.doggydine_ref = db.reference('/DoggyDine/UserAccount')
        self.bucket = storage.bucket()

    def upload_image(self, local_file_path, storage_file_path):
        blob = self.bucket.blob(storage_file_path)
        blob.upload_from_filename(local_file_path)
        blob.make_public()
        return blob.public_url

    def sending(self):
        file_path = 'test.jpg'
        storage_file_path = f'{self.user_id}/profile/detected.png'
        public_url = self.upload_image(file_path, storage_file_path)
        self.doggydine_ref.child(f'{self.user_id}').update({'profile': public_url})
        print(f"Image uploaded and URL saved to database: {public_url}")

def main():
    user_id = 'TDQvhGXWwQcsFWrJ0wmnTS38d602'
    sending_instance = Sending(user_id)
    sending_instance.sending()

if __name__ == '__main__':
    main()