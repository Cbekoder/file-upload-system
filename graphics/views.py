from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import OuterRef, Subquery, Q
from django.views import View
from users.models import User
from .models import *


def UserNotifications(user):
    categories = Category.objects.filter(is_active=True)
    notifications = {}
    all_notifications = 0
    all_categories = []
    for category in categories:
        unread_count = RecievedFiles.objects.filter(
            file__category=category,
            file__to_user=user,
            isRead=False,
        ).count()
        if unread_count > 0:
            notifications[int(category.id)] = unread_count
            all_notifications += unread_count
            all_categories.append(category.id)
    if all_notifications > 0:
        notifications['all'] = all_notifications
    notifications["all_categories"] = all_categories
    return notifications

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'index.html',)
        return redirect('login')

class FilesView(View):
    def get(self, request, typef, category):
        if request.user.is_authenticated:
            if category != "all":
                category = get_object_or_404(Category, title__iexact=category)

            if typef == "data":
                files = File.objects.filter(
                    Q(user=request.user) | Q(to_user=request.user)
                )
            elif typef == "to":
                if category == "all":
                    files = File.objects.filter(
                        to_user=request.user,
                    ).annotate(
                        is_read=Subquery(
                            RecievedFiles.objects.filter(
                                file=OuterRef('pk')
                            ).values('isRead')[:1])
                    )
                else:
                    files = File.objects.filter(
                        to_user=request.user,
                        category=category,
                    ).annotate(
                        is_read=Subquery(
                            RecievedFiles.objects.filter(
                                file=OuterRef('pk')
                            ).values('isRead')[:1])
                    )
            elif typef == "from":
                if category == "all":
                    files = File.objects.filter(
                        user=request.user,
                    )
                else:
                    files = File.objects.filter(
                        user=request.user,
                        category=category,
                    )
            else:
                return render(request, '404.html')

            # Handle Filtering
            filter_by = request.GET.get('filter')
            if filter_by:
                if filter_by == 'unread':
                    unread_received_files = RecievedFiles.objects.filter(isRead=False, file__to_user=request.user)
                    files = File.objects.filter(id__in=unread_received_files.values('file_id'))
                elif filter_by == 'isNotCompleted':
                    undonefiles = RecievedFiles.objects.filter(isCompleted=False, file__to_user=request.user, file__category__is_done_required=True)
                    files = File.objects.filter(id__in=undonefiles.values('file_id'))


            sort_by = request.GET.get('sort')
            if sort_by=="uploaded_date":
                files = files.order_by("-uploaded_date")
            elif sort_by=="-uploaded_date":
                files = files.order_by("uploaded_date")

            # Pagination
            per_page = request.GET.get('per_page', 10)
            paginator = Paginator(files, per_page)
            page = request.GET.get('page')

            try:
                paginated_files = paginator.page(page)
            except PageNotAnInteger:
                paginated_files = paginator.page(1)
            except EmptyPage:
                paginated_files = paginator.page(paginator.num_pages)

            context = {
                'per_page': int(per_page),
                "files": paginated_files,
                "user_by": request.user,
                'categories': Category.objects.all(),  # Include categories for filtering
                'users': User.objects.all(),  # Include users for filtering
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
            to_user_id = request.POST.get('to_user')
            description = request.POST.get('desc')
            category_id = request.POST.get('category')
            category_instance = get_object_or_404(Category, pk=category_id)
            to_user = get_object_or_404(User, id=to_user_id)
            uploaded_file = request.FILES.get('file')

            file_instance = File.objects.create(
                file=uploaded_file,
                user=request.user,
                category=category_instance,
                to_user=to_user,
                description=description,
            )
            RecievedFiles.objects.create(
                file=file_instance,
            )
            return redirect(f'/files/from/{Category.objects.get(id=category_id).title.lower()}/')
        return redirect('login')

class FileDetailView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            categories = Category.objects.all()
            file = File.objects.get(id=pk)
            recieved = RecievedFiles.objects.filter(file=file).first()
            if file.to_user == request.user:
                recieved.isRead = True
                recieved.save()
            context = {
                "user": request.user,
                "recieved": recieved,
                "categories": categories,
                "file": file,
            }
            return render(request, "file_detail.html", context)
        return redirect('login/')
    def post(self, request, pk):
        if request.user.is_authenticated:
            file = File.objects.get(id=pk)
            received = RecievedFiles.objects.get(file=file)
            received.comment = request.POST.get('desc')
            received.isCompleted = True
            received.save()
            return redirect(f'/files/to/{file.category.title.lower()}/')
        return redirect('login')


class CategoriesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                "user": request.user,
                'categories': Category.objects.all()
            }
            return render(request, 'categories.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            if request.POST.get('action') == 'new':
                Category.objects.create(
                    title=request.POST.get('title').title(),
                )
            elif request.POST.get('action') == 'alter':
                category = Category.objects.get(id=request.POST.get('cid'))
                category.title = request.POST.get('title').title()
                category.is_active = True if request.POST.get('is_active') == "on" else False
                category.is_done_required = True if request.POST.get('is_done_required') == "on" else False
                category.save()
            return redirect('categories')
        return redirect('login')

class RolesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                "user": request.user,
                'roles': Role.objects.all()
            }
            return render(request, 'roles.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            if request.POST.get('action') == 'new':
                Role.objects.create(
                    title=request.POST.get('title').title(),
                )
            elif request.POST.get('action') == 'alter':
                role = Role.objects.get(id=request.POST.get('cid'))
                role.title = request.POST.get('title').title()
                role.save()
            return redirect('roles')
        return redirect('login')





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
