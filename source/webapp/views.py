from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.utils.timezone import make_naive

from webapp.models import Shop
from .forms import ShopForm


def index_view(request):
    data = Shop.objects.all()
    return render(request, 'index.html', context={
        'articles': data
    })


def shop_view(request, pk):
    shop = get_object_or_404(Shop, pk=pk)

    context = {'shop': shop}
    return render(request, 'shop_view.html', context)


def shop_create_view(request):
    if request.method == "GET":
        form = ShopForm()
        return render(request, 'shop_create.html', context={
            'form': form
        })
    elif request.method == 'POST':
        form = ShopForm(data=request.POST)
        if form.is_valid():
            shop = Shop.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                price=form.cleaned_data['price']
            )
            return redirect('shop_view', pk=shop.pk)
        else:
            return render(request, 'shop_create.html', context={
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def shop_update_view(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == "GET":
        form = ShopForm(initial={
            'name': shop.name,
            'description': shop.description,
            'category': shop.category,
            'amount': shop.amount,
            # форматирование перед выводом для DateTime.
            'price': make_naive(shop.price)\
                .strftime(BROWSER_DATETIME_FORMAT)
            # для дат выглядит просто как:
            # 'price': shop.price
        })
        return render(request, 'shop_update.html', context={
            'form': form,
            'shop': shop
        })
    elif request.method == 'POST':
        form = ShopForm(data=request.POST)
        if form.is_valid():
            # Shop.objects.filter(pk=pk).update(**form.cleaned_data)
            shop.name = form.cleaned_data['name']
            shop.description = form.cleaned_data['description']
            shop.category = form.cleaned_data['category']
            shop.amount = form.cleaned_data['amount']
            shop.price = form.cleaned_data['price']
            shop.save()
            return redirect('shop_view', pk=shop.pk)
        else:
            return render(request, 'shop_update.html', context={
                'shop': shop,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def shop_delete_view(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'GET':
        return render(request, 'shop_delete.html', context={'shop': shop})
    elif request.method == 'POST':
        shop.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
