from flask import Flask, jsonify, request
import models, authentication
from flask_pydantic import validate
import dboperations as db

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "WORKING PROPERLY"


@app.route('/addstudents/', methods=['POST'])
@validate(body=models.Student)
def addstudent():
    if is_admin():
        model = request.get_json()
        flag = db.addStudent(model)
        if flag:
            return {'details': model}
        else:
            return jsonify({"detials": "Data failed to save in the database"})
    else:
        print("UNAUTHORIZED")
        return {"details": "unauthorized"}


def is_admin():
    """
    Admin and Token Validation
    :return:
    """
    token = request.headers.get("token")
    if token is None:
        return False
    user = authentication.verify_accrss_token(token)
    if user is not None:
        flag = db.verifyAdmin(user)
        return flag


@app.route('/getstudent/<sid>', methods=['GET'])
def getstudentbyid(sid):
    if is_admin():
        student = db.getStudentById(sid)
        if student is not None:
            print(student)
            return {'details': student}
        else:
            return {"details": None}
    else:
        return {"details": "unauthorized"}


@app.route('/admin/signup/', methods=['POST'])
@validate(body=models.Admin)
def adminsignup():
    admin = request.get_json()
    signature = {
        "email_address": admin['email_address'],
        "user_name": admin['user_name'],
        "password": admin['password']
    }
    token = authentication.createAccessToken(signature)
    flag = db.createAdmin(admin)
    if flag:
        print(f"Toke Successfully Created: {token}")
        return {"token": f"{token}"}
    else:
        return {"details": "failed"}


@app.route('/admin/login/', methods=['POST'])
@validate(body=models.AdminLogin)
def adminlogin():
    admin = request.get_json()
    data = db.getAdminByUserName(admin)
    if data['details'] == 'invalid':
        return data
    if data['details'] != 'invalid':
        token = authentication.createAccessToken(admin)
        if token is not None:
            print(token)
            return {"token": f"{token}",
                    "details": data['details']}
    else:
        return {"details": "Error Occurred..."}


@app.route('/getallstudents/', methods=['GET'])
def get_all_students():
    if is_admin():
        student = db.getallstudents()
        return student


@app.route('/deletestudent/<id>', methods=['DELETE'])
def delete_student(id):
    if is_admin():
        flag = db.deleteStudent(id)
        if flag['details']:
            return jsonify(flag)
        else:
            return {"details": 404}
    else:
        return {'details': 'Unauthorized'}


@app.route('/updatestudent/', methods=['POST'])
def updatestudent():
    if is_admin():
        model = request.get_json()
        flag = db.update_student(model)
        return flag


if __name__ == '__main__':
    app.run(debug=True)
