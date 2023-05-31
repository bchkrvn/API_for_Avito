from factory.django import DjangoModelFactory
from factory import Faker

from skymarket.ads.models import Ad
from skymarket.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    phone = Faker('phone')
    email = Faker('email')


print(UserFactory())


class AdFactory(DjangoModelFactory):
    class Meta:
        model = Ad

    title = Faker('sentence', nb_words=4)
    price = Faker('random_number')
    description = Faker('text', max_nb_chars=20)
