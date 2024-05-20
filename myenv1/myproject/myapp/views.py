from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.cache import never_cache
import requests
import razorpay
from django.conf import settings

# Create your views here.     
def signup(request):
    if request.POST:
        try:
            User.objects.get(email = request.POST["uemail"])
            msg = "email already exists !!"
            messages.error(request,'Email alredy exists!!!')
            return redirect('login')

        except:
            if request.POST["upassword"] == request.POST["ucpassword"]:
                User.objects.create(
                    email = request.POST["uemail"],
                    name = request.POST["uname"],
                    contact = request.POST["ucontact"],
                    password = request.POST["upassword"],
                    picture = request.FILES["picture"],
                    role = request.POST['srole']
                )
                msg = "signup successfulyy."
                messages.success(request,msg)
                return redirect('login')
                
            else:
                msg = "password and confirm password does not match!!"
                messages.error(request,msg) 
                return render(request,'signup.html')
    else:
       return render(request,'signup.html')
    
def login(request):
    if request.POST:
        try:
            user = User.objects.get(email = request.POST["uemail"])
            if user.password == request.POST["password"]:
                if user.role == "buyer":
                    wishlist = Wishlist.objects.filter(user = user)
                    request.session['email'] = user.email
                    request.session['name'] = user.name
                    request.session['password'] = user.password
                    request.session['picture'] = user.picture.url
                    request.session['contact'] = user.contact
                    request.session['wishlist_count'] = len(wishlist)
                    msg = "Login successfully..."
                    messages.success(request,msg)
                    return redirect('home')
                
                elif user.role == "seller":
                    request.session['email'] = user.email
                    request.session['name'] = user.name
                    request.session['password'] = user.password
                    request.session['picture'] = user.picture.url
                    request.session['contact'] = user.contact
                    msg = "Login successfully..."
                    messages.success(request,msg)
                    return redirect('sindex')
                else:
                    return render(request,'login.html')
            else:
                msg = "Wrong password !!"
                messages.error(request,msg)
                return render(request,'login.html')
        except:
            msg = "email does not register !!"
            messages.error(request,msg)
            return render(request,'login.html')
    else:
        return render(request,'login.html')
    
def logout(request):
    if request.session['email']:
        user = User.objects.get(email = request.session["email"])
        del request.session['email']
        del request.session['name']
        del request.session['password']
        del request.session['picture']
        del request.session['contact']
        if user.role == "buyer":
            del request.session['wishlist_count']
        msg = "Logout Successfully ...."
        messages.success(request,msg)
        return redirect('home')
    else:
        return render(request,'index.html')
    
def mymail(subject, template, to, context, otp):
    subject = subject
    template_str = 'myapp/' + template +'.html'
    context['otp'] = otp
    html_message = render_to_string(template_str, context)
    plain_message = strip_tags(html_message)
    from_email = 'smitchauhan2712@gmail.com'
    send_mail(
        subject,
        plain_message,
        from_email,
        [to],
        html_message=html_message,
        fail_silently=False,
    )


def fpass(request):
    if request.POST:
        try:
            #print('hello')
            user = User.objects.get(email = request.POST['email'])
            email = request.POST['email']
            otp = random.randint(1001,9999)
            print(otp)
            request.session['email'] = email
            request.session['sotp'] = otp
            #print("=====================================",otp)
            subject = 'OTP for reset password'
            template = "etemplate"
            to = user.email
            context = {'user':user.name}
            mymail(subject, template, to, context,otp)
            print('======================send otp successfully')
            return redirect("otp")
    
        except:
            msg = 'email does not  exist!'
            messages.warning(request,msg)
            return render(request,'fpass.html')
    else:
        return render(request,'fpass.html')
   
