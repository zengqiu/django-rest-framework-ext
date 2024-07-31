from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import ExportPermission


class ExportModelViewSet(viewsets.ModelViewSet):
    @action(methods=['get'], detail=False, url_name='export', permission_classes=[ExportPermission])
    def export(self, request, pk=None):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response(serializer.data)
