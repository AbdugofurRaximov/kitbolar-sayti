import generics as generics
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from api.seralizers import BookReviewSerializer
from rest_framework.response import Response
from books.models import BookReview
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets





#  Viewsetlar bilan ishlash


class BookReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-created_at')
    lookup_field = 'id'








class BookReviewDetailApiView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all()
    lookup_field = 'id'

#  Buni qolda yozilgani

# class BookReviewDetailApiView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(book_review)
#         return Response(data=serializer.data)
#
#     def delete(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         book_review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def put(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(instance=book_review, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(instance=book_review, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-created_at')


# #  Buni qolda yozilgani


# class BookListAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         book_reviews = BookReview.objects.all().order_by('-created_at')
#
#         paginator = PageNumberPagination()
#         page_obj = paginator.paginate_queryset(book_reviews, request)
#         serializer = BookReviewSerializer(page_obj, many=True)
#         # return Response(data=serializer.data)
#         return paginator.get_paginated_response(data=serializer.data)
#
#     def post(self, request):
#         serializer = BookReviewSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)










        #  Qolda yozish bu Viewni uzidan foydalangan holda API chiqarish
        # json_response = {
        #     "id": book_review.id,
        #     "stars_given": book_review.stars_given,
        #     "comment": book_review.comment,
        #     "book": {
        #         "id": book_review.book.id,
        #         "title": book_review.book.title,
        #         "isbn": book_review.book.isbn,
        #         "describtion": book_review.book.description
        #     },
        #
        #     "user": {
        #         "id": book_review.user.id,
        #         "first_name": book_review.user.first_name,
        #         "last_name": book_review.user.last_name,
        #         "email": book_review.user.email,
        #         "username": book_review.user.username
        #     }
        # }

        # return JsonResponse(json_response)
