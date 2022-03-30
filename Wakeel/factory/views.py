from base64 import urlsafe_b64encode
from collections import UserString
from email import quoprimime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

from .decorators import allowed_users, unauthenticated_user
from .forms import *
from .models import Client, Project, Proposal, Employee, Job, Task, Document


# from .decorators import unauthenticated_user, admin_only, allowed_users


# Create your views here.

def dashboard(request):
    return render(request, 'dashboard.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = UserString.objects.filter(
                quoprimime(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_b64encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


#
# class SignUpView(TemplateView):
#     template_name = 'registration/signup.html'

#
# class SalesSignUpView(CreateView):
#     model = User
#     form_class = SalesSignUpForm
#     template_name = 'registration/signup_form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'sales'
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')
#
#
# class ManagerSignUpView(CreateView):
#     model = User
#     form_class = ManagerSignUpForm
#     template_name = 'registration/signup_form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'manager'
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')

#
# @unauthenticated_user
# def registerPage(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#
#             messages.success(request, 'Account was created for ' + username)
#
#             return redirect('/login')
#
#     context = {'form': form}
#     return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/login')


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def user_list(request):
#     context = {'user_list': Users.objects.all()}
#     return render(request, "users/user_list.html", context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def user_view(request, id):
#     context = {'user_view': Users.objects.get(pk=id)}
#     return render(request, "users/user_view.html", context)


# @login_required(login_url='login')
# @admin_only
# def user_create(request, id=0):
#     if request.method == "GET":
#         if id == 0:
#             form = UserForm()
#         else:
#             user = get_object_or_404(Users, pk=id)
#             form = UserForm(instance=user)
#         return render(request, "users/user_create.html", {'form': form})
#     else:
#         if request.method == "POST":
#             if id == 0:
#                 form = UserForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         return redirect('/users/list')


# @login_required(login_url='login')
# @admin_only
# def user_update(request, id):
#     user = get_object_or_404(Users, pk=id)
#     form = UserForm(instance=user)
#
#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('/users/list')
#
#     context = {'form': form}
#     return render(request, 'users/user_update.html', context)


# @login_required(login_url='login')
# @admin_only
# def user_delete(request, id):
#     user = get_object_or_404(Users, pk=id)
#     user.delete()
#     return render(request, 'users/user_delete.html')


# Client
@login_required(login_url='login')
def client_list(request):
    context = {'client_list': Client.objects.all()}
    return render(request, "clients/client_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def client_view(request, id):
    proposal_views = Proposal.objects.get(pk=id)
    context = {'client_view': get_object_or_404(Client, pk=id), 'proposal_views': proposal_views}
    return render(request, "clients/client_view.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def client_create(request, id=0):
    if 'client_name' in request.POST and 'client_personal_id' in request.POST and 'client_home_tel' in request.POST and \
            'client_office_tel' in request.POST and 'client_mobile' in request.POST and 'client_address' in request.POST and \
            'client_province' in request.POST and 'client_nghood' in request.POST and 'client_pobox' in request.POST and \
            'contact_name' in request.POST and 'contact_id' in request.POST and 'contact_mobile' in request.POST and \
            'updated_date' in request.POST and 'created_date' in request.POST:

        client_name = request.POST['client_name']
        client_personal_id = request.POST['client_personal_id']
        client_home_tel = request.POST['client_home_tel']
        client_office_tel = request.POST['client_office_tel']
        client_mobile = request.POST['client_mobile']
        client_address = request.POST['client_address']
        client_province = request.POST['client_province']
        client_nghood = request.POST['client_nghood']
        client_pobox = request.POST['client_pobox']
        contact_name = request.POST['contact_name']
        contact_id = request.POST['contact_id']
        contact_mobile = request.POST['contact_mobile']
        created_date = request.POST['created_date']
        updated_date = request.POST['updated_date']

    else:
        client_name = False
        client_personal_id = False
        client_home_tel = False
        client_office_tel = False
        client_mobile = False
        client_address = False
        client_province = False
        client_nghood = False
        client_pobox = False
        contact_name = False
        contact_id = False
        contact_mobile = False
        created_date = False
        updated_date = False

    if request.method == "GET":
        if id == 0:
            form = ClientForm()
        else:
            client = get_object_or_404(Client, pk=id)
            form = ClientForm(instance=client)
        return render(request, "clients/client_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/client/list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def client_update(request, id):
    client = get_object_or_404(Client, pk=id)
    form = ClientForm(instance=client)

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()

            return redirect('/client/list')

    return render(request, 'clients/client_update.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def client_delete(request, id):
    client = get_object_or_404(Client, pk=id)
    client.delete()
    return redirect('/client/list')


# Employee

@login_required(login_url='login')
def employee_list(request):
    context = {'employee_list': Employee.objects.all()}
    return render(request, "employees/employee_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def employee_view(request, id):
    context = {'employee_view': get_object_or_404(Employee, pk=id)}
    return render(request, "employees/employee_view.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def employee_create(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = EmployeeForm()
        else:
            employee = get_object_or_404(Employee, pk=id)
            form = EmployeeForm(instance=employee)
        return render(request, "employees/employee_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/employee/list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def employee_update(request, id):
    employees = get_object_or_404(Employee, pk=id)
    form = EmployeeForm(instance=employees)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employees)
        if form.is_valid():
            form.save()
            return redirect('/employee/list')
    return render(request, 'employees/employee_update.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def employee_delete(request, id):
    employee = get_object_or_404(Employee, pk=id)
    employee.delete()
    return redirect('/employee/list')


# Job
@login_required(login_url='login')
def job_list(request):
    context = {'job_list': Job.objects.all()}
    return render(request, "jobs/job_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def job_view(request, id):
    context = {'job_view': get_object_or_404(Job, pk=id)}
    return render(request, "jobs/job_view.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def job_create(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = JobForm()
        else:
            job = get_object_or_404(Job, pk=id)
            form = JobForm(instance=job)
        return render(request, "jobs/job_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/job/list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def job_update(request, id):
    job = get_object_or_404(Job, pk=id)
    form = JobForm(instance=job)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect('/job/list')

    return render(request, 'jobs/job_update.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def job_delete(request, id):
    job = get_object_or_404(Job, pk=id)
    job.delete()
    return redirect('/job/list')


# Proposal
@login_required(login_url='login')
def proposal_list(request):
    context = {'proposal_list': Proposal.objects.all()}
    return render(request, "proposal/proposal_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def proposal_view(request, id):
    client_views = Client.objects.get(pk=id)
    proposal_view = get_object_or_404(Proposal, pk=id)
    context = {'proposal_view': proposal_view, 'client_views': client_views}
    return render(request, "proposal/proposal_view.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def proposal_create(request, id=0):
    if 'created_date' in request.POST and 'updated_date' in request.POST:
        created_date = request.POST['created_date']
        updated_date = request.POST['updated_date']

    else:
        created_date = False
        updated_date = False
    if request.method == "GET":
        if id == 0:
            form = ProposalForm()
        else:
            proposal = get_object_or_404(Proposal, pk=id)
            form = ProposalForm(instance=proposal)
        return render(request, "proposal/proposal_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = ProposalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/proposal/list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def proposal_update(request, id):
    proposal = get_object_or_404(Proposal, pk=id)
    form = ProposalForm(instance=proposal)

    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect('/proposal/list')

    return render(request, 'proposal/proposal_update.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def proposal_delete(request, id):
    proposal = get_object_or_404(Proposal, pk=id)
    proposal.delete()
    return redirect('/proposal/list')


# def proposal_pdf_view(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=Proposal' + \
#                                       str(datetime.datetime.now()) + '.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'

#     proposal_pdf = Proposal.objects.filter(proposal_id=request.user)

#     p = proposal_pdf.aggregate(Sum('proposal_amount'))

#     html_string = render_to_string('proposal/proposal_output.html',
#                                    {'proposal': proposal_pdf, 'total': p['proposal_amount__sum']})
#     html = HTML(string=html_string)

#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())

#         return response


# def proposal_excel_view(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename=Proposal' + \
#                                       str(datetime.datetime.now()) + '.xls'
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Proposal')
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['Id', 'proposal id', 'contract status', 'item type']

#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()

#     rows = Proposal.objects.filter(proposal_id=request.user).values_list('proposal_id', 'proposal_amount',
#                                                                          'proposal_status', 'item_type')

#     for row in rows:
#         row_num += 1

#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, str(row[col_num]), font_style)

#     wb.save(response)
#     return response

# Contract
@login_required(login_url='login')
def contract_list(request):
    context = {'contract_list': Contract.objects.all()}
    return render(request, "contract/contract_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def contract_view(request, id):
    context = {'contract_view': get_object_or_404(Contract, pk=id)}
    return render(request, "contract/contract_view.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def contract_create(request, id=0):
    if 'created_date' in request.POST and 'updated_date' in request.POST and 'contract_start_date' in request.POST \
            and 'contract_delivery_date' in request.POST:
        created_date = request.POST['created_date']
        updated_date = request.POST['updated_date']
        contract_start_date = request.POST['contract_start_date']
        contract_delivery_date = request.POST['contract_delivery_date']

    else:
        created_date = False
        updated_date = False
        contract_start_date = False
        contract_delivery_date = False

    if request.method == "GET":
        if id == 0:
            form = ContractForm()
        else:
            contract = get_object_or_404(Contract, pk=id)
            form = ContractForm(instance=contract)
        return render(request, "contract/contract_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/contract/list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def contract_update(request, id):
    contract = get_object_or_404(Contract, pk=id)
    form = ContractForm(instance=contract)

    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            form.save()
            return redirect('/contract/list')

    return render(request, 'contract/contract_update.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def contract_delete(request, id):
    contract = get_object_or_404(Contract, pk=id)
    contract.delete()
    return redirect('/contract/list')


# def contract_pdf_view(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=Contract' + \
#                                       str(datetime.datetime.now()) + '.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'

#     contract_pdf = Contract.objects.filter(contract_id=request.user)

#     # c = contract_pdf.aggregate(Sum('contract_amount'))

#     html_string = render_to_string('contract/contract_output.html',
#                                    {'contract': contract_pdf, 'total': 0})
#     html = HTML(string=html_string)

#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())

#         return response


# def contract_excel_view(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename=Contract' + \
#                                       str(datetime.datetime.now()) + '.xls'
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Contract')
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['Id', 'contract id', 'contract status', 'item type']

#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()

#     rows = Contract.objects.filter(contract_id=request.user).values_list('contract_id',
#                                                                          'contract_status', 'item_type')

#     for row in rows:
#         row_num += 1

#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, str(row[col_num]), font_style)

#     wb.save(response)
#     return response

# Project
@login_required(login_url='login')
def project_list(request):
    context = {'project_list': Project.objects.all()}
    return render(request, "project/project_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def project_view(request, id):
    project_view = get_object_or_404(Project, pk=id)
    # c = project_view.contract
    # print(c)
    # p = c.proposal
    # cl = p.client

    task_view = Task.objects.filter(Q(project__id=project_view.id))

    client_view = get_object_or_404(Client, pk=id)
    context = {'project_view': project_view, 'task_view': task_view,
               'client_view': client_view}
    return render(request, "project/project_view.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def project_create(request, id=0):
    if 'created_date' in request.POST and 'updated_date' in request.POST and 'end_date' in request.POST and \
            'project_plan_delivery_date' in request.POST and 'project_delivery_date' in request.POST:
        created_date = request.POST['created_date']
        updated_date = request.POST['updated_date']
        end_date = request.POST['end_date']
        project_plan_delivery_date = request.POST['project_plan_delivery_date']
        project_delivery_date = request.POST['project_delivery_date']

    else:
        created_date = False
        updated_date = False
        end_date = False
        project_plan_delivery_date = False
        project_delivery_date = False

    if request.method == "GET":
        if id == 0:
            form = ProjectForm()
        else:
            project = get_object_or_404(Project, pk=id)
            form = ProjectForm(instance=project)
        return render(request, "project/project_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/project/list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def project_update(request, id):
    project = get_object_or_404(Project, pk=id)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('/project/list')

    return render(request, 'project/project_update.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def project_delete(request, id):
    project = get_object_or_404(Project, pk=id)
    project.delete()
    return redirect('/project/list')


# def project_pdf_view(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=Project' + \
#                                       str(datetime.datetime.now()) + '.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'

#     project_pdf = Project.objects.filter(project_id=request.user)

#     # pj = project_pdf.aggregate(Sum('project_name'))

#     html_string = render_to_string('project/project_output.html',
#                                    {'project': project_pdf, 'total': 0})
#     html = HTML(string=html_string)

#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())

#         return response


# def project_excel_view(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename=Project' + \
#                                       str(datetime.datetime.now()) + '.xls'
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Project')
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['Id', 'project id', 'project name', 'project status']

#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()

#     rows = Project.objects.filter(project_name=request.user).values_list('project_id',
#                                                                          'project_name', 'project_status')

#     for row in rows:
#         row_num += 1

#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, str(row[col_num]), font_style)

#     wb.save(response)
#     return response

# Task
@login_required(login_url='login')
def task_list(request):
    task_list = Task.objects.all()
    context = {'task_list': task_list}
    return render(request, "task/task_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def task_view(request, id):
    context = {'task_view': get_object_or_404(Task, pk=id)}
    return render(request, "task/task_view.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def task_create(request, id=0):
    if 'created_date' in request.POST and 'task_delivery_date' in request.POST and \
            'end_date' in request.POST:

        created_date = request.POST['created_date']
        task_delivery_date = request.POST['task_delivery_date']
        end_date = request.POST['end_date']


    else:

        created_date = False
        task_delivery_date = False
        end_date = False

    if request.method == "GET":
        if id == 0:
            # TaskFormset = formset_factory(TaskForm,max_num=10,extra=1)
            formset = TaskFormSet(queryset=Task.objects.none())
        else:
            task = get_object_or_404(Task, pk=id)
            formset = TaskFormSet(queryset=Task.objects.none())
        return render(request, "task/task_create.html", {'task_formset': formset})
    else:
        if request.method == "POST":
            if id == 0:
                formset = TaskFormSet(request.POST, request.FILES)

        if formset.is_valid():
            formset.save()

        return redirect('/task/list')


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['projectmanager', 'admin'])
# class TaskAddView(TemplateView):
#     template_name = "task/task_create.html"
#
#     def get(self, *args, **kwargs):
#         # Create an instance of the formset
#         formset = TaskFormSet(queryset=Task.objects.none())
#         return self.render_to_response({'task_formset': formset})
#
#     def post(self, *args, **kwargs):
#         formset = TaskFormSet(data=self.request.POST)
#
#         # Check if submitted forms are valid
#         if formset.is_valid():
#             formset.save()
#             return redirect(reverse_lazy("task_list"))
#
#         return self.render_to_response({'task_formset': formset})


@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def task_update(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/task/list')

    return render(request, 'task/task_update.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('/task/list')


# Document
@login_required(login_url='login')
def document_list(request):
    context = {'document_list': Document.objects.all()}
    return render(request, "document/document_list.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def document_view(request, id):
    document_data_view = get_object_or_404(Document, pk=id)
    client_data_view = get_object_or_404(Client, pk=id)
    proposal_data_view = get_object_or_404(Proposal, pk=id)
    contract_data_view = get_object_or_404(Contract, pk=id)
    project_data_view = get_object_or_404(Project, pk=id)
    task_data_view = get_object_or_404(Task, pk=id)
    context = {'document_data_view': document_data_view, 'client_data_view': client_data_view,
               'proposal_data_view': proposal_data_view, 'contract_data_view': contract_data_view,
               'project_data_view': project_data_view, 'task_data_view': task_data_view
               }
    return render(request, "document/document_view.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def document_create(request, id=0):
    if 'created_date' in request.POST and 'updated_date' in request.POST:
        created_date = request.POST['created_date']
        updated_date = request.POST['updated_date']

    else:
        created_date = False
        updated_date = False
    if request.method == "GET":
        if id == 0:
            form = DocumentForm()
        else:
            document = get_object_or_404(Document, pk=id)
            form = DocumentForm(instance=document)
        return render(request, "document/document_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/document/list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def document_update(request, id):
    document = get_object_or_404(Document, pk=id)
    form = DocumentForm(instance=document)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('/document/list')

    return render(request, 'document/document_update.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def document_delete(request, id):
    document = get_object_or_404(Document, pk=id)
    document.delete()
    return redirect('/document/list')


# client proposal create
@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def proposal_client_create(request, id):
    client = Client.objects.get(pk=id)
    form = ProposalForm(instance=client)
    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES,
                            initial={'client': client})
        if form.is_valid():
            client = Client.objects.get(pk=id)
            obj = form.save(commit=False)
            obj.client = client
            obj.save()
            return redirect('/proposal/list')
    context = {'form': form, 'client': client}
    return render(request, 'proposal/proposal_create.html', context)


# proposal contract create
@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'admin'])
def proposal_contract_create(request, id):
    contract_data = Proposal.objects.get(id=id)
    client_to_join = contract_data.client
    form = ContractForm(instance=contract_data)

    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, initial={'contract_data': contract_data})
        if form.is_valid():
            proposal = Proposal.objects.get(pk=id)
            obj = form.save(commit=False)
            obj.proposal = proposal
            obj.save()

        return redirect('/contract/list')
    context = {'form': form, 'contract_data': contract_data, 'client': client_to_join}
    return render(request, 'contract/contract_create.html', context)


# contract project create
@login_required(login_url='login')
@allowed_users(allowed_roles=['sales', 'projectmanager', 'admin'])
def contract_project_create(request, id):
    contract_project_data = Contract.objects.get(id=id)
    proposal_to_join = contract_project_data.proposal
    client_to_join = contract_project_data.proposal.client
    form = ProjectForm(instance=contract_project_data)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES,
                           initial={'contract_project_data': contract_project_data})
        if form.is_valid():
            contract = Contract.objects.get(pk=id)
            obj = form.save(commit=False)
            obj.contract = contract
            obj.save()

            return redirect('/project/list')
    context = {'form': form, 'contract_project_data': contract_project_data, 'proposal_to_join': proposal_to_join,
               'client_to_join': client_to_join}
    return render(request, 'project/project_create.html', context)


# project task create
@login_required(login_url='login')
@allowed_users(allowed_roles=['projectmanager', 'admin'])
def task_project_create(request, id):
    project_data = Project.objects.get(id=id)
    contract_to_join = project_data.contract
    proposal_to_join = contract_to_join.proposal
    client_to_join = contract_to_join.proposal.client
    initial = [{'project_data': project_data}]  # for q in project_data
    # TaskFormSet = modelformset_factory(
    #     Task, exclude=("sales_id", "project_manager_id"), extra=initial, form=TaskForm)
    formset = TaskFormSet(queryset=Task.objects.none(), initial=initial)  # initial=initial, extra=len(initial)

    if request.method == 'POST':
        print(request.POST)
        formset = TaskFormSet(request.POST or None, request.FILES)
        if formset.is_valid():
            print(formset.is_valid())
            project = Project.objects.get(id=id)
            obj = formset.save(commit=False)
            for member in obj:
                member.project = project
                member.save()

            # pj = formset.save(commit=False)
            # for member in pj:
            #     member.project = project
            #     member.save()
            # formset.save()
            # project = Project.objects.get(pk=id)
            # obj.project = project
            # obj.save()

            return redirect('/task/list')
    context = {'task_formset': formset, 'project_data': project_data, 'contract_to_join': contract_to_join,
               'proposal_to_join': proposal_to_join, 'client_to_join': client_to_join}
    return render(request, 'task/task_create.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['projectmanager', 'admin'])
def document_task_create(request, id):
    task_data = Task.objects.get(id=id)
    project_to_join = task_data.project
    contract_to_join = project_to_join.contract
    proposal_to_join = contract_to_join.proposal
    client_to_join = proposal_to_join.client
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES,
                            initial={'task_data': task_data})
        if form.is_valid():
            task = Task.objects.get(pk=id)
            obj = form.save(commit=False)
            obj.task = task
            obj.save()

            return redirect('/document/list')
    context = {'form': form, 'task_data': task_data, 'project_to_join': project_to_join,
               'contract_to_join': contract_to_join, 'proposal_to_join': proposal_to_join,
               'client_to_join': client_to_join}
    return render(request, 'document/document_create.html', context)
