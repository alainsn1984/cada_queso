import pytest
from pytest_django.asserts import (
    assertContains,
    assertRedirects
)
from django.urls import reverse, resolve
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import (
    CheeseCreateView,
    CheeseListView,
    CheeseDetailView,
    CheeseUpdateView
)
from .factories import CheeseFactory, cheese
pytestmark = pytest.mark.django_db


def test_good_cheese_list_view_expanded(rf:RequestFactory):
    # Get the request
    request = rf.get(reverse('cheeses:list'))
    # Use the request  to get the response
    response = CheeseListView.as_view()(request)
    # Test that the response is valid
    assertContains(response, 'Cheese List')


def test_good_cheese_detail_view():
    """Test the `CheeseDetailView` when route is:
       /chesses/<name_cheese>/
    """
    cheese = CheeseFactory()
    view = resolve(f'/cheeses/{cheese.slug}/')
    assert view.func.__name__== CheeseDetailView.as_view().__name__


def test_good_cheese_create_view(rf, admin_user):
    # Order some cheese from the CheeseFactory
    cheese = CheeseFactory()
    # Make a request for our new cheese
    request = rf.get(reverse('cheeses:add'))
    request.user = admin_user
    # Use the request  to get the response
    response = CheeseCreateView.as_view()(request)
    assert response.status_code == 200

def test_cheese_list_contains_2_cheeses(rf):
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    assert response.status_code == 200


def test_cheese_create_form_valid(rf:RequestFactory, admin_user):
    form_data = {
        'name':'Paski Sir',
        'description':'A salty hard cheese',
        'firmness':Cheese.Firmness.HARD
    }
    request = rf.post(reverse('cheeses:add'), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    cheese = Cheese.objects.get(name='Paski Sir')
    assert cheese.description == 'A salty hard cheese'
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user

def test_cheese_create_correct_title(rf,admin_user):
    """Page title for CheeseCreateView should be Add Cheese
    """
    request = rf.get(reverse('cheeses:add'))
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)
    assertContains(response, 'Add Cheese')

def test_good_cheese_update_view():
    cheese = CheeseFactory()
    view = resolve(f'/cheeses/{cheese.slug}/update/')
    assert view.func.__name__ == CheeseUpdateView.as_view().__name__


