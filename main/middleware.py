from django.utils import translation


class LanguageSyncMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_language = getattr(request.user.profile, "preferred_language", None)
            if user_language:
                translation.activate(user_language)
                request.LANGUAGE_CODE = translation.get_language()
        else:
            pass

        response = self.get_response(request)
        return response
