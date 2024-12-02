from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .forms import PropertyOwnerSignUpForm


class PropertyOwnerSignUpView(View):
    template_name = "inventory/signup.html"

    def get(self, request):
        form = PropertyOwnerSignUpForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PropertyOwnerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            # Add user to Property Owners group
            property_owners_group = Group.objects.get(name="Property Owners")
            user.groups.add(property_owners_group)
            return redirect("property_owner_signup")  # Redirect to a success page
        return render(request, self.template_name, {"form": form})
