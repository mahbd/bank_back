from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    kyc_verified = models.BooleanField(default=False)
    balance = models.FloatField(default=0)

    def max_allowed_deposit(self) -> float:
        return 100

    def max_allowed_withdrawal(self) -> float:
        return min(self.balance - 10, 100)

    def max_allowed_transfer(self) -> float:
        return min(self.balance - 10, 100)

    def min_allowed_deposit(self) -> float:
        return 10

    def min_allowed_withdrawal(self) -> float:
        return 10

    def min_allowed_transfer(self) -> float:
        return 10
