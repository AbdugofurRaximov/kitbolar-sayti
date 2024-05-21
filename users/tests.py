from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user

class RegisterTestCase(TestCase):
    def test_account_iscreated(self):
        self.client.post(
         reverse("users:register"),
         data={
            "username":'Abdugofur',
            "first_name":'Aziz',
            "last_name":"raximov",
            "email":'admin@gmail.com',
            'password':'admin123 '}
                         )

        user = CustomUser.objects.get(username="Abdugofur")
        self.assertEqual(user.first_name, "Aziz")
        self.assertEqual(user.last_name, 'raximov')
        self.assertEqual(user.email, 'admin@gmail.com')
        self.assertNotEqual(user.password, 'admin123')
        self.assertTrue(user.check_password, 'admin123')



    def test_required_id(self):
        response=self.client.post(
            reverse('users:register'),
            data={
                "first_name":"Aziz",
                "email":'admin@gmail.com'
            }

        )

        user_count=CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response,"form",'username','This field is required.')
        self.assertFormError(response,"form",'password','This field is required.')

    def test_invalid_email(self):
        response=self.client.post(
            reverse("users:register"),
            data={
                "username": 'Abdugofur',
                "first_name": 'Aziz',
                "last_name": "raximov",
                "email": 'admin12ekdndf',
                'password': 'admin123 '}
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response,"form","email","Enter a valid email address.")


    def test_unique_username(self):
        user=CustomUser.objects.create(username='Abdugofur',first_name='Aziz')
        user.set_password("admin123")
        user.save()

        response=self.client.post(
            reverse('users:register'),
            data={
                'username':'Abdugofur',
                'first_name':'Aziz',
                'last_name':'raximov',
                'email':'admin@gmail.com',
                'password':'admin123'
            }
        )
        user_count=CustomUser.objects.count()
        self.assertEqual(user_count,1)
        self.assertFormError(response,'form','username','A user with that username already exists.')


class LoginTestCase(TestCase):

    def setUp(self):
        self.db_user = CustomUser.objects.create(username='Abdugofur', first_name='Aziz')
        self.db_user.set_password('admin123')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'Abdugofur',
                'password':'admin123'
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='Abdugofur', password='admin123')
        self.client.get(reverse("users:logout"))
        user=get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_wrong_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username": "wrong test",
                "password": "adminnnn"
            }
        )
        user=get_user(self.client)
        self.assertFalse(user.is_authenticated)


        self.client.post(
            reverse('users:login'),
            data={
                "username":"Abdugofur",
                "password":"somepass"
            }
        )

        user=get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):

    def test_login_required(self):
        response=self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,reverse("users:login")+"?next=/users/profile/")

    def test_profile_details(self):

        user=CustomUser.objects.create(username="Abdugofur", first_name='Aziz', last_name='raximov',email='admin@gmail.com')

        user.set_password('admin123')
        user.save()
        self.client.login(username="Abdugofur",password='admin123')

        response=self.client.get(reverse("users:profile"))

        self.assertContains(response,user.username)
        self.assertContains(response,user.first_name)
        self.assertContains(response,user.last_name)
        self.assertContains(response,user.email)


    def test_updateprofile(self):
        user = CustomUser.objects.create(username="Abdugofur", first_name='Aziz', last_name='raximov',email='admin@gmail.com')
        user.set_password('admin123')
        user.save()
        self.client.login(username="Abdugofur", password='admin123')

        response=self.client.post(
            reverse("users:profile-edit"),

            data={
                "username":"Abdugofur",
                "first_name":"Aziza",
                "last_name":"azimov",
                "email":"admin@gmail.com"
            }
        )

        # user=User.objects.get(pk=user.pk)
        user.refresh_from_db()

        self.assertEqual(user.first_name,"Aziza")
        self.assertEqual(user.last_name,'azimov')
        self.assertEqual(response.url,reverse("users:profile"))