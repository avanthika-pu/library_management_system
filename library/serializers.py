from rest_framework import serializers
from .models import Author, Book, Borrower


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'published_date', 'available_copies']

class BorrowerSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )

    class Meta:
        model = Borrower
        fields = ['id', 'name', 'email', 'book', 'book_id', 'borrowed_date', 'return_date']

    def validate(self, data):
        book = data['book']
        if book.available_copies <= 0:
            raise serializers.ValidationError("No available copies for this book.")
        return data

    def create(self, validated_data):
        book = validated_data['book']
        if book.available_copies <= 0:
            raise serializers.ValidationError("No available copies for this book.")
        book.available_copies -= 1
        book.save(update_fields=["available_copies"])
        borrower = Borrower.objects.create(**validated_data)
        return borrower
