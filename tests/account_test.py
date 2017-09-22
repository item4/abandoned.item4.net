import json
import re

from allauth.account.models import EmailAddress

import pytest


CONFIRM_URL_RE = re.compile('(/auth/confirm/.+?/)')


@pytest.mark.django_db()
def test_register_fine(client, mailoutbox):
    """Register user correctly."""

    ADDRESS = 'item4@example.com'
    PASSWORD = '$uper$escret$uper$escret$uper$escret'
    SUBJECT = '[item4.net] Please Confirm Your E-mail Address'
    res = client.post('/auth/register/', json.dumps({
        'email': ADDRESS,
        'password1': PASSWORD,
        'password2': PASSWORD,
    }), content_type='application/json')
    data = res.json()
    assert data['detail'] == "Verification e-mail sent."

    address = EmailAddress.objects.get(email=ADDRESS)

    assert address
    assert not address.verified

    assert len(mailoutbox) == 1

    mail = mailoutbox[0]

    assert mail.subject == SUBJECT
    assert ADDRESS in mail.body
    assert list(mail.to) == [ADDRESS]

    match = CONFIRM_URL_RE.search(mail.body)
    assert match

    res = client.get(match.group(1))
    data = res.json()
    assert data['key']

    res = client.post('/auth/confirm/', json.dumps(data),
                      content_type='application/json')
    data = res.json()
    address.refresh_from_db()

    assert data['detail'] == 'ok'
    assert address.verified


@pytest.mark.django_db()
def test_register_no_fields(client):
    """Register without fields"""

    res = client.post('/auth/register/', json.dumps({
    }), content_type='application/json')
    data = res.json()
    assert data['email'] == ['This field is required.']
    assert data['password1'] == ['This field is required.']
    assert data['password2'] == ['This field is required.']


@pytest.mark.django_db()
def test_register_empty_fields(client):
    """Register with empty values"""

    res = client.post('/auth/register/', json.dumps({
        'email': '',
        'password1': '',
        'password2': '',
    }), content_type='application/json')
    data = res.json()
    assert data['email'] == ['This field may not be blank.']
    assert data['password1'] == ['This field may not be blank.']
    assert data['password2'] == ['This field may not be blank.']


@pytest.mark.django_db()
def test_register_invalid_email(client):
    """Register with invalid email"""

    ADDRESS = 'invalid#example.com'
    PASSWORD = '$uper$escret$uper$escret$uper$escret'
    res = client.post('/auth/register/', json.dumps({
        'email': ADDRESS,
        'password1': PASSWORD,
        'password2': PASSWORD,
    }), content_type='application/json')
    data = res.json()
    assert data['email'] == ['Enter a valid email address.']


@pytest.mark.django_db()
def test_register_invalid_password(client):
    """Register with invalid password"""

    ADDRESS = 'item4@example.com'
    PASSWORD = '1234'
    res = client.post('/auth/register/', json.dumps({
        'email': ADDRESS,
        'password1': PASSWORD,
        'password2': PASSWORD,
    }), content_type='application/json')
    data = res.json()
    assert data['password1'] == [
        'This password is too short. It must contain at least 16 characters.',
        'This password is too common.',
        'This password is entirely numeric.',
    ]


@pytest.mark.django_db()
def test_register_different_password(client):
    """Register with different password 1 and 2"""

    ADDRESS = 'item4@example.com'
    res = client.post('/auth/register/', json.dumps({
        'email': ADDRESS,
        'password1': '$uper$escret$uper$escret$uper$escret',  # used $
        'password2': 'supersescretsupersescretsupersescret',  # used s
    }), content_type='application/json')
    data = res.json()
    assert data['non_field_errors'] == [
        "The two password fields didn't match.",
    ]


@pytest.mark.django_db()
def test_login_fine(rf, django_user_model, client):
    """Login successfully"""

    ADDRESS = 'item4@example.com'
    PASSWORD = '$uper$escret$uper$escret$uper$escret'

    user = django_user_model.objects.create_user(ADDRESS, PASSWORD)
    request = rf.get('/')
    address = EmailAddress.objects.add_email(request, user, ADDRESS)
    address.verified = True
    address.save()

    res = client.post('/auth/login/', json.dumps({
        'email': ADDRESS,
        'password': PASSWORD,
    }), content_type='application/json')
    data = res.json()
    assert data['key']


@pytest.mark.django_db()
def test_login_no_verified(rf, django_user_model, client):
    """Login with no-verified account"""

    ADDRESS = 'item4@example.com'
    PASSWORD = '$uper$escret$uper$escret$uper$escret'

    user = django_user_model.objects.create_user(ADDRESS, PASSWORD)
    request = rf.get('/')
    EmailAddress.objects.add_email(request, user, ADDRESS)

    res = client.post('/auth/login/', json.dumps({
        'email': ADDRESS,
        'password': PASSWORD,
    }), content_type='application/json')
    data = res.json()
    assert data['non_field_errors'] == ['E-mail is not verified.']


@pytest.mark.django_db()
def test_login_wrong_email(client):
    """Login with wrong email"""

    ADDRESS = 'item4@example.com'
    PASSWORD = '$uper$escret$uper$escret$uper$escret'

    res = client.post('/auth/login/', json.dumps({
        'email': ADDRESS,
        'password': PASSWORD,
    }), content_type='application/json')
    data = res.json()
    assert data['non_field_errors'] == [
        'Unable to log in with provided credentials.',
    ]


@pytest.mark.django_db()
def test_login_wrong_password(rf, django_user_model, client):
    """Login with wrong password"""

    ADDRESS = 'item4@example.com'
    PASSWORD = '$uper$escret$uper$escret$uper$escret'

    user = django_user_model.objects.create_user(ADDRESS, PASSWORD)
    request = rf.get('/')
    address = EmailAddress.objects.add_email(request, user, ADDRESS)
    address.verified = True
    address.save()

    res = client.post('/auth/login/', json.dumps({
        'email': ADDRESS,
        'password': 'wrongpa$$wordwrongpa$$wordwrongpa$$word',
    }), content_type='application/json')
    data = res.json()
    assert data['non_field_errors'] == [
        'Unable to log in with provided credentials.',
    ]


@pytest.mark.django_db()
def test_logout(client):
    """Logout"""

    res = client.post('/auth/logout/', json.dumps({}),
                      content_type='application/json')
    data = res.json()
    assert data['detail'] == 'Successfully logged out.'
