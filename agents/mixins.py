from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, reverse

class OrganizerAndLoginRequiredMixin(AccessMixin): 
    def dispatch(self, request, *args, **kwargs): 
        if not request.user.is_authenticated and not request.user.is_organizer: 
            return redirect("leads:lead-list")
        return super().dispatch(request, *args, **kwargs)