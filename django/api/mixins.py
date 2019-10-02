from rest_framework import serializers


class ReadOnlySerializerMixin(serializers.Field):

    def __new__(cls, *args, **kwargs):
        setattr(
            cls.Meta,
            "read_only_fields",
            [f.name for f in cls.Meta.model._meta.get_fields()],
        )
        return super().__new__(cls, *args, **kwargs)
