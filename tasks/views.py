from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Task
from .forms import TaskForm


def task_list(request):
    """Dashboard view — lists all tasks with optional filtering."""
    filter_status = request.GET.get('status', '')
    filter_priority = request.GET.get('priority', '')

    tasks = Task.objects.all()

    if filter_status:
        tasks = tasks.filter(status=filter_status)
    if filter_priority:
        tasks = tasks.filter(priority=filter_priority)

    # Stats
    total = Task.objects.count()
    completed = Task.objects.filter(status='completed').count()
    pending = Task.objects.filter(status='pending').count()
    in_progress = Task.objects.filter(status='in_progress').count()

    context = {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
        'in_progress': in_progress,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
    }
    return render(request, 'tasks/task_list.html', context)


def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


def task_edit(request, pk):
    """Edit an existing task."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit', 'task': task})


def task_delete(request, pk):
    """Confirm and delete a task."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def task_toggle(request, pk):
    """Toggle a task between completed and pending."""
    task = get_object_or_404(Task, pk=pk)
    if task.status == 'completed':
        task.status = 'pending'
        messages.info(request, f'Task "{task.title}" marked as pending.')
    else:
        task.status = 'completed'
        messages.success(request, f'Task "{task.title}" completed! 🎉')
    task.save()
    return redirect('task_list')
