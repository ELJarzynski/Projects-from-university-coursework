from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Board, BoardUser
from .serializer import BoardUserSerializer

CREATE_USER_BOARD_URL = '/board/add_user/'
CREATE_BOARD_URL = '/board/create_board/'


class CreateBoardViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_create_board_success(self):
        """Test creating a new board"""
        payload = {
            'name': 'Test Board',
            'description': 'Test Board Description',
            'due_date': '2024-03-15'
        }
        response = self.client.post(CREATE_BOARD_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Sprawdź, czy tablica została utworzona
        self.assertTrue(Board.objects.filter(name=payload['name']).exists())

        # Sprawdź, czy użytkownik został dodany jako właściciel tablicy
        board = Board.objects.get(name=payload['name'])
        self.assertTrue(BoardUser.objects.filter(board=board, user=self.user, is_owner=True).exists())


class CreateUserBoardViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = get_user_model().objects.create_user(
            email='owner@example.com',
            password='testpass'
        )
        self.client.force_authenticate(self.owner)

        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass'
        )

    def test_create_user_board_success(self):
        """Test creating a new BoardUser by owner"""
        board = Board.objects.create(name='Test Board', description='Test Board Description', due_date='2024-03-15')
        payload = {'board_id': board.id, 'email': self.user.email}  # Poprawiony klucz na 'email'
        response = self.client.post(CREATE_USER_BOARD_URL, payload)

        self.assertTrue(Board.objects.filter(name='Test Board').exists())  # Sprawdź, czy tablica została utworzona
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Sprawdź, czy użytkownik został dodany do tablicy
        board_user = BoardUser.objects.filter(board=board, user=self.user)
        self.assertTrue(board_user.exists())
        print(board_user[0].board)

        # Sprawdź, czy użytkownik został dodany jako właściciel tablicy
        # self.assertTrue(BoardUser.objects.filter(board=board, user=self.owner, is_owner=True).exists())



