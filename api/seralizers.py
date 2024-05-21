from rest_framework import serializers
from books.models import Book, BookReview
from users.models import CustomUser


# BU ModelSerialzierdan foydalangan holda yozilgan

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'isbn', 'description')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "username", "email")


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id=serializers.IntegerField(write_only=True)
    book_id=serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ("id", "stars_given", "comment", "user", "book","user_id","book_id")

#  Bu Serializerni uzidan foydalangan holda yozilgan
# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     description = serializers.CharField()
#     isbn = serializers.CharField(max_length=17)
#
#
# class UserSerializer(serializers.Serializer):
#     username=serializers.CharField(max_length=250)
#     first_name=serializers.CharField(max_length=250)
#     last_name=serializers.CharField(max_length=250)
#     email=serializers.EmailField()
#
#
# class BookReviewSerializer(serializers.Serializer):
#     stars_given = serializers.IntegerField(min_value=1, max_value=5)
#     comment = serializers.CharField()
#     book=BookSerializer()
#     user=UserSerializer()
