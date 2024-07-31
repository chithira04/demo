from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

from .forms import TodoForm
from .models import Task

# Create your views here.
def add(request):
    task_view = Task.objects.all()
    if request.method=='POST':
        name1=request.POST.get('task','')
        prio=request.POST.get('priority','')
        dat = request.POST.get('date', '')
        task_add=Task(name=name1,priority=prio,date=dat)
        task_add.save()

    return render(request,'home.html',{'tasks':task_view})

def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method=='POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    taskid=Task.objects.get(id=id)
    f=TodoForm(request.POST or None,instance=taskid)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':taskid})

####------class generic view------------
class Taskview(ListView):
    model=Task
    template_name = 'home.html'
    context_object_name = 'tasks'
class Taskdetailview(DetailView):
    model=Task
    template_name = 'detail.html'
    context_object_name = 'task'
class Taskupdateview(UpdateView):
    model=Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk': self.object.id})

class deleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')


