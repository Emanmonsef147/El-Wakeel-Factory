from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.forms import modelformset_factory
from django.utils.translation import gettext_lazy as _

from .models import *


# User = get_user_model()


# class SalesSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Users
#
#     @transaction.atomic
#     def save(self):
#         User = get_user_model()
#         user = super().save(commit=False)
#         user.is_sales = True
#         user.save()
#         sales = Employee.objects.create(user_account_id=user)
#         return user

# class ManagerSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Users
#
#     def save(self, commit=True):
#         # User = get_user_model()
#         user = super().save(commit=False)
#         user.is_manager = True
#         if commit:
#             user.save()
#         return user


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = ['user_type', 'user_email',
#                   'user_password', 're_type_password', 'username']
#
#     labels = {
#         'user_type': 'User Type',
#         'user_email': 'User Email',
#         'user_password': 'User password',
#         're_type_password': 'Re-Type Password',
#         'username': 'User Name',
#
#     }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_job_id', 'user_account_id', 'employee_name', 'employee_pid', 'employee_mobile',
                  'employee_address']

    labels = {
        'employee_job_id': 'Employee Job-ID',
        'user_account_id': 'User Account-ID',
        'employee_name': 'Employee Name',
        'employee_pid': 'Employee Pid',
        'employee_mobile': 'Employee Mobile',
        'employee_address': 'Employee Address',
    }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job', 'job_description']

    labels = {'job': 'Job',
              'job_description': 'Job description'
              }


class ClientForm(forms.ModelForm):
    client_personal_id = forms.CharField(validators=[validators.MinLengthValidator(4)],
                            widget=forms.TextInput(attrs={'class':'form-control form-rounded',
                                  "placeholder":"Enter Client Poposal ID"}))
    class Meta:
        model = Client
        fields = ['client_name', 'client_personal_id', 'client_home_tel', 'client_office_tel', 'client_mobile',
                  'client_address', 'client_province', 'client_nghood', 'client_pobox',
                  'contact_name', 'contact_id', 'contact_mobile',
                  'created_by', 'created_date',
                  'updated_by', 'updated_date']
        widgets = {
             'client_name' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Client Name"}),
             'client_home_tel' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Client Home Telephone"}),
             'client_office_tel' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Client Office Telephone"}),
             'client_mobile' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Client Mobile"}),
             'client_address' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Client Address"}),
            'client_province': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Client Province "}),
            'client_nghood': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Client NgHood "}),
            'client_pobox': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Client PoBox "}), 
             'contact_name': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Contact Name "}),                      
             'contact_id': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Contact ID "}), 
             'contact_mobile': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Contact Mobile "}),
             'created_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Created BY "}),
             'created_date': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Created Date "}),
            'updated_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Updated BY "}),
            
         }
    def clean_personal_id(self):
        client_personal_id = self.cleaned_data['client_personal_id']
        contact_id = self.cleaned_data['contact_id']

        if len(client_personal_id) < 4 and len(contact_id) < 4:
            raise forms.ValidationError("Id must be 8 numbers")
        return client_personal_id, contact_id

    labels = {
        'client_name': 'Client Name',
        'client_personal_id': 'ClientPersonal-ID',
        'client_home_tel': 'ClientHome-Tel',
        'client_office_tel': 'ClientOffice-Tel',
        'client_mobile': 'Client Mobile',
        'client_address': 'Client Address',
        'client_province': 'Client Province',
        'client_nghood': 'Client NGhood',
        'client_pobox': 'Client PoBox',
        'contact_name': 'Contact Name',
        'contact_id': 'Contact-PID',
        'contact_mobile': 'Contact Mobile',
        'created_by': 'Created By',
        'created_date': 'Created Date',
        'updated_by': 'Update By',
        'updated_date': 'Updated By'

    }


