from django.contrib import admin
from core.models import Fragment


class FragmentTagFilter(admin.SimpleListFilter):
    title = 'Tags'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        tags = Fragment.objects.values_list('tags', flat=True)
        tags = [(t, t) for sublist in tags for t in sublist if t]
        tags = sorted(set(tags))
        return tags

    def queryset(self, request, queryset):
        lookup_value = self.value()
        if lookup_value:
            queryset = queryset.filter(tags__contains=[lookup_value])

        return queryset
