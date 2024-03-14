from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
import json
from django.views import View
from users.models import User
from .models import *

class NodeGroupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                "user": request.user,
                'groups': NodeGroups.objects.filter(user_id=request.user.id)
            }
            return render(request, 'tables.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            if request.POST.get('action') == 'new':
                group = NodeGroups.objects.create(
                    title=request.POST.get('title').title(),
                    status="Yangi",
                    user_id=request.user
                )
            elif request.POST.get('action') == 'alter':
                group = NodeGroups.objects.get(id=request.POST.get('groid'))
                group.title = request.POST.get('title').title()
                group.status = request.POST.get('status')
                group.save()
            return redirect('folders')
        return redirect('login')


class TreeNode(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            folder = NodeGroups.objects.get(id=pk)
            context = {
                "user": request.user,
                "folder": folder,
                "scripts": Script.objects.filter(folder_id=folder)
            }
            return render(request, 'tree_node.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            if request.POST.get('forma') == 'f1':
                node = Script.objects.get(id=request.POST.get("node_id"))
                node.question_uz = request.POST.get('question_uz')
                node.answer_uz = request.POST.get('answer_uz')
                node.question_ru = request.POST.get('question_ru')
                node.answer_ru = request.POST.get('answer_ru')
                node.save()

            elif request.POST.get('forma') == 'f2':
                script = Script.objects.create(
                    folder_id = NodeGroups.objects.get(id=pk),
                    question_uz = request.POST.get('question_uz'),
                    question_ru = request.POST.get('question_ru'),
                    answer_uz = request.POST.get('answer_uz'),
                    answer_ru = request.POST.get('answer_ru'),
                    parent_id = Script.objects.get(id=request.POST.get('parent_id'))
                )


            return redirect(f'/edit/groups/{pk}')
        return redirect('login')

class DefaultAdd(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            folder = NodeGroups.objects.get(id=pk)
            if Script.objects.filter(folder_id=folder).count() == 0 and folder.user_id == request.user:
                script = Script.objects.create(
                    folder_id= folder,
                    question_uz="Robot",
                    answer_uz="Assalomu alaykum",
                    question_ru="Робот",
                    answer_ru="Привет",
                    parent_id=None
                )
                folder.status = "Faol"
                folder.save()

                return redirect(f'/edit/groups/{pk}')
        return redirect('login')

def delete_group(request, pk):
    group = get_object_or_404(NodeGroups, id=pk)
    if request.user.is_authenticated and group.user_id == request.user:
        group.delete()
        return redirect('/edit/groups/')
    return redirect('login')

def delete_script(request, pk):
    script = get_object_or_404(Script, id=pk)
    group_id = script.folder_id
    if request.user.is_authenticated and group_id.user_id == request.user:
        script.delete()
        return redirect(f'/edit/groups/{group_id.id}')
    return redirect('login')

class JSONConvView(View):
    def get(self, request, pk):
        # download = request.GET.get('download', False)
        download = True
        if download:
            # Download the JSON file
            data = self.get_tree_structure(pk)
            response = JsonResponse(data, json_dumps_params={'indent': 2}, safe=False)
            response['Content-Disposition'] = 'attachment; filename=tree_data.json'
            return response
        else:
            # Return JSON data
            data = self.get_tree_structure(pk)
            return JsonResponse(data, json_dumps_params={'indent': 2})

    def get_tree_structure(self, pk, parent_id=None):
        scripts = Script.objects.filter(parent_id=parent_id, folder_id=pk)
        data = []
        for script in scripts:
            script_data = {
                'id': script.id,
                'question': script.question,
                'answer': script.answer,
                'parent_id': script.parent_id,  # Use script.parent_id_id to get the actual ID
                'child_nodes': self.get_tree_structure(script.id)
            }
            data.append(script_data)

        # If parent_id is None, include Profile data
        if parent_id is None:
            profile = User.objects.filter(id=self.request.user.id).first()
            if profile:
                profile_data = {
                    'id': 'profile',
                    'name': profile.username,
                    # 'company': profile.company,
                    # 'location': profile.location,
                    # 'description': profile.description,
                    # 'type': profile.type,
                    # 'pro': profile.pro
                }
                data.insert(0, profile_data)

        return data


