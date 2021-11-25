
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil


def index(request):
      allProds = []
      catprods = Product.objects.values('Category', 'id')
      print(catprods)
      cats = {item['Category'] for item in catprods}
      for cat in cats:
            prod = Product.objects.filter(Category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
      param = {'allProds': allProds}
      return render(request, 'e_commerce/index.html', param)

def contact(request):
      if request.method == "POST":
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            desc = request.POST.get('desc', '')
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
      return render(request,'e_commerce/contact.html')

def about(request):
      return render(request, 'e_commerce/about.html')

def tracker(request):
      if request.method == "POST":
            orderId = request.POST.get('orderId', '')
            email = request.POST.get('email', '')
            try:
                  order = Orders.objects.filter(order_id=orderId, email=email)
                  if len(order) > 0:
                        update = OrderUpdate.objects.filter(order_id=orderId)
                        updates = []
                        for item in update:
                              updates.append({'text': item.update_desc, 'time': item.timestamp})
                              response = json.dumps(updates, default=str)
                        return HttpResponse(response)
                  else:
                        return HttpResponse('{}')
            except Exception as e:
                  return HttpResponse('{}')

      return render(request, 'e_commerce/tracker.html')
def searchMatch(query, item):
    if query in item.desc.lower() or  query in item.product_name.lower() or query in item.Category.lower():
        return True
    else:
        return False
def search(request):
      query = request.GET.get('search')
      allProds = []
      catprods = Product.objects.values('Category', 'id')
      cats = {item['Category'] for item in catprods}
      for cat in cats:
            prodtemp = Product.objects.filter(Category=cat)
            prod = [item for item in prodtemp if searchMatch(query, item)]

            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            if len(prod) != 0:
                  allProds.append([prod, range(1, nSlides), nSlides])
      params = {'allProds': allProds, "msg": ""}
      if len(allProds) == 0 or len(query) < 4:
            params = {'msg': "Please make sure to enter relevant search query"}
      return render(request, 'e_commerce/search.html', params)

def productview(request,myid):
      product=Product.objects.filter(id=myid);
      return render(request,'e_commerce/prodView.html', {'product': product[0]})

def checkout(request):
      if request.method == "POST":
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')

            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                           zip_code=zip_code, phone=phone)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
            update.save()
            thank = True
            id = order.order_id
            return render(request, 'e_commerce/checkout.html', {'thank': thank, 'id': id})
      return render(request,'e_commerce/checkout.html')