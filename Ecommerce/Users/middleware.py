from django.http import JsonResponse
from django.conf import settings
import jwt
from .models import client
from .serializer  import UserSerializer

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=401)

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, key='asdrft123', algorithms=["HS256"])
            user_id = payload.get("id")
            if not user_id:
                return JsonResponse({"error": "Invalid token"}, status=401)

            user = client.objects.get(id=user_id)
            user_data = UserSerializer(user)

            if not user_data.data['isAdmin']:
                return JsonResponse({"error": "Access denied"}, status=403)

            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"error": "Invalid token encoding"}, status=401)

        response = self.get_response(request)

        return response

