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

python manage.py startapp todo

```

This command should be executed in the same directory where the ```manage.py``` file is located, which is the root directory of your Django project.

After running this command, Django will generate a new folder named "todo" with the initial structure of the app

Once you've created the "todo" app, you'll need to include it in your project's settings. Open the ```shop/settings.py``` file and find the ```INSTALLED_APPS``` list and add ```"todo"``` to the list

```

INSTALLED_APPS = [
    # ...
    "todo",
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
from django.conf import settings


class TodoItem(models.Model):  
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="todo_item")

    class Meta:
        app_label = "todo"
        db_table = "todo_item"
        verbose_name = "todo_item"
        verbose_name_plural = "todo_items"

    def __str__(self):
        return self.name   
        
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("todo.urls")),
]

```

## Step 5: Creating Views

***Creating User Registration function***

Inside the todo app create a ```forms.py``` file and paste the below code

```

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ["username", "password1", "password2"]
        
```

Add the code given below to ```todo/views.py```

```

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


def register(request):   
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "todo/register.html", context)
        
```

Add code given below to ```todo/urls.py```

```

from django.urls import path
from .views import register


urlpatterns = [
    path("register/", register, name="register"),
]

```

## Step 6: Creating static folder

Static folder is to store the stylesheets, javascript files, and images.

Create a directory called static inside project root directory

Go to ```myapp/settings.py``` and configure static files.

```

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


STATIC_ROOT = "/static/"

```

Create ```login.css``` inside ```static``` folder and copy code given below

```

:root {
    --dark-pink: #f14182;
    --light-pink: #f16498;
    --primary-red: rgb(235, 78, 78);
    --primary-green: rgb(25, 151, 25);
}

.content-section {
    /* background-color: aquamarine; */
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.form-group {
    border: 0;
}

.form-group legend {
    font-size: 1.5rem;
    color: var(--dark-pink);
    font-weight: 500;
    /* border: 2px solid blueviolet; */
    text-align: center;
    margin-bottom: 10px;
}
.form-group hr {
    margin-bottom: 20px;
}

form {
    padding: 30px;
    /* border: 2px solid green; */
    width: 40%;
}

/* -------------------- Login Button ------------ */
.form-submit button {
    margin: 15px 0 15px 0;
    padding: 6px 20px;
    background-color: #fff;
    border: 1px solid var(--primary-green);
    border-radius: 3px;
    color: var(--primary-green);
    font-size: medium;
    font-weight: 500;
    cursor: pointer;
}
.form-submit button:hover {
    background-color: var(--primary-green);
    border: 1px solid #fff;
    border-radius: 3px;
    color: #fff;
}

#create-account {
    text-align: end;
    font-size: small;
    margin-top: 15px;
}

/* -----------------------Sign up link -------------------- */
#create-account a:link {
    font-size: small;
    text-decoration: none;
    border: 1px solid var(--primary-red);
    background-color: #fff;
    color: var(--primary-red);
    border-radius: 3px;
    padding: 2px 10px;
}
#create-account a:hover {
    font-size: small;
    text-decoration: none;
    border: 1px solid #fff;
    background-color: var(--primary-red);
    color: #fff;
    border-radius: 3px;
    padding: 4px 10px;
}

/* Below class and id name are generated by crispy forms.
    Check more about these in browser inspect tool.
*/
.form-group label {
    font-size: medium;
}

.control-group {
    margin-bottom: 20px;
}

.textInput {
    margin: 3px 0 5px 0;
    width: 100%;
    height: 30px;
    border: 1px solid gray;
    border-radius: 3px;
}
.alert li {
    font-size: medium;
    font-weight: 800;
    color: var(--primary-red);
    margin-bottom: 10px;
    text-align: center;
}

```


Create ```register.css``` inside ```static``` folder and copy code given below

```

:root {
    --dark-pink: #f14182;
    --light-pink: #f16498;
    --primary-red: rgb(235, 78, 78);
    --primary-green: rgb(25, 151, 25);
}

.register-content {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.register-form-group {
    border: 0;
}
.register-form-group > legend {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 500;
    margin-bottom: 10px;
    color: var(--dark-pink);
}
.register-form-group hr {
    margin-bottom: 20px;
}

.login-account {
    margin-top: 10px;
    text-align: end;
    font-size: small;
}
.login-account a:link {
    text-decoration: none;
    background-color: #fff;
    color: var(--primary-red);
    border: 1px solid var(--primary-red);
    border-radius: 3px;
    padding: 2px 10px;
    font-size: small;
}
.login-account a:hover {
    text-decoration: none;
    color: #fff;
    background-color: var(--primary-red);
    border: 1px solid #fff;
    border-radius: 3px;
    padding: 2px 10px;
    font-size: small;
}


/* Below class and id name are generated by crispy forms.
    Check more about these in browser inspect tool.
*/
.register-form-group p {
    font-size: small;
    margin-left: 20px;
    color: rgb(61, 60, 60);
    margin-top: 0;
}
.register-form-group .control-group li {
    list-style: disc;
    list-style-position: inside;
    font-size: small;
    margin-left: 20px;
    color: rgb(61, 60, 60);
}

.register-form-group .error #error_1_id_password2 {
    font-size: 1rem;
    font-weight: 800;
    color: var(--primary-red);
    margin-bottom: 3px;
}

