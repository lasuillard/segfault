from django.db import models


class TagManager(models.Manager):

    def get_or_create_from_string(self, tags):
        """
        Return string mapping to Tag model instance, create if does not exists.

        :param tags: pure string array,
        :return: list of Tag instances.
        """
        if any(map(lambda t: not isinstance(t, str), tags)):
            raise ValueError('tags should be pure array of string.')

        tags_already_exists = super().get_queryset().filter(name__in=tags)
        for tag in tags_already_exists:
            tags.remove(tag.name)

        tags_newly_created = map(lambda t: self.create(name=t), tags)
        return [*tags_already_exists, *tags_newly_created]


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    is_official = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    objects = TagManager()

    def __str__(self):
        return f"{ self.pk } { self.name[:10] if len(self.name) > 10 else self.name }"

    def get_content_count(self):
        return self.fragment_set.count()
