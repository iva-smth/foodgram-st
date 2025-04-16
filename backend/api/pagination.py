from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    default_limit = 6
    limit_query_param = 'limit'
    # offset_query_param = 'offset'
    # max_limit = 50