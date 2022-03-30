from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.


# class Users(AbstractUser):
#     USER_TYPE_CHOICES = (
#         (1, 'admin'),
#         (2, 'sales'),
#         (3, 'manager'),
#     )
#     user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)
#     username = models.CharField(max_length=150, unique=True, null=True, blank=True)
#     password = models.CharField(max_length=100, null=True, blank=True)
#     is_sales = models.BooleanField(default=False)
#     is_manager = models.BooleanField(default=True)
# user_type = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class Client(models.Model):
    client_name = models.CharField(max_length=200, null=True, blank=True)
    client_personal_id = models.CharField(max_length=30, null=True, blank=True)
    client_home_tel = models.CharField(max_length=15, null=True, blank=True)
    client_office_tel = models.CharField(max_length=15, null=True, blank=True)
    client_mobile = models.CharField(max_length=25, null=True, blank=True)
    client_address = models.CharField(max_length=500, null=True, blank=True)
    client_province = models.CharField(max_length=200, null=True, blank=True)
    client_nghood = models.CharField(max_length=300, null=True, blank=True)
    client_pobox = models.CharField(max_length=300, null=True, blank=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    contact_id = models.CharField(max_length=30, null=True, blank=True)
    contact_mobile = models.CharField(max_length=25, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='create_client', null=True,
                                   blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='update_client', null=True,
                                   blank=True)
    created_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return self.client_name


class Job(models.Model):
    job = models.CharField(max_length=150, null=True, blank=True)
    job_description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.job


class Employee(models.Model):
    employee_job_id = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, )
    user_account_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, default=False)
    employee_name = models.CharField(max_length=150, null=True, blank=True)
    employee_pid = models.CharField(max_length=150, null=True, blank=True)
    employee_mobile = models.CharField(max_length=25, null=True, blank=True)
    employee_address = models.CharField(max_length=150, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='create_employee', null=True,
                                   blank=True)
    created_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='update_employee', null=True,
                                   blank=True)
    update_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.employee_name


class Proposal(models.Model):
    PROPOSAL_STATUS = (
        ('Delivered', 'Delivered'),
        ('Executed', 'Executed'),
        ('Pricing', 'Pricing')
    )
    proposal_id = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    proposal_status = models.CharField(max_length=255, choices=PROPOSAL_STATUS, null=True, blank=True)
    proposal_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    proposal_amount = models.FloatField(null=True, blank=True)
    item_type = models.CharField(max_length=255, null=True, blank=True)
    no_items = models.CharField(max_length=255, null=True, blank=True)
    item_details = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to="images/", null=True, blank=True)
    es_width = models.FloatField(null=True, blank=True)
    es_height = models.FloatField(null=True, blank=True)
    fn_width = models.FloatField(null=True, blank=True)
    fn_height = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='create_proposal', null=True,
                                   blank=True)
    created_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='update_proposal', null=True,
                                   blank=True)
    updated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)


class Contract(models.Model):
    CONTRACT_STATUS = (
        ('A', 'A'),
        ('B', 'B'),
    )
    contract_id = models.CharField(max_length=255, null=True, blank=True)
    # client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='proposal_contract',
                                 null=True, blank=True)
    contract_status = models.CharField(max_length=255, choices=CONTRACT_STATUS, null=True, blank=True)
    item_type = models.CharField(max_length=255, null=True, blank=True)
    no_items = models.CharField(max_length=255, null=True, blank=True)
    item_details = models.CharField(max_length=255, null=True, blank=True)
    fn_width = models.FloatField(null=True, blank=True)
    fn_height = models.FloatField(null=True, blank=True)
    img = models.ImageField(upload_to="images/", null=True, blank=True)
    contract_start_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    contract_delivery_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='create_contract', null=True,
                                   blank=True)
    created_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='update_contract', null=True,
                                   blank=True)
    updated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.contract_id


class Project(models.Model):
    PROJECT_STATUS = (
        ('A', 'A'),
        ('B', 'B'),
    )

    project_id = models.CharField(max_length=255, null=True, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_project', null=True,blank=True)        
    project_name = models.CharField(max_length=255, null=True, blank=True)
    project_status = models.CharField(
        max_length=255, choices=PROJECT_STATUS, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    project_plan_delivery_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    project_delivery_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    contract_start_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    contract_delivery_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    sales = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='employee_sales')
    project_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='pj_manager_employee')
    item_type = models.CharField(max_length=255, null=True, blank=True)
    no_items = models.CharField(max_length=255, null=True, blank=True)
    item_details = models.CharField(max_length=255, null=True, blank=True)
    fn_width = models.FloatField(null=True, blank=True)
    fn_height = models.FloatField(null=True, blank=True)
    img = models.ImageField(upload_to="images/", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='create_project', null=True,
                                   blank=True)
    created_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='update_project', null=True,
                                   blank=True)
    updated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    TASK_STATUS = (
        ('A', 'A'),
        ('B', 'B'),
    )

    task_id = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='task_project')

    sales_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='task_sales_employee')
    project_manager_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='task_pj_manager_employee')
    task_name = models.CharField(max_length=255, null=True, blank=True)
    item_type = models.CharField(max_length=255, null=True, blank=True)
    no_items = models.CharField(max_length=255, null=True, blank=True)
    item_details = models.CharField(max_length=255, null=True, blank=True)
    fn_width = models.FloatField(null=True, blank=True)
    fn_height = models.FloatField(null=True, blank=True)
    task_delivery_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    task_status = models.CharField(max_length=255, choices=TASK_STATUS, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    img = models.ImageField(upload_to="images/", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='create_task', null=True,
                                   blank=True)
    created_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.task_id


class Document(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    document_id = models.CharField(max_length=255, null=True, blank=True)
    document_name = models.CharField(max_length=255, null=True, blank=True)
    document_type = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='create_document', null=True,
                                   blank=True)
    create_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='update_document', null=True,
                                   blank=True)

    def __str__(self):
        return self.document_id