def otp(request):
    if request.POST:
        print("hello")   
        otp = int(request.session['sotp'])
        uotp = int(request.POST['uotp'])
        print(otp)
        print(uotp)
        print(type(otp))
        print(type(uotp))
        
        if otp==uotp:
            print("Hello")
            del request.session['sotp']
            #del request.session['email']
            return redirect("newpass")
        else:
            msg = 'Wrong otp please try again...!'
            messages.warning(request,msg)
            return render(request,"otp.html")
        
    else:
        return render(request,"otp.html") 
    
def newpass(request):
    user = User.objects.get(email = request.session['email'])
    if request.POST:
        if request.POST['npassword'] == request.POST['cpassword']:
            print("============Hello newpass page")
            print(user.password)
            user.password = request.POST['npassword']
            print('===================update pass',user.password)
            user.save()
            del request.session['email']
            msg = 'password successfully reset...!'
            messages.success(request,msg)
            return redirect("login")
        
        else:
            msg = 'new password and confirm password does not match!'
            messages.error(request,msg)
            return render(request,"newpass.html",{'msg':msg})  
    else:
        return render(request,"newpass.html")

def profile(request):
    user = User.objects.get(email = request.session['email'])
    print(user.email)
    try:
        if request.POST:
            print("hello")
            user.picture = request.FILES["picture"]
            user.save() 
            request.session['picture'] = user.picture.url
            return render(request ,'profile.html',{'user':user})
        else:
            print("-------------------------------------------------")
            return render(request ,'profile.html',{'user':user})     
    except: 
        pass
    
def changepassword(request):
    if request.session['email']:
        if request.POST:
            if request.session['password'] == request.POST['password']:
                if request.POST['npassword'] == request.POST['cpassword']:
                    user = User.objects.get(email=request.session['email'])
                    user.password = request.POST['npassword']
                    user.save()
                    del request.session['email']
                    del request.session['name']
                    del request.session['password']
                    del request.session['contact']
                    del request.session['picture']
                    if User.role == 'buyer':
                        msg = "password Successfully change...."
                        messages.success(request,msg)
                        return redirect('login')
                    else:
                        msg = "password Successfully change...."
                        messages.success(request,msg)
                        return redirect('login')
                else:
                    if User.role == 'buyer':
                        msg = 'Password and confirm Password Does Not Match'
                        messages.warning(request,msg)
                        return render(request,'edit_profile.html')
                    else:
                        msg = 'Password and confirm Password Does Not Match'
                        messages.warning(request,msg)
                        return render(request,'schangepassword.html')
                
            else:
                if User.role == 'buyer':
                    msg = 'Old Password is Wrong Please Try Again...!'
                    messages.warning(request,msg)
                    return render(request,'edit_profile.html')
                else:
                    msg = 'Old Password is Wrong Please Try Again...!'
                    messages.warning(request,msg)
                    return render(request,'schangepassword.html')
        else:
            if User.role == 'buyer':
                return render(request,'edit_profile.html')
            else:
                return render(request,'schangepassword.html')

    else:
        if User.role == 'buyer':
            return render(request,'login.html')
        else:
            return render(request,'schangepassword.html')
            

def edit_profile(request):
    if request.session['email']:
        if request.POST:
            if request.session['password'] == request.POST['password']:
                user = User.objects.get(email=request.session['email'])
                user.name = request.POST['name']
                user.contact = request.POST['contact']
                user.email = request.POST['email']
                user.save()
                del request.session['email']
                del request.session['name']
                del request.session['contact']
                request.session['email'] = user.email
                request.session['name'] = user.name
                request.session['contact'] = user.contact
                msg = "Profile updated Successfully!"
                messages.success(request,msg)
                return redirect('profile')
                 
            else:
                msg = 'Old Password is Wrong Please Try Again...!'
                messages.warning(request,msg)
                return render(request,'edit_profile.html')
        else:
            return render(request,'edit_profile.html')
    else:
        return redirect('login')
    


def home(request): 
    product = Product.objects.all()
    return render(request,'index.html',{'product':product})

