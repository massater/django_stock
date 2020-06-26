from django.shortcuts import render, redirect
import requests  # Need to install: pip install requests
import json
from django.views.generic import CreateView
from .models import Person
from .models import Stock
from django.contrib import messages
from .forms import StockForm

class PersonCreateView(CreateView):
    model = Person
    fields = ('name', 'email', 'job_title', 'bio')

# Create your views here.
def home(request):
    if request.method == "POST":
        ticker = request.POST['ticker']
        url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_1d4384d5ca2a4c51a63e36e9f7cf6df3"
        api_request = requests.get(url)

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added!"))
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            url = "https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_1d4384d5ca2a4c51a63e36e9f7cf6df3"
            api_request = requests.get(url)
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output} )

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})