from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from django.core.cache import cache

from django.urls import reverse
from posts.models import Post, Group

class TestImageView(TestCase):

    def setUp(self):
        cache.clear()

        self.client = Client()
        self.user = User.objects.create_user(
            username='sarah_conor',
            email='conor@gmail.com',
            password='12345ASDFqwer'
        )
        self.client.force_login(self.user)

        self.post_not_img = self.client.post(
            reverse('new_post'),
                data={
                    'author': self.user,
                    'text': 'Тест без картинки!',
                },
            follow=True
        )

        group = Group.objects.create(
            title='Тестовая группа 1', 
            slug='test-link', 
            description='Тестовое описание группы'
        )
        
        with open('imagetest.jpg','rb') as img:
            self.post_with_img = self.client.post(
                reverse('new_post'),
                    data={
                        'author': self.user,
                        'text': 'Тест с картинкой!',
                        'image': img,
                        'group': group.pk
                    },
                follow= True,
            )
        self.assertEqual(self.post_not_img.status_code, 200)
        self.assertEqual(self.post_with_img.status_code, 200)

        self.assertEqual(Post.objects.count(), 2)

        self.post_not_img = Post.objects.get(text='Тест без картинки!')
        self.post_with_img = Post.objects.get(text='Тест с картинкой!')


    def test_image_contains(self):
        # urls_with_img = [
        #     reverse('index'),
        #     reverse('post', kwargs={
        #                 'username': self.user.username,
        #                 'post_id': self.post_with_img.pk}),
        #     reverse('profile',kwargs={
        #                 'username': self.user.username}),
        # ]
        
        # for url in urls_with_img:
        #     # print(url)
        #     response = self.client.get(url)
        #     # print(response.content.decode())
        #     self.assertEqual(response.status_code, 200)
        #     self.assertContains(response, 'img')
        pass