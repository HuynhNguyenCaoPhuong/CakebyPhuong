from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from cart.models import Order, OrderItem
# from cart.cart import Cart
from classes.models import Course, Category
from . models import Customer
from . forms import FormCustomer, FormUser

cats = Category.objects.all()

def user_login(request):
    # cart = Cart(request)
    result = ''
    if request.POST.get('btnLogin'):
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        auth = authenticate(request, username=username, password=password)

        if auth:
            login(request, auth)
            return redirect('classes:index')
        else:
            result = '''
                <div class="alert alert-danger" role="alert">
                    Đăng nhập không thành công!
                </div>
            '''

    return render(request, 'users/login.html',{
        'cats': cats,
        'result': result,
        # 'cart': cart,
    })


def user_signup(request):
    # cart = Cart(request)
    form_user = FormUser()
    form_customer = FormCustomer()
    result = ''
    if request.POST.get('btnSignup'):
        form_user = FormUser(request.POST, User)
        form_customer = FormCustomer(request.POST, Customer)
        if form_user.is_valid() and form_customer.is_valid():
            # User
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            # Customer
            customer = form_customer.save(commit=False)
            customer.user = user
            customer.tel = form_customer.cleaned_data['tel']
            customer.address = form_customer.cleaned_data['address']
            customer.save()

            result = '''
                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                        </symbol>
                    </svg>
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
                        <div>
                            Bạn đã đăng ký thành công!
                        </div>
                    </div>
                '''
        else:
            result = '''
                <div class="alert alert-danger" role="alert">
                    Đăng ký không thành công!
                </div>
            '''


    return render(request, 'users/signup.html',{
        'cats': cats,
        'form_user' : form_user,
        'form_customer' : form_customer,
        'result': result,
        # 'cart': cart,
    })

def user_logout (request):
    logout(request)
    return redirect('users:login')


def my_account(request):
    result = ''
    if not request.user.username:
        messages.warning(request,"Vui lòng đăng nhập lại.")
        return redirect('users:login')
    
    
    if request.POST.get('btnUpdateUser'):
        ho = request.POST.get('last_name')
        ten = request.POST.get('first_name')
        dt = request.POST.get('mobile')
        mail = request.POST.get('email')
        dc = request.POST.get('address')

        s_customer = request.user
        customer = Customer.objects.get(user__id=s_customer.id)
        customer.user.last_name = ho
        customer.user.first_name = ten
        customer.user.email = mail
        customer.tel = dt
        customer.address = dc
        customer.save()
        customer.user.save()

        s_customer.last_name = ho
        s_customer.first_name = ten
        result = '''
                <div class = "col-md-12">
                    <div class="alert alert-success" role="alert">
                        Cập nhật thông tin thành công!
                    </div>
                </div>
                '''
        
    if request.POST.get('btnUpdatePass'):
        s_customer = request.user
        matkhauhientai = request.POST.get('current_password')
        matkhaucapnhat = request.POST.get('new_password')
        matkhaucapnhat_conf = request.POST.get('new_password_conf')

        if s_customer.check_password(matkhauhientai) and matkhaucapnhat==matkhaucapnhat_conf:
            s_customer.set_password(matkhaucapnhat)
            s_customer.save()
            result = '''
                    <div class = "col-md-12">
                        <div class="alert alert-success" role="alert">
                            Cập nhật mật khẩu thành công!
                        </div>
                    </div>
                    '''
            
        else:
            result = '''
                <div class = "col-md-12">
                    <div class="alert alert-danger" role="alert">
                        Vui lòng kiểm tra lại mật khẩu!
                    </div>
                </div>
                '''
    
    # cart = Cart(request)
    # orders = Order.objects.filter(username=request.user.username)
    # dict_orders = {}
    # for order in orders:
    #     items = list(OrderItem.objects.filter(order=order.id).values())
    #     for item in items:
    #         product = Product.objects.get(id=item['product_id'])
    #         item['product_name'] = product.name
    #         item['product_image'] = product.image_product
    #         item['total_price'] = order.total
    #     else:
    #         dict_orders_items = {
    #             order.id: items
    #         }
    #         dict_orders.update(dict_orders_items)
            
    return render(request, 'users/my_account.html',{
        'cats': cats,
        'result': result,
        # 'cart': cart,
        # 'orders': orders,
        # 'dict_orders': dict_orders,
    })