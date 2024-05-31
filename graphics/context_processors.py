from users.models import User
from .models import Category, RecievedFiles
def common_data(request):
    if request.user.is_authenticated:
        icategories = Category.objects.filter(is_active=True)
        notifications = {}
        all_notifications = 0
        all_categories = []
        for category in icategories:
            unread_count = RecievedFiles.objects.filter(
                file__category=category,
                file__to_user=request.user,
                isRead=False,
            ).count()
            if unread_count > 0:
                notifications[int(category.id)] = unread_count
                all_notifications += unread_count
                all_categories.append(category.id)
        if all_notifications > 0:
            notifications['all'] = all_notifications
        notifications["all_categories"] = all_categories
        return {
            'icategories': icategories,
            'notifications': notifications,
            'user': request.user,
        }
    return {}