```

Create ```style.css``` inside ```static``` folder and copy code given below

```

@import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,400;0,500;0,600;1,500&display=swap');

:root {
    --gray: #6c757d;
    --gray-dark: #343a40;
    --gray-100: #f8f9fa;
    --gray-200: #e9ecef;
    --gray-300: #dee2e6;
    --gray-400: #ced4da;
    --gray-500: #adb5bd;
    --gray-600: #6c757d;
    --gray-700: #495057;
    --gray-800: #343a40;
    --gray-900: #212529;
    --primary: #0d6efd;
    --secondary: #6c757d;
    --success: #198754;
    --info: #0dcaf0;
    --warning: #ffc107;
    --danger: #dc3545;
    --light: #f8f9fa;
    --dark: #212529;
    --primary-background: #cfe2ff;
    --dark-pink: #f14182;
    --light-pink: #f16498;
}

* {
    margin: 0;
    padding: 0;
    list-style: none;
    font-family: "Source Code Pro", monospace;
}

.navbar {
    display: flex;
    justify-content: space-evenly;
    background: #f16498;
    color: #fff;
    padding: 1%;
}
.navbar p, a {
    font-size: large;
}
.navbar ul {
    display: flex;
}
.navbar a:link {
    text-decoration: none;
    color: #fff;
}
.navbar a:hover {
    text-decoration: underline;
    color: #fff;
}

/* ------------------------------------- Create Todo Form ------------------------------- */

.container {
    margin: 30px;
    /* border: 1px solid black; */
    /* display: flex;
    justify-content: center;
    align-items: center; */
}
#welcome-user {
    font-size: large;

}
.container-section {
    /* border: 1px solid blue; */
    width: 100%;
    margin: 20px 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.container-section .create-todo-form {
    /* border: 2px solid yellowgreen; */
    box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
    margin-left: 5%;
    width: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.create-todo-form input {
    width: 300px;
    height: 35px;
    border: 2px solid gray;
    border-radius: 3px;
    margin-right: 5px;
}
.create-todo-form button {
    width: 100px;
    height: 35px;
    color:var(--primary);
    background-color: var(--light);
    border: 2px solid var(--primary);
    border-radius: 3px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
}
.create-todo-form button:hover {
    width: 100px;
    height: 35px;
    background-color:var(--primary);
    color: var(--light);
    border: 2px solid var(--primary);
    border-radius: 3px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
}

.todo-container {
    /* border: 2px solid var(--gray-dark); */
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;
    background-color: pink;
    width: 50%;
    margin: 0 0 15px 27.5%;
}

.todos {
    /* border: 2px solid rgb(223, 247, 7); */
    padding: 2%;
    margin: 10px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
}
.todos p {
    font-size: medium;
    font-weight: 800;
    color: rgb(31, 29, 29);
}
.todos li {
    display: inline-flex;
}
.todos a:link {
    font-size: medium;
    text-decoration: none;
}

.crud-buttons #edit-todo {
    width: 60px;
    background-color: #fff;
    color: var(--success);
    border: 1px solid var(--success);
    border-radius: 3px;
    padding: 0 2px;
}
.crud-buttons #edit-todo:hover {
    width: 60px;
    color: #fff;
    background-color: var(--success);
    border: 1px solid var(--success);
    border-radius: 3px;
    padding: 0 2px;
}

.crud-buttons #complete-todo {
    width: 95px;
    background-color: #fff;
    color: var(--gray-dark);
    border: 1px solid var(--gray-dark);
    border-radius: 3px;
    padding: 0 2px;
}
.crud-buttons #complete-todo:hover {
    width: 95px;
    color: #fff;
    background-color: var(--gray-dark);
    border: 1px solid var(--gray-dark);
    border-radius: 3px;
    padding: 0 2px;
}

.crud-buttons #delete-todo {
    width: 65px;
    background-color: #fff;
    color: var(--danger);
    border: 1px solid var(--danger);
    border-radius: 3px;
    padding: 0 2px;
}
.crud-buttons #delete-todo:hover {
    width: 65px;
    color: #fff;
    background-color: var(--danger);
    border: 1px solid var(--danger);
    border-radius: 3px;
}

