from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view

from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by("id")
    serializer_class = StudentSerializer


class ApiTokenView(ObtainAuthToken):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


schema_view = get_schema_view(
    title="Students API",
    description="Create, view, update, and delete student records.",
    version="1.0.0",
    public=True,
    renderer_classes=[JSONOpenAPIRenderer],
    authentication_classes=[],
    permission_classes=[AllowAny],
)


def api_schema(request):
    response = schema_view(request)
    schema = response.data
    schema.setdefault("components", {})["securitySchemes"] = {
        "TokenAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter `Token <your-token>`.",
        }
    }
    for path, operations in schema.get("paths", {}).items():
        if path.startswith("/api/students/"):
            for operation in operations.values():
                operation["security"] = [{"TokenAuth": []}]
    return JsonResponse(schema)


def api_docs(request):
    return HttpResponse(
        """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Students API</title>
  <link rel="stylesheet"
        href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => SwaggerUIBundle({
      url: "/api/schema/",
      dom_id: "#swagger-ui",
      deepLinking: true
    });
  </script>
</body>
</html>"""
    )


@require_GET
def api_health(request):
    return JsonResponse({"status": "ok"})


def home(request):
    return HttpResponse("server run like new")
