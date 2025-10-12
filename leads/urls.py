from django.urls import path 
from . import views 

# namespacing for include(..., namespace='leads') in project urls
app_name = 'leads'

urlpatterns = [
    #path("", views.lead_list,  name = "lead-list"),
    path("", views.LeadListView.as_view(), name = "lead-list"), 
    #path("<int:pk>/", views.lead_detail, name = "lead-detail"), #The variable that shows here is the same that the one passed to lead_detail, we need to specify it's an int so that pk doesn't try to match everything
    path("<int:pk>/", views.LeadDetailView.as_view(), name = "lead-detail"), 
    #path("<int:pk>/update/", views.lead_update, name = "lead-update"), 
    path("<int:pk>/update/", views.LeadUpdateView.as_view(), name = "lead-update"), 
    #path("<int:pk>/delete/", views.lead_delete, name = "lead-delete"), 
    path("<int:pk>/delete/", views.LeadDeleteView.as_view(), name = "lead-delete"), 
    #path("create/", views.lead_create, name = "lead-create"), 
    path("<int:pk>/assign-agent/", views.AssignAgentView.as_view(), name = "assign-agent"), 
    path("create/", views.LeadCreateView.as_view(), name = "lead-create"), 
    path("categories/", views.CategoryListView.as_view(), name = "category-list"), 
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name = "category-detail"), 
    path("<int:pk>/category/", views.LeadCategoryUpdateView.as_view(), name = "category-update"), 
]