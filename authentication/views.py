from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from project import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db import transaction
from .models import Profile
from .decorators import supplier_login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import update_session_auth_hash

from .models import Profile
from products.models import Product
import re  # Import the re module for regular expression support



# Create your views here.
def home(request):
    # Check if the session is locked
    
    return render(request, "authentication/index.html")








'''def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, "Username must be less than 10 characters")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('signup')

        # Password validation
        if len(pass1) <= 6:
            messages.error(request, "Password must be more than 6 characters long")
            return redirect('signup')

        if not re.search(r'[A-Z]', pass1):
            messages.error(request, "Password must contain at least one uppercase letter")
            return redirect('signup')

        if not re.search(r'[a-z]', pass1):
            messages.error(request, "Password must contain at least one lowercase letter")
            return redirect('signup')

        if not re.search(r'[0-9]', pass1):
            messages.error(request, "Password must contain at least one number")
            return redirect('signup')

        if not re.search(r'[\W_]', pass1):
            messages.error(request, "Password must contain at least one symbol")
            return redirect('signup')

        with transaction.atomic():
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()

            Profile.objects.create(user=myuser, user_type='farmer')

        messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account")

        # Welcome email
        subject = "Welcome to Auth"
        message = f"Hello, {myuser.first_name}!\n\nWelcome to Auth.\n\nThank you for visiting our website. We have also sent you a confirmation email, please confirm your email address in order to activate your account.\n\nThanking You,\nSimiyu Michael"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @Auth-Django login"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )

        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")'''

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.db import transaction
import re
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, "Username must be less than 10 characters")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('signup')

        # Password validation
        if len(pass1) <= 6:
            messages.error(request, "Password must be more than 6 characters long")
            return redirect('signup')

        if not re.search(r'[A-Z]', pass1):
            messages.error(request, "Password must contain at least one uppercase letter")
            return redirect('signup')

        if not re.search(r'[a-z]', pass1):
            messages.error(request, "Password must contain at least one lowercase letter")
            return redirect('signup')

        if not re.search(r'[0-9]', pass1):
            messages.error(request, "Password must contain at least one number")
            return redirect('signup')

        if not re.search(r'[\W_]', pass1):
            messages.error(request, "Password must contain at least one symbol")
            return redirect('signup')

        with transaction.atomic():
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()

        messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account")

        # Welcome email
        subject = "Welcome to Auth"
        message = f"Hello, {myuser.first_name}!\n\nWelcome to Auth.\n\nThank you for visiting our website. We have also sent you a confirmation email, please confirm your email address in order to activate your account.\n\nThanking You,\nSimiyu Michael"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @Auth-Django login"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': PasswordResetTokenGenerator().make_token(myuser)
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )

        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")


# authentication/views.py

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from products.models import Product

@login_required
def farmer_index(request):
    fname = request.user.first_name
    products = Product.objects.all()
    return render(request, 'authentication/farmer_index.html', {'fname': fname, 'products': products})



from django.shortcuts import redirect

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            request.session['unlocked'] = True  # Set session as unlocked upon successful login
            return redirect('farmer_index')
        else:
            messages.error(request, "Wrong Credentials")
            return render(request, "authentication/signin.html")  # Render sign-in page with error message

    return render(request, "authentication/signin.html")




'''def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            request.session['unlocked'] = True  # Set session as unlocked upon successful login
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
        else:
            messages.error(request, "Wrong Credentials")
            return render(request, "authentication/signin.html")  # Render sign-in page with error message

    return render(request, "authentication/signin.html")
'''


def signout(request):
    logout(request)
    request.session.flush() 
    messages.success(request, "Logged out successfully")
    return redirect('signin')



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')


@login_required
def lock_screen(request):
    return render(request, 'authentication/lockscreen.html')


@login_required
def unlock_screen(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            request.session['unlocked'] = True  # Unlock the screen
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password')
            return render(request, 'authentication/lockscreen.html')
    return redirect('home')




def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "authentication/password_reset_email.html"
                    context = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Your Site Name',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except Exception as e:
                        messages.error(request, 'Error sending email: {}'.format(str(e)))
                        return redirect('password_reset')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("password_reset_done")
            else:
                messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="authentication/password_reset.html", context={"password_reset_form": password_reset_form})

# views.py

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile  # Adjust the import path as needed

