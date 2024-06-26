from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookAuthor
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_Book_list(self):
        book1 = Book.objects.create(title='Book1', description='Description1', isbn='123123')
        book2 = Book.objects.create(title='Book2', description='Description2', isbn='1111111')
        book3 = Book.objects.create(title='Book3', description='Description3', isbn='222222')

        response = self.client.get(reverse('books:list') + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
            self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_Detail(self):
        book = Book.objects.create(title='Book', description='Description', isbn='4545464')

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title='Sport', description='Description1', isbn='123123')
        book2 = Book.objects.create(title='Guide', description='Description2', isbn='1111111')
        book3 = Book.objects.create(title='Shoe Dog', description='Description3', isbn='222222')

        response = self.client.get(reverse("books:list") + "?q=Sport")

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Guide")

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Shoe Dog")

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)


class BookReviewTestCase(TestCase):
    def test_book_review(self):
        book = Book.objects.create(title='Book', description='Description', isbn='4545464')

        user = CustomUser.objects.create(username="Abdugofur", first_name='Aziz', last_name='raximov',
                                         email='admin@gmail.com')

        user.set_password('admin123')
        user.save()
        self.client.login(username="Abdugofur", password='admin123')

        self.client.post(reverse('books:reviews', kwargs={"id": book.id}),
                                    data={
                                        "stars_given": 3,
                                        "comment" : "Nice book!!!!!!"

                                    })
        book_reviews=book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book!!!!!!")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)


