from rest_framework import serializers
from ..model.books import Books
from ..model.borrow_requests import BorrowRequests

class BorrowRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequests
        fields = "__all__"
    