#close-edit-modal {
    padding: 2px 7px !important;
    background-color: var(--light);
    border: 0;
}
.modal-footerr {
    width: 100%;
    display: flex;
    margin-left: 90%;
}
.modal-footerr buttons {
    display: inline-flex;
    /* width: 20%; */
}
#edit-todo-submit {
    width: 50%;
    margin-left: 10px;
}

/* ------------------ Page Navigation ------------------------- */

nav .page-item {
    border: 1px solid var(--primary);
    border-radius: 4px;
    margin: 0 1px;
}

```

## Step 7: Creating templates

Create a folder called ```templates``` in ```myapp/todo```

Create a folder called ```todo``` in ```myapp/todo/templates```

Ceate a file called ```index.html``` inside directory ```myapp/todo/templates/todo```

```

{% load static %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>CRUD Application</title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="{% static '/css/style.css' %}">
    <link rel="stylesheet" href="{% static '/css/login.css' %}">
    <link rel="stylesheet" href="{% static '/css/register.css' %}">
</head>

<body>
    <nav class="navbar">
	    <p class="navbar-brand">CRUD Application</p>

        {% if user.is_authenticated %}
            <p id="welcome-user">Welcome, {{ request.user.username }}</p>

            <ul>
                <li class="navbar-item">
                    <a class="link" href="{% url 'logout' %}">Logout</a>
                </li>
            </ul>
        {% else %}
            <ul>
                {% if request.path == '/register/' %}
                    <li>
                        <a class="link" href="{% url 'login' %}">Login</a>
                    </li>
                {% elif request.path == '/login/' %}
                    <li>
                        <a class="link" href="{% url 'register' %}">Register</a>
                    </li>
                {% endif %}
            </ul>
        {% endif %}
	</nav>

    {% block content %}
    {% endblock %}
    <!-- Below jquery javascript is required for modal functionalities -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
    <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script> -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
</body>
</html>

```

Ceate a file called ```crud.html``` inside directory ```myapp/todo/templates/todo```

```

{% extends 'todo/index.html' %}

{% block content %}

<div class="container">
    <div class="container-section">
        <form action="{% url 'home' %}" method="post" class="create-todo-form">
            {% csrf_token %}

            <input type="text" name="new-todo" id="new-todo" required>
            <button type="submit">Add Todo</button>
        </form>
    </div>

    {% for i in page_obj %}
    <div class="todo-container">
        <div class="todos">
            <p>{{ i.name }}</p>
            <ul class="crud-buttons">
                <li>
                    <button id="edit-todo" data-toggle="modal" data-target="#editTodoModal_{{ i.id }}">Edit</button>

                    <div class="modal fade" id="editTodoModal_{{ i.id }}" tabindex="-1" role="dialog"
                        aria-labelledby="editTodoModalLabel" aria-hidden="true">
                        <div class="modal-dialog" role="document">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="editTodoModalLabel">Update Todo Item</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true" id="close-edit-modal">&times;</span>
                                    </button>
                                </div>
                                <form action="{% url 'update_todo' i.id %}" method="post" class="edit-todo-form">
                                    {% csrf_token %}
                                    <div class="modal-body">
                                        <input type="text" name="todo_{{ i.id }}" id="" value="{{ i.name }}" required
                                            size="40">
                                    </div>
                                    <div class="modal-footerr">
                                        <button type="button" class="btn btn-sm btn-secondary"
                                            data-dismiss="modal">Close</button>
                                        <button type="submit" class="btn btn-sm btn-primary"
                                            id="edit-todo-submit">Submit</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </li>
                <li><a href="{% url 'complete_todo' i.id %}" id="complete-todo">Completed</a></li>
                <li><a href="{% url 'delete_todo' i.id %}" id="delete-todo">Delete</a></li>
            </ul>
        </div>
    </div>
    {% endfor %}

    <nav aria-label="Page navigation example">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
                <li class="page-item previous-page">
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}" tabindex="-1">Previous</a>
                </li>
            {% else %}
                <li class="page-item disabled previous-page">
                    <a class="page-link" href="?page=0" tabindex="-1">Previous</a>
                </li>
            {% endif %}

            <li class="page-item active current-page">
                <a class="page-link" href="?page={{ page_obj.number }}">{{ page_obj.number }}</a>
            </li>

            {% if page_obj.has_next %}
                <li class="page-item next-page">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}" tabindex="-1">Next</a>
                </li>
            {% else %}
                <li class="page-item disabled next-page">
                    <a class="page-link" href="?page=0" tabindex="-1">Next</a>
                </li>
            {% endif %}
        </ul>
    </nav>
