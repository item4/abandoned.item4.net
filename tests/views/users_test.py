from api.users.viewsets import UserViewSet

import pytest

from rest_framework.test import force_authenticate


@pytest.mark.django_db()
def test_users_retrieve(client, django_user_model):
    PASSWORD = '$uper$ecret' * 4
    user1 = django_user_model.objects.create_user(
        'item1@example.com',
        PASSWORD,
    )
    user2 = django_user_model.objects.create_user(
        'item2@example.com',
        PASSWORD,
    )

    user1.is_active = False
    user1.save()

    user2.name = '홍길동'
    user2.tz = 'Asia/Tokyo'
    user2.save()

    res = client.get('/users/1/')
    data = res.json()
    assert res.status_code == 404
    assert data['detail'] == 'Not found.'

    res = client.get('/users/3/')
    data = res.json()
    assert res.status_code == 404
    assert data['detail'] == 'Not found.'

    res = client.get('/users/2/')
    data = res.json()
    assert res.status_code == 200
    assert data['date_joined'].startswith(
        user2.date_joined.strftime('%Y-%m-%dT%H:%M:%S')
    )
    assert data['email'] == 'item2@example.com'
    assert data['name'] == '홍길동'
    assert data['pk'] == 2
    assert data['tz'] == 'Asia/Tokyo'

    res = client.get('/users/me/')
    assert res.status_code == 401

    client.login(email='item2@example.com', password=PASSWORD)

    res = client.get('/users/me/')
    data = res.json()
    assert res.status_code == 200
    assert data['date_joined'].startswith(
        user2.date_joined.strftime('%Y-%m-%dT%H:%M:%S')
    )
    assert data['email'] == 'item2@example.com'
    assert data['name'] == '홍길동'
    assert data['pk'] == 2
    assert data['tz'] == 'Asia/Tokyo'


@pytest.mark.django_db()
def test_users_partial_update(django_user_model, factory):
    view = UserViewSet.as_view({'patch': 'partial_update'})

    PASSWORD = '$uper$ecret' * 4
    user1 = django_user_model.objects.create_user(
        'item1@example.com',
        PASSWORD,
    )
    user2 = django_user_model.objects.create_user(
        'item2@example.com',
        PASSWORD,
    )

    user1.is_active = False
    user1.save()

    user2.name = '홍길동'
    user2.tz = 'Asia/Tokyo'
    user2.save()

    request = factory.patch('/users/1/')
    res = view(request)
    assert res.status_code == 403

    request = factory.patch('/users/2/')
    res = view(request)
    assert res.status_code == 403

    request = factory.patch('/users/me/')
    res = view(request)
    assert res.status_code == 403

    request = factory.patch('/users/1/')
    force_authenticate(request, user=user2)
    res = view(request)
    assert res.status_code == 403

    request = factory.patch('/users/2/', format='json')
    force_authenticate(request, user=user2)
    res = view(request, pk=2)
    data = res.data
    assert res.status_code == 400
    assert data['name'] == [
        'This field is required.',
    ]
    assert data['tz'] == [
        'This field is required.',
    ]

    request = factory.patch('/users/2/', {
        'name': '',
        'tz': '',
    }, format='json')
    force_authenticate(request, user=user2)
    res = view(request, pk=2)
    data = res.data
    assert res.status_code == 400
    assert data['name'] == [
        'This field may not be blank.',
    ]
    assert data['tz'] == [
        'This field may not be blank.',
    ]

    request = factory.patch('/users/2/', {
        'name': '이소룡',
        'tz': 'Asia/Seoul',
    }, format='json')
    force_authenticate(request, user=user2)
    res = view(request, pk=2)
    data = res.data
    assert res.status_code == 202
    assert data['detail'] == 'Saved.'
    user2.refresh_from_db()
    assert user2.name == '이소룡'
    assert user2.tz.zone == 'Asia/Seoul'

    request = factory.patch('/users/me/', {
        'name': '키리가야 카즈토',
        'tz': 'Asia/Tokyo',
    }, format='json')
    force_authenticate(request, user=user2)
    res = view(request, pk='me')
    data = res.data
    assert res.status_code == 202
    assert data['detail'] == 'Saved.'
    user2.refresh_from_db()
    assert user2.name == '키리가야 카즈토'
    assert user2.tz.zone == 'Asia/Tokyo'


@pytest.mark.django_db()
def test_users_destory(django_user_model, factory):
    view = UserViewSet.as_view({'delete': 'destroy'})

    PASSWORD = '$uper$ecret' * 4
    user1 = django_user_model.objects.create_user(
        'item1@example.com',
        PASSWORD
    )
    user2 = django_user_model.objects.create_user(
        'item2@example.com',
        PASSWORD
    )

    request = factory.delete('/users/1/')
    res = view(request, pk=1)
    assert res.status_code == 403

    request = factory.delete('/users/2/')
    res = view(request, pk=2)
    assert res.status_code == 403

    request = factory.delete('/users/me/')
    res = view(request, pk='me')
    assert res.status_code == 403

    request = factory.delete('/users/2/')
    force_authenticate(request, user=user1)
    res = view(request, pk=2)
    assert res.status_code == 403

    request = factory.delete('/users/1/')
    force_authenticate(request, user=user1)
    res = view(request, pk=1)
    data = res.data
    assert res.status_code == 202
    assert data['detail'] == 'Done.'
    user1.refresh_from_db()
    assert user1.email == f'out_{user1.pk}@out.out'
    assert user1.name == '탈퇴회원'
    assert not user1.is_active

    request = factory.delete('/users/me/')
    force_authenticate(request, user=user2)
    res = view(request, pk='me')
    data = res.data
    assert res.status_code == 202
    assert data['detail'] == 'Done.'
    user2.refresh_from_db()
    assert user2.email == f'out_{user2.pk}@out.out'
    assert user2.name == '탈퇴회원'
    assert not user2.is_active
