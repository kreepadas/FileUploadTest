from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from fileapp.models import Employee
from django.db.models import Q
import xlrd
import datetime

def home(request):
    employees = Employee.objects.all()
    return render(request, 'fileapp/home.html', {'employees': employees})

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        loc = ('D:\git projects\FileUploadTest\media\Interview File upload.xlsx')
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        count = 0
        for i in range(1, sheet.nrows):
            emp_obj = []
            emp_obj.append(sheet.row_values(i))
            cell = sheet.cell(i, 3)
            value = cell.value
            if cell.ctype == 3:
                value = datetime.datetime(*xlrd.xldate_as_tuple(value, wb.datemode))

            emp_age = calculateAge(value)
            # print(type(emp_obj[0][2]), type(emp_age))
            emp = Employee(count, emp_obj[0][0], emp_obj[0][1], int(emp_obj[0][2]), emp_age)

            count += 1
            emp.save()


        uploaded_file_url = fs.url(filename)
        return render(request, 'fileapp/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'fileapp/simple_upload.html')


def search(request, *args, **kwargs):
    if request.method == 'GET':
        employee_name = request.GET.get('Name')
        employee_email_id = request.GET.get('Email')
        employee_Phone_number = request.GET.get('Phone_Number')
        employee_age = request.GET.get('age')
        try:
            filters = Q(Q(Name__icontains=employee_name) & Q(Email__icontains=employee_email_id) & Q(Phone_Number__contains=employee_Phone_number) & Q(age__contains=employee_age))

            status = Employee.objects.filter(
                filters)
            print(status.query)
        except Employee.DoesNotExist:
            status = None
        return render(request, "fileapp/search.html", {"employees": status})
    else:
        return render(request, "fileapp/search.html", {})


def calculateAge(birthDate):
    today = datetime.date.today()
    Age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))

    return Age
