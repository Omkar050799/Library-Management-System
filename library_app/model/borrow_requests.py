from django.db import models
from ..models import Base
from ..models import Books
from ..models import User

class BorrowRequests(Base):
    book = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank= True)
    end_date = models.DateField(null=True, blank=True)
    STATUS_CHOICE = ((1,"Pending"), (2, "Approved"), (3, "Denied"))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICE, default=1)

    class Meta:
        db_table = "borrow_requests"

    def __str__(self) -> str:
        return super().__str__()