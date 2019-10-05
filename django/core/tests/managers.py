from django.test import TestCase
from ..models import Tag
from ..factories import TagFactory


class TagManagerTest(TestCase):

    def test_tag_manager_get_or_create_from_string_all_tags_does_not_exist(self):
        # all tags does not exist
        tags = ['qr/631fx', '21^_3h90e1$', 'asfUG+;']
        # extract name field only
        converted_tags = map(lambda ct: ct.name, Tag.objects.get_or_create_from_string(tags))
        # check all tags given got or created properly
        self.assertTrue(all(map(lambda t: t in converted_tags, tags)))

    def test_tag_manager_get_or_create_from_string_some_tags_already_not_exist(self):
        # some tags does not exist
        tags = ['531uufd', '~$5jfh%_+', TagFactory(name='xaffnhh').name]
        # extract name field only
        converted_tags = map(lambda ct: ct.name, Tag.objects.get_or_create_from_string(tags))
        # check all tags given got or created properly
        self.assertTrue(all(map(lambda t: t in converted_tags, tags)))

    def test_tag_manager_get_or_create_from_string_malformed_tags(self):
        # totally bad case
        tags = [3, 'afxx_5', -518]
        with self.assertRaises(ValueError) as _:
            _ = Tag.objects.get_or_create_from_string(tags)
