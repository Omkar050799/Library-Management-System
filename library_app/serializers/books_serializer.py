from rest_framework import serializers
from ..model.books import Books

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"
    
