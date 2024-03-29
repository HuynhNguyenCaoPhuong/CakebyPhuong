from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from . models import Category, Course, Blog, Comment, Contact, Blogcomment, PaidCourses

from users.models import User
from . form import FormContact, FormComment, FormBlogcomment

cats = Category.objects.all()


def index(request):
    recent_courses = Course.objects.all()[:6]
    recent_blogs = Blog.objects.all()[:6]

    return render(request, 'classes/index.html',{
        'cats': cats,
        'recent_courses': recent_courses,
        'recent_blogs': recent_blogs,
    })


def course(request):
    recent_courses = Course.objects.all()[:6]
    return render(request, 'classes/course.html',{
        'cats': cats,
        'recent_courses': recent_courses,
    })


def category(request, slug):
    course = Course.objects.filter(category__slug=slug)
    category = Category.objects.get(slug=slug)

    page = request.GET.get('page', 1)
    paginator = Paginator(course, 12)
    courses_pager = paginator.page(page)


    return render(request, 'classes/category.html',{
        'cats': cats,
        'course': courses_pager,
        'category': category,
    })

    # users_id = comments.values_list('user_id')
    # user = User.objects.filter(id__in=users_id)
    # for name in user:
    #     print(name.username)

def single(request, id):
    course = Course.objects.get(id=id)
    paid_course = PaidCourses.objects.filter(course=course)
    category = Category.objects.get(id=course.category_id)
    recent_courses = Course.objects.all()[:3]

    
    comments = Comment.objects.filter(course=course, parent_comment__isnull=True)
    replys = Comment.objects.filter(course=course, parent_comment__isnull=False)

    
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 10)
    commnets_pager = paginator.page(page)


    comment_number = comments.count() + replys.count()
    
    form = FormComment()

    if request.POST.get('button-submit'):
        form = FormComment(request.POST, request.FILES, Comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = course
            comment.user = request.user
            comment.user_first_name = request.user.first_name
            comment.user_last_name = request.user.last_name
            comment.user_avatar = request.user.customer.avatar
            comment.content = form.cleaned_data['content']
            parent_comment_id = request.POST.get('parent_comment')
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                comment.parent_comment = parent_comment
            if 'image' in request.FILES:
                comment.image = request.FILES['image']
            comment.save()
            return redirect('classes:single', id=course.id)
        
    if course.is_free == False and not request.user.username:
        messages.warning(request,"Vui lòng đăng nhập để tham gia khóa học")
        return redirect('users:login')
        
    if course.is_free == False and request.user.username and not paid_course.filter(username=request.user.username).exists():
        messages.error(request, f'Vui lòng thanh toán học phí để được tham gia khóa học')
        return redirect('classes:index')
    

    return render(request, 'classes/single.html', {
        'course': course,
        'category': category,
        'cats': cats,
        'recent_courses': recent_courses,
        'comments': commnets_pager,
        'replys':replys,
        'form': form,
        'comment_number': comment_number,
    })


def blog(request):
    blog = Blog.objects.all()
    recent_blogs = Blog.objects.all()[:3]

    page = request.GET.get('page', 1)
    paginator = Paginator(blog, 12)
    blogs_pager = paginator.page(page)


    return render(request, 'classes/blog.html', {
        'cats': cats,
        'blog': blogs_pager,
        'recent_blogs': recent_blogs,
    })


def tip(request, id):
    blog = Blog.objects.get(id=id)
    recent_blogs = Blog.objects.all()[:9]


    comments = Blogcomment.objects.filter(blog=blog, parent_comment__isnull=True)
    replys = Blogcomment.objects.filter(blog=blog, parent_comment__isnull=False)


    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 10)
    commnets_pager = paginator.page(page)


    comment_number = comments.count() + replys.count()

    
    form = FormBlogcomment()

    if request.POST.get('button-submit'):
        form = FormBlogcomment(request.POST, request.FILES, Blogcomment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.user_first_name = request.user.first_name
            comment.user_last_name = request.user.last_name
            comment.user_avatar = request.user.customer.avatar
            comment.content = form.cleaned_data['content']
            parent_comment_id = request.POST.get('parent_comment')
            if parent_comment_id:
                parent_comment = Blogcomment.objects.get(id=parent_comment_id)
                comment.parent_comment = parent_comment
            if 'image' in request.FILES:
                comment.image = request.FILES['image']
            comment.save()
            return redirect('classes:tip', id=blog.id)

    return render(request, 'classes/tip.html', {
        'cats': cats,
        'blog': blog,
        'recent_blogs': recent_blogs,
        'comments': commnets_pager,
        'replys':replys,
        'form': form,
        'comment_number': comment_number,
    })


def search_course(request):
    course_name = ''
    if request.GET.get('course_name'):
        course_name = request.GET.get('course_name')
        search_courses = Course.objects.filter(name__contains=course_name)

    page = request.GET.get('page', 1)
    paginator = Paginator(search_courses, 12)
    courses_pager = paginator.page(page)


    return render(request, 'classes/category.html', {
        'course': courses_pager,
        'course_name': course_name,
        'cats': cats,
    })


def search_blog(request):
    blog_name = ''
    search_blog = True
    if request.GET.get('blog_name'):
        blog_name = request.GET.get('blog_name')
        search_blogs = Blog.objects.filter(name__contains=blog_name)

    page = request.GET.get('page', 1)
    paginator = Paginator(search_blogs, 12)
    blogs_pager = paginator.page(page)


    return render(request, 'classes/blog.html', {
        'blog': blogs_pager,
        'blog_name': blog_name,
        'search_blog': search_blog,
        'cats': cats,
    })


def about(request):

    return render(request, 'classes/about.html', {
        'cats': cats,
    })


def contact(request):
    form = FormContact()
    result = ''
    if request.POST.get('button-submit'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()
            result = '''
                    <div class = "col-md-12">
                        <div class="alert alert-success" role="alert">
                            Đã gửi tin nhắn thành công!
                        </div>
                    </div>
                    '''
        else:
            result = '''
                <div class = "col-md-12">
                    <div class="alert alert-danger" role="alert">
                        Vui lòng kiểm tra lại nội dung!
                    </div>
                </div>
                '''

    return render(request, 'classes/contact.html', {
        'cats': cats,
        'form': form,
        'result': result,
    })


def teacher(request):

    return render(request, 'classes/teacher.html', {
        'cats': cats,
    })


def custom_301(request, exception):
    return render(request, 'classes/301.html', status=301)


def custom_403(request, exception):
    return render(request, 'classes/403.html', status=403)


def custom_404(request, exception):
    return render(request, 'classes/404.html', status=404)


def custom_505(request, exception):
    return render(request, 'classes/505.html', status=505)


