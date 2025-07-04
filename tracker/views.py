from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_htmx.http import retarget

from tracker.forms import TransactionForm
from .models import Transaction
from .filters import TransactionFilter

# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()

    context = {
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income - total_expenses
    }
    if request.htmx:
        return render(request, 'tracker/partials/transactions_container.html', context)

    return render(request, 'tracker/transactions_list.html', context)

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message': "Transaction was added successfully"}
            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {'form': form}
            response = render(request, 'tracker/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')

    context = {'form': TransactionForm()}

    return render(request, 'tracker/partials/create-transaction.html', context)

def update_transactions(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            context = {'message': "Transaction was updateed successfully"}
            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {
                'form': form,
                'transaction': transaction
            }
            response = render(request, 'tracker/partials/update-transaction.html', context)
            return retarget(response, '#transaction-block')
        
    context = {
        'form': TransactionForm(instance=transaction),
        'transaction': transaction
    }

    return render(request, 'tracker/partials/update-transaction.html', context)