from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.shortcuts import redirect
from django.utils import timezone
from .models import Item,OrderItem,Order
from django .contrib import messages



class HomeView(ListView):
   model = Item
   paginate_by = 10
   template_name = "core/home.html"
   

def checkout(request):
   return render (request, "core/checkout.html")


def products(request):
   context = {
        'items': Item.objects.all()
    }
   return render (request, "core/products.html",context)


class ItemDetailView(DetailView):
   model = Item
   template_name = "core/product.html"



#login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("website:product",slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("website:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("website:order-summary")


#login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
      )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("website:product",slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("website:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("website:product", slug=slug)
