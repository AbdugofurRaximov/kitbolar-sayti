from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='Abdugofur', first_name='Aziz')
        self.user.set_password('admin123')
        self.user.save()
        self.client.login(username='Abdugofur', password='admin123')

    def test_book_api_view(self):
        book = Book.objects.create(title='Book', description='Description', isbn='4545464')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Very kind Book")

        response = self.client.get(reverse('api:review-detail', kwargs={'id': br.id}))
        print(response.data.keys(), 'skjkfkjqbwk')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 4)
        self.assertEqual(response.data['comment'], "Very kind Book")

        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], 'Abdugofur')
        self.assertEqual(response.data['user']['first_name'], 'Aziz')

        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book')
        self.assertEqual(response.data['book']['description'], 'Description')
        self.assertEqual(response.data['book']['isbn'], '4545464')

    def test_delete_api(self):
        book = Book.objects.create(title="Book12", description='Description', isbn="64466")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Good book")

        response = self.client.delete(reverse("api:review-detail", kwargs={'id': br.id}))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title="Book12", description="Description", isbn="14643121")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Good book")
        response = self.client.patch(reverse("api:review-detail", kwargs={'id': br.id}), data={'stars_given': 3})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 3)

    def test_put_review(self):
        book = Book.objects.create(title="Book12", description="Description", isbn="1415454643")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Nice book")

        response = self.client.put(reverse("api:review-detail", kwargs={'id': br.id}),
                                   data={"stars_given": 4, "comment": 'nice', "user_id": self.user.id,
                                         "book_id": book.id})
        br.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice')

    def test_create_review(self):
        book = Book.objects.create(title="Book12", description="Description", isbn="1213186")

        data = {
            "stars_given": 2,
            "comment": "bad book",
            "user_id": self.user.id,
            "book_id": book.id
        }

        response = self.client.post(reverse('api:review-list'), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 2)
        self.assertEqual(br.comment, "bad book")

    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='Azum', first_name='Azizaaaa')
        book = Book.objects.create(title='Book', description='Description', isbn='4545464')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="Very kind Book")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=2, comment="Not good Book")

        response = self.client.get(reverse("api:review-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][0]['id'], br_two.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br_two.comment)

        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)
