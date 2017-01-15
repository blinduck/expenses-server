from django.shortcuts import render, HttpResponse, get_object_or_404
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models import *
from .permissions import IsOwner
from django.contrib.auth import authenticate
from datetime import datetime


# Create your views here.

def test(request):
  return HttpResponse('testing')

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
  username = request.data['username']
  password = request.data['password']

  if username and password:
    user = authenticate(username=username, password=password)
    if user:
      ser = UserSerializer(user)
      return Response(ser.data, status.HTTP_200_OK)
  return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def base_data(request):
  masterbudgets = MasterBudget.objects.filter(user=request.user)
  categories = Category.objects.filter(household=request.user.household)

  data = {
    'masterbudgets': MasterBudgetSerializer(masterbudgets, many=True).data,
    'categories': CategorySerializer(categories, many=True).data,
    'record_type_choices': [x[0] for x in Record.TYPE_CHOICES]
  }
  return Response(data)

class RecordList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
  permission_classes = [IsAuthenticated]
  serializer_class = RecordSerializer
  def get_queryset(self):
    startDate = datetime.utcfromtimestamp(float(self.request.query_params['startDate']))
    endDate = datetime.utcfromtimestamp(float(self.request.query_params['endDate']))
    expenseType = self.request.query_params['expenseType']
    querySet =  Record.objects.filter(
      user=self.request.user,
      time__range=(startDate, endDate)
    )
    if expenseType is not None and expenseType in ['Personal', 'Household']:
      querySet = querySet.filter(type = expenseType)
    querySet = querySet.order_by('-time')
    return querySet

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

class RecordDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
  # todo implement proper object level permissions for the records.
  queryset = Record.objects.all()
  serializer_class = RecordSerializer
  permission_classes = [IsAuthenticated, IsOwner]

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

class BudgetList(generics.GenericAPIView, mixins.ListModelMixin):
  permission_classes = [IsAuthenticated]
  serializer_class = BudgetSerializer

  def get_queryset(self):
    return Budget.active_budgets(self.request.user)

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

class MasterBudgetList(generics.GenericAPIView, mixins.ListModelMixin):
  permission_classes = [IsAuthenticated]
  serializer_class = MasterBudgetWithCurrentBudgetSerializer


  def get_queryset(self):
    return MasterBudget.objects.filter(household=self.request.user.household)

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

