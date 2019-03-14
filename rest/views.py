""" REST views for the data API
"""
import json
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.components.data import api as data_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_main_app.rest.data.serializers import DataSerializer, DataWithTemplateInfoSerializer
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.boolean import to_bool
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.utils.file import get_file_http_response
from core_main_app.utils.pagination.rest_framework_paginator.pagination import StandardResultsSetPagination



class DataList(APIView):
    """ List all user Data, or create a new one.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        """ Get all user Data

        Url Parameters:

            template: template_id
            title: document_title

        Examples:

            ../data/
            ../data?template=[template_id]
            ../data?title=[document_title]
            ../data?template=[template_id]&title=[document_title]

        Args:

            request: HTTP request
			pk: WorkspaceId

        Returns:

            - code: 200
              content: List of data
            - code: 500
              content: Internal server error
        """
		
	try:
            # Get object
            workspace_object = workspace_api.get_by_id(pk)
            #data_object_list = data_api.get_all_by_user(request.user)
            data_object_list = data_api.get_all_by_workspace(workspace_object,request.user)
            #data_object_list = data_object_list.filter(workspace=pk)
            # Serialize object
            data_serializer = DataSerializer(data_object_list, many=True)

            # Return response
            return Response(data_serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)