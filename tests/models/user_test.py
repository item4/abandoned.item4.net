from datetime import date

import pytest


def test_create_user_empty_email(django_user_model):
    with pytest.raises(ValueError):
        django_user_model.objects.create_user(
            '',
            '$uper$ecret$uper$ecret',
        )


def test_create_user_empty_password(django_user_model):
    with pytest.raises(ValueError):
        django_user_model.objects.create_user(
            'test@example.com',
            '',
        )


def test_create_user_fine(django_user_model):
    today = date.today()
    user = django_user_model.objects.create_user(
        'test@example.com',
        '$uper$ecret$uper$ecret',
    )

    assert user.email == 'test@example.com'
    assert user.check_password('$uper$ecret$uper$ecret')
    assert user.exp == 0
    assert user.last_login is None
    assert user.is_active
    assert not user.is_banned
    assert not user.is_admin
    assert user.date_joined.year == today.year
    assert user.date_joined.month == today.month
    assert user.date_joined.day == today.day


def test_create_superuser(django_user_model):
    today = date.today()
    user = django_user_model.objects.create_superuser(
        'test@example.com',
        '$uper$ecret$uper$ecret',
    )

    assert user.email == 'test@example.com'
    assert user.check_password('$uper$ecret$uper$ecret')
    assert user.exp == 0
    assert user.last_login is None
    assert user.is_active
    assert not user.is_banned
    assert user.is_admin
    assert user.date_joined.year == today.year
    assert user.date_joined.month == today.month
    assert user.date_joined.day == today.day
