from django.shortcuts import render, redirect
from .models import product, Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from  django.contrib.auth import authenticate, login, logout


def index(request):
    allProds = []
    catprods = product.objects.values('catogary', 'id')
    cats = {item['catogary'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(catogary=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.catogary.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = product.objects.values('catogary', 'id')
    cats = {item['catogary'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(catogary=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/index.html', params)


def productView(request, myid):

    # Fetch the product using the id
    Product = product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':Product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')

def handleSignup(request):

    if request.method == 'POST':

        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if len(username)>10:
            messages.error(request, "username must be under 10 character")
            return redirect('shophome')

        if not username.isalnum():
            messages.error(request, "username must be only contain letter and number ")
            return redirect('shophome')


        if pass1 != pass2:
            messages.error(request, "password do not match")
            return redirect('shophome')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        #myuser.confirm_password = pass2
        myuser.save()
        messages.success(request, "your acccount has been created")
        return redirect('shophome')
    else:

        return HttpResponse('404 not found')



def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']


        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "succecsfull login")
            return redirect('shophome')

        else:
            messages.error(request, "invalid credition , please try again")
            return redirect('shophome')


    return HttpResponse('handleLogin')


def handleLogout(request):

    logout(request)
    messages.success(request, " succsessfull logout")
    return redirect('shophome')