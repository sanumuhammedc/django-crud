# django-crud

In this tutorial we will create a django todo app to familiarize crud operations and authentication in django if you are new to django please refer [Django for beginners](https://github.com/sanumuhammedc/django-for-beginners) before continuing with this tutorial 

## Step 1: Setting Up the Project

Install Python: Follow the official Python installation guide for your operating system.

**Create a Virtual Environment:**

Open your terminal and run the following commands:

```
python -m venv myenv
```

```
source myenv/bin/activate
```

**Install Django:**

Run the command in your virtual environment to install Django.
```
pip install django
```

To check installation
```
python -m django --version
```

**Create a Django Project:**

Run 

```
django-admin startproject myapp
```
To create a new Django project named ``` myapp ```.

Run

```
python3 manage.py runserver 
```

To run the development server

## Step 2: Create todo app

create an app called todo 

``` 
python manage.py startapp ```todo```
```


create an app called ```account``` 

``` 

python manage.py startapp account

```

This command should be executed in the same directory where the ```manage.py``` file is located, which is the root directory of your Django project.

After running this command, Django will generate a new folder named "todo" with the initial structure of the app

Once you've created the "todo" app, you'll need to include it in your project's settings. Open the ```shop/settings.py``` file and find the ```INSTALLED_APPS``` list and add ```"todo"``` to the list

```

INSTALLED_APPS = [
    # ...
    "todo.apps.TodoConfig",
    "crispy_forms",
    # ...
]

```

## Step 3: Create Models

To do the initial migration run 

```

python manage.py migrate

```

After the successful initial migration create models in ```todo/models.py```

```
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Task(models.Model):
    user = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d %H:%M"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        
```

Apply these changes on database file myapp/db.sqlite3 by running the below commands in order.
 
```
python manage.py makemigrations
```
```
python manage.py migrate
```

## Step 4: Managing urls

Add the following code in ```myapp/urls.py``` file.

```
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('accounts/', include('accounts.urls')),
]
```

## Step 5: Creating Views

***Creating User Registration function***

Inside the todo app create a ```form.py``` file and paste the below code

```
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add Task Here...'}))
    user = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'style': 'display:none'}))

    class Meta:
        model = Task
        fields = ['title', 'user']


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'complete']
        
```

Add the code given below to ```todo/views.py```

```
from django.shortcuts import render

# Create your views here.
import datetime
from django.shortcuts import render, redirect
from .models import Task
from .form import TaskForm, UpdateTaskForm
from django.http import QueryDict


# Create your views here.

def tasklist(request):
    user = request.user.username
    todos = Task.objects.filter(user=user, complete=False)
    dones = Task.objects.filter(user=user, complete=True)
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    print(now)

    if request.method == 'POST':
        data = {'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'], 'title': request.POST['title'],
                'user': request.user.username}
        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)
        form = TaskForm(query_dict)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TaskForm()

    context = {
        'todos': todos,
        'form': form,
        'dones': dones,
        'now': now,
    }

    return render(request, 'todo/index.html', context)


def update(request, pk):
    todo = Task.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UpdateTaskForm(instance=todo)
    context = {
        'form': form
    }
    return render(request, 'todo/update.html', context)


def delete(request, pk):
    todo = Task.objects.get(id=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('/')
    return render(request, 'todo/delete.html')        
```

Add code given below to ```todo/urls.py```

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasklist, name='tasks'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]
```

## Step 6: Creating templates

Create a folder called ```templates``` in ```myapp```

Create a folder called ```todo``` and ```partials``` in ```myapp/templates```

Ceate a file called ```index.html``` inside directory ```myapp/todo/templates/todo```

```
{% extends 'partials/base.html' %}

{% load crispy_forms_tags %}

{% block content %}


    <div class="border p-3 m-3 shadow">
        <form method="post">
            {% csrf_token %}
            {{ form | crispy }}
            <input class="btn btn-success btn-block w-100 mt-2" type="submit" value="Submit">
        </form>
        <hr>
        {% for todo in todos %}
            {% if todo.deadline > now or todo.deadline is None %}
                <div class="border p-3 mb-3">
                <small>Created: {{ todo.created }}</small><br>
                <div class="row mt-3">
                    <div class="col-md-8">
                        {% if todo.complete == True %}
                            <s><p>{{ todo.title }}</p></s>
                        {% else %}
                            <h5>{{ todo.title }}</h5>
                        {% endif %}
                    </div>
                    <div class="col-md-4">
                        <a class="btn btn-info btn-sm" href="{% url 'update' todo.id %}">Edit</a>
                        <a class="btn btn-danger btn-sm" href="{% url 'delete' todo.id %}">Delete</a>
                    </div>
                </div>
            </div>
            {% endif %}
        {% endfor %}
    </div>
{% endblock %}
```

Ceate a file called ```delete.html``` inside directory ```myapp/todo/templates/todo```

```
   {% extends 'partials/base.html' %}
{% load crispy_forms_tags %}
{% block content %}

    <div class="border p-3 m-3">
        <h4>Delete Task</h4>
        <div class="alert alert-danger">
            <p>Are You Sure Want To Delete</p>
        </div>
        <form method="post">
            {% csrf_token %}
            <a class="btn btn-secondary" href="{% url 'tasks' %}">Cancel</a>
            <input class="btn btn-danger" type="submit" value="Confirm">
        </form>
    </div>

