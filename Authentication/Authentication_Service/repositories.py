from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser 
from django.db.models import QuerySet
from .event_emitter import EventEmitter 

class UserRepository:
    def __init__(self):
        self.event_emitter = EventEmitter()
    
    
    def create_user(self , validated_data) -> CustomUser:
        email = validated_data.get('email')
        if not email: 
             raise ValueError("Email is required")
        
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        self.event_emitter.emit_user_created_event(user)
        return user

    def get_user_by_email(self, user_email: str) -> CustomUser:
        try:
            return CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            raise ObjectDoesNotExist("User not found.")   