from django.contrib.auth.models import User

class UserService:
    def __init__(self):
        pass

    def get_by_username(self, username):
        user = User.objects.get(username=username)
        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }

    def get_by_id(self, id):
        user = User.objects.get(id=id)
        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }

    def create(self, username:str, first_name:str, last_name:str, email:str, password:str):
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        user.save()
        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }

    def update(self):
        pass

    def delete(self):
        pass