def product(request,cat):
    # product = product()
    if cat=="all":
        product = Product.objects.all()
        print(product)
    elif cat=="Men":  
        product = Product.objects.filter(categorie="Men") 
    elif cat=="Women":  
        product = Product.objects.filter(categorie="Women") 
    elif cat=="Chiled":  
        product = Product.objects.filter(categorie="Chiled") 
        
    return render(request,'product.html',{'product':product})
   
    
def pbdetail(request,pk):
    product = Product.objects.get(pk = pk)
    try:
        addcart = Cart.objects.get(product = product)
        print("===",addcart)
        return render(request,'pbdetail.html', {'product':product,'addcart':addcart})
    except:
        return render(request,'pbdetail.html', {'product':product})
    
def addtowishlist(request,pk):
    if 'email' in request.session:
        user = User.objects.get(email = request.session['email'])
        product = Product.objects.get(pk = pk)
        try:
            Wishlist.objects.get(user = user , product = product)
            return render(request,'product.html')
        except:
            Wishlist.objects.create(user = user , product = product)
            return redirect('wishlist')
    else:
        return redirect('home')
     
def product_detail(request):
    return render(request,"product-detail.html")   
    
def wishlist(request):
    if 'email' in request.session:
        user = User.objects.get(email = request.session['email'])
        wishlist = Wishlist.objects.filter(user = user)
        request.session['wishlist_count'] = len(wishlist)
        return render(request,'wishlist.html',{'wishlist':wishlist})
    else:
        return redirect('home')

def removewishlist(request,pk):
    user = User.objects.get(email = request.session['email'])
    wishlist = Wishlist.objects.get(user = user , pk = pk)
    wishlist.delete()
    return redirect('wishlist')


def blog(request):
    return render(request,'blog.html')

