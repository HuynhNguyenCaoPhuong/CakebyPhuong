from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from classes.models import Course, Category
from . models import Customer, User
from . forms import FormCustomer, FormUser, PasswordResetForm
# Email verification
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils import timezone
from . tokens import account_activation_token
# Reset password
from django.db.models.query_utils import Q



cats = Category.objects.all()

def user_login(request):
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
    })


def user_signup(request):
    form_user = FormUser()
    form_customer = FormCustomer()
    result = ''
    if request.POST.get('btnSignup'):
        form_user = FormUser(request.POST, User)
        form_customer = FormCustomer(request.POST, Customer)
        if form_user.is_valid() and form_customer.is_valid():
            # User
            user = form_user.save(commit=False)
            user.set_password(user.password)
            user.is_active=False
            user.save()

            # Customer
            customer = form_customer.save(commit=False)
            customer.user = user
            customer.tel = form_customer.cleaned_data['tel']
            customer.address = form_customer.cleaned_data['address']
            customer.save()

            # Gửi email xác nhận
            activateEmail(request, user, form_user.cleaned_data.get('email'))

            result = '''
                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                        </symbol>
                    </svg>
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
                        <div>
                            Bạn đã đăng ký thành công! Vui lòng kiểm tra email để xác nhận tài khoản của bạn. Nếu bạn không thấy email trong hộp thư đến của mình, hãy kiểm tra thư mục spam hoặc thư rác của bạn.
                        </div>
                    </div>
                '''
        else:
            if 'username' in form_user.errors:
                result = '''
                <div class="alert alert-danger" role="alert">
                    Đăng ký không thành công! Username đã có người khác sử dụng, vui lòng chọn username khác
                </div>
            '''
            elif 'email' in form_user.errors:
                result = '''
                <div class="alert alert-danger" role="alert">
                    Đăng ký không thành công! Email đã có người khác sử dụng, vui lòng chọn email khác
                </div>
            '''
            else:
                result = '''
                    <div class="alert alert-danger" role="alert">
                        Đăng ký không thành công! Vui lòng kiểm tra lại thông tin.
                    </div>
                '''


    return render(request, 'users/signup.html',{
        'cats': cats,
        'form_user' : form_user,
        'form_customer' : form_customer,
        'result': result,
    })


def activateEmail(request, user, to_email):
    mail_subject = "Kích hoạt tài khoản CakebyPhuong"
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        customer = Customer.objects.get(user=user)
        customer.token = account_activation_token.make_token(user)
        customer.save()
        messages.success(request, f'Xin chào {user}, Vui lòng kiểm tra email  {to_email} để xác nhận tài khoản của bạn. Lưu ý: Nếu bạn không thấy email trong hộp thư đến của mình, hãy kiểm tra thư mục spam hoặc thư rác của bạn.')
    else:
        messages.error(request, f'Có vấn đề trong việc gửi email đến {to_email}, vui lòng kiểm tra lại.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        customer = Customer.objects.get(user=user)
        if customer.token == None:
            messages.error(request, "Liên kết này đã được sử dụng.")
            return redirect("classes:index")
        else:
            user.is_active = True
            customer.token = None
            customer.save()
            user.save()

            messages.success(request, "Cảm ơn đã xác nhận email, bạn có thế đăng nhập và sử dụng.")
            return redirect('users:login')
    else:
        # Kiểm tra xem người dùng chưa được kích hoạt đã lưu trước đó
        confirmation_limit = timezone.now() - timezone.timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT)
        User.objects.filter(is_active=False, date_joined__lt=confirmation_limit).delete()
        messages.error(request, "Không xác nhận được tài khoản.")

    return redirect('classes:index')


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
        facebook = request.POST.get('facebook')
        dc = request.POST.get('address')

        s_customer = request.user
        customer = Customer.objects.get(user__id=s_customer.id)

        if 'avatar' in request.FILES:
            customer.avatar = request.FILES['avatar']
        if ho == "":
            customer.user.last_name =  customer.user.last_name
        else:
            customer.user.last_name = ho
        if ten == "":
            customer.user.first_name = customer.user.first_name
        else:
            customer.user.first_name = ten
        if mail == "":
            customer.user.email = customer.user.email
        else:
            customer.user.email = mail
        if dt == "":
            customer.tel = customer.tel
        else:
            customer.tel = dt
        if dc == "":
            customer.address = customer.address
        else:
            customer.address = dc
        if facebook == "":
            customer.facebook = customer.facebook
        else:
            customer.facebook = facebook

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
    
    return render(request, 'users/my_account.html',{
        'cats': cats,
        'result': result,
    })


def password_reset_request(request):
    if request.POST.get('btnResetpass'):
        user_email = request.POST.get('email')
        user_name = request.POST.get('username')
        associated_user = get_user_model().objects.filter(Q(email=user_email, username=user_name)).first()
        if associated_user:
            subject = "Yêu cầu đặt lại mật khẩu tài khoản CakebyPhuong"
            message = render_to_string("users/template_reset_password.html", {
                'user': associated_user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                'token': account_activation_token.make_token(associated_user),
                "protocol": 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(subject, message, to=[associated_user.email])
            if email.send():
                user = Customer.objects.get(user=associated_user)
                user.token = account_activation_token.make_token(associated_user)
                user.save()
                messages.success(request,
                    """
                    Email khôi phục mật khẩu đã được gửi đi.
                        Chúng tôi đã gửi cho bạn hướng dẫn để thiết lập mật khẩu mới nếu có một tài khoản tồn tại với địa chỉ email bạn đã nhập.
                        Bạn sẽ nhận được email này trong thời gian sớm nhất.Nếu bạn không nhận được email, hãy đảm bảo bạn đã nhập đúng địa chỉ mà bạn đã đăng ký và kiểm tra thư mục thư rác.
                    """
                )
            else:
                messages.error(request, "Có lỗi trong việc đặt lại mật khẩu")

        return redirect('classes:index')

        # for key, error in list(form.errors.items()):
        #     if key == 'captcha' and error[0] == 'This field is required.':
        #         messages.error(request, "You must pass the reCAPTCHA test")
        #         continue

    return render(
        request=request, 
        template_name="users/password_reset.html", 
        )


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        customer = Customer.objects.get(user=user)
        if customer.token == None:
            messages.error(request, "Liên kết này đã được sử dụng.")
            return redirect("classes:index")
        else:
            if request.POST.get('btnUpdatePass'):
                matkhaucapnhat = request.POST.get('new_password')
                matkhaucapnhat_conf = request.POST.get('new_password_conf')

                if matkhaucapnhat==matkhaucapnhat_conf:
                    user.set_password(matkhaucapnhat)
                    user.save()
                    messages.success(request, "Đã đặt lại mật khẩu, vui lòng đăng nhập.")
                    customer.token = None
                    customer.save()
                    return redirect('classes:index')
                else:
                    messages.error(request, "Mật khẩu không khớp, vui lòng thử lại.")


            return render(request, 'users/password_reset_confirm.html',)
    else:
        messages.error(request, "Đường dẫn đã hết hạn")

    messages.error(request, 'Có lỗi, đang chuyển hướng về trang chủ')
    return redirect("classes:index")