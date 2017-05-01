from django.conf.urls import url
from rest_framework.authtoken import views as drf_views
from . import views


urlpatterns = [
  url(r'^login$', views.login),
  url(r'^base_data$', views.base_data),
  url(r'^test$', views.test),
  url(r'^users', views.UserListCreateView.as_view(), name='users_list'),
  # url(r'^records$', views.records_list, name ='records_list'),
  url(r'^records$', views.RecordList.as_view(), name ='records_list'),
  url(r'^records/(?P<pk>[0-9]+)', views.RecordDetail.as_view(), name='records_detail'),
  url(r'^budgets$', views.BudgetList.as_view(), name='budgets_list'),
  url(r'^master_budgets$', views.MasterBudgetList.as_view(), name='master_budget_list'),
  url(r'^categories$', views.CategoryListCreateView.as_view(), name='category_list'),
  url(r'^summary$', views.summary, name='summary_view')

]
