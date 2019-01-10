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
from django.db import transaction
from django.db.models import Q
from .sheet_data import get_data, write_to_row
import logging

logger = logging.getLogger('django')

# Create your views here.

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
    ## data that is required when addding a record
    ## user needs to select from the available budgets, categories and record_types

    masterbudgets = MasterBudget.objects.filter(
        household=request.user.household
    ).exclude(
        # exclude personal budgets that don't belong to the user
        Q(expense_type='Personal') & ~Q(user=request.user)
    )
    user = request.user
    categories = Category.objects.filter(household=user.household) \
        .filter(Q(cat_type="Household") | Q(user=user))

    data = {
        'masterbudgets': MasterBudgetSerializer(masterbudgets, many=True).data,
        'categories': CategorySerializer(categories, many=True).data,
        'record_type_choices': [x[0] for x in Record.TYPE_CHOICES]
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary(request):
    user = request.user
    current_date = datetime.now()
    year = int(request.query_params.get('year', current_date.year))
    month = int(request.query_params.get('month', current_date.month))
    type = request.query_params.get('type', 'all')
    data = {
        'category_summary': Record.monthly_category_summary(
            user, year, month, type
        ),
        'type_summary': Record.type_summary(user, year, month)
    }
    return Response(data=data)


class RecordList(generics.GenericAPIView,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return RecordListSerializer
        elif self.request.method == 'POST':
            return RecordCreateSerializer

    def get_queryset(self):
        user = self.request.user
        household = user.household
        startDate = datetime.utcfromtimestamp(
            float(self.request.query_params['startDate']))
        endDate = datetime.utcfromtimestamp(
            float(self.request.query_params['endDate']))
        expenseType = self.request.query_params['expenseType']

        querySet = Record.objects.filter(
            household=household,
            time__range=(startDate, endDate)
        )
        # any household expense, or a user's personal expenses
        querySet = querySet.filter(
            Q(type='Household') | Q(user=user)
        )

        if expenseType is not None and expenseType in ['Personal', 'Household']:
            querySet = querySet.filter(type=expenseType)
        querySet = querySet.order_by('-time')
        return querySet

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BudgetsWithRecords(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetWithRecordsSeralizer

    def get_queryset(self):
        self.mb = MasterBudget.objects.get(id = self.request.query_params['mb_id'])
        return Budget.objects.filter(masterbudget=self.mb)

    def get(self, request, *args, **kwargs):
        response = super().list(request, args, **kwargs)
        response.data['budgetName'] = self.mb.name
        return response



class RecordDetail(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):

    # todo implement proper object level permissions for the records.

    queryset = Record.objects.all()
    serializer_class = RecordCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BudgetList(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.active_budgets(self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MasterBudgetList(generics.GenericAPIView,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = MasterBudgetWithCurrentBudgetSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user, household=user.household)

    def get_queryset(self):
        return MasterBudget.objects.filter(
            household=self.request.user.household
        ).exclude(
            Q(expense_type='Personal') & ~Q(user=self.request.user)
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserListCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryListCreateView(generics.GenericAPIView,
                             mixins.CreateModelMixin,
                             mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(household=user.household)\
            .filter(Q(cat_type="Household") | Q(user=user))

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(household=user.household, user=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryDetailView(generics.GenericAPIView,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin
                         ):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TimJean(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    permission_classes = []
    authentication_classes = []

    def get_serializer(self, *args, **kwargs):
        return None

    def get(self, request, *args, **kwargs):
        data =  get_data()
        return Response(data)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        index = data.get('perms').get('index')
        data = [
            "Yes",
            data.get('attendingChurch', ""),
            data.get('churchTotal', ""),
            data.get('attendingDinner', ""),
            data.get('dietaryRestriction', ""),
            data.get('dinnerTotalComing', "")
        ]
        resp = write_to_row(index, data)
        return Response()


class ChatBot(generics.GenericAPIView, mixins.CreateModelMixin):
    permission_classes = []
    authentication_classes = []



    def post(self, request, *args, **kwargs):
        data = request.data
        logger.info(data)
        return Response({"test": "test"})

