from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, "pages/index.html", {})
