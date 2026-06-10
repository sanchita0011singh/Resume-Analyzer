from django.shortcuts import render , redirect ,HttpResponse
import PyPDF2
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# 🔹 Job roles dataset
JOB_SKILLS = {
    # Technical
    "Web Developer": ["HTML", "CSS", "JavaScript", "Django"],
    "Data Analyst": ["Python", "SQL", "Excel"],
    "AI Engineer": ["Python", "Machine Learning"],
    
    # Non-Technical
    "HR Manager": ["Communication", "Recruitment"],
    "Digital Marketing": ["SEO", "Social Media"],
    "Project Manager": ["Leadership", "Planning"]
}


# 🔹 Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    
    for page in reader.pages:
        text += page.extract_text()
    
    return text


# 🔹 Extract skills from resume
def extract_skills(resume_text, skills_list):
    found_skills = []
    resume_text = resume_text.lower()
    
    for skill in skills_list:
        if skill.lower() in resume_text:
            found_skills.append(skill)
    
    return found_skills


# 🔹 Match skills
def match_skills(user_skills, required_skills):
    matched = []
    missing = []
    
    for skill in required_skills:
        if skill in user_skills:
            matched.append(skill)
        else:
            missing.append(skill)
    
    return matched, missing


# 🔹 Match percentage
def calculate_match_percentage(matched, total_required):
    if total_required == 0:
        return 0
    return int((len(matched) / total_required) * 100)


# 🔹 Suggestions
def suggest_skills(user_skills):
    suggestions = []
    
    if "Python" in user_skills and "Django" not in user_skills:
        suggestions.append("Learn Django for backend development")
    
    if "HTML" in user_skills and "JavaScript" not in user_skills:
        suggestions.append("Learn JavaScript to improve frontend skills")
    
    if "SQL" not in user_skills:
        suggestions.append("Basic SQL knowledge is recommended")
    
    return suggestions


# 🔹 Upload Page
@login_required(login_url='Loginpage')
def upload_resume(request):
    return render(request, 'resume_app/upload.html')


# 🔹 Result Page (Main Logic)
def result(request):
    if request.method == "POST":
        
        resume_file = request.FILES['resume']
        selected_role = request.POST.get('job_role')

        # Extract text
        resume_text = extract_text_from_pdf(resume_file)

        # Get required skills
        required_skills = JOB_SKILLS.get(selected_role, [])

        # Extract skills from resume
        user_skills = extract_skills(resume_text, required_skills)

        # Match skills
        matched, missing = match_skills(user_skills, required_skills)

        # Match percentage
        match_percentage = calculate_match_percentage(matched, len(required_skills))

        # Suggestions
        suggestions = suggest_skills(user_skills)

        context = {
            'matched': matched,
            'missing': missing,
            'suggestions': suggestions,
            'match_percentage': match_percentage
        }

        return render(request, 'resume_app/result.html', context)

    return render(request, 'resume_app/upload.html')
@login_required(login_url='Loginpage')
def homepage(request):
    return render(request, 'resume_app/home.html')
def reg(request):
     if request.method == "POST":
        full_name = request.POST.get('name')   # 👈 NEW
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('regpage')

        # Username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('regpage')

        # Email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('regpage')

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 👇 Full name split (optional but better)
        if full_name:
            name_parts = full_name.split()
            user.first_name = name_parts[0]
            if len(name_parts) > 1:
                user.last_name = " ".join(name_parts[1:])

        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect('loginpage')

     return render(request, 'resume_app/reg.html') 

def Login(request):
     if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')   # homepage pe bhejega
        else:
            return render(request, 'resume_app/login.html', {
                'error': 'Invalid username or password'
            })
     return render(request,'resume_app/Login.html')


def Logout(request):
    logout(request)
    return redirect('Loginpage')   # logout ke baad login page
