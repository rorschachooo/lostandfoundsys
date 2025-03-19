from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers

# Create your models here.
# user
class Member(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="number", help_text="number")
    username = models.CharField(max_length=255, verbose_name="Log in to your account ", null=True, blank=True, help_text="Log in to your account")
    name = models.CharField(max_length=255, verbose_name="Name ", null=True, blank=True, help_text="Name")
    user_id = models.IntegerField(verbose_name="User ", null=True, blank=True, help_text="User")
    phone = models.CharField(max_length=255, verbose_name="phone number ", null=True, blank=True, help_text="phone number")

    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "member"
        verbose_name = "user"
        verbose_name_plural = verbose_name

class MemberSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id


# Lost and Found
class Recruit(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="number", help_text="number")
    category_id = models.IntegerField(verbose_name="Item Classification ", null=True, blank=True, help_text="Item Classification")
    name = models.CharField(max_length=255, verbose_name="Item Name ", null=True, blank=True, help_text="Item Name")
    img = models.CharField(max_length=255, verbose_name="Item Image ", null=True, blank=True, help_text="Item Image")
    content = models.TextField(verbose_name="Item Description ",null=True, blank=True,  help_text="Item Description")
    address = models.CharField(max_length=255, verbose_name="Pickup Location ", null=True, blank=True, help_text="Pickup Location")
    time = models.CharField(max_length=255, verbose_name="Pickup time ", null=True, blank=True, help_text="Pickup time")
    user_id = models.IntegerField(verbose_name="Publisher ", null=True, blank=True, help_text="Publisher")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Release time ", verbose_name="Release time")

    @property
    def categoryId(self):
        return self.category_id
    @property
    def userId(self):
        return self.user_id
    @property
    def createTime(self):
        return self.create_time

    class Meta:
        db_table = "recruit"
        verbose_name = "Lost and Found"
        verbose_name_plural = verbose_name

class RecruitSerializer(serializers.ModelSerializer):
    categoryId = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()

    class Meta:
        model = Recruit
        fields = '__all__'

    def get_categoryId(self, obj):
        return obj.category_id
    def get_userId(self, obj):
        return obj.user_id
    def get_createTime(self, obj):
        return obj.create_time

# Report lost items
class Lost(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="number", help_text="number")
    category_id = models.IntegerField(verbose_name="Item Classification", null=True, blank=True, help_text="Item Classification")
    name = models.CharField(max_length=255, verbose_name="Item Name ", null=True, blank=True, help_text="Item Name")
    img = models.CharField(max_length=255, verbose_name="Item Image ", null=True, blank=True, help_text="Item Image")
    content = models.TextField(verbose_name="Item Description ",null=True, blank=True,  help_text="Item Description")
    address = models.CharField(max_length=255, verbose_name="Lost location ", null=True, blank=True, help_text="Lost location")
    time = models.CharField(max_length=255, verbose_name="Lost time ", null=True, blank=True, help_text="Lost time")
    phone = models.CharField(max_length=255, verbose_name="Contact Details ", null=True, blank=True, help_text="Contact Details")
    user_id = models.IntegerField(verbose_name="Publisher", null=True, blank=True, help_text="Publisher")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Release time", verbose_name="Release time")

    @property
    def categoryId(self):
        return self.category_id
    @property
    def userId(self):
        return self.user_id
    @property
    def createTime(self):
        return self.create_time

    class Meta:
        db_table = "lost"
        verbose_name = "Report lost items"
        verbose_name_plural = verbose_name

class LostSerializer(serializers.ModelSerializer):
    categoryId = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()

    class Meta:
        model = Lost
        fields = '__all__'

    def get_categoryId(self, obj):
        return obj.category_id
    def get_userId(self, obj):
        return obj.user_id
    def get_createTime(self, obj):
        return obj.create_time

# Item Type
class Category(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="number", help_text="number")
    name = models.CharField(max_length=255, verbose_name="Category Name ", null=True, blank=True, help_text="Category Name")


    class Meta:
        db_table = "category"
        verbose_name = "Item Type"
        verbose_name_plural = verbose_name

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


# Information to be claimed
class Cart(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Claim Number", help_text="Claim Number")
    user_id = models.IntegerField(verbose_name="Claim User", null=True, blank=True, help_text="Claim User")
    name = models.CharField(max_length=255, verbose_name="Claiming items ", null=True, blank=True, help_text="Claiming items")
    img = models.CharField(max_length=255, verbose_name="Item Image ", null=True, blank=True, help_text="Item Image")
    biz_user_id = models.IntegerField(verbose_name="Pickup Person", null=True, blank=True, help_text="Pickup Person")
    goodid = models.IntegerField(verbose_name="Item Number", null=True, blank=True, help_text="Item Number")

    @property
    def userId(self):
        return self.user_id
    @property
    def bizUserId(self):
        return self.biz_user_id

    class Meta:
        db_table = "cart"
        verbose_name = "Information to be claimed"
        verbose_name_plural = verbose_name

class CartSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()
    bizUserId = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id
    def get_bizUserId(self, obj):
        return obj.biz_user_id

# Lost and found records
class Orders(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Claim Number", help_text="Claim Number")
    name = models.CharField(max_length=255, verbose_name="Claim Number ", null=True, blank=True, help_text="Claim Number")
    content = models.TextField(verbose_name="Claim details ",null=True, blank=True,  help_text="Claim details")
    state_radio = models.CharField(max_length=255, verbose_name="Order status, claiming|confirmed as lost|returned|cancelled ", null=True, blank=True, help_text="Order status, claiming|confirmed as lost|returned|cancelled")
    user_id = models.IntegerField(verbose_name="Claim User", null=True, blank=True, help_text="Claim User")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="Application period", verbose_name="Application period")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="",verbose_name="Update time")
    biz_user_id = models.IntegerField(verbose_name="Lost and found person", null=True, blank=True, help_text="Lost and found person")
    goodids = models.CharField(max_length=255, verbose_name="Item Number ", null=True, blank=True, help_text="Item Number")

    @property
    def stateRadio(self):
        return self.state_radio
    @property
    def userId(self):
        return self.user_id
    @property
    def createTime(self):
        return self.create_time
    @property
    def updateTime(self):
        return self.update_time
    @property
    def bizUserId(self):
        return self.biz_user_id

    class Meta:
        db_table = "orders"
        verbose_name = "Lost and found records"
        verbose_name_plural = verbose_name

class OrdersSerializer(serializers.ModelSerializer):
    stateRadio = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()
    updateTime = serializers.SerializerMethodField()
    bizUserId = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = '__all__'

    def get_stateRadio(self, obj):
        return obj.state_radio
    def get_userId(self, obj):
        return obj.user_id
    def get_createTime(self, obj):
        return obj.create_time
    def get_updateTime(self, obj):
        return obj.update_time
    def get_bizUserId(self, obj):
        return obj.biz_user_id


# Slideshow
class Banner(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Slideshow number", help_text="Slideshow number")
    img = models.CharField(max_length=255, verbose_name="picture ", null=True, blank=True, help_text="picture")
    url = models.CharField(max_length=255, verbose_name="Link address ", null=True, blank=True, help_text="Link address")
    index_radio = models.CharField(max_length=255, verbose_name="Is it home page ", null=True, blank=True, help_text="Is it home page")

    @property
    def indexRadio(self):
        return self.index_radio

    class Meta:
        db_table = "banner"
        verbose_name = "Slideshow"
        verbose_name_plural = verbose_name

class BannerSerializer(serializers.ModelSerializer):
    indexRadio = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = '__all__'

    def get_indexRadio(self, obj):
        return obj.index_radio

