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