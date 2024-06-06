import firebase_admin
from firebase_admin import credentials, db
import urllib.request
import os

class Link_firebase:
    def __init__(self, user_id):
        self.user_id = user_id
        self.cred = credentials.Certificate('library/doggy-dine-firebase-adminsdk-6tcsx-e66d564d1b.json')
        firebase_admin.initialize_app(self.cred, {'databaseURL' : "https://doggy-dine-default-rtdb.firebaseio.com/"})
        self.doggydine_ref = db.reference('/DoggyDine/UserAccount')
        self.user_folder = os.path.join('firebase', self.user_id)
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)
        self.Done = False
        
    def save_images(self):
        pets = self.doggydine_ref.child(self.user_id + '/pet/').get()
        if pets:
            for pet_name, pet_info in pets.items():
                pet_folder = os.path.join(self.user_folder, pet_name)
                if not os.path.exists(pet_folder):
                    os.makedirs(pet_folder)
                
                if 'profile' in pet_info:
                    profile_images = pet_info['profile']
                    
                    for i, (key, profile_image_url) in enumerate(profile_images.items()):
                        image_name = f"image_{i}.jpg"
                        image_path = os.path.join(pet_folder, image_name)
                        print(f"Downloading {profile_image_url} to {image_path}")
                        with urllib.request.urlopen(profile_image_url) as response, open(image_path, 'wb') as out_file:
                            out_file.write(response.read())
                    
        self.Done = True
    
    def waiting(self):
        detected_ref = self.doggydine_ref.child(f"{self.user_id}/Detected/start")
        start_value = detected_ref.get()
        if start_value == True:
            self.Done = True
            
    def get_names(self):
        pets = self.doggydine_ref.child(self.user_id + '/pet/').get()
        if pets:
            for pet_name, pet_info in pets.items():
                dog_name = pet_name
                if dog_name:
                    print(f"Pet Name ({pet_name}): {dog_name}")
        return [pet_name for pet_name in pets.keys()]

def main():
    user_id = 'TDQvhGXWwQcsFWrJ0wmnTS38d602'
    linking = Link_firebase(user_id)
    linking.save_images()
    linking.get_names()
    
if __name__ == '__main__':
    main()