def supplier_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        profile_picture = request.FILES.get('profile_picture')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('supplier_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('supplier_signup')

        if len(username) > 10:
            messages.error(request, "Username must be less than 10 characters")
            return redirect('supplier_signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('supplier_signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('supplier_signup')

        # Password validation
        if len(pass1) <= 6:
            messages.error(request, "Password must be more than 6 characters long")
            return redirect('supplier_signup')

        if not re.search(r'[A-Z]', pass1):
            messages.error(request, "Password must contain at least one uppercase letter")
            return redirect('supplier_signup')

        if not re.search(r'[a-z]', pass1):
            messages.error(request, "Password must contain at least one lowercase letter")
            return redirect('supplier_signup')

        if not re.search(r'[0-9]', pass1):
            messages.error(request, "Password must contain at least one number")
            return redirect('supplier_signup')

        if not re.search(r'[\W_]', pass1):
            messages.error(request, "Password must contain at least one symbol")
            return redirect('supplier_signup')

        try:
            with transaction.atomic():
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name = fname
                myuser.last_name = lname
                myuser.is_active = False
                myuser.save()

                # Check if the user already has a profile
                profile, created = Profile.objects.get_or_create(user=myuser, defaults={'user_type': 'supplier'})
                if created and profile_picture:
                    profile.profile_picture = profile_picture
                    profile.save()
                elif not created:  # Profile already existed
                    if profile_picture:
                        profile.profile_picture = profile_picture
                        profile.save()

            messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account")

            # Send confirmation and welcome emails here

            return redirect('supplier_signin')

        except IntegrityError:
            messages.error(request, "An error occurred while creating your account. Please try again.")
            return redirect('supplier_signup')

    return render(request, "authentication/supplier_signup.html")


# views.py
'''from django.shortcuts import render
from .models import Profile

@login_required
def supplier_dashboard(request):
    user_profile = Profile.objects.get(user=request.user)
    if user_profile.user_type == 'supplier':
        return render(request, "authentication/supplier_dashboard.html")
    else:
        messages.error(request, "Access Denied")
        return redirect('supplier_signin')

@login_required
def farmer_dashboard(request):
    user_profile = Profile.objects.get(user=request.user)
    if user_profile.user_type == 'farmer':
        return render(request, "authentication/farmer_dashboard.html")
    else:
        messages.error(request, "Access Denied")
        return redirect('signin')'''


@login_required(login_url='supplier_signin')
def supplier_index(request):
    # Assuming you have logic here to fetch necessary data for the supplier dashboard
    fname = request.user.first_name  # Get first name of logged-in user
    return render(request, 'authentication/supplier_index.html', {'fname': fname})


def supplier_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            request.session['unlocked'] = True  # Set session as unlocked upon successful login
            return redirect('supplier_index')  # Redirect to supplier dashboard
        else:
            messages.error(request, "Wrong Credentials")
            return render(request, "authentication/supplier_signin.html")  # Render sign-in page with error message

    return render(request, "authentication/supplier_signin.html")


def supplier_signout(request):
    logout(request)
    request.session.flush()  # Flush all session data
    messages.success(request, "Logged out successfully")
    return redirect('home')

def supplier_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and default_token_generator.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')


@login_required
def supplier_lock_screen(request):
    return render(request, 'authentication/supplier_lockscreen.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import supplier_login_required

@supplier_login_required
@never_cache
def supplier_unlock_screen(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            request.session['unlocked'] = True  # Unlock the screen
            return redirect('supplier_index')
        else:
            messages.error(request, 'Incorrect password')
            return render(request, 'authentication/supplier_lockscreen.html')
    return redirect('home')



def supplier_password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "authentication/supplier_password_reset_email.html"
                    context = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Your Site Name',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except Exception as e:
                        messages.error(request, 'Error sending email: {}'.format(str(e)))
                        return redirect('supplier_password_reset')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("supplier_password_reset_done")
            else:
                messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="authentication/supplier_password_reset.html", context={"password_reset_form": password_reset_form})


# authentication/views.py


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SupplierEditForm, ProfileEditForm

@login_required
def edit_supplier(request):
    if request.method == 'POST':
        u_form = SupplierEditForm(request.POST, instance=request.user)
        p_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('edit_supplier')
    else:
        u_form = SupplierEditForm(instance=request.user)
        p_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'authentication/edit_supplier.html', context)

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FarmerEditForm, ProfileEditForm

@login_required
def edit_farmer(request):
    if request.method == 'POST':
        u_form = FarmerEditForm(request.POST, instance=request.user)
        p_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('edit_farmer')
    else:
        u_form = FarmerEditForm(instance=request.user)
        p_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'authentication/edit_farmer.html', context)

