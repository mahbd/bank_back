from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator

from constants import *
from users.models import User as UserModel

User: UserModel = get_user_model()


class ExternalBank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    information = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.user}'


class KYC(models.Model):
    name = models.CharField(max_length=255)
    doc = models.FileField(upload_to='documents/')
    date = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    amount = models.FloatField(validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=255)
    receiver: UserModel = models.ForeignKey(User, on_delete=models.CASCADE,
                                            related_name='receiver', null=True, blank=True)
    status = models.CharField(max_length=255, choices=TRANSACTION_STATUSES, default=TRANSACTION_STATUSES[0][0])
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPES)
    user: UserModel = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if self.type == TRANSACTION_TYPE_DEPOSIT:
            validate_deposit(self)
        elif self.type == TRANSACTION_TYPE_WITHDRAW:
            validate_withdrawal(self)
        elif self.type == TRANSACTION_TYPE_TRANSFER:
            validate_transfer(self)
        else:
            raise ValidationError('Invalid transaction type')

    def save(self, *args, **kwargs):
        self.clean()
        self.clean_fields()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        raise ValidationError('You cannot delete a transaction')

    def accept_transaction(self):
        if self.type == TRANSACTION_TYPE_DEPOSIT:
            accept_deposit(self)
        elif self.type == TRANSACTION_TYPE_WITHDRAW:
            accept_withdrawal(self)
        elif self.type == TRANSACTION_TYPE_TRANSFER:
            accept_transfer(self)
        else:
            raise ValidationError('Invalid transaction type')

    def reject_transaction(self):
        if self.type == TRANSACTION_TYPE_DEPOSIT:
            reject_deposit(self)
        elif self.type == TRANSACTION_TYPE_WITHDRAW:
            reject_withdrawal(self)
        elif self.type == TRANSACTION_TYPE_TRANSFER:
            reject_transfer(self)
        else:
            raise ValidationError('Invalid transaction type')

    def __str__(self):
        return f'{self.user} - {self.amount}'


def validate_deposit(deposit: Transaction):
    if deposit.user.max_allowed_deposit() < deposit.amount:
        raise ValidationError('Deposit amount is greater than the maximum allowed')

    if deposit.user.min_allowed_deposit() > deposit.amount:
        raise ValidationError('Deposit amount is less than the minimum allowed')


def validate_withdrawal(withdrawal: Transaction):
    if withdrawal.user.max_allowed_withdrawal() < withdrawal.amount:
        raise ValidationError('Withdrawal amount is greater than the maximum allowed')

    if withdrawal.user.min_allowed_withdrawal() > withdrawal.amount:
        raise ValidationError('Withdrawal amount is less than the minimum allowed')


def validate_transfer(transfer: Transaction):
    if transfer.user.max_allowed_transfer() < transfer.amount:
        raise ValidationError('Transfer amount is greater than the maximum allowed')

    if transfer.user.min_allowed_transfer() > transfer.amount:
        raise ValidationError('Transfer amount is less than the minimum allowed')

    if transfer.receiver == transfer.user:
        raise ValidationError('Transfer receiver is the same as the sender')


def accept_deposit(deposit: Transaction, update_balance=True):
    if deposit.status == TRANSACTION_STATUS_PENDING:
        if update_balance:
            deposit.user.balance += deposit.amount
            deposit.user.save()
        deposit.status = TRANSACTION_STATUS_COMPLETED
        deposit.save()
    else:
        if deposit.status == TRANSACTION_STATUS_COMPLETED:
            raise ValidationError('Transaction is already completed')
        else:
            raise ValidationError('Transaction is not pending')


def accept_withdrawal(withdrawal: Transaction):
    if withdrawal.status == TRANSACTION_STATUS_PENDING:
        withdrawal.status = TRANSACTION_STATUS_COMPLETED
        withdrawal.save()
    else:
        if withdrawal.status == TRANSACTION_STATUS_COMPLETED:
            raise ValidationError('Transaction is already completed')
        else:
            raise ValidationError('Transaction is not pending')


def accept_transfer(transfer: Transaction, update_receiver_balance=True):
    if transfer.status == TRANSACTION_STATUS_PENDING:
        if update_receiver_balance:
            transfer.receiver.balance += transfer.amount
            transfer.receiver.save()
        transfer.status = TRANSACTION_STATUS_COMPLETED
        transfer.save()
    else:
        if transfer.status == TRANSACTION_STATUS_COMPLETED:
            raise ValidationError('Transaction is already completed')
        else:
            raise ValidationError('Transaction is not pending')


def reject_deposit(deposit: Transaction):
    if deposit.status == TRANSACTION_STATUS_PENDING:
        deposit.status = TRANSACTION_STATUS_FAILED
        deposit.save()
    else:
        if deposit.status == TRANSACTION_STATUS_FAILED:
            raise ValidationError('Transaction is already failed')
        else:
            raise ValidationError('Transaction is not pending')


def reject_withdrawal(withdrawal: Transaction, update_balance=True):
    if withdrawal.status == TRANSACTION_STATUS_PENDING:
        if update_balance:
            withdrawal.user.balance += withdrawal.amount
            withdrawal.user.save()
        withdrawal.status = TRANSACTION_STATUS_FAILED
        withdrawal.save()
    else:
        if withdrawal.status == TRANSACTION_STATUS_FAILED:
            raise ValidationError('Transaction is already failed')
        else:
            raise ValidationError('Transaction is not pending')


def reject_transfer(transfer: Transaction, update_sender_balance=True, update_receiver_balance=False):
    if transfer.status == TRANSACTION_STATUS_PENDING:
        if update_sender_balance:
            transfer.user.balance += transfer.amount
            transfer.user.save()
        if update_receiver_balance:
            transfer.receiver.balance -= transfer.amount
            transfer.receiver.save()
        transfer.status = TRANSACTION_STATUS_FAILED
        transfer.save()
    else:
        if transfer.status == TRANSACTION_STATUS_FAILED:
            raise ValidationError('Transaction is already failed')
        else:
            raise ValidationError('Transaction is not pending')