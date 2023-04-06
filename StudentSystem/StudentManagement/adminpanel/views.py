from typing import Optional
from django.core.files import File
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

TOKEN = "$"
USER = ""
URL = 'http://127.0.0.1:5000/'
USER_FLAG = False


def index(request):
    global TOKEN, USER_FLAG
    return render(request, 'index.html', {'token': TOKEN, 'user': USER_FLAG})


# Create your views here.
def handlelogin(request):
    global TOKEN, USER, USER_FLAG
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        payload = {
            'user_name': username,
            'password': password
        }
        if (username is not None) and (password is not None):
            response = requests.post(URL + "admin/login/", json=payload)
            data = response.json()
            admininfo = data['details']
            if admininfo == 'invalid':
                return HttpResponse("Invalid Credentials")
            USER = admininfo['user_name']
            print(admininfo)
            TOKEN = data['token']
            USER_FLAG = True
            return render(request, 'index.html', {'admin': admininfo, 'token': TOKEN, 'user': USER_FLAG})

    return HttpResponse("404-NOT FOUND")


def handlelogout(request):
    global TOKEN, USER_FLAG
    USER_FLAG = False
    TOKEN = "$"
    return render(request, 'index.html', {'token': TOKEN, 'user': USER_FLAG})


def signup(request):
    global TOKEN, USER
    if request.method == "POST":
        full_name = request.POST.get('fullname', None)
        cnic = request.POST.get('cnic', None)
        gender = request.POST.get('gender', None)
        date_of_birth = request.POST.get('dateofbirth', None)
        email_address = request.POST.get('email', None)
        user_name = request.POST.get('username', None)
        password = request.POST.get('password', None)
        conpass = request.POST.get('confirmpassword', None)
        if password == conpass:
            payload = {
                'full_name': full_name,
                'cnic': cnic,
                'gender': gender,
                'date_of_birth': date_of_birth,
                'email_address': email_address,
                'user_name': user_name,
                'password': password
            }
            response = requests.post(URL + "admin/signup/", json=payload)
            data = response.json()
            TOKEN = data['token']
            USER = user_name
            return render(request, 'index.html', {'payload': payload, 'token': TOKEN})

    return render(request, 'signup.html')


def addstudent(request):
    global TOKEN, USER
    if request.method == "POST":
        sid = request.POST.get('id', None)
        name = request.POST.get('name', None)
        fathers_name = request.POST.get('fathername', None)
        fathers_cnic = request.POST.get('cnic', None)
        fathers_phone = request.POST.get('phone', None)
        gender = request.POST.get('gender', None)
        date_of_birth = request.POST.get('dateofbirth', None)
        class_enrolled = request.POST.get('class')
        payload = {
            '_id': sid,
            'name': name,
            'fathers_name': fathers_name,
            'fathers_cnic': fathers_cnic,
            'fathers_phone': fathers_phone,
            'gender': gender,
            'date_of_birth': date_of_birth,
            'class_enrolled': class_enrolled,
            'added_by': USER
        }
        print(payload)
        response = requests.post(URL + "addstudents/", json=payload, headers={'token': TOKEN})
        data = response.json()
        if data['details'] == 'unauthorized':
            return HttpResponse("Unauthorized User", status=405)
        params = {
            'token': TOKEN
        }
        return render(request, 'index.html', {'token': TOKEN})
    return render(request, 'addstudent.html')


def showstudents(request):
    global TOKEN
    if TOKEN != "$":
        response = requests.get(URL + "getallstudents/", headers={'token': TOKEN})
        payload = response.json()
        student = payload['details']
        for s in student:
            s['id'] = s['_id']
        if payload['details'] != 404:
            print(student)
            return render(request, 'showstudents.html', {'student': student, 'token': TOKEN})
        else:
            return HttpResponse('No Record Found')
    else:
        return HttpResponse("404 Not Found")


def getstudent(request):
    global TOKEN
    sid = int(request.GET.get('id'))
    response = requests.get(URL + f"getstudent/{sid}", headers={'token': TOKEN})
    payload = response.json()
    print(payload)
    student = payload['details']
    student['id'] = student['_id']
    if student is not None:
        return render(request, 'studentinfo.html', {'token': TOKEN, 'student': student})
    return HttpResponse("NO STUDENT AVAILABLE")


def deletestudent(request, sid):
    global TOKEN
    res = requests.delete(URL + f"deletestudent/{sid}", headers={'token': TOKEN}).json()
    if res['details'] == 404:
        return HttpResponse("NO RECORD FOUND")
    else:
        return HttpResponse("DELETION Successful")


def updatestudent(request, sid: Optional):
    global TOKEN, USER
    if request.method == "GET":
        response = requests.get(URL + f"getstudent/{sid}", headers={'token': TOKEN})
        payload = response.json()
        print(payload)
        student = payload['details']
        if student is not None:
            student['id'] = student['_id']
            return render(request, 'updatestudent.html', {'token': TOKEN, 'student': student})
        else:
            return HttpResponse("NO STUDENT AVAILABLE")
    elif request.method == "POST":
        id = request.POST.get('id', '')
        name = request.POST.get('name', '')
        fathers_name = request.POST.get('fathername', '')
        fathers_cnic = request.POST.get('cnic', '')
        fathers_phone = request.POST.get('phone', '')
        date_of_birth = request.POST.get('dateofbirth', '')
        class_enrolled = request.POST.get('class', '')
        payload = {
            "_id": id,
            "name": name,
            "fathers_name": fathers_name,
            "fathers_cnic": fathers_cnic,
            "fathers_phone": fathers_phone,
            "date_of_birth": date_of_birth,
            "class_enrolled": class_enrolled,
            "added_by": USER
        }
        res = requests.post(URL + "updatestudent/", headers={'token': TOKEN}, json=payload).json()
        if res['details'] is not None:
            return redirect('showstudents')
        else:
            return HttpResponse(f"NO STUDENT WITH ID {id}")


