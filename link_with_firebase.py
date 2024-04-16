import firebase_admin
from firebase_admin import credentials, db
import urllib.request
import os

class Link_firebase:
    def __init__(self, user_id):
        self.user_id = user_id
        self.cred = credentials.Certificate('library/DOGGYDINE_KEY')
        firebase_admin.initialize_app(self.cred, {'databaseURL' : "https://doggy-dine-default-rtdb.firebaseio.com/"})

        self.doggydine_ref = db.reference('/DoggyDine/UserAccount')
        self.user_image_folder = os.path.join('firebase', self.user_id)
        if not os.path.exists(self.user_image_folder):
            os.makedirs(self.user_image_folder)
        self.downloading_done = False
        
    def save_image(self):
        profile_images = self.doggydine_ref.child(self.user_id + '/profile').get()
        if profile_images:
            images_folder = os.path.join(self.user_image_folder, 'images')
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
                
            image_name = "profile_image.jpg"  # 이미지의 이름은 여기서 설정할 수 있습니다.
            image_path = os.path.join(images_folder, image_name)
            urllib.request.urlretrieve(profile_images, image_path)
            
            # 여러 장일 때.    
            # for image_name, image_url in profile_images.items():
            #     image_path = os.path.join(images_folder, image_name)
            #     urllib.request.urlretrieve(image_url, image_path)
        self.downloading_done = True
    
    def get_name(self):
        dog_name = self.doggydine_ref.child(self.user_id + '/dog_name').get()
        if dog_name:
            print("Dog Name:", dog_name)
        return dog_name
        
def main():
    user_id = 'Hi7x9pviAzeVXtXeQYQRV7Z4Inh2'
    linking = Link_firebase(user_id)
    linking.save_image()
    linking.get_name()
    
if __name__ == '__main__':
    main()
