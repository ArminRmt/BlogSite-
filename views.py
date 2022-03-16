from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import *
from .forms import CommentForm, OrderForm, StockHistorySearchForm
from .models import Post
from django.views.generic import ListView ,CreateView,DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
import time
from django.db.models import Q







def home_page(request):

    sliders_pic = Post.objects.filter(promote = True)[0:1].get()
    sliders_pic1 = Post.objects.filter(promote = True)[1]
    sliders_pic2 = Post.objects.filter(promote = True)[2]
    
    
    most_recent = Post.objects.order_by('-created_date')[:5]
    most_visited = Post.objects.order_by('-viewers')[:5]
    
        # پگنیگیتور اماده دنگو

    object_list = Post.objects.all()
    paginator = Paginator(object_list, 6)  
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
            # اگر صفحه عددنبود صفحه اول رو برگردونه
        posts = paginator.page(1)
    except EmptyPage:
        # اگر صفحه موجود نبود صفحه اخر رو برگردونه
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'app/index.html',
                  {'page': page,
                   'posts': posts ,
                   'most_visited':most_visited,
                   'most_recent':most_recent,
                   'sliders_pic':sliders_pic,
                   'sliders_pic1':sliders_pic1,
                   'sliders_pic2':sliders_pic2})
    
 
 
 
 
    
def date_view(request):
    
    date_view1 = request.GET['date1']
    date_view2 = request.GET['date2']
    posts =Post.objects.filter(Q(created_date__gte=date_view1) & Q(created_date__lte=date_view2))

    
    
    # paginator = Paginator(posts, 2)
    # page = request.GET.get('page1')
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)
    
        
    
    
    return render(request, 'app/news-list.html', {'posts':posts })



    
    
def list_akhbar(request):
    

        
    
    object_list = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')
    paginator= Paginator(object_list, 2)
    page = request.GET.get('page1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
        
        
    object_list2 = Post.objects.order_by('-viewers' , '-created_date')  #صعودی
    # object_list2 = Post.objects.order_by('-viewers' , '-created_date')[::-1]   # نزولی
    
    paginator = Paginator(object_list2, 2)
    page = request.GET.get('page2')
    try:
        object_list2 = paginator.page(page)
    except PageNotAnInteger:
        object_list2 = paginator.page(1)
    except EmptyPage:
        object_list2 = paginator.page(paginator.num_pages)
        
        

                
        
    
    return render(request,
            'app/news-list.html',
            {'object_list': object_list,
            'object_list2':object_list2, 
            })
    
    
    
# سرچ با استفاده از لیست ویو
    
class SearchView(ListView):

    model = Post
    template_name = 'app/search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('search')
       if query:
          postresult = Post.objects.filter(title__contains=query)
          postresult2 = Post.objects.filter(text__contains=query)
          from itertools import chain
          result_list = list(chain(postresult, postresult2))
          result = result_list
       else:
           result = None
       return result
    
    



# صفحه هر موضوع



def Edame_Akhbar(request,id):
    post = get_object_or_404(Post,id = id)
    return render(request, 'app/index3.html', {'post': post})




def Varzeshi(request):
    posts = Post.objects.filter(title2 = 'ورزشی')
    return render(request, 'app/Varzeshi.html', {'posts': posts})


def Elmi(request):
    posts = Post.objects.filter(title2 = 'علمی')
    return render(request, 'app/elmi.html', {'posts': posts})


def Siasi(request):
    posts = Post.objects.filter(title2 = 'سیاسی')
    return render(request, 'app/siasi.html', {'posts': posts})


def Eghtesadi(request):
    posts = Post.objects.filter(title2 = 'اقتصادی')
    return render(request, 'app/eghtesadi.html', {'posts': posts})




# ثبت نام 

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "نام وجود دارد ! نام دیگری وارد کنید")
            return redirect("signup")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "کاربری با این ایمیل ثبت نام کرده است!")
            return redirect("signup")
        
        if len(username)>20:
            messages.error(request, "نام کاربری باید زیر 20 کاراکتر باشه")
            return redirect("signup")
        
        if pass1 != pass2:
            messages.error(request, "پسورد ها با هم سازگاری ندارند")
            return redirect("signup")
        
        if not username.isalnum():
            messages.error(request, "نام کاربری باید عدد یا کاراکتر باشد")
            return redirect("signup")
        
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.is_active = False
        myuser.save()
        messages.success(request, "اکانت شما با موفقیت ساخته شد")
        
        # خوش امد گویی ایمیل
        subject = "به خبرگزاری فارس خوش امدید"
        message = "سلام " + myuser.first_name + "!! \n" + "به خبرگزاری فارس خوش امدید!! \n. ایمیل خود را کانفیرم کنید. \n\nبا تشکر\nآرمین رحمتی"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        return redirect('signin')

        
        
    return render(request, "app/index4.html")
 




# ورود
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.username
            messages.success(request, "با موفقیت وارد شدید")
            return render(request, "app/index.html",{"fname":fname})
        else:
            messages.error(request, "خطا")
            return redirect('home')
    
    return render(request, "app/index5.html")



def signout(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید")
    return redirect('home')




# اپدیت هر پست


def updatePost(request, pk):

	order = Post.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'app/post.html', context)




#حذف هر پست


def deletePost(request, pk):
	order = Post.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'app/delete.html', context)






# ساخت پست جدید


def CreatePost(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/')

	return render(request, 'app/post.html', {'form':form})




#ادامه مطلب هر پست



def post_detail(request, pk):
    
    
    post = get_object_or_404(Post, id=pk)
    post.viewers = post.viewers + 1
    post.save()

    
    
    # لیست کامت های پدر فعال
    comments = post.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        # کامنت اضافه شد
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # ایدی کامنت پدر را از اینپوت غیر فعال میگیره
            try:
                # ایدی عددی
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # اگر کامنتی با ایدی پدر تابمیت شده بود ایدی ابجکت پدر را بگیر
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # اگر ابجکت پدر موجود بود
                if parent_obj:
                    # ابجکت ریپلای کامنت
                    replay_comment = comment_form.save(commit=False)
                    # وصل ابجکت پدر به کامنت ریپلای
                    replay_comment.parent = parent_obj
            # کامنت جدید معمولی
            # ایجاد ابجکت کانت معمولی بدون سیو در دیتابیس
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect("home")
    else:
        comment_form = CommentForm()
    return render(request,
                  'app/index3.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})

    
