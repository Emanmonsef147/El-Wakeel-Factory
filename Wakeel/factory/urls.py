from django.urls import path

from .views import dashboard, loginPage, logoutUser, client_list, client_view, client_create, client_update, \
    client_delete, employee_list, employee_view, employee_create, employee_update, employee_delete, job_list, job_view, \
    job_create, job_update, job_delete, proposal_list, proposal_view, proposal_create, proposal_update, proposal_delete, \
    contract_list, contract_view, contract_create, contract_update, contract_delete, project_list, project_view, \
    project_create, project_update, project_delete, task_list, task_view, task_update, task_delete, \
    document_list, document_view, document_create, document_update, document_delete, proposal_client_create, \
    proposal_contract_create, contract_project_create, task_project_create, document_task_create, \
    task_create
from django.contrib.auth import views as auth_views
# from .views import SalesSignUpView, ManagerSignUpView, SignUpView

urlpatterns = [
    path('', dashboard, name='dashboard'),

    # Login and Register
    # path('register/', views.registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),

    # Password
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

    # path('accounts/signup/', SignUpView.as_view(), name='signup'),
    # path('accounts/signup/sales/', SalesSignUpView.as_view(), name='sales_signup'),
    # path('accounts/signup/manager/', ManagerSignUpView.as_view(), name='manager_signup'),

    # users
    # path('users/list/', views.user_list, name='user_list'),
    # path('users/view/<int:id>/', views.user_view, name='user_view'),
    # path('users/create/', views.user_create, name='user_create'),
    # path('users/update/<int:id>/', views.user_update, name='user_update'),
    # path('users/delete/<int:id>/', views.user_delete, name='user_delete'),

    # Client 

    path('client/list/', client_list, name='client_list'),
    path('client/view/<int:id>/', client_view, name='client_view'),
    path('client/create/', client_create, name='client_create'),
    path('client/update/<int:id>/', client_update, name='client_update'),
    path('client/delete/<int:id>/', client_delete, name='client_delete'),

    # Employee
    path('employee/list/', employee_list, name='employee_list'),
    path('employee/view/<int:id>/', employee_view, name='employee_view'),
    path('employee/create/', employee_create, name='employee_create'),
    path('employee/update/<int:id>/', employee_update, name='employee_update'),
    path('employee/delete/<int:id>/', employee_delete, name='employee_delete'),

    # Job
    path('job/list/', job_list, name='job_list'),
    path('job/view/<int:id>/', job_view, name='job_view'),
    path('job/create/', job_create, name='job_create'),
    path('job/update/<int:id>/', job_update, name='job_update'),
    path('job/delete/<int:id>/', job_delete, name='job_delete'),

    # Proposal

    path('proposal/list/', proposal_list, name='proposal_list'),
    path('proposal/view/<int:id>/', proposal_view, name='proposal_view'),
    path('proposal/create/', proposal_create, name='proposal_create'),
    path('proposal/update/<int:id>/', proposal_update, name='proposal_update'),
    path('proposal/delete/<int:id>/', proposal_delete, name='proposal_delete'),
    # path('proposal/pdf_view/', views.proposal_pdf_view, name='proposal_pdf_view'),
    # path('proposal/excel_view/', views.proposal_excel_view, name='proposal_excel_view'),

    # Contract

    path('contract/list/', contract_list, name='contract_list'),
    path('contract/view/<int:id>/', contract_view, name='contract_view'),
    path('contract/create/', contract_create, name='contract_create'),
    path('contract/update/<int:id>/', contract_update, name='contract_update'),
    path('contract/delete/<int:id>/', contract_delete, name='contract_delete'),
    # path('contract/pdf_view/', views.contract_pdf_view, name='contract_pdf_view'),
    # path('contract/excel_view/', views.contract_excel_view, name='contract_excel_view'),

    # Project
    path('project/list/', project_list, name='project_list'),
    path('project/view/<int:id>/', project_view, name='project_view'),
    path('project/create/', project_create, name='project_create'),
    path('project/update/<int:id>/', project_update, name='project_update'),
    path('project/delete/<int:id>/', project_delete, name='project_delete'),
    # path('project/pdf_view/', views.project_pdf_view, name='project_pdf_view'),
    # path('project/excel_view/', views.project_excel_view, name='project_excel_view'),

    # Task
    path('task/list/', task_list, name='task_list'),
    path('task/view/<int:id>/', task_view, name='task_view'),
    path('task/create/', task_create, name='task_create'),
    path('task/update/<int:id>/', task_update, name='task_update'),
    path('task/delete/<int:id>/', task_delete, name='task_delete'),

    # path('task/create/', TaskAddView.as_view(), name="task_create"),

    # Document
    path('document/list/', document_list, name='document_list'),
    path('document/view/<int:id>/', document_view, name='document_view'),
    path('document/create/', document_create, name='document_create'),
    path('document/update/<int:id>/', document_update, name='document_update'),
    path('document/delete/<int:id>/', document_delete, name='document_delete'),

    # client, proposal, contract, project, task, document create instance
    path('client/proposal/<int:id>/', proposal_client_create, name='proposal_client_create'),
    path('contract/proposal/<int:id>/', proposal_contract_create, name='proposal_contract_create'),
    path('project/contract/<int:id>/', contract_project_create, name='contract_project_create'),
    path('project/task/<int:id>/', task_project_create, name='task_project_create'),
    path('task/document/<int:id>/', document_task_create, name='document_task_create'),

]
