from django.core.exceptions import ValidationError
from django.test import TestCase

from constants import *
from users.tests import create_user
from .models import Transaction


class TransactionTest(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_create_deposit(self):
        transaction = Transaction(type=TRANSACTION_TYPE_DEPOSIT, amount=50, method='test', user=self.user)
        transaction.save()
        self.assertEqual(transaction.type, TRANSACTION_TYPE_DEPOSIT)

    def test_create_deposit_with_negative_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_DEPOSIT, amount=-100, method='test', user=self.user)
        with self.assertRaises(ValidationError, msg='Negative amount is not allowed'):
            transaction.save()

    def test_create_deposit_low_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_DEPOSIT, amount=1, method='test', user=self.user)
        with self.assertRaises(ValidationError, msg='Amount is too low'):
            transaction.save()

    def test_create_deposit_high_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_DEPOSIT, amount=100000, method='test', user=self.user)
        with self.assertRaises(ValidationError, msg='Amount is too high'):
            transaction.save()

    def test_create_withdrawal(self):
        transaction = Transaction(type=TRANSACTION_TYPE_WITHDRAW, amount=50, method='test', user=self.user)
        transaction.save()
        self.assertEqual(transaction.type, TRANSACTION_TYPE_WITHDRAW)

    def test_create_withdrawal_with_negative_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_WITHDRAW, amount=-100, method='test', user=self.user)
        with self.assertRaises(ValidationError, msg='Negative amount is not allowed'):
            transaction.save()

    def test_create_withdrawal_low_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_WITHDRAW, amount=1, method='test', user=self.user)
        with self.assertRaises(ValidationError, msg='Amount is too low'):
            transaction.save()

    def test_create_withdrawal_high_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_WITHDRAW, amount=100000, method='test', user=self.user)
        with self.assertRaises(ValidationError, msg='Amount is too high'):
            transaction.save()
