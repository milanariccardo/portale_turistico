from django.urls import path

from forum.views import MainPageForum, CreateCategoryForum, UpdateCategoryForum, ViewThreadCategoryForum, \
    CreateThreadForum, ViewThreadCommentForum, CreateCommentThreadForum, lockThread, delete_thread, unlockThread, \
    delete_comment, EditCommentForum

urlpatterns = [
    path('', MainPageForum.as_view(), name='mainPageCategory'),
    path('create_category/', CreateCategoryForum.as_view(), name='createCategory'),
    path('edit_category/<int:pk>/', UpdateCategoryForum.as_view(), name='editCategory'),
    path('thread_category/<int:pk>/', ViewThreadCategoryForum.as_view(), name='viewThreadCategory'),
    path('thread_category/<int:pk>/create_thread/', CreateThreadForum.as_view(), name='createThread'),
    path('thread_category/<int:pk_category>/view_thread_comment/<int:pk_thread>/', ViewThreadCommentForum.as_view(), name='viewThreadComment'),
    path('thread_category/<int:pk_category>/view_thread_comment/<int:pk_thread>/create_comment/', CreateCommentThreadForum.as_view(), name='createComment'),
    path('thread_category/<int:pk_category>/lock_thread/<int:pk_thread>/', lockThread, name='lockThread' ),
    path('thread_category/<int:pk_category>/unlock_thread/<int:pk_thread>/', unlockThread, name='unlockThread' ),
    path('thread_category/<int:pk_category>/delete_thread/<int:pk_thread>/', delete_thread, name='deleteThread' ),
    path('thread_category/<int:pk_category>/view_thread_comment/<int:pk_thread>/delete_comment/<int:pk_comment>/', delete_comment, name='deleteComment' ),
    path('thread_category/<int:pk_category>/view_thread_comment/<int:pk_thread>/edit_comment/<int:pk_comment>/', EditCommentForum.as_view(), name='editComment' ),
    # path('title_exist/', ajax_title_existing, name='ajax-title-existing'),
]
