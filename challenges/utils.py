from django.http import JsonResponse
from django.db import models
from django.db.models import QuerySet
from django.core import serializers


def to_json(obj: models.Model) -> str:
    serialized_obj = serializers.serialize('json', [obj])
    return serialized_obj


def queryset_to_json_response(query_set: QuerySet) -> JsonResponse:
    serialized_query_set = [to_json(object) for object in query_set]
    return JsonResponse(serialized_query_set, safe=False)


def method_get_error_response() -> JsonResponse:
    return JsonResponse({'error': 'The response is available only via a GET request.'}, status=403)


def request_not_be_empty() -> JsonResponse:
    return JsonResponse({'error': 'The request cannot be empty. Enter a request.'}, status=404)