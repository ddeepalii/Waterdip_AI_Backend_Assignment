from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.views import View
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


'''View to create a new task with a title property and a boolean determining whether the task has been completed. 
A new unique id would be created for each new task'''
@method_decorator(csrf_exempt, name='dispatch')             #This disables the CSRF protection for all HTTP methods
class CreateTask(View):
    def post(self, request):
        data = json.loads(request.body)                    #parse the data into json
        task = Tasks.objects.create(title=data['title'], completion_status=data['completion_status'])
        return JsonResponse({'id': task.id}, status=201)   #returns task id with 201 status


'''View to list all tasks created'''
@method_decorator(csrf_exempt, name='dispatch')
class ListTask(View):
    def get(self, request):
        tasks = Tasks.objects.all().values('id', 'title', 'completion_status') #lists of dictionaries is returned
        return JsonResponse({'tasks': list(tasks)}, status=200)                 #returns list of tasks with 200 status



'''View to get a specific task (by id)'''
@method_decorator(csrf_exempt, name='dispatch')
class TaskDetail(View):
    def get(self, request, id):
        task = Tasks.objects.filter(id=id).first()
        if task:
            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'completion_status': task.completion_status
            }, status=200)
        else:
            return JsonResponse({'error: There is no task at this id'}, status=404,safe=False)  # returns error in json format


'''View to delete a specified task (by id)'''
@method_decorator(csrf_exempt, name='dispatch')
class DeleteTask(View):
    def delete(self, request, id):
        task = Tasks.objects.filter(id=id).first()
        if task:
            task.delete()                       #deletes if task exists
            return HttpResponse(status=204)         #returns no content but 204 status
        else :
            return JsonResponse({'error': 'There is no task at this id'}, status=404)


'''View to edit the title or completion of a specific task'''
@method_decorator(csrf_exempt, name='dispatch')
class UpdateTask(View):
    def put(self, request,id):
            task = get_object_or_404(Tasks, id=id)
            if task:
                data = json.loads(request.body)            #parse the data into json
                task.title = data.get('title', task.title)
                task.completion_status = data.get('completion_status', task.completion_status)
                task.save()                                 #saves the updation
                return HttpResponse(status=204)             #return no content but 204 status
            else:
                return JsonResponse({'error: There is no task at this is'}, status=404) #returns error with status 404


@method_decorator(csrf_exempt, name='dispatch')
class AddBulkTasks(View):
    def post(self,request):
        # try:
            data = json.loads(request.body)
            tasks_data = data.get('tasks', [])
            tasks = []                          #list to store task information
            for item in tasks_data:
                title = item.get('title')
                completion_status = item.get('completion_status',False)  #By default False
                task = Tasks(title=title, completion_status=completion_status)   #Object creation
                task.save()
                tasks.append({'id': task.id})   #appends data wrt to id in task list
            return JsonResponse({'tasks': tasks}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteBulkTasks(View):
    def delete(self,request):
        data = json.loads(request.body)
        task_ids = data.get('ids', [])

        for tid in task_ids:
            try:
                task = Tasks.objects.get(id=tid)
                task.delete()       #deletes the task
            except Tasks.DoesNotExist:
                continue

        return JsonResponse(status=204)



