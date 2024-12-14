import operator
from datetime import datetime
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from functools import reduce
from simple_search import search_filter
from django.db.models import Q
from django.db import transaction
from rest_apiresponse.apiresponse import ApiResponse

""" permissions """
from rest_framework.permissions import IsAuthenticated
from job_portal.permissions import (
    is_super_user_or_mf_user,
    super_user_or_employer_job_seeker,
)

""" utility """
from utility.constants import MESSAGES, TOPICS
from utility.utils import (
    MultipleFieldPKModelMixin,
    CreateRetrieveUpdateViewSet,
    create_or_update_serializer,
    get_required_fields,
    get_pagination_resp,
    transform_list,
    validate_empty_strings,
)

""" model imports """
from ..models import Faq

""" serializers """
from ..serializers.faq_serializer import FaqSerializer

""" swagger """
from ..swagger.faq_swagger import (
    swagger_auto_schema_list,
    swagger_auto_schema_post,
    swagger_auto_schema,
    swagger_auto_schema_update,
    swagger_auto_schema_delete,
    swagger_auto_schema_bulk_delete,
)


class FaqView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FaqSerializer
    singular_name = "Faq"
    model_class = Faq.objects

    search_fields = ["question", "answer"]

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except Exception:
            return None

    @swagger_auto_schema
    @super_user_or_employer_job_seeker
    def retrieve(self, request, *args, **kwargs):
        """
        :To get the single record
        """
        """ capture data """
        get_id = self.kwargs.get("id")

        """ process/format on data """
        instance = self.get_object(get_id)
        if instance:
            if request.query_params.get("is_all_data"):
                resp_dict = self.transform_single_with_to_dict(instance)
            else:    
                resp_dict = self.transform_single(instance)

            
            return ApiResponse.response_ok(self, data=resp_dict)

        return ApiResponse.response_not_found(self, message=self.singular_name + MESSAGES['not_found'])

    @swagger_auto_schema_post
    @transaction.atomic()
    @is_super_user_or_mf_user
    def create(self, request, *args, **kwargs):
        """
        :To create the new record
        """
        sp1 = transaction.savepoint()

        """ capture data """
        req_data = request.data.copy()
        if not req_data:
            return ApiResponse.response_bad_request(self, message=MESSAGES["all_fields_should_not_empty"])

        question = req_data.get("question")
        answer = req_data.get("answer")
        topic = req_data.get("topic")
        
        required_field = ["question","answer","topic"]
        if required_field := get_required_fields(required_field, req_data):
            return ApiResponse.response_bad_request(self, message=required_field)

        if error_message := validate_empty_strings({"question":question, "answer":answer}, req_data):
            return ApiResponse.response_bad_request(self, message=error_message)

        if topic not in TOPICS:
            return ApiResponse.response_bad_request(self, message="Invalid topic.")

        if self.model_class.filter(question__iexact=question, topic=topic).exists():
            return ApiResponse.response_bad_request(self, message="Faq already exists.")

        """ validate serializer """
        _, error = create_or_update_serializer(self.serializer_class, req_data, sp1)
        if error:
            return ApiResponse.response_bad_request(self, message=error)

        """ success response """
        transaction.savepoint_commit(sp1)
        return ApiResponse.response_created(self, data=req_data, message=self.singular_name + MESSAGES["created"])

    @swagger_auto_schema_update
    @transaction.atomic()
    @is_super_user_or_mf_user
    def partial_update(self, request, *args, **kwargs):
        """
        :To update the existing record
        """
        sp1 = transaction.savepoint()

        """ capture data """
        req_data = request.data
        if not req_data:
            return ApiResponse.response_bad_request(self, message=MESSAGES["all_fields_should_not_empty"])
        
        get_id = self.kwargs.get("id")
        instance = self.get_object(get_id)
        if not instance:
            return ApiResponse.response_not_found(self, message=self.singular_name + MESSAGES['not_found'])
        
        question = req_data.get("question")
        answer = req_data.get("answer")
        topic = req_data.get("topic")
        
        if error_message := validate_empty_strings({"question":question, "answer":answer}, req_data):
            return ApiResponse.response_bad_request(self, message=error_message)

        if topic and topic not in TOPICS:
            return ApiResponse.response_bad_request(self, message="Invalid topic.")

        """ validate serializer """
        _, error = create_or_update_serializer(self.serializer_class, req_data, sp1, instance)
        if error:
            return ApiResponse.response_bad_request(self, message=error)

        """ success response """
        transaction.savepoint_commit(sp1)
        return ApiResponse.response_ok(self, data=req_data, message=self.singular_name + MESSAGES["updated"])

    @swagger_auto_schema_list
    @super_user_or_employer_job_seeker
    def list(self, request, *args, **kwargs):
        """
        :To get the all records
        """
        where_array = request.query_params

        sort_by = where_array.get("sort_by") if where_array.get("sort_by") else "id"

        sort_direction = where_array.get("sort_direction") if where_array.get("sort_direction") else "ascending"
        
        if sort_direction == "descending":
            sort_by = "-" + sort_by

        obj_list = []

        if where_array.get("id"):
            obj_list.append(("id", where_array.get("id")))

        if topic := where_array.get("topic"):
            topic = int(topic)
            if topic in TOPICS:
                obj_list.append(("topic", topic))
            else:
                return ApiResponse.response_bad_request(self, message="Invalid topic.")

        start_date = where_array.get("start_date")
        end_date = where_array.get("end_date")
        if start_date and end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            end_date = datetime.combine(end_date, datetime.max.time())
            obj_list.append(["created_at__range", [start_date, end_date]])

        elif start_date:
            obj_list.append(["created_at__gte", start_date])

        elif end_date:
            obj_list.append(["created_at__lte", end_date])

        q_list = [Q(x) for x in obj_list]
        if q_list:
            queryset = self.model_class.filter(reduce(operator.and_, q_list)).order_by(sort_by)
        else:
            queryset = self.model_class.order_by(sort_by)

        """Search for keyword"""
        if where_array.get("keyword"):
            queryset = queryset.filter(search_filter(self.search_fields, where_array.get("keyword")))

        resp_data = get_pagination_resp(queryset, request)

        if is_all_data:=request.query_params.get("is_all_data"):
            response_data = transform_list(self, resp_data.get("data"), is_all_data)
            
        else:
            response_data = transform_list(self, resp_data.get("data"))

        return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get("paginator"))

    @swagger_auto_schema_delete
    @is_super_user_or_mf_user
    def delete(self, request, *args, **kwargs):
        """
        :To delete the single record.
        """
        get_id = self.kwargs.get("id")

        """ get instance """
        instance = self.get_object(get_id)
        if not instance:
            return ApiResponse.response_not_found(self, message=self.singular_name + MESSAGES['not_found'])

        instance.delete()

        
        return ApiResponse.response_ok(self, message=self.singular_name + " deleted")

    @swagger_auto_schema_bulk_delete
    @is_super_user_or_mf_user
    def bulk_delete(self, request, *args, **kwargs):
        """
        :To delete the multiple record.
        """
        """ capture data """
        req_data = request.data
        
        ids = req_data.get("ids")
        if not ids or not isinstance(ids, list):
            return ApiResponse.response_bad_request(self, message="Please select " + self.singular_name.lower())

        """ get instance """
        queryset = self.model_class.filter(id__in=ids)
        if not queryset:
            return ApiResponse.response_not_found(self, message=self.singular_name + MESSAGES['not_found'])

        queryset.delete()

        
        return ApiResponse.response_ok(self, message=self.singular_name + " deleted.")

    ##Generate the response
    def transform_single(self, instance):
        resp_dict = dict()
        if instance:
            resp_dict['id'] = instance.id
            resp_dict['question'] = instance.question
            resp_dict['answer'] = instance.answer
            resp_dict['topic'] = instance.topic
            resp_dict['topic_name'] = instance.get_topic_display()
                
        return resp_dict

        # Generate the response
    def transform_single_with_to_dict(self, instance):
        resp_dict = {}
        resp_dict = Faq.to_dict(instance)
    
        return resp_dict 