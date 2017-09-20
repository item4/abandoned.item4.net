from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from timezone_field import TimeZoneField


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address to login',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='닉네임',
        max_length=25,
    )
    exp = models.IntegerField(
        verbose_name='경험치',
        default=0,
    )
    tz = TimeZoneField(
        verbose_name='Timezone',
        default='Asia/Seoul',
    )

    is_banned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name='회원가입일',
        auto_now_add=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self) -> str:
        return f'{self.name}({self.email})'

    def has_perm(self, perm, obj=None) -> bool:
        """Does the user have a specific permission?"""
        return not self.is_banned

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return not self.is_banned

    @property
    def level(self) -> int:
        return self.exp // 100  # type: ignore

    @property
    def is_staff(self) -> bool:
        """Is the user a member of staff?"""
        return bool(self.is_admin)
