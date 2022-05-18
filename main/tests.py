from django.core.exceptions import ValidationError
from django.test import TestCase

from constants import *
from users.tests import create_user
from .models import Transaction

"""
Tests for Transaction model
Test Coverage:
Deposit:
    - Create deposit
    - Create deposit with negative amount
    - Create deposit with amount greater than MAX_AMOUNT
    - Create deposit with amount less than MIN_AMOUNT
    - Delete deposit
Withdrawal:
    - Create withdrawal
    - Create withdrawal with negative amount
    - Create withdrawal with amount greater than MAX_AMOUNT
    - Create withdrawal with amount less than MIN_AMOUNT
    - Delete withdrawal
Transfer:
    - Create transfer
    - Create transfer with negative amount
    - Create transfer with amount greater than MAX_AMOUNT
    - Create transfer with amount less than MIN_AMOUNT
    - Create transfer to self
    - Delete transfer
TODO:
Deposit:
    - Accept pending deposit
    - Accept canceled deposit
    - Accept accepted deposit
    - Reject pending deposit
    - Reject accepted deposit
    - Reject canceled deposit
    - Cancel pending deposit
    - Cancel accepted deposit
    - Cancel canceled deposit
Withdrawal:
    - Accept pending withdrawal
    - Accept canceled withdrawal
    - Accept accepted withdrawal
    - Reject pending withdrawal
    - Reject accepted withdrawal
    - Reject canceled withdrawal
    - Cancel pending withdrawal
    - Cancel accepted withdrawal
    - Cancel canceled withdrawal
Transfer:
    - Accept pending transfer
    - Accept canceled transfer
    - Accept accepted transfer
    - Reject pending transfer
    - Reject accepted transfer
    - Reject canceled transfer
    - Cancel pending transfer
    - Cancel accepted transfer
    - Cancel accepted transfer if recipient has insufficient funds
    - Cancel canceled transfer
"""


class TransactionTest(TestCase):

    def setUp(self) -> None:
        self.user = create_user(balance=60)

    def test_delete_transaction(self):
        transaction = Transaction(type=TRANSACTION_TYPE_DEPOSIT, amount=50, method='test', user=self.user)
        transaction.save()
        with self.assertRaises(ValidationError, msg='Transaction should not be deleted'):
            transaction.delete()


class DepositTests(TransactionTest):
    def setUp(self) -> None:
        super().setUp()
        self.transaction = Transaction(type=TRANSACTION_TYPE_DEPOSIT, amount=50, method='test', user=self.user)
        self.transaction.save()

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

    def test_delete_deposit(self):
        transaction = Transaction(type=TRANSACTION_TYPE_DEPOSIT, amount=50, method='test', user=self.user)
        transaction.save()
        with self.assertRaises(ValidationError, msg='Transaction is not allowed to be deleted'):
            transaction.delete()

    def test_accept_pending_deposit(self):
        self.transaction.accept()


class WithdrawTests(TransactionTest):
    def setUp(self) -> None:
        super().setUp()

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

    def test_create_withdrawal_with_insufficient_balance(self):
        transaction = Transaction(type=TRANSACTION_TYPE_WITHDRAW, amount=60, method='test', user=self.user)
        with self.assertRaises(ValidationError, msg='Insufficient balance'):
            transaction.save()

    def test_delete_withdrawal(self):
        transaction = Transaction(type=TRANSACTION_TYPE_WITHDRAW, amount=50, method='test', user=self.user)
        transaction.save()
        with self.assertRaises(ValidationError, msg='Transaction is not allowed to be deleted'):
            transaction.delete()


class TransferTest(TransactionTest):
    def setUp(self) -> None:
        super().setUp()

    def test_create_transfer(self):
        transaction = Transaction(type=TRANSACTION_TYPE_TRANSFER, amount=50, method='test', user=self.user,
                                  receiver=create_user(balance=50))
        transaction.save()
        self.assertEqual(transaction.type, TRANSACTION_TYPE_TRANSFER)

    def test_create_transfer_with_negative_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_TRANSFER, amount=-100, method='test', user=self.user,
                                  receiver=create_user(balance=50))
        with self.assertRaises(ValidationError, msg='Negative amount is not allowed'):
            transaction.save()

    def test_create_transfer_low_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_TRANSFER, amount=1, method='test', user=self.user,
                                  receiver=create_user(balance=50))
        with self.assertRaises(ValidationError, msg='Amount is too low'):
            transaction.save()

    def test_create_transfer_high_amount(self):
        transaction = Transaction(type=TRANSACTION_TYPE_TRANSFER, amount=100000, method='test', user=self.user,
                                  receiver=create_user(balance=50))
        with self.assertRaises(ValidationError, msg='Amount is too high'):
            transaction.save()

    def test_create_transfer_with_insufficient_balance(self):
        transaction = Transaction(type=TRANSACTION_TYPE_TRANSFER, amount=60, method='test', user=self.user,
                                  receiver=create_user(balance=50))
        with self.assertRaises(ValidationError, msg='Insufficient balance'):
            transaction.save()

    def test_create_transfer_same_user(self):
        transaction = Transaction(type=TRANSACTION_TYPE_TRANSFER, amount=50, method='test', user=self.user,
                                  receiver=self.user)
        with self.assertRaises(ValidationError, msg='Cannot transfer to yourself'):
            transaction.save()

    def test_delete_transfer(self):
        transaction = Transaction(type=TRANSACTION_TYPE_TRANSFER, amount=50, method='test', user=self.user,
                                  receiver=create_user(balance=50))
        transaction.save()
        with self.assertRaises(ValidationError, msg='Transaction is not allowed to be deleted'):
            transaction.delete()
