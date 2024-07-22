from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order, OrderItem
from .forms import MenuItemForm, OrderForm, OrderItemForm, LoginForm, SignUpForm,UpdateOrderStatusForm
from rest_framework import viewsets
from .serializers import MenuItemSerializer, OrderSerializer
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import csv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .permissions import IsOwnerGroup
from rest_framework.decorators import api_view, permission_classes
from .forms import LoginForm
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission
from django.contrib import messages



def is_waiter(user):
    return user.groups.filter(name='Waiter').exists()

def is_Owner(user):
    return user.groups.filter(name='Owner').exists()
def is_Chef(user):
    return user.groups.filter(name='chef').exists()

def is_User(user):
    return user.groups.filter(name='user').exists()

def is_waiter_or_owner(user):
    return is_waiter(user) or is_Owner(user)

def is_owner_or_chef(user):
    return is_Owner(user) or is_Chef(user)

def is_waiter_or_chef(user):
    return is_waiter(user) or is_Chef(user)

def is_waiter_or_chef_or_Owner(user):
    return is_waiter(user) or is_Chef(user) or is_Owner(user)

@login_required
@user_passes_test(is_owner_or_chef)
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            
            item_name = form.cleaned_data['name']
            if MenuItem.objects.filter(name=item_name).exists():
                print("Item Exixts")
            else:
                form.save()
                return redirect('menu_list')
    else:
        form = MenuItemForm()
    
    return render(request, 'restaurantApp/add_to_menu.html', {'form': form})

def user_login(request):
    
    request.session.flush()

    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                request.session['user_id'] = user.id


                user_groups = user.groups.values_list('name', flat=True)
                request.session['user_groups'] = list(user_groups)[0]
                print(list(user_groups)[0])

                if(list(user_groups)[0]=='chef'):
                    return redirect('menu_lists')
                return redirect('menu_list')
    else:
        form = LoginForm()

    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'restaurantApp/login.html', {'form': form, 'username': username})

@login_required
@user_passes_test(is_Chef)
def accept_order(request):
    orders = Order.objects.filter(status__in=['ordered', 'cooking'])
    return render(request, 'restaurantApp/accept_order.html', {'orders': orders})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request) 
        request.session.flush()  
    return redirect('user_login') 

@login_required
@user_passes_test(is_waiter_or_chef)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = UpdateOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('accept_order')
    else:
        form = UpdateOrderStatusForm(instance=order)
    return render(request, 'restaurantApp/update_order_status.html', {'form': form, 'order': order})



def update_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        print(item.quantity_sold)
        if form.is_valid():
            form.save()
            return redirect('menu_lists') 
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'restaurantApp/update_menu_item.html', {'form': form, 'item': item})



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            
            group_name = form.cleaned_data.get('group')
            if group_name:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)

            return redirect('signup_success')
    else:
        form = SignUpForm()
    
    groups = Group.objects.all()
    return render(request, 'account/signup.html', {'form': form, 'groups': groups})

def signup_success(request):
    return render(request, 'account/success.html')



class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions,BasePermission]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions,BasePermission]



@login_required
def menu_list(request):
    if request.method == "POST":
        selected_items = request.POST.getlist('selected_items')
        customer_name = request.POST.get('customer_name')
        if selected_items and customer_name:
            order = Order.objects.create(
                customer_name=customer_name,
                total_price=0,
                waiter=request.user
                
            )
            
            total_price = 0
            for item_id in selected_items:
                item = MenuItem.objects.get(id=item_id)
                order_item = OrderItem.objects.create(order=order, item=item, quantity=1)
                total_price += item.price * order_item.quantity
            
            order.total_price = total_price
            order.save()

            return redirect('order_detail', order_id=order.id)
    
    menu_items = MenuItem.objects.all()
    return render(request, 'restaurantApp/menu_list.html', {'menu_items': menu_items})

@login_required
@user_passes_test(is_waiter_or_chef_or_Owner)
def menu_list_chef(request):
    if request.method == "POST":
        selected_items = request.POST.getlist('selected_items')
        customer_name = request.POST.get('customer_name')
        if selected_items and customer_name:
            order = Order.objects.create(
                customer_name=customer_name,
                total_price=0,
                waiter=request.user  
                
            )
            
            total_price = 0
            for item_id in selected_items:
                item = MenuItem.objects.get(id=item_id)
                order_item = OrderItem.objects.create(order=order, item=item, quantity=1)
                total_price += item.price * order_item.quantity
            
            order.total_price = total_price
            order.save()

            return redirect('order_detail', order_id=order.id)
    
    menu_items = MenuItem.objects.all()
    return render(request, 'restaurantApp/menu_list_chef.html', {'menu_items': menu_items})
@login_required
@user_passes_test(is_waiter_or_chef_or_Owner)
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    return redirect('menu_list')

@login_required
@user_passes_test(is_waiter_or_chef_or_Owner)
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'restaurantApp/order_list.html', {'orders': orders})

@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('menu_list')
    return render(request, 'restaurantApp/order_confirm_delete.html', {'order': order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'restaurantApp/order_detail.html', {'order': order})


@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":

        selected_items = request.POST.getlist('add_items')  
        customer_name = request.POST.get('customer_name')

        if customer_name:
            order.customer_name = customer_name


        for item in order.orderitem_set.all():
            item_id_str = str(item.item.id)
            quantity_str = request.POST.get(f'quantity_{item_id_str}')
            if quantity_str is not None:
                item.quantity = int(quantity_str)
                print(item.quantity)
                item.save()


        selected_item_ids = set(map(int, selected_items))
        total_price = 0

        for item_id in selected_item_ids:
            item = get_object_or_404(MenuItem, id=item_id)
            order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
            if created:
                order_item.quantity = 1
            else:
                order_item.quantity += 1
            order_item.save()


        total_price = sum(
            order_item.item.price * order_item.quantity
            for order_item in order.orderitem_set.all()
        )


        order.total_price = total_price
        order.save()

        return redirect('order_detail', order_id=order.id)


    order_form = OrderForm(instance=order)
    order_item_forms = [OrderItemForm(instance=item) for item in order.orderitem_set.all()]
    menu_items = MenuItem.objects.all()

    return render(request, 'restaurantApp/update_order.html', {
        'order_form': order_form,
        'order_item_forms': order_item_forms,
        'order': order,
        'menu_items': menu_items,
    })

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = 0
            order.waiter = request.user  
            order.save()

            total_price = 0
            for item in form.cleaned_data['items']:
                order_item = OrderItem(order=order, item=item, quantity=1)
                order_item.save()
                total_price += item.price * order_item.quantity

            order.total_price = total_price
            order.save()

            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'restaurantApp/create_order.html', {'form': form})

@login_required
def myorders(request):
    orders = Order.objects.filter(waiter=request.user)
    return render(request, 'restaurantApp/myorders.html', {'orders': orders})



@login_required
@user_passes_test(is_Owner)
def print_order_history(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer Name', 'Order Date', 'Total Amount'])

    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.customer_name, order.order_date, order.total_price])

    return response

@login_required
@user_passes_test(is_Owner)
def clear_all_orders(request):
    Order.objects.all().delete()
    return redirect('create_order')