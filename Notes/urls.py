from django.urls import path
from . import views

app_name="notes"
urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.home, name='home'),
    path('eleves', views.eleves, name='eleves'),
    path('eleves/<int:eleve_id>/', views.eleve, name='eleve'),
    path('matieres', views.matieres, name='matieres'),
    path('matieres/<int:matiere_id>/', views.matiere, name='matiere'),
    path('niveau/<int:niveau_id>', views.niveau, name='niveau'),
]