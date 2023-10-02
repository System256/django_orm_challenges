from django.http import JsonResponse
from django.db import models
from django.db.models import QuerySet
from django.core import serializers


def to_json(obj: models.Model) -> str:
    serialized_obj = serializers.serialize('json', [obj])
    return serialized_obj


def sterilize_and_response(query_set: QuerySet) -> JsonResponse:
    sterilized_query_set = [to_json(object) for object in query_set]
    return JsonResponse(sterilized_query_set, safe=False)


def is_not_get_request() -> JsonResponse:
    return JsonResponse({'error': 'The response is available only via a GET request.'})


def request_not_be_empty() -> JsonResponse:
    return JsonResponse({'error': 'The request cannot be empty. Enter a request.'})