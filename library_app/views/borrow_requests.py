import operator
import traceback
from library_management.throttles import LightRateLimit
from library_management.permissions import is_librarian_and_is_book_user
from utility.utils import get_serielizer_error, get_pagination_resp, transform_list, create_excel_file
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from ..serializers.login_serializer import LoginSerializer
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet
from utility.response import ApiResponse
from django.db import transaction
from datetime import datetime
from django.db.models import Q
from functools import reduce
from simple_search import search_filter
from utility.constants import STATUS_PENDING ,STATUS_APPROVED, STATUS_DECLINED, BOOK_USER
from ..swagger.borrow_request_swagger import *

from ..models import Books, BorrowRequests

from ..serializers.borrow_requests_serializer import BorrowRequestsSerializer

class BorrowRequestsView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [LightRateLimit]
    model_class = BorrowRequests.objects
    serializer_class = BorrowRequestsSerializer

    @swagger_auto_schema
    @is_librarian_and_is_book_user
    def retrieve(self, request, *args, **kwargs):
        try:
            get_id = self.kwargs.get('id')
            instance = self.model_class.filter(id = get_id).first()

            if not instance:
                return ApiResponse.response_bad_request(self, message="Borrow request details not present.")
            
            resp_dict = self.transform_single(instance)
            
            return ApiResponse.response_ok(self, data=resp_dict)
            
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    @swagger_auto_schema_post
    @is_librarian_and_is_book_user
    @transaction.atomic()
    def create(self, request, *args, **kwrgs):
        try:
            sp1 = transaction.savepoint()
            req_data = request.data.copy()
            book_id = req_data.get('book')
            # user_id = req_data.get('user')
            user_id = request.user.id
            start_date = req_data.get('start_date')
            end_date = req_data.get('end_date')
            status = req_data.get('status')

            if not user_id or not book_id:
                return ApiResponse.response_bad_request(self, message="Book Id and User Id are mandetory.")

            if check_is_exists := self.model_class.filter(Q(book_id = book_id), Q(Q(user_id=user_id) | ~Q(user_id=user_id)), 
                                                            Q(start_date__gte = start_date), Q(start_date__lte = end_date), 
                                                            Q(status__in = [STATUS_APPROVED, STATUS_PENDING])
                                                            ).first():
                return ApiResponse.response_bad_request(self, message="Borrow request is already exists with User details.")
            
            serializer = self.serializer_class(data=req_data)

            if not serializer.is_valid():
                serializer_error = get_serielizer_error(serializer)
                transaction.savepoint_rollback(sp1)
                return ApiResponse.response_bad_request(self, message=serializer_error)
            
            serializer.save()
            return ApiResponse.response_created(self, data=req_data, message="Borrow request stored successfully.")

        except Exception as e:
            print("tracenback", traceback.format_exc())
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
    
    @swagger_auto_schema_update
    @is_librarian_and_is_book_user
    @transaction.atomic()
    def update(self, request, *args, **kwrgs):
        try:
            sp1 = transaction.savepoint()
            req_data = request.data.copy()
            book_id = req_data.get('book')
            user_id = req_data.get('user')
            # user_id = request.user.id
            start_date = req_data.get('start_date')
            end_date = req_data.get('end_date')
            status = req_data.get('status')
            get_id = self.kwargs.get('id')

            if request.user.role_id == BOOK_USER:
                req_data.pop('status')

            instance = self.model_class.get(id = get_id)

            if not instance:
                return ApiResponse.response_not_found(self, message="Borrow request not found.")
            
            if request.user.role_id == BOOK_USER:
                if check_is_exists := self.model_class.filter(Q(book_id = book_id), Q(Q(user_id=user_id) | ~Q(user_id=user_id)), 
                                                                Q(start_date__gte = start_date), Q(start_date__lte = end_date), 
                                                                Q(status__in = [STATUS_APPROVED, STATUS_PENDING])
                                                                ).exclude(id=instance.id).exists():
                    return ApiResponse.response_bad_request(self, message="Borrow request is already exists with User.")

            serializer = self.serializer_class(instance, data=req_data, partial = True)

            if not serializer.is_valid():
                serializer_error = get_serielizer_error(serializer)
                transaction.savepoint_rollback(sp1)
                return ApiResponse.response_bad_request(self, message=serializer_error)
            
            serializer.save()
            return ApiResponse.response_ok(self, data=req_data, message="Borrow request updated successfully.")

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
    
    @swagger_auto_schema_list
    @is_librarian_and_is_book_user
    def list(self, request, *args, **kwrgs):
        try:
            where_array = request.query_params
            sort_by = where_array.get('sort_by') if where_array.get('sort_by') else "id"
            sort_direction = where_array.get('sort_direction') if where_array.get('sort_direction') else "ascending"
            if sort_direction == "descending":
                sort_by = "-" + sort_by

            obj_list = []

            if where_array.get('user_id'):
                obj_list.append(('user_id',where_array.get('user_id')))
            
            if where_array.get('book_id'):
                obj_list.append(('book_id',where_array.get('book_id')))

            if where_array.get('status'):
                status = int(where_array.get('status'))
                if status in [STATUS_APPROVED, STATUS_DECLINED, STATUS_DECLINED]:
                    obj_list.append(("status", status))
                else:
                    return ApiResponse.response_bad_request(self, message="Invalid status.")

            start_date = where_array.get("start_date")
            end_date = where_array.get("end_date")
            if start_date and end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                end_date = datetime.combine(end_date, datetime.max.time())
                obj_list.append(["start_date__range", [start_date, end_date]])

            elif start_date:
                obj_list.append(["start_date__gte", start_date])
    
            elif end_date:
                obj_list.append(["start_date__lte", end_date])
            
            q_list = [Q(x) for x in obj_list]

            if q_list:
                queryset = self.model_class.filter(reduce(operator.and_, q_list)).order_by(sort_by)
            else:
                queryset = self.model_class.order_by(sort_by)
            
            """Search for keyword"""
            if where_array.get("keyword"):
                queryset = queryset.filter(search_filter(self.search_fields, where_array.get("keyword")))

            resp_data = get_pagination_resp(queryset, request)
            response_data = transform_list(self, resp_data.get('data'))

            return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get("paginator"))
            
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
    
    @is_librarian_and_is_book_user
    def get_borrow_history(self, request, *args, **kwrgs):
        try:
            where_array = request.query_params
            is_download_file = where_array.get('is_download_file')
            
            sort_by = where_array.get('sort_by') if where_array.get('sort_by') else "id"
            sort_direction = where_array.get('sort_direction') if where_array.get('sort_direction') else "ascending"
            if sort_direction == "descending":
                sort_by = "-" + sort_by
            
            obj_list = []
            obj_list.append(("status", STATUS_APPROVED))

            print("request.user.id", request.user.id)
            if where_array.get('user_id'):
                obj_list.append(('user_id',where_array.get('user_id')))
            else:
                obj_list.append(('user_id',request.user.id))                

            start_date = where_array.get("start_date")
            end_date = where_array.get("end_date")
            if start_date and end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                end_date = datetime.combine(end_date, datetime.max.time())
                obj_list.append(["start_date__range", [start_date, end_date]])

            elif start_date:
                obj_list.append(["start_date__gte", start_date])
    
            elif end_date:
                obj_list.append(["start_date__lte", end_date])
            
            q_list = [Q(x) for x in obj_list]

            if q_list:
                queryset = self.model_class.filter(reduce(operator.and_, q_list)).order_by(sort_by)
            else:
                queryset = self.model_class.order_by(sort_by)
            
            """Search for keyword"""
            if where_array.get("keyword"):
                queryset = queryset.filter(search_filter(self.search_fields, where_array.get("keyword")))

            if is_download_file:
                if queryset:
                    file_name = create_excel_file(list(queryset))
                    return ApiResponse.response_ok(self, data={"file_name":file_name}, message="File generated successfully.")
                else:
                    return ApiResponse.response_bad_request(self, message="No data present.")

            else:
                resp_data = get_pagination_resp(queryset, request)
                response_data = transform_list(self, resp_data.get('data'))
                return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get("paginator"))
        except Exception as e:
            print("traceback", traceback.format_exc())
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    @swagger_auto_schema_delete
    @is_librarian_and_is_book_user
    def delete(self, request, *args, **kwrgs):
        try:
            get_id = self.kwargs.get('id')
            instance = self.model_class.filter(id = get_id).first()

            if not instance:
                return ApiResponse.response_bad_request(self, message="Borrow request not present.")
            
            instance.delete()
            
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
    
    def transform_single(self, instance):
        resp_dict = dict()
        if instance:
            resp_dict['id'] = instance.id
            if instance.book_id:
                resp_dict["book_id"] = instance.book_id
                resp_dict["title"] = instance.book.title
                resp_dict["author"] = instance.book.author
            if instance.user_id:
                resp_dict["user_id"] = instance.user_id
                resp_dict["user_name"] = f"{instance.user.first_name} {instance.user.last_name}"
                
            resp_dict["start_date"] = instance.start_date
            resp_dict["end_date"] = instance.end_date
            resp_dict["status"] = instance.get_status_display()
            resp_dict["status_name"] = instance.status
                
        return resp_dict

