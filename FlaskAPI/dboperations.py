import pymongo

#   Connection with MongoClient i.e. mongo server
client = pymongo.MongoClient("mongodb://localhost:27017")
# client = pymongo.MongoClient("mongodb+srv://zainarif00456:fuckyou12345@democluster.iou8h7n.mongodb.net/test")

# Connection with database in MongoDB server
db = client['StudentManagement']


def addStudent(model):
    """
    This function add student information in Mongo Database
    :param model:
    :return:
    """
    if model is None:
        return False
    # connection with collection in the selected database
    collection = db['StudentInformation']
    # Insertion of document in the given collection
    collection.insert_one(model)
    return True


def getStudentById(_id):
    """
    Get Student by ID from database.
    '_id' key is default key.
    :param _id:
    :return:
    """
    collection = db['StudentInformation']
    student = collection.find_one({"_id": _id})
    print(student)
    return student


def createAdmin(admin):
    """
    This function is for admin sign up. Creating admin account.
    :param admin:
    :return:
    """
    collection = db['Admin']
    collection.insert_one(admin)
    return True


def getAdminByUserName(admininfo):
    """
    This is admin login Function. This function verifies the user with username
    :param admininfo:
    :return:
    """
    collection = db['Admin']
    admin = collection.find_one({"user_name": admininfo['user_name']}, {"_id": 0})
    if admin is not None:
        if admin['password'] == admininfo['password']:
            print("ADMIN CONFIRMED")
            return {'details': admin}
        else:
            print("Password Didnt match")
            return {"details": "invalid"}
    else:
        return {"details": "invalid"}


def verifyAdmin(admininfo):
    """
    Verifying admin with token authentication.
    :param admininfo:
    :return:
    """
    collection = db['Admin']
    admin = collection.find_one({"user_name": admininfo['user_name']}, {"_id": 0})
    if admin is not None:
        if admin['password'] == admininfo['password']:
            return True
        else:
            print("Password Didnt match")
            return False
    else:
        return None


def getallstudents():
    """
    Function will return all students available in the database.
    :return:
    """
    collection = db["StudentInformation"]
    cursor = collection.find({})
    student = []
    for document in cursor:
        student.append(document)
    print(student)
    if student is not None:
        return {'details': student}
    else:
        return {"details": 404}


def deleteStudent(id):
    """
    Function to delete student by ID from the database.
    :param id:
    :return:
    """
    collection = db["StudentInformation"]
    student = collection.find_one({'_id': id})
    if student is not None:
        res = collection.delete_one({'_id': id})
        print(res)
        return {'details': True}
    else:
        return {'details': False}


def update_student(model: dict):
    """
    Function will update information received as parameter and save the updated information.
    :param model:
    :return:
    """
    collection = db["StudentInformation"]
    if collection.find_one({"_id": f"{model['_id']}"}) is not None:
        id = model.pop('_id')
        print(id)
        print(collection.update_one({"_id": f"{id}"}, {"$set": model}).modified_count)
        return {'details': "updated"}
    else:
        return {"details": None}

