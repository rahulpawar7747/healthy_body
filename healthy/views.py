from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from django.conf import settings
import json
import os
import google.generativeai as genai
from .models import UserDietPlan,BMIRecord,UserHealthPlan,DietSchedule,UserDiet,UserExercise
import re
from .models import HealthProgress
from .utils import convert_table_to_html, send_health_mail
from datetime import datetime, time
from django.core.mail import send_mail  # ← jo tum already use karte ho


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def cron_trigger_mails(request):
    key = request.GET.get("key")
    if key != "rahul_secret_key_123":
        return HttpResponse("Unauthorized", status=401)

    for user in User.objects.all():

        diet_obj = UserDiet.objects.filter(user=user).last()
        ex_obj = UserExercise.objects.filter(user=user).last()

        if diet_obj and ex_obj and user.email:

            diet_html = convert_table_to_html(diet_obj.diet_reply)
            exercise_html = convert_table_to_html(ex_obj.exercise_reply)

            html_message = f"""
            <h1>🎉 Your AI Health Plan</h1>

            <h2>🥗 Diet Plan</h2>
            {diet_html}

            <h2>💪 Exercise Plan</h2>
            {exercise_html}
            """

            send_health_mail(user, "🎉 Your AI Health Plan", html_message)

    return HttpResponse("Emails Sent Successfully")

