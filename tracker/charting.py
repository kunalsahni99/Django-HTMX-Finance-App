import plotly.express as px
from django.db.models import Sum

def plot_income_expense_bar_chart(qs):
    x_vals = ['Income', 'Expenditure']

    total_income = qs.filter(type='income').aggregate(
        total=Sum('amount')
    )['total']

    total_expense = qs.filter(type='expense').aggregate(
        total=Sum('amount')
    )['total']

    fig = px.bar(x=x_vals, y=[total_income, total_expense])

    return fig