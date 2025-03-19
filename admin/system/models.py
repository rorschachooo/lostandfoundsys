from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers

# Create your models here.

# User Table
class User(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    username = models.CharField(max_length=255, db_index=True, verbose_name="username",help_text="username")
    password = models.CharField(max_length=255, null=True, blank=True,verbose_name="password", help_text="password")
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nick name", help_text="Nick name")
    email = models.EmailField(max_length=255, verbose_name="Mail", null=True, blank=True, help_text="Mail")
    address = models.CharField(max_length=255, verbose_name="address", null=True, blank=True, help_text="address")
    avatar = models.CharField(max_length=255, verbose_name="avatar", null=True, blank=True, help_text="avatar")
    uid = models.CharField(max_length=100, verbose_name="User unique id", null=True, blank=True, help_text="User unique id")
    role = models.CharField(max_length=255, verbose_name="Role", null=True, blank=True, help_text="Role")
    deleted = models.IntegerField(verbose_name="Logical deletion", null=True, blank=True, help_text="Logical deletion",default=0)
    score = models.IntegerField(verbose_name="integral", null=True, blank=True, help_text="integral",default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Creation time",verbose_name="Creation time")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="Modification time",verbose_name="Modification time")

    class Meta:
        db_table = "sys_user"
        verbose_name = "User Table"
        verbose_name_plural = verbose_name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Permissions Menu
class Permission(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, null=True, verbose_name="Permission Name", help_text="Permission Name")
    path = models.CharField(max_length=255, null=True, verbose_name="path", help_text="path")
    orders = models.IntegerField(verbose_name="Order", null=True, blank=True, help_text="Order")
    icon = models.CharField(max_length=255, null=True, verbose_name="icon", help_text="icon")
    page = models.CharField(max_length=255, null=True, verbose_name="Page Path", help_text="Page Path")
    auth = models.CharField(max_length=255, null=True, verbose_name="Permissions", help_text="Permissions")
    p_id = models.IntegerField(verbose_name="Parent ID", null=True, blank=True, help_text="Parent ID")
    deleted = models.IntegerField(verbose_name="Logical deletion", null=True, blank=True, help_text="Logical deletion",default=0)
    type = models.IntegerField(verbose_name="type", null=True, blank=True, help_text="type")
    hide = models.BooleanField(verbose_name="Is it hidden", null=True, blank=True, help_text="Is it hidden")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Creation time",verbose_name="Creation time")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="Modification time",verbose_name="Modification time")

    class Meta:
        db_table = "sys_permission"
        verbose_name = "Permissions"
        verbose_name_plural = verbose_name

class PermissionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = '__all__'


# Role List
class Role(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, verbose_name="Role Name", help_text="Role Name")
    flag = models.CharField(max_length=255, verbose_name="Unique ID", help_text="Unique ID")
    deleted = models.IntegerField(verbose_name="Logical deletion", null=True, blank=True, help_text="Logical deletion",default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Creation time",verbose_name="Creation time")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="Modification time",verbose_name="Modification time")
    permission = models.ManyToManyField(Permission)

    class Meta:
        db_table = "sys_role"
        verbose_name = "Role List"
        verbose_name_plural = verbose_name

class RoleSerializer(serializers.ModelSerializer):
    permissionIds = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'

    def get_permissionIds(self, obj):
        return [permission.id for permission in obj.permission.all()]


# Data dictionary
class SysDict(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    code = models.CharField(max_length=255, verbose_name="coding", help_text="coding")
    value = models.CharField(max_length=255, null=True, verbose_name="content", help_text="content")
    type = models.CharField(max_length=10, null=True, verbose_name="type", help_text="type")
    deleted = models.IntegerField(verbose_name="Logical deletion", null=True, blank=True, help_text="Logical deletion", default=0)

    class Meta:
        db_table = "dict"
        verbose_name = "Data dictionary table"
        verbose_name_plural = verbose_name

class SysDictSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysDict
        fields = '__all__'


# Website Announcement
class Notice(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, verbose_name="title ", null=True, blank=True, help_text="title")
    content = models.TextField(verbose_name="content ",null=True, blank=True,  help_text="content")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Creation time", verbose_name="Creation time")
    user_id = models.IntegerField(verbose_name="Publisher", null=True, blank=True, help_text="Publisher")

    @property
    def userId(self):
        return self.user_id
    @property
    def createTime(self):
        return self.create_time
		
    class Meta:
        db_table = "notice"
        verbose_name = "Website Announcement"
        verbose_name_plural = verbose_name

class NoticeSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()
	
    class Meta:
        model = Notice
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id
    def get_createTime(self, obj):
        return obj.create_time		
