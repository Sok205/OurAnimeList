"""
Django views for the main app
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class ApiRoot(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        """
        Returns a list of available API endpoints.
        """

        content = {
                'message': 'Weeb API - Get your favourite anime!',
                'endpoints': {
                    'token_obtain_pair': '/api/token/',
                    'token_refresh': '/api/token/refresh/',
                }
            }

        return Response(content)