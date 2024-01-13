from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name="notes"
urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    #path('', views.home, name='home'),
    path('eleves', views.eleves, name='eleves'),
    path('eleves/<int:eleve_id>/', views.eleve, name='eleve'),
    path('matieres', views.matieres, name='matieres'),
    path('matieres/<int:matiere_id>/', views.matiere, name='matiere'),
    path('niveau/<int:niveau_id>', views.niveau, name='niveau'),
    path('add_note/<int:id_eleve>/<int:matiere_id>', views.add_note, name='add_note'),
    path('add_notes/<int:matiere_id>', views.add_notes, name='add_notes'),
    path('add_eleve', views.add_eleve, name='add_eleve'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("ouvrir_pdf", views.listEleves, name='listEleves'),
    path("niveau_eleve/<int:niveau_id>/", views.niveauElv, name='niveau_eleve'),
    path("notesEleves/<int:matiere_id>/",views.notesEleves, name="notesEleves"),
    path("notesynthese/<int:eleve_id>/", views.notesSynthese, name='notesynthese'),
    #path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html")),
]