from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their 
    email address as an alternative to their username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Login with either email or username (for maximum flexibility)
            user = UserModel.objects.filter(Q(email__iexact=username) | Q(username__iexact=username)).distinct()
        except UserModel.DoesNotExist:
            return None

        if user.exists():
            user_obj = user.first()
            if user_obj.check_password(password):
                return user_obj
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
