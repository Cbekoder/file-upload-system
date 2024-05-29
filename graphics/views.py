from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
import json
from django.views import View
from users.models import User
from .models import *

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            notifications = {}

            for category in categories:
                unread_count = RecievedFiles.objects.filter(
                    file__category=category,
                    isRead=False,
                ).count()
                if unread_count > 0:
                    notifications[category.id] = unread_count

            context = {
                "user": request.user,
                "categories": categories,
                'notifications': notifications,
            }

            return render(request, 'index.html', context)
        return redirect('login')

class FilesView(View):
    def get(self, request, type, category):
        if request.user.is_authenticated:
            category = get_object_or_404(Category, title__iexact=category)
            if type == "from":
                files = File.objects.filter(
                    user=request.user,
                    category=category,
                )
            elif type == "to":
                files = File.objects.filter(
                    to_user=request.user,
                    category=category,
                )
            else:
                return render(request,'404.html')

            categories = Category.objects.all()
            roles = Role.objects.all()
            users = User.objects.exclude(id=request.user.id)
            user_by=request.user
            context = {
                "user": request.user,
                "categories": categories,
                "roles": roles,
                "users": users,
                "files": files,
                "user_by": user_by,
            }
            return render(request, 'files.html', context)
        return redirect('login')



class UploadFileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            roles = Role.objects.all()
            users = User.objects.exclude(id=request.user.id)
            user_by = request.user
            context = {
                "user": request.user,
                "categories": categories,
                "roles": roles,
                "users": users,
                "user_by": user_by,
            }
            return render(request, 'file_upload.html', context)
        return redirect('/login')
    def post(self, request):
        if request.user.is_authenticated:
            file = request.FILES['file']
            category_title = request.POST.get('category')
            to_user_id = request.POST.get('to_user')
            description = request.POST.get('desc')

            category = get_object_or_404(Category, title__iexact=category_title)
            to_user = get_object_or_404(User, id=to_user_id)

            file = File.objects.create(
                file=file,
                user=request.user,
                category=category,
                to_user=to_user,
                description=description,
            )
            resieved_file=RecievedFiles.objects.create(
                file=file.id,

            )
            return redirect('/files')
        return redirect('/login')










# class NodeGroupView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             context = {
#                 "user": request.user,
#                 'groups': NodeGroups.objects.filter(user_id=request.user.id)
#             }
#             return render(request, 'categories.html', context)
# #         return redirect('login')
#
#     def post(self, request):
#         if request.user.is_authenticated:
#             if request.POST.get('action') == 'new':
#                 group = NodeGroups.objects.create(
#                     title=request.POST.get('title').title(),
#                     status="Yangi",
#                     user_id=request.user
#                 )
#             elif request.POST.get('action') == 'alter':
#                 group = NodeGroups.objects.get(id=request.POST.get('groid'))
#                 group.title = request.POST.get('title').title()
#                 group.status = request.POST.get('status')
#                 group.save()
#             return redirect('folders')
#         return redirect('login')


# class TreeNode(View):
#     def get(self, request, pk):
#         if request.user.is_authenticated:
#             folder = NodeGroups.objects.get(id=pk)
#             context = {
#                 "user": request.user,
#                 "folder": folder,
#                 "scripts": Script.objects.filter(folder_id=folder)
#             }
#             return render(request, 'tree_node.html', context)
#         return redirect('login')
#
#     def post(self, request, pk):
#         if request.user.is_authenticated:
#             if request.POST.get('forma') == 'f1':
#                 node = Script.objects.get(id=request.POST.get("node_id"))
#                 node.question_uz = request.POST.get('question_uz')
#                 node.answer_uz = request.POST.get('answer_uz')
#                 node.question_ru = request.POST.get('question_ru')
#                 node.answer_ru = request.POST.get('answer_ru')
#                 node.save()
#
#             elif request.POST.get('forma') == 'f2':
#                 script = Script.objects.create(
#                     folder_id = NodeGroups.objects.get(id=pk),
#                     question_uz = request.POST.get('question_uz'),
#                     question_ru = request.POST.get('question_ru'),
#                     answer_uz = request.POST.get('answer_uz'),
#                     answer_ru = request.POST.get('answer_ru'),
#                     parent_id = Script.objects.get(id=request.POST.get('parent_id'))
#                 )
#
#
#             return redirect(f'/edit/groups/{pk}')
#         return redirect('login')

# class DefaultAdd(View):
#     def get(self, request, pk):
#         if request.user.is_authenticated:
#             folder = NodeGroups.objects.get(id=pk)
#             if Script.objects.filter(folder_id=folder).count() == 0 and folder.user_id == request.user:
#                 script = Script.objects.create(
#                     folder_id= folder,
#                     question_uz=None,
#                     answer_uz="Assalomu alaykum, Bu botning birinchi xabari!!!",
#                     question_ru=None,
#                     answer_ru="Привет! Это первая новость об этом боте!!!",
#                     parent_id=None
#                 )
#                 folder.status = "Faol"
#                 folder.save()
#
#                 return redirect(f'/edit/groups/{pk}')
#         return redirect('login')
#
# def delete_group(request, pk):
#     group = get_object_or_404(NodeGroups, id=pk)
#     if request.user.is_authenticated and group.user_id == request.user:
#         group.delete()
#         return redirect('/edit/groups/')
#     return redirect('login')
#
# def delete_script(request, pk):
#     script = get_object_or_404(Script, id=pk)
#     group_id = script.folder_id
#     if request.user.is_authenticated and group_id.user_id == request.user:
#         script.delete()
#         return redirect(f'/edit/groups/{group_id.id}')
#     return redirect('login')
#