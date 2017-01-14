from django.conf.urls import url
from rest_framework.authtoken import views as drf_views
from . import views


urlpatterns = [
  url(r'^login$', views.login),
  url(r'^base_data$', views.base_data),
  # url(r'^records$', views.records_list, name ='records_list'),
  url(r'^records$', views.RecordList.as_view(), name ='records_list'),
  url(r'^records/(?P<pk>[0-9]+)', views.RecordDetail.as_view(), name='records_detail'),
  url(r'^budgets$', views.BudgetList.as_view(), name='budgets_list'),
  url(r'^master_budgets$', views.MasterBudgetList.as_view(), name='master_budget_list')

]
