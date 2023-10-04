"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from challenges.models import Laptop
from challenges.utils import to_json, serialize_and_response, is_not_get_request


def laptop_details_view(request: HttpRequest, laptop_id: int) -> JsonResponse | Http404:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    laptop_detail = get_object_or_404(Laptop, id=laptop_id)
    return JsonResponse(to_json(laptop_detail), safe=False)


def laptop_in_stock_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops_in_stock = Laptop.objects.filter(quantity_in_stock__gt=0).order_by('created_at')
    return serialize_and_response(laptops_in_stock)


def laptop_filter_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    if request.method == 'GET':
        brand = request.GET.get('brand')
        min_price = request.GET.get('min_price')

        laptops_brand = Laptop.objects.filter(brand=brand).exists()
        
        if not laptops_brand or int(min_price) < 0:
            return JsonResponse({'error': f'{brand} brand is not in our database or the price is negative'}, status=403)

        laptops_brand_min_price = Laptop.objects.filter(brand=brand, price__gt=min_price).order_by('price')
        return serialize_and_response(laptops_brand_min_price)
    
    return is_not_get_request()


def last_laptop_details_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    if Laptop.objects.exists():
        last_laptop_details = to_json(Laptop.objects.latest())
        return JsonResponse(last_laptop_details, safe=False)
    
    return JsonResponse({'error': 'laptops are missing'}, status=404)
