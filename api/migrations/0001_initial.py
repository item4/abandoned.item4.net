from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'password',
                    models.CharField(
                        max_length=128,
                        verbose_name='password'
                    )
                ),
                (
                    'last_login',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name='last login'
                    )
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text=('Designates that this user has all '
                                   'permissions without explicitly '
                                   'assigning them.'),
                        verbose_name='superuser status'
                    )
                ),
                (
                    'email',
                    models.EmailField(
                        max_length=255,
                        unique=True,
                        verbose_name='email address to login'
                    )
                ),
                (
                    'name',
                    models.CharField(max_length=25, verbose_name='닉네임')
                ),
                (
                    'exp',
                    models.IntegerField(default=0, verbose_name='경험치')
                ),
                (
                    'tz',
                    timezone_field.fields.TimeZoneField(
                        default='Asia/Seoul',
                        verbose_name='Timezone'
                    )
                ),
                (
                    'is_banned',
                    models.BooleanField(default=False)
                ),
                (
                    'is_active',
                    models.BooleanField(default=True)
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='회원가입일'
                    )
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text=('The groups this user belongs to. A user '
                                   'will get all permissions granted to each '
                                   'of their groups.'),
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Group',
                        verbose_name='groups'
                    )
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Permission',
                        verbose_name='user permissions'
                    )
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
