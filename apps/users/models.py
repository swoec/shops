# Create your models here.

from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, post_save
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import models

User = get_user_model()


class UserProfile(AbstractUser):
    """
    UserProfile
    """
    name = models.CharField(max_length=80, null=True, blank=True, verbose_name="name")
    gender = models.CharField(max_length=6, choices=(("male", "male"), ("female", "female")), default="female",
                              verbose_name="gender")
    birthday = models.DateField(null=True, blank=True, verbose_name="birthday")
    address = models.CharField(max_length=120, null=True, blank=True, verbose_name="address")
    email = models.EmailField(max_length=120, null=True, blank=True, verbose_name="email")
    mobile = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=40, null=False, blank=False, default="anon")
    is_superuser = models.BooleanField(
        default=False,
        help_text=
        'Designates that this user has all permissions without ',

    )
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text=
        'The groups this user belongs to. A user will get all permissions '
        ,
        related_name="userprofile_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="userprofile_set",
        related_query_name="user",
    )

    class Meta:
        permissions = (
            ('forum.comments', 'get comments'),
            ('view_comments', 'view comments'),
        )
        verbose_name = "user Profile"
        verbose_name_plural = verbose_name

    def has_perm(self, perm, obj=None):
        try:
            user_perm = self.user_permissions.get(codename=perm)
        except ObjectDoesNotExist:
            user_perm = False
        if user_perm:
            return True
        else:
            return False

    def permission_required(*perms):
        from django.contrib.auth.decorators import user_passes_test
        return user_passes_test(lambda u: any(u.has_perm(perm) for perm in perms), login_url='/login')

    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    code = models.CharField(max_length=4)
    mobile = models.CharField(max_length=20)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "verifycode"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class Citizen(models.Model):
    title = models.CharField(max_length=40, verbose_name='title', null=True, blank=True)
    name = models.CharField(max_length=40, verbose_name="name", null=True, blank=True)

    class Meta:
        verbose_name = 'citizen'
        verbose_name_plural = verbose_name
        # permissions = (
        #     ('forum.comments', 'get comments'),
        #     ('view_comments', 'view comments'),
        # )

    def has_perm(self, perm, obj=None):
        try:
            user_perm = self.user_permissions.get(codename=perm)
        except ObjectDoesNotExist:
            user_perm = False
        if user_perm:
            return True
        else:
            return False

    def permission_required(*perms):
        from django.contrib.auth.decorators import user_passes_test
        return user_passes_test(lambda u: any(u.has_perm(perm) for perm in perms), login_url='/login')


class Position(models.Model):
    title = models.CharField(max_length=40, verbose_name='title')
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    max_members = models.PositiveSmallIntegerField(default=100)

    def remove_from_group(self, users):
        for user in users:
            self.group.user_set.remove(user)

    def add_to_group(self, users):
        for user in users:
            self.group.user_set.add(user)

    @staticmethod
    def consistent_permissions(sender, instance, action, reverse, model, pk_set, **kwargs):

        if action == 'pre_add':
            if len(pk_set) + instance.users.count() > instance.max_members:
                raise ValidationError('This only holds {} members.'.format(instance.max_members))

        if action == 'post_add':
            instance.add_to_group(instance.users.all())
        elif action == 'pre_remove':
            instance.remove_from_group(instance.users.all())

    def __str__(self):
        return str(self.title)


@receiver(pre_delete, sender=Position)
def update_position_member_groups_on_delete(sender, instance, *args, **kwargs):
    instance.remove_from_group(instance.users.all())


@receiver(pre_save, sender=Citizen)
def pre_save_committee_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instance.slug = slug


# @receiver(post_save, sender=User)
# def create_user(sender, instance, *args, **kwargs):
#     password = instance.password
#     instance.set_password(password)
#     instance.save()


m2m_changed.connect(receiver=Position.consistent_permissions, sender=Position.users.through)
