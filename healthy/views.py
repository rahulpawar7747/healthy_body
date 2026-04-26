from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from google import genai

client = genai.Client()


def aiapp_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        reply = response.text if hasattr(response, "text") else str(response)
        return JsonResponse({"reply": response.text})

    return render(request, "Normal.html")
def login_page(request):
        if request.method=='POST':
            username=request.POST.get('username')
            pass1=request.POST.get('pass')
            user=authenticate(request,username=username,password=pass1)
            if user is not None:
                 login(request,user)
                 return redirect('home')
            else:
                 messages.error(request, "Invalid username or password")
        return render(request, 'login.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def SignuPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # ✅ Email format check
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address")
            return redirect('signup')

        # ✅ Password match
        if pass1 != pass2:
            messages.error(request, "Passwords are not matching")
            return redirect('signup')

        # ✅ Username exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        # ✅ Email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        # ✅ Create user
        User.objects.create_user(username=uname, email=email, password=pass1)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'signup.html')
def LogoutPage(request):
     logout(request)
     return redirect('login')

def bmi(request):
    context = {"progress": 0}
    if request.method == "POST":
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        weight = request.POST.get("weight")
        height = request.POST.get("height")

        if age and weight and height:
            age = int(age)
            weight = float(weight)
            height = float(height) * 0.3048

            bmi = round(weight / (height * height), 2)
            request.session['age'] = age
            request.session['gender'] = gender
            request.session['weight'] = weight
            request.session['height'] = height
            request.session['bmi'] = bmi
            if bmi < 18.5:
                status = "Underweight"
                progress = 25

            elif bmi < 25:
                status = "Normal"
                progress = 50

            elif bmi < 30:
                status = "Overweight"
                progress = 75

            else:
                status = "Obese"
                progress = 100

            context = {
                "bmi": bmi,
                "status": status,
                "progress": progress,
                "age": age,
                "gender": gender
            }
            if status == "Underweight":
                  return render(request, "Underweight.html",context)
            if status == "Overweight":
                  return render(request, "Overweight.html",context)
            if status == "Normal":
                  return render(request, "Normal.html",context)
            if status == "Obese":
                  return render(request, "Obese.html",context)
    return render(request, "BMI.html", context)
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Yaha aap chahe to DB me save karo ya email bhejo
        print(name, email, subject, message)

        return redirect('/contact/')

    return render(request, 'contact.html')

def weight_gain(request):
    return render(request, 'weight_gain.html')
def diet(request):
    return render(request, 'Diet.html')
def exercise(request):
    return render(request, 'Exercise.html')
def privacy(request):
    return render(request, 'privacy.html')
def About(request):
     return render(request, 'about.html')
def Excercise(request):
     return render(request, 'Exercise.html')
def help(request):
     return render(request, 'help.html')
def Faq(request):
     return render(request, 'Faq.html')
def Terms(request):
     return render(request, 'Terms.html')
def Feedback(request):
     return render(request, 'Feedback.html')
def Underweight(request):
    return render(request, "Underweight.html")
def Overweight(request):
    return render(request, "Overweight.html")
def Obese(request):
    return render(request, "Obese.html")