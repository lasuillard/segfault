from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    is_official = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{ self.pk } { self.name[:10] if len(self.name) > 10 else self.name }"

    def get_content_count(self):
        if not hasattr(self, 'fragment_set'):
            raise AttributeError(
                'fragment_set does not exists. please be make sure that model Fragment has tags field.'
            )

        return self.fragment_set.count()
