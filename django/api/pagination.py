from rest_framework.pagination import LimitOffsetPagination


class TinyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20


class SmallLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