</div>

{% endblock %}

```

Ceate a file called ```login.html``` inside directory ```myapp/todo/templates/todo```

```

{% extends 'todo/index.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="content-section">
    <form action="" method="POST">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend>Login</legend>
            <hr>
            {{ form | crispy }}
        </fieldset>

        <div class="form-submit">
            <button class="login-submit-btn" type="submit">Login</button>
        </div>

        <hr>

        <div id="create-account">
            <medium class="text-muted">
                Don't Have an Account?
                <a href="{% url 'register' %}" class="register-link">Sign Up</a>
            </medium>
        </div>
    </form>
</div>
{% endblock %}

```

Ceate a file called ```logout.html``` inside directory ```myapp/todo/templates/todo```

```

{% extends 'todo/index.html' %}

{% block content %}

    <h2 class="text-md-center">You Have Been Logged Out!</h2>
    <div class="border-top pt-3 text-center">
        <a href="{% url 'login' %}" class="">Login Again</a>      
    </div>

{% endblock %}

```

Ceate a file called ```register.html``` inside directory ```myapp/todo/templates/todo```

```

{% extends 'todo/index.html' %}
{% load crispy_forms_tags %}

{% block content %}
    
    <div class="register-content">
        <form action="" method="POST">
            {% csrf_token %}
            <fieldset class="register-form-group">
                <legend>Register</legend>
                <hr>
                {{ form | crispy }}
            </fieldset>

            <div class="form-submit">
                <button class="btn btn-success" type="submit">Sign Up</button>
            </div>

            <hr>
            
            <div class="login-account">
                <medium class="text-muted">
                    Already Have an Account?
                    <a href="{% url 'login' %}" class="login-link">Login</a>
                </medium>
            </div>
        </form>
    </div>

{% endblock %}

```

## Step 8: Adding login and logout functionality

In ```todo/urls.py``` add given code to configure login and logout url

```
from django.urls import path
from .views import register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(template_name="todo/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="todo/logout.html"), name="logout"),
    path("register/", register, name="register"),
]
```

Next we need to mention the redirect URL

Open the ```myapp/settings.py``` and paste the below code.

```

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home" 
LOGOUT_REDIRECT_URL = "login"

```

## Step 9: Creating main functions

Inside ```todo/views.py``` add home function which render user's todo list

```

from django.contrib.auth.decorators import login_required
from .models import TodoItem


@login_required
def home(request):
    if request.method == 'POST':
        todo_name = request.POST.get("new-todo")
        todo = TodoItem.objects.create(name=todo_name, user=request.user)
        return redirect("home")

    todos = TodoItem.objects.filter(user=request.user, is_completed=False).order_by("-id")

    context = {"todos": todos}
    return render(request, "todo/crud.html", context)
    
```

***Upadate todo function***

```

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

def update_todo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)

    todo.name = request.POST.get(f"todo_{pk}")
    todo.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
```

***Delete todo function***

```

def delete_todo(request, pk):  
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
```

***Mark as complete function***

```

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect


def complete_todo(request, pk):   
    todo = get_object_or_404(TodoItem, id=pk, user=request.user)
    todo.is_completed = True
    todo.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
```

Inside ```todo/urls.py``` add urls

```

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (home, register, update_todo, complete_todo,
    delete_todo)


urlpatterns = [
    path("", home, name="home"),
    path("login/", LoginView.as_view(template_name="todo/login.html"),name="login"),
    path("logout/", LogoutView.as_view(template_name="todo/logout.html"),name="logout"),
    path("register/", register, name="register"),
  
    path("update/todo/<int:pk>/", update_todo, name="update_todo"),
    path("complete/todo/<int:pk>/", complete_todo, name="complete_todo"),
    path("delete/todo/<int:pk>/", delete_todo, name="delete_todo"),
]

```

## Step 10: Implementing Pagination

To implement pagination modify home function in ```todo/views.py```

```

from django.core.paginator import Paginator


@login_required
def home(request):
    if request.method == 'POST':
        todo_name = request.POST.get("new-todo")
        todo = TodoItem.objects.create(name=todo_name, user=request.user)
        return redirect("home")

    # retrieving todo items which are incomplete
    todos = TodoItem.objects.filter(user=request.user, is_completed=False).order_by("-id")

    # paginating 4 items per page
    paginator = Paginator(todos, 4)
    
    # It's URL param for getting the current page number
    page_number = request.GET.get("page")
    
    # retrieving all the todo items for that page
    page_obj = paginator.get_page(page_number)

    context = {"todos": todos, "page_obj": page_obj}
    return render(request, "todo/crud.html", context)
    
```

### Finally the Django ToDo App is completed