{% endblock %}
```

Ceate a file called ```login.html``` inside directory ```myapp/todo/templates/todo```

```
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>Task Manager | Login</title>
</head>
<body>
{% include 'partials/navbar.html' %}

    <div style="height: 100vh;" class="d-flex justify-content-center align-items-center">
        <div class="col-md-4">
        {% if request.user.is_authenticated %}
            <h4 class="text-center">You are logged in as {{ user.username }}!</h4>
        {% else %}
        <form action="" method="post">
            {% csrf_token %}
            <h4 class="mb-3">Login</h4>
      <div class="mb-3">
        <input required class="form-control" type="text" name="username" placeholder="User Name">
      </div>
      <div class="mb-3">
        <input required class="form-control" type="password" name="password" placeholder="Password">
      </div>
      <input class="btn btn-primary" value="Login" type="submit">
    </form>

        <div>
        {% for message in messages %}
            <h3>{{ message}}</h3>
        {% endfor %}
        </div>
        {% endif %}
    </div>
    </div>
</body>
</html>
```

Ceate a file called ```update.html``` inside directory ```myapp/todo/templates/todo```

```
{% extends 'partials/base.html' %}

{% load crispy_forms_tags %}

{% block content %}


    <div class="border p-3 m-3">
        <form method="post">
            {% csrf_token %}
            {{ form | crispy }}
            <input class="btn btn-info btn-block mt-3" type="submit" value="Update">
        </form>
    </div>
{% endblock %}
```

Ceate a file called ```register.html``` inside directory ```myapp/todo/templates/todo```

```
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>Task Manager | Sign Up</title>
</head>
<body>
    {% include 'partials/navbar.html' %}
    <div style="height: 100vh;" class="d-flex justify-content-center align-items-center">
        <div class="col-md-4">
        {% if request.user.is_authenticated %}
            <h4 class="text-center">You are logged in as {{ user.username }}!</h4>
        {% else %}
            <form action="" method="post">
            {% csrf_token %}
            <h4 class="mb-3">Sign Up</h4>
              <div class="mb-3">
                 <input required class="form-control" type="text" name="username" placeholder="User Name">
              </div>
              <div class="mb-3">
                  <input required class="form-control" type="password" name="password" placeholder="Password">
              </div>
            <input class="btn btn-primary" value="Sign Up" type="submit">
        </form>

        <div>
        {% for message in messages %}
            <h3>{{ message}}</h3>
        {% endfor %}
        </div>
        {% endif %}

        </div>
    </div>
</body>
</html>
```

Ceate a file called ```base.html``` inside directory ```myapp/todo/templates/partials```

```
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <title>Task Manager</title>
  </head>
  <body>
    {% include 'partials/navbar.html' %}

    {% if request.user.is_authenticated %}
        <div class="container">
            <div class="row">
                <div class="col-md-8 mt-5">
                    <h4 class="mt-5">Hello {{ user.username }}!</h4>
                    {% block content %}

                    {% endblock %}
                </div>

                <div class="col-md-4">
                    {% include 'partials/beside.html' %}
                </div>

            </div>
        </div>
    {% else %}
        <div style="height: 100vh" class="d-flex justify-content-center align-items-center">
            <a class="btn btn-primary mx-3" href='accounts/login/'>Login</a>
            <a class="btn btn-primary" href='accounts/register/'>Sign Up</a>
        </div>
    {% endif %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
  </body>
</html>
```

Ceate a file called ```beside.html``` inside directory ```myapp/todo/templates/partials```

```
<div style="margin-top: 5rem !important;" class="border p-3 shadow">
    <div class="border p-3 mb-2">
        <h3>Completed tasks</h3>
        {% for done in dones %}
        <div class="border p-3 mb-3">
            <small>Created: {{ done.created }}</small><br>
            <div class="row mt-3">
                <div class="col-md-8">
                    {% if done.complete == True %}
                        <s><p>{{ done.title }}</p></s>
                    {% else %}            {% if todo.deadline %}
                    <small>Deadline: {{ done.deadline }}</small>
                {% endif %}
                        <h5>{{ done.title }}</h5>
                    {% endif %}
                </div>
                <div class="col-md-4">
                    <a class="btn btn-info btn-sm" href="{% url 'update' done.id %}">Edit</a>
                    <a class="btn btn-danger btn-sm" href="{% url 'delete' done.id %}">Delete</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
```

Ceate a file called ```navbar.html``` inside directory ```myapp/todo/templates/partials```

```
  <nav class="navbar navbar-expand-lg navbar-info bg-info position-fixed w-100">
      <div class="container">
        <a class="navbar-brand text-white" href="{% url 'tasks' %}">Task Manager</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            {% if request.user.is_authenticated %}
                <li class="nav-item">
                  <a class="btn btn-danger" href='accounts/logout/'>Logout</a>
                </li>
            {% endif %}
          </ul>
        </div>
      </div>
    </nav>
```

## Step 7: Adding login and logout functionality

In ```accounts/urls.py``` add given code to configure login and logout url

```
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]

```

Next we need to mention the redirect URL

Open the ```accounts/views.py``` and paste the below code.

```
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'todo/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Already Exist')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('login')

    else:
        return render(request, 'todo/register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
```

### Finally the Django ToDo App is completed
