from django.contrib import admin
from django.utils.html import format_html

from .models import Transaction
from constants import *


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'amount', 'status', 'created', 'action_button')
    readonly_fields = ('created',)
    list_per_page = 20
    search_fields = ('id', 'user__username', 'amount', 'type', 'method')
    list_filter = ('type', 'status', 'created')
    autocomplete_fields = ('user', 'receiver')

    def action_button(self, obj):
        if obj.status == TRANSACTION_STATUS_PENDING:
            return format_html(
                '<a class="button" href="/admin/main/transaction/{}/approve/">Approve</a>'
                '<a style="background-color: red; color: white; padding: 4px" href="/admin/main/transaction/{}/deny/">Deny</a>',
                obj.id, obj.id)
        return format_html(
            '<a class="button" href="{}">{}</a>',
            '/admin/main/transaction/{}/'.format(obj.id),
            'View'
        )

