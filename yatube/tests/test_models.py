from django.test import TestCase

from posts.models import Post

class PostModelTest(TestCase):
    @classmethod
    def setUpData(cls):
        Post.objects.create(text='This is test text')
    
    def test_text_name_label(self):
        posts=Post.objects.get(id=1)
        field_label = posts._meta.get_field('post').verbose_name
        self.assertEquals(field_label,'post')