from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget

from tracker.models import Category, Transaction

class TransactionResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )
    date = fields.Field(
        column_name='date',
        attribute='date',
        widget=DateWidget(format='%d-%m-%Y')
    )

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.user = kwargs.get('user')

    class Meta:
        model = Transaction
        fields = (
            'amount',
            'type',
            'date',
            'category'
        )
        import_id_fields = (
            'amount',
            'type',
            'date',
            'category'
        )