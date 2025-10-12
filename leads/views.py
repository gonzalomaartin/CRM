from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from django.views import generic 
from .models import Lead, Category
from .forms import LeadModelForm, LeadForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from agents.mixins import OrganizerAndLoginRequiredMixin

# turn the function views into class views

class LandingPageView(TemplateView): 
    template_name = "landing.html"

def landing_page(request): 
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, ListView): 
    template_name = "lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user #We've got a request user, because we first made sure the user is logged in through the mixin
        if user.is_organizer: 
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull = False)
        else: 
            queryset = Lead.objects.filter(organization = user.agent.organization, agent__isnull = False)
            queryset = queryset.filter(agent__user = user)

        return queryset

    def get_context_data(self, **kwargs):  # Changed from context_data to get_context_data
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer: 
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull = True)
            context.update({
                "unassigned_leads": queryset
            })
        return context
    

def lead_list(request):
    leads = Lead.objects.all() 
    context = {
        "leads": leads
    }
    return render(request, "lead_list.html", context)

class LeadDetailView(LoginRequiredMixin, DetailView): 
    template_name = "lead_detail.html"
    queryset = Lead.objects.all() #it automatically searches for the primary key that you pass to it 
    context_object_name = "lead"


    def get_queryset(self):
        user = self.request.user #We've got a request user, because we first made sure the user is logged in through the mixin
        if user.is_organizer: 
            queryset = Lead.objects.filter(organization = user.userprofile)
        else: 
            queryset = Lead.objects.filter(organization = user.agent.organization)
            queryset = queryset.filter(agent__user = user)

        return queryset


def lead_detail(request, pk): 
    lead = Lead.objects.get(id = pk)
    context = {
        "lead": lead
    }
    return render(request, "lead_detail.html", context)


class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView): 
    template_name = "lead_create.html"
    form_class = LeadModelForm
    context_object_name = "lead"

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form): 
        # set the lead's organization to the organization of the user
        # creating the lead (organizer.userprofile or agent.organization)
        user = self.request.user
        if user.is_organizer:
            form.instance.organization = user.userprofile
        else:
            form.instance.organization = user.agent.organization

        # keep existing behavior: if an agent was chosen on the form, the
        # lead.agent will be set from the form; organization now has been
        # assigned from the creator's org so leads are correctly scoped.
        send_mail(
            subject = "A lead has been created",
            message = "Go to the site to see the new lead",
            from_email = "test@test.com",
            recipient_list = ["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

def lead_create(request): 
    form = LeadModelForm() 
    if request.method == "POST": 
        print("Recieving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid(): 
            form.save() 
            return redirect("/leads")
    context = {
        "form": LeadModelForm()
    }
    return render(request, "lead_create.html", context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView): 
    template_name = "lead_update.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user #We've got a request user, because we first made sure the user is logged in through the mixin
        return Lead.objects.filter(organization = user.userprofile)

def lead_update(request, pk): 
    lead = Lead.objects.get(id = pk)
    form = LeadModelForm() 
    if request.method == "POST": 
        form = LeadModelForm(request.POST, instance = lead)
        if form.is_valid(): 
            form.save()
            return redirect("/leads")
        
    context = {
        "lead": lead, 
        "form": form, 
    }
    return render(request, "lead_update.html", context)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView): 
    template_name = "lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user #We've got a request user, because we first made sure the user is logged in through the mixin
        return Lead.objects.filter(organization = user.userprofile)


def lead_delete(request, pk): 
    lead = Lead.objects.get(id = pk)
    lead.delete() 
    return redirect("/leads")



class SignupView(CreateView): 
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")
    


class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView): 
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs): 
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")


    def form_valid(self, form): 
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent 
        lead.save() 
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView): 
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs): 
        user = self.request.user #We've got a request user, because we first made sure the user is logged in through the mixin
        if user.is_organizer: 
            queryset = Lead.objects.filter(organization = user.userprofile)
        else: 
            queryset = Lead.objects.filter(organization = user.agent.organization)
        context = super().get_context_data(**kwargs)
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull = True).count()
        })
        return context 
    
    def get_queryset(self):
        user = self.request.user #We've got a request user, because we first made sure the user is logged in through the mixin
        if user.is_organizer: 
            queryset = Category.objects.filter(organization = user.userprofile)
        else: 
            queryset = Category.objects.filter(organization = user.agent.organization)

        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView): 
    template_name = "category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs): 
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        leads = self.get_object().leads.all()
        context.update({
            "leads": leads
        })
        return context 

    def get_queryset(self):
        user = self.request.user #We've got a request user, because we first made sure the user is logged in through the mixin
        if user.is_organizer: 
            queryset = Category.objects.filter(organization = user.userprofile)
        else: 
            queryset = Category.objects.filter(organization = user.agent.organization)

        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView): 
    template_name = "lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user #We've got a request user, because we first made sure the user is logged in through the mixin
        if user.is_organizer: 
            queryset = Lead.objects.filter(organization = user.userprofile)
        else: 
            queryset = Lead.objects.filter(organization = user.agent.organization)
            queryset = queryset.filter(agent__user = user)

        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs = {"pk": self.get_object().id})
