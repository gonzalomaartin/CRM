from django.shortcuts import render, reverse
from django.views import generic 
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .mixins import OrganizerAndLoginRequiredMixin
from . import forms 
from django.core.mail import send_mail

class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView): 
    template_name = "agent/agent_list.html"
    context_object_name = "agents"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.all()


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView): 
    template_name = "agent/agent_create.html"
    form_class = forms.AgentModelForm 

    def get_success_url(self): 
        return reverse("agents:agent-list")

    def form_valid(self, form): 
        user = form.save(commit = False)
        user.is_agent = True 
        user.is_organizer = False 
        user.set_password("TemporaryPass123")
        user.save() 
        Agent.objects.create(
            user = user, 
            organization = self.request.user.userprofile, 
        )
        send_mail(
            subject = "You are invited to be an agent", 
            message = "You were added as an agent on the CRM. Please login to start working", 
            from_email = "admin@test.com", 
            recipient_list = [user.email]
        )
        #agent.organization = self.request.user.userprofile
        #agent.save() 
        return super(AgentCreateView, self).form_valid(form)
    
class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView): 
    template_name = "agent/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        return Agent.objects.all()

class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView): 
    template_name = "agent/agent_update.html"
    form_class = forms.AgentModelForm 

    def get_success_url(self): 
        return reverse("agents:agent-list")

    def get_queryset(self): 
        return Agent.objects.all()

class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView): 
    template_name = "agent/agent_delete.html"
    context_object_name = "agent"


    def get_queryset(self):
        return Agent.objects.all() 
    
    def get_success_url(self):
        return reverse("agents:agent-list")