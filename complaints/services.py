# services.py
import random
from django.conf import settings
from google import genai
from google.api_core import exceptions
from google.genai import types


class GeminiService:

    structure_data = {
        "date": "",
        "anonymous": True,
        "channel": "Web",
        "reporter": {"relationship_to_company": "employee", "country": "México"},
        "people": {
            "offender": {
                "name": "",
                "position": "",
                "department": "",
            }
        },
        "incident": {
            "type": "",
            "description": "",
            "approximate_date": "",
            "is_ongoing": True,
        },
        "location": {
            "city": "", 
            "work_related": True
            },
        "evidence": {
            "has_evidence": True,
            "description": "",
        },
    }

    def __init__(self):
        # Inicializamos el cliente una sola vez
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-2.0-flash"

    def get_complaint(self):
        types = [
            "fraude",
            "acoso laboral",
            "robo de inventario",
            "conflicto de interés",
        ]
        random_type = random.choice(types)

        prompt = (
            f"ACTÚA COMO UN USUARIO DENUNCIANTE. Tu objetivo es redactar el cuerpo de una denuncia "
            f"basándote en esta estructura de datos: {self.structure_data}. "
            f"El incidente principal es: {random_type}."
            f"REGLAS DE FORMATO OBLIGATORIAS:"
            f"1. RESPONDE ÚNICAMENTE con el texto del relato. Está prohibido saludar o dar explicaciones."
            f"2. PROHIBIDO usar Markdown: no uses asteriscos (**), no uses hashtags (#), no uses guiones para listas."
            f"3. PROHIBIDO usar encabezados como 'Descripción:' o 'Nombre:'. Integra la información de forma natural en los párrafos."
            f"4. Escribe en texto plano, con saltos de línea normales entre párrafos."
            f"INSTRUCCIONES DE NARRATIVA:"
            f"- Usa un tono humano, puede ser molesto, formal o preocupado."
            f"- Menciona el nombre del implicado inventado y su puesto de forma fluida."
            f"EJEMPLO DE SALIDA ESPERADA (No uses este contenido, solo el formato):"
            f"El pasado mes de diciembre noté que en el área de compras se están saltando los procesos. "
            f"El gerente Juan Pérez ha estado aprobando facturas de su propia familia. Esto lo sé porque "
            f"tengo los correos guardados. Sigue pasando a día de hoy en la oficina de Monterrey y "
            f"me parece una falta de ética total."
        )
        response = self.send_prompt(prompt)
        return response

    def parse_complaint_to_json(self, complaint):
        """
        Method to parse a complaint in plain text to a JSON with the Structure defined in self.structure_data
        """
        prompt = (
            f"ACTÚA COMO UN EXPERTO EN EXTRACCIÓN DE DATOS.\n"
            f"Tu objetivo es convertir el siguiente texto de denuncia en un objeto JSON "
            f"que siga ESTRICTAMENTE la estructura proporcionada.\n\n"
            f"ESTRUCTURA JSON OBJETIVO:\n"
            f"{self.structure_data}\n\n"
            f"TEXTO DE LA DENUNCIA:\n"
            f"'{complaint}'\n\n"
            f"INSTRUCCIONES:\n"
            f"1. Extrae toda la información posible del texto.\n"
            f"2. Si un campo no se menciona, usa null o una cadena vacía según corresponda, pero mantén la estructura.\n"
            f"3. Devuelve SOLAMENTE el JSON válido, sin bloques de código ```json ``` ni explicaciones adicionales."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            # Aseguramos que devolvemos un objeto Python (dict) para que JsonResponse lo serialice bien
            import json
            return json.loads(response.text)
        except Exception as e:
            return {"error": f"Error al parsear denuncia: {str(e)}"}


    def send_prompt(self, prompt):
        """
        Method to send a prompt to the Gemini model and return the response
        """
        # return {"respuesta": prompt}
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                    temperature=0.2,
                ),
            )
            return response.text
        except Exception as e:
            return f"Error inesperado: {str(e)}"
