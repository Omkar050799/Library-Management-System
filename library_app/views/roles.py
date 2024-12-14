from simple_search import search_filter
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

""" utility """
from utility.response import ApiResponse
from utility.utils import (
    MultipleFieldPKModelMixin,
    CreateRetrieveUpdateViewSet,
    get_pagination_resp,
    transform_list,
)
from utility.constants import *

""" model imports """
from ..models import Roles

"""swagger"""
from ..swagger.roles_swagger import (
    swagger_auto_schema_list,
)


class RolesView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):

    authentication_classes = [ OAuth2Authentication ]
    model_class = Roles.objects

    search_fields = ["name"]

    @swagger_auto_schema_list
    def list(self, request, *args, **kwargs):
        """
        :To get the all records
        """
        # capture data
        sort_by = request.query_params.get("sort_by") if request.query_params.get("sort_by") else "id" 
        sort_direction = (
            request.query_params.get("sort_direction")
            if request.query_params.get("sort_direction")
            else "ascending"
        )
        if sort_direction == "descending":
            sort_by = "-" + sort_by

        where_array = request.query_params
        queryset = self.model_class.order_by(sort_by)

        """Search for keyword"""
        if where_array.get("keyword"):
            queryset = queryset.filter(search_filter(self.search_fields, where_array.get("keyword")))

        resp_data = get_pagination_resp(queryset, request)
        response_data = transform_list(self, resp_data.get("data"))

        return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get("paginator"))

    # Generate the response
    def transform_single(self, instance):
        resp_dict = dict()
        resp_dict["id"] = instance.id
        resp_dict["designation"] = instance.name
        return resp_dict