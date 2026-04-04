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

Middleware yang mengatur (akan default ke 'id' sesuai settings.LANGUAGE_CODE)
 override di sini, sehingga jika kita buat tombol ganti bahasa untuk guest,
 tiba-tiba keriset ke 'id' lagi.
            pass

        response = self.get_response(request)
        return response
