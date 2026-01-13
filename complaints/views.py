import json
from django.conf import settings
from google import genai
from complaints.services import GeminiService

# DRF Imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def testAI(request):

    prompt = request.data.get("mensaje")
    if not prompt:
        return Response({"error": "The Field ''mensaje' is required"}, status=400)
    else:
        gemini_service = GeminiService()
        response = gemini_service.send_prompt(prompt)
        return Response({"response": response})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_complaint(request):
    gemini_service = GeminiService()
    response = gemini_service.get_complaint()
    return Response({"response": response})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_complaint(request):
    complaint = request.data.get("complaint")

    if not complaint:
        return Response({"error": "The Field 'complaint' is required"}, status=400)
    else:
        gemini_service = GeminiService()
        response = gemini_service.parse_complaint_to_json(complaint)

        """
        In this part, we're going to do all logic to manage the data, like validate and sanitizade the data, save the complaint in the database, and return the response 
        """
        return Response({"response": response})
