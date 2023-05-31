from pytest_factoryboy import register

from .factories import UserFactory, AdFactory

register(UserFactory)
register(AdFactory)
