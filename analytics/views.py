from django.shortcuts import render
from django.contrib.auth.models import User  # Import User model
from products.models import Category, Product
import plotly.graph_objs as go
from plotly.offline import plot

def analytics_dashboard(request):
    # Retrieve categories and their counts
    categories = Category.objects.all()

    # Bar chart data
    bar_labels = [category.name for category in categories]
    bar_values = [Product.objects.filter(category=category).count() for category in categories]

    bar_chart = go.Figure(data=[go.Bar(x=bar_labels, y=bar_values)])
    bar_div = plot(bar_chart, output_type='div', include_plotlyjs=False)

    # Pie chart data
    suppliers_count = User.objects.filter(profile__user_type='supplier').count()
    farmers_count = User.objects.filter(profile__user_type='farmer').count()

    labels = ['Farmers', 'Suppliers']
    values = [60, 40]

    pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
    pie_div = plot(pie_chart, output_type='div', include_plotlyjs=False)

    context = {
        'bar_div': bar_div,
        'pie_div': pie_div,
    }

    return render(request, 'analytics_dashboard.html', context)