def blogdetail(request):
    return render(request,'blog-detail.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

#===================================seller======================================

def sindex(request):
    return render(request,'sindex.html')

def addproduct(request):
    if 'email' in request.session:
        seller = User.objects.get(email = request.session['email'])
        if request.POST:
            Product.objects.create(
                user_id = seller,
                categorie = request.POST['categorie'],
                size = request.POST['size'],
                brand = request.POST['brand'],
                pname = request.POST['pname'],
                ppicture = request.FILES['ppicture'],
                disc = request.POST['disc'],
                pprice = request.POST['pprice']
            )
            msg = "Product successfully added"
            messages.success(request,msg)
            return render(request,'addproduct.html')
        else:
            return render(request,'addproduct.html')
    else:
        msg = "Please login !!"
        messages.error(request,msg)
        return redirect('login')

def viewproduct(request,cat):
    if 'email' in request.session:  
        seller = User.objects.get(email = request.session['email'])
        # product = Product.objects.filter(user_id = seller)  
        if cat=="all":
            product = Product.objects.filter(user_id = seller)
            print(product)
        elif cat=="Men":  
            product = Product.objects.filter(categorie="Men",user_id = seller) 
        elif cat=="Women":  
            product = Product.objects.filter(categorie="Women",user_id = seller) 
        elif cat=="Chiled":  
            product = Product.objects.filter(categorie="Chiled",user_id = seller)        
        return render(request,'viewproduct.html',{'product':product})
       
    else:
        msg = "Please login !!"
        messages.error(request,msg)
        return redirect('login')

def sprofile(request):
    if request.session['email']:
        user = User.objects.get(email = request.session['email'])
        print(user.email)
        try:
            if request.POST:
                print("hello")
                user.picture = request.FILES["picture"]
                user.save() 
                request.session['picture'] = user.picture.url
                return render(request ,'sprofile.html',{'user':user})
            else:
                print("-------------------------------------------------")
                return render(request ,'sprofile.html',{'user':user})     
        except: 
            pass

    else:
        return render(request,'login.html')


def pdetail(request,pk):
    product = Product.objects.get(pk = pk)
    return render(request,"pdetail.html" , {'product':product})

def pedit(request,pk):
    if 'email' in request.session:
        product = Product.objects.get(pk = pk)
        if request.POST:
            product.categorie = request.POST['categorie']
            product.size = request.POST['size']
            product.brand = request.POST['brand']
            product.pname = request.POST['pname']
            product.ppicture = request.FILES['ppicture']
            product.disc = request.POST['disc']
            product.pprice= request.POST['pprice']
            
            product.save()
            msg = "Edit successfully"
            messages.success(request,msg)
            return render(request,'pdetail.html',{'product':product})
        else:
            return render(request,'pedit.html',{'product':product})
    else:
        msg = "Please login !!"
        messages.error(request,msg)
        return redirect('login')

def pdelete(request,pk):
    product = Product.objects.get(pk = pk)
    product.delete()
    
    if 'email' in request.session:  
        seller = User.objects.get(email = request.session['email'])
        product = Product.objects.filter(user_id = seller)  
        msg = "Product successfully delete"
        messages.success(request,msg)
        return render(request,'viewproduct.html',{'product':product})
       
    else:
        msg = "Please login !!"
        messages.error(request,msg)
        return redirect('login')
    
    
@never_cache
def add_to_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    Cart.objects.create(user=user,
                        product=product,
                        cart_price=product.pprice,
                        total_price=product.pprice,
                        quantity=1
                        )
    return redirect("shoping_cart")

@never_cache
def shoping_cart(request):
    if not request.session['email']:
        msg="Please login first!!!"
        messages.info(request,msg)
        return render(request,"product.html")
        
    else:
        subtotal=0
        ship=0
        user=User.objects.get(email=request.session['email']) 
        cart=Cart.objects.filter(user=user)
        request.session['cart']=len(cart)
        # print("======================",request.session['cart'])
        for i in cart:
            subtotal+=i.total_price
        if subtotal<=20000:
            ship=100
            total=subtotal+ship
        else:
            total=subtotal
        request.session['total'] = total
        return render(request,"shoping_cart.html",{'cart':cart,'subtotal':subtotal,'ship':ship,'user':user,'total':total})

@never_cache    
def delete_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    cart=Cart.objects.get(user=user,product=product)
    cart.delete()
    return redirect("shoping_cart")

@never_cache
def change_quantity(request,pk):
    cart=Cart.objects.get(pk=pk)
    cart.quantity=int(request.POST['qty'])
    request.session['cart_quantity'] = cart.quantity
    print("Cart Quantity in session:", request.session.get('cart_quantity'))
    cart.save()
    cart.total_price=cart.cart_price*cart.quantity
    
    cart.save()
    return redirect("shoping_cart") 

@never_cache
def order_details(request):
    user=User.objects.get(email=request.session['email'])
    if request.POST:
        try:
            print("hii smit")
            order_details = Order_details.objects.create(
                user=user,
                address = request.POST['address'],
                pincode = request.POST['pincode']  
            )
            order_details.save()
            print("hii")
            return render(request,"payment.html")
        except:
            print("hii nikhil")
            return redirect("payment")
        
    else:
        return render(request,"payment.html")
    
def check_out(request):
    user=User.objects.get(email=request.session['email'])
    order=Order_details.objects.filter(user=user)
    return render(request,"check_out.html",{'user':user,'order':order})

@never_cache
def payment(request):
    user=User.objects.get(email=request.session['email'])
    order=Order_details.objects.filter(user=user)
    cart=Cart.objects.filter(user=user)
    total=request.session['total']
    print("================",total)

    client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': total * 100, 'currency': 'INR', 'payment_capture': 1})
    context = {
        'payment': payment,
        }
    print("=======================",context)
    print("&7777777777777777777777",payment)
    
    return render(request,"payment.html",{'user':user,'order':order,'context':context})

@never_cache
def success(request):
    try:
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.filter(user=user,pyment_status=False)

        for i in cart:
            i.pyment_status=True
            i.save()
        return render(request,"success.html",{'cart':cart})
    except:
        return redirect("home")
