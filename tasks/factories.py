import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")
    password = "senha_padrao_123"

    class Meta:
        model = User


class TaskFactory(factory.django.DjangoModelFactory):
    description = factory.Sequence(lambda n: f"Task {n}")
    user = factory.SubFactory(UserFactory)
    init_time = (
        timezone.now().replace(hour=10, minute=0, second=0, microsecond=0).time()
    )
    end_time = timezone.now().replace(hour=11, minute=0, second=0, microsecond=0).time()