class ProposalForm(forms.ModelForm):
    proposal_id = forms.CharField(validators=[validators.MinLengthValidator(4)])

    class Meta:
        model = Proposal
        fields = ['proposal_id', 'proposal_status',
                  'proposal_amount', 'item_type', 'no_items',
                  'item_details',
                  'img', 'es_width', 'es_height', 'fn_width', 'fn_height',
                  'created_by', 'created_date', 'updated_by', 'updated_date']
       
            
        widgets = {
             'item_type' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Item Type"}),
             'no_items' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter No Items "}),
            'es_width': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter ES Width"}),
            'es_height': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Es Height "}), 
             'fn_width': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Final Width "}),                      
             'fn_height': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Final Height "}), 
             'created_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Created BY "}),
            'updated_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Updated BY "}),}
    def clean_proposal_id(self):
        proposal_id = self.cleaned_data['proposal_id']
        if len(proposal_id) < 4:
            raise forms.ValidationError("Id must be 4 numbers")
        return proposal_id

    labels = {
        'proposal_id': 'Proposal-ID',
        'proposal_status': 'Proposal Status',
        'proposal_amount': 'Proposal Amount',
        'item_type': 'Item Type',
        'no_items': 'No Items',
        'item_details': 'Item Details',
        'img': 'Image',
        'es_width': 'ES Width',
        'es_height': 'Es Height',
        'fn_width': 'Fn Width',
        'fn_height': 'Fn Height',
        'created_by': 'Created By',
        'created_date': 'Created Date',
        'updated_by': 'Update By',
        'updated_date': 'Updated By'

    }


class ContractForm(forms.ModelForm):
    contract_id = forms.CharField(validators=[validators.MinLengthValidator(4)],
                  widget=forms.TextInput(attrs={'class':'form-control form-rounded',
                                  "placeholder":"Enter Contract ID"}))

    class Meta:
        model = Contract
        fields = ['contract_id', 'contract_status',
                  'item_type', 'no_items',
                  'item_details', 'fn_width', 'fn_height',
                  'img', 'contract_start_date', 'contract_delivery_date',
                  'created_by', 'created_date', 'updated_by', 'updated_date']
        widgets = {
             'contract_status' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Contract Status "}),
             'item_type' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Item Type "}),
             'no_items' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter No Item "}),
             'item_details' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Item Details "}),
             'fn_width': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Final Width "}),                      
             'fn_height': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Final Height "}), 
             'img': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Image "}), 
             'created_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Created BY "}),
            'updated_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Updated BY "}),}
    def clean_contract_id(self):
        contract_id = self.cleaned_data['contract_id']
        if len(contract_id) < 4:
            raise forms.ValidationError("Id must be 4 numbers")
        return contract_id

    labels = {
        'contract_id': 'Contract ID',
        'contract_status': 'Contract Status',
        'item_type': 'Item Type',
        'no_items': 'No Items',
        'item_details': 'Item Details',
        'fn_width': 'Width',
        'fn_height': 'Height',
        'img': 'Image',
        'contract_start_date': 'Contract Start Date',
        'contract_delivery_date': 'Contract Delivery Date',
        'created_by': 'Created By',
        'created_date': 'Created Date',
        'updated_by': 'Update By',
        'updated_date': 'Updated By'
    }


class ProjectForm(forms.ModelForm):
    project_id = forms.CharField(validators=[validators.MinLengthValidator(4)],
     widget=forms.TextInput(attrs={'class':'form-control form-rounded',
                                  "placeholder":"Enter Project ID"}))

    class Meta:
        model = Project
        fields = ['project_id', 'project_status',
                  'project_name', 'sales', 'project_manager',
                  'item_type', 'no_items',
                  'item_details', 'fn_width', 'fn_height', 'img',
                  'end_date', 'project_plan_delivery_date', 'project_delivery_date',
                  'contract_start_date', 'contract_delivery_date', 'created_by', 'updated_by', 'created_date',
                  'updated_date']
        widgets = {
             'project_status' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Project Status "}),
             'project_name' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Project Name "}),
             'sales' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Sales "}),
             'project_manager': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Project Manager "}),
             'item_type' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Item Type "}),                      
             'no_items': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter No Items "}), 
             'item_details': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Item Details "}), 
            'fn_width': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Final Width "}),                      
             'fn_height': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Final Height "}), 
             'img': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Image "}), 
            'end_date': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter End Date "}), 
            'project_plan_delivery_date': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Project Plan Delivery Date "}), 
            'contract_start_date': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Contract Start Date"}),
            'project_delivery_date' :  forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Project Delivery Date"}),
            'contract_delivery_date' :  forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Contract Delivery Date"}),
             'created_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Created BY "}),
            'updated_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Updated BY "}),}
    def clean_project_id(self):
        project_id = self.cleaned_data['project_id']
        if len(project_id) < 4:
            raise forms.ValidationError("Id must be 4 numbers")
        return project_id

    labels = {
        'project_id': 'Project ID',
        'project_status': 'Project Status',
        'project_name': 'Project Name',
        'sales': 'Sales-ID',
        'project_manager': 'Project Manager-ID',
        'item_type': 'Item Type',
        'no_items': 'No Items',
        'item_details': 'Item Details',
        'fn_width': 'Width',
        'fn_height': 'Height',
        'end_date': 'End Date',
        'project_plan_delivery_date': 'Project Plan Delivery Date',
        'project_delivery_date': 'Project Delivery Date',
        'created_by': 'Created By',
        'created_date': 'Created Date',
        'updated_by': 'Update By',
        'updated_date': 'Updated By'
        # 'item_type': 'Item Type',
        # 'no_items': 'No Items',
        # 'item_details': 'Item Details',
        # 'fn_width': 'Width',
        # 'fn_height': 'Height',
        # 'img': 'Image',

    }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_id', 'document_name', 'document_type', 'created_by']
        widgets = {
             'document_id' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Document ID "}),
             'document_name' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Document Name "}),
             'document_type' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Document Type "}),
             'created_by': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Created BY "}),}
    labels = {
        'document_id': 'Document ID',
        'document_name': 'Document Name',
        'document_type': 'Document Type',
        'created_by': 'Created By',

    }


#
# class TaskForm(forms.ModelForm):
#     task_id = forms.CharField(validators=[validators.MinLengthValidator(4)])
#
#     class Meta:
#         model = Task
#         fields = ['task_id', 'sales_id', 'project_manager_id',
#                   'task_name', 'task_status', 'item_type', 'no_items',
#                   'end_date', 'img', 'task_delivery_date',
#                   'item_details', 'fn_width', 'fn_height', 'created_by', 'created_date',
#
#                   ]
#
#     def clean_task_id(self):
#         task_id = self.cleaned_data['task_id']
#         if len(task_id) < 4:
#             raise forms.ValidationError("Id must be 4 numbers")
#         return task_id

# labels = {
#     'task_id': 'Task ID',
#     'sales_id': 'Sales-ID',
#     'project_manager_id': 'Project Manager-ID',
#     'task_name': 'Task Name',
#     'task_status': 'Task Status',
#     'item_type': 'Item Type',
#     'no_items': 'No Items',
#     'item_details': 'Item Details',
#     'fn_width': 'Width',
#     'fn_height': 'Height',
#     'created_by': 'Created By',
#     'created_date': 'Created Date',
#     'task_delivery_date': 'Task Delivery Date',
#     'end_date': 'End Date',

# }

class TaskForm(forms.ModelForm):
    task_id = forms.CharField(validators=[validators.MinLengthValidator(4)],
     widget=forms.TextInput(attrs={'class':'form-control form-rounded',
                                  "placeholder":"Enter Task ID"}))

    class Meta:
        model = Task
        fields = ['task_id', 'sales_id', 'project_manager_id', 'project',
                  'task_name', 'task_status', 'item_type', 'no_items',
                  'end_date', 'img', 'task_delivery_date',
                  'item_details', 'fn_width', 'fn_height', 'created_by', 'created_date']
        widgets = {
             'sales_id' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Sales ID "}),
             'project_manager_id' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Project Manager ID "}),
             'project' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Project "}),
             'task_name': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Task Name "}),
             'task_status' : forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Task Status "}),                      
             'item_type': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Item Type "}), 
             'no_items': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter No Items "}),
            'end_date': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter End Date "}),
            'img': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Image "}), 
            'task_delivery_date': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Task Delivery Date "}), 
            'fn_width': forms.TextInput(attrs={'class': 'form-control form-rounded',
                                  "placeholder":"Enter Final Width "}),                      
             'fn_height': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Final Height "}), 
            'project_plan_delivery_date': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Project Plan Delivery Date "}), 
            'contract_start_date': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Contract Start Date"}),
            'project_delivery_date' :  forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Project Delivery Date"}),
            'contract_delivery_date' :  forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Contract Delivery Date"}),
            'item_details': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Item Details "}), 
             'created_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
            
                                  "placeholder":"Enter Created BY "}),
            'updated_by': forms.TextInput(attrs={'class': 'form-control form-rounded', 
                                  "placeholder":"Enter Updated BY "}),}

TaskFormSet = modelformset_factory(
    Task, exclude=("sales_id", "project_manager_id", "project"), extra=1)
