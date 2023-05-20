from django.conf import settings
from django.http import HttpRequest
from typing import Mapping, Any


def my_context(request: HttpRequest) -> Mapping[str, Any]:
    return {"website_url": settings.G_WEBSITE_URL}
