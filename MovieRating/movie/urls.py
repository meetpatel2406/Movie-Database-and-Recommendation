from django.urls import path 
from . import views 
urlpatterns = [
    path('<int:movie_id>', views.add, name='add'),
    path('search/', views.search,name='search'),
    path('display/<int:movie_id>/',views.display,name='display'), 
    path('add/<int:movie_id>/', views.add,name='add'),
    path('category/<int:movie_id>/',views.add_cat,name="category"),
    path('display_home/<int:movie_id>/',views.display_home,name='display_home'),
    path('delete/<int:movie_id>/',views.delete,name='delete'),
    path('review/<int:movie_id>/create',views.create_reviews,name="createreview"),
    path('review/<int:review_id>/',views.update_reviews,name="updatereview"),
    path('review/<int:review_id>/delete',views.deletereview,name='deletereview'),
      ]
 