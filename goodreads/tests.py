from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview

from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_case(self):
        book = Book.objects.create(title='Book', description='Description', isbn='4545464')
        user = CustomUser.objects.create(username="Admin", first_name='Abdug\'ofur', last_name='Raximov',
                                         email='admin@gmail.com')

        user.set_password('0777')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Useful book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Book very gergous")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Very wonderful book")

        response = self.client.get(reverse("home_page") + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response,review1.comment)
