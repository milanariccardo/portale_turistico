from django.urls import path

from forum.views import MainPageForum, CreateCategoryForum, UpdateCategoryForum

urlpatterns = [
    path('', MainPageForum.as_view(), name='mainPageCategory'),
    path('create_category/', CreateCategoryForum.as_view(), name='createCategory'),
    # path('edit_category/<char:title>/', UpdateCategoryForum.as_view(), name='editCategory'),

]
