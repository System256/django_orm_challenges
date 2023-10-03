"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими постами для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект поста в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.db.models import Q
from challenges.models import Post
from challenges.utils import sterilize_and_response, request_not_be_empty, is_not_get_request
from datetime import timedelta


def last_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    last_posts = Post.objects.all().order_by('published_in')[:3]
    return sterilize_and_response(last_posts)


def posts_search_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    if request.method == 'GET':
        search_query = request.GET.get('query')

        if len(search_query) > 0:
            posts_search = (Post.objects\
                            .filter(Q(title__icontains=search_query) | Q(text__icontains=search_query)))
            return sterilize_and_response(posts_search)
        
        return request_not_be_empty()

    return is_not_get_request()



def untagged_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    untagged_posts = (Post.objects\
                        .filter(category__exact='')\
                        .order_by('authors_name')\
                        .order_by('created_at'))
    return sterilize_and_response(untagged_posts)


def categories_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    if request.method == 'GET':
        categories = request.GET.get('categories').split(',')

        if len(categories) > 0:
            categories_posts = Post.objects.filter(category__in=categories)
            return sterilize_and_response(categories_posts)

        return request_not_be_empty()
    
    return is_not_get_request()


def last_days_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    if request.method == 'GET':
        last_days = request.GET.get('last_days')

        last_days_posts = (Post.objects\
            .filter(published_in__gte=timezone.now() - timedelta(days=int(last_days))))\
            .filter(status='pub')
        return sterilize_and_response(last_days_posts)
    
    return is_not_get_request()
