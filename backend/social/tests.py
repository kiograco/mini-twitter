from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Like, Follow
from rest_framework_simplejwt.tokens import RefreshToken

class SocialAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        # Login para obter token JWT
        response = self.client.post('/api/token/', {
            'username': 'user1',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_post(self):
        response = self.client.post('/api/posts/', {
            'content': 'Meu primeiro post!'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_like_post(self):
        post = Post.objects.create(author=self.user2, content="Post do user2")
        response = self.client.post(f'/api/posts/{post.id}/like/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 1)

    def test_follow_user(self):
        response = self.client.post('/api/follows/', {
            'following': self.user2.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Follow.objects.count(), 1)

    def test_feed_pagination_and_cache(self):
        for i in range(15):
            Post.objects.create(author=self.user1, content=f"Post {i}")

        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 10)  # PAGE_SIZE = 10

    def test_follow_self(self):
        # Tentar seguir a si mesmo (não deveria ser permitido)
        response = self.client.post('/api/follows/', {
            'following': self.user1.id  # tentando seguir a si mesmo
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Follow.objects.count(), 0)

    def test_like_post_again(self):
        post = Post.objects.create(author=self.user2, content="Post do user2")
        self.client.post(f'/api/posts/{post.id}/like/')
        
        # Tentando curtir o mesmo post novamente (deve falhar)
        response = self.client.post(f'/api/posts/{post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_feed(self):
        # Testa feed vazio (sem posts)
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 0)

    def test_pagination_next_page(self):
        # Cria 25 posts
        for i in range(25):
            Post.objects.create(author=self.user1, content=f"Post {i}")

        # Primeira página (deve ter 10 posts)
        response = self.client.get('/api/posts/?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data['results']), 10)

        # Segunda página (deve ter 10 posts)
        response = self.client.get('/api/posts/?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data['results']), 10)

def test_create_post_without_authentication(self):
    self.client.credentials()  # Remove o token de autenticação
    response = self.client.post('/api/posts/', {'content': 'Post sem autenticação'})
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ThrottleTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='throttle_user', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_throttle_limit_exceeded(self):
        url = '/api/posts/'  # ajuste conforme sua URL real

        # Realiza 6 requisições (1 a mais que o limite de 5/min)
        for i in range(6):
            response = self.client.get(url)

        # A última requisição deve retornar status 429
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)