def send_scheduled_emails(request):
    # simple security key
    key = request.GET.get("key")
    if key != "MY_SECRET_123":
        return HttpResponse("Unauthorized", status=401)

    for user in User.objects.all():
        if user.email:
            send_mail(
                "Your Diet & Exercise Plan",
                "Hello! This is your scheduled reminder.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

    return HttpResponse("Emails sent")



@login_required(login_url='login')
# @csrf_exempt
def aiapp_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message")

        # ✅ CHECK EXISTING PLAN
        existing_diet = UserDiet.objects.filter(user=request.user).first()
        existing_ex = UserExercise.objects.filter(user=request.user).first()

        if existing_diet and existing_ex:
            return JsonResponse({
                "diet": existing_diet.diet_reply,
                "exercise": existing_ex.exercise_reply,
                "from_db": True
            })

        bmi = request.session.get("bmi", "")
        status = request.session.get("status", "")
        age = request.session.get("age", "")
        gender = request.session.get("gender", "")
        # Budget aur food type message se nikaalo
        budget_match = re.search(r'\d+', user_message)
        budget = int(budget_match.group()) if budget_match else 0
        food_type = "Vegetarian" if "vegetarian" in user_message.lower() else "Non-Vegetarian"
        body_goal = "general fitness"
        if "body goal is" in user_message.lower():
            lines = user_message.splitlines()
            for line in lines:
                if "body goal is" in line.lower():
                    body_goal = line.replace("My body goal is", "").strip()
                    break
        # body_goal = body_goal_match.group(1) if body_goal_match else "general fitness"

          # AI ko proper instruction
        
        full_prompt = f"""
        You are a professional Indian health planner.

        User Details:
        BMI: {bmi}
        Status: {status}
        Age: {age}
        Gender: {gender}
        Budget: ₹{budget}
        Food Type: {food_type}
        Body Goal: {body_goal}
        First give DIET PLAN in table format which includes meals for each day.
        Then give EXERCISE PLAN in table format which includes exercises for each day.
        IMPORTANT:
            Do NOT write any introduction, explanation, greeting, advice, or paragraph.
            Output ONLY two sections:

        First give DIET PLAN in table format which includes meals for each day.
        Then give EXERCISE PLAN in table format which includes exercises for each day.
        IMPORTANT:
            Do NOT write any introduction, explanation, greeting, advice, or paragraph.
            Output ONLY two sections:


        Strict Rules:
        - Indian foods only
        - Budget friendly
        - Separate sections clearly as:

        DIET PLAN:
        (table)

        EXERCISE PLAN:
        (table)
        """
        try:
            response = model.generate_content(full_prompt)
            reply = response.text if hasattr(response, "text") else "No response from AI"
        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})
        # 🔥 Split diet and exercise
        diet_match = re.search(r'(?is)diet plan\s*:?(.*?)(?=exercise plan)', reply)
        exercise_match = re.search(r'(?is)exercise plan\s*:?(.*)', reply)

        diet_part = diet_match.group(1).strip() if diet_match else ""
        exercise_part = exercise_match.group(1).strip() if exercise_match else ""

        # Save Diet
        # UserDietPlan.objects.update_or_create(
        #     user=request.user,
        #     defaults={
        #         "bmi": bmi,
        #         "status": status,
        #         "budget": budget,
        #         "food_type": food_type,
        #         "body_goal": body_goal,
        #         "ai_reply": diet_part
        #     }
        # )

        # Save Exercise
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        UserDiet.objects.update_or_create(
            user=request.user,
            defaults={"diet_reply": diet_part}
        )

        UserExercise.objects.update_or_create(
            user=request.user,
            defaults={"exercise_reply": exercise_part}
)


        today = datetime.now().strftime("%d %b %Y")

        # diet_html = convert_table_to_html(diet_part)
        # exercise_html = convert_table_to_html(exercise_part)

        html_message = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            .card {{
                max-width:700px;
                margin:auto;
                padding:15px;
            }}
            table {{
                width:100%;
                border-collapse:collapse;
            }}
            th, td {{
                border:1px solid #444;
                padding:8px;
                text-align:center;
                font-size:14px;
            }}
            h2 {{
                background:#4CAF50;
                color:white;
                padding:10px;
            }}
        </style>
        </head>
        <body>

        <div class="card">

        <h1 style="text-align:center">🎉 Your AI Health Plan</h1>
        <p style="text-align:center;color:gray">{today}</p>

        <h2>🥗 Diet Plan</h2>
        {diet_html}

        <br><br>

        <h2>💪 Exercise Plan</h2>
        {exercise_html}

        </div>

        </body>
        </html>
        """

    send_health_mail(request.user, "🎉 Your AI Health Plan", html_message)



    full_reply = diet_part + "\n\n<h2>EXERCISE PLAN</h2>\n" + exercise_part
    return JsonResponse({
    "diet": diet_part,
    "exercise": exercise_part
        })

    return render(request, "ai_planner.html")

@login_required
def progress_chart(request):
    data = HealthProgress.objects.filter(user=request.user).order_by('date')

    dates = [d.date.strftime("%d-%b") for d in data]
    bmis = [d.bmi for d in data]
    weights = [d.weight for d in data]
    goal_bmi = [22 for _ in data]  # ideal BMI line

    return render(request, "progress.html", {
            "dates_json": json.dumps(dates),
            "bmis_json": json.dumps(bmis),
            "weights_json": json.dumps(weights),
            "goal_bmi_json": json.dumps(goal_bmi),
        })
@login_required
def diet_view(request):
    plan = UserDiet.objects.filter(user=request.user).first()
    return render(request, "Diet.html", {"diet_markdown": plan.diet_reply if plan else ""})
def diet(request):
    bmi_id = request.session.get('bmi_id')

    if bmi_id:
        record = BMIRecord.objects.get(id=bmi_id)

        context = {
            "age": record.age,
            "gender": record.gender,
            "bmi": record.bmi,
            "status": record.status
        }

        return render(request, "Diet.html", context)

    return redirect('bmi')
@login_required
def exercise_view(request):
    plan = UserExercise.objects.filter(user=request.user).first()
    return render(request, "Exercise.html", {
        "exercise_markdown": plan.exercise_reply if plan else ""
    })
# @login_required
# def diet_page(request):
#     diet = DietPlan.objects.filter(user=request.user).first()
#     return render(request, "Diet.html", {"diet": diet})
# @login_required
# def exercise_page(request):
#     exercise = ExercisePlan.objects.filter(user=request.user).first()
#     return render(request, "Exercise.html", {"exercise": exercise})   
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
        # signup view me
    return render(request, 'signup.html')
def LogoutPage(request):
     logout(request)
     return redirect('login')

def bmi(request):
    context = {"progress": 0}

    if request.method == "POST":
        age = int(request.POST.get("age"))
        gender = request.POST.get("gender")
        weight = float(request.POST.get("weight"))
        height = float(request.POST.get("height")) * 0.3048

        bmi = round(weight / (height * height), 2)

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

        # ✅ DATABASE ME SAVE
        record = BMIRecord.objects.create(
            age=age,
            gender=gender,
            weight=weight,
            height=height,
            bmi=bmi,
            status=status
        )

        HealthProgress.objects.create(
            user=request.user,
            bmi=bmi,
            weight=weight
        )
        # session optional (quick access ke liye)
        request.session['bmi_id'] = record.id
        request.session['bmi'] = bmi
        request.session['status'] = status
        request.session['age'] = age
        request.session['gender'] = gender

        context = {
            "bmi": bmi,
            "status": status,
            "progress": progress,
            "age": age,
            "gender": gender
        }

        return render(request, "ai_planner.html", context)

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
# @login_required
# def generate_plan(request):
#     user = request.user

#     # ✅ Agar pehle se plan bana hai to wahi bhejo
#     diet = DietPlan.objects.filter(user=user).first()
#     exercise = ExercisePlan.objects.filter(user=user).first()

#     if diet and exercise:
#         return render(request, "ai_planner.html", {
#             "diet": diet.diet_text,
#             "exercise": exercise.exercise_text
#         })

#     # ❗ Agar nahi hai tab AI call karo
#     ai_response = aiapp_view()   # tumhara Gemini/OpenAI

#     # 🔥 Yaha split karna hai
#     diet_text = ai_response.split("Exercise Plan:")[0]
#     exercise_text = ai_response.split("Exercise Plan:")[1]

#     # ✅ Separate save
#     DietPlan.objects.create(user=user, diet_text=diet_text)
#     ExercisePlan.objects.create(user=user, exercise_text=exercise_text)

#     return render(request, "ai_planner.html", {
#         "diet": diet_text,
#         "exercise": exercise_text
#     })

def weight_gain(request):
    return render(request, 'weight_gain.html')
# def exercise(request):
#     return render(request, 'Exercise.html')
def privacy(request):
    return render(request, 'privacy.html')
def About(request):
     return render(request, 'about.html')
# def Excercise(request):
#      return render(request, 'Exercise.html')
def help(request):
     return render(request, 'help.html')
def Faq(request):
     return render(request, 'Faq.html')
def Terms(request):
     return render(request, 'Terms.html')
def Feedback(request):
     return render(request, 'Feedback.html')
