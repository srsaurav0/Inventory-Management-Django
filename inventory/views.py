from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
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
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            # Add user to Property Owners group
            property_owners_group = Group.objects.get(name="Property Owners")
            user.groups.add(property_owners_group)

            # Add a success message
            messages.success(
                request, "Sign-up successful! Welcome to Property Management System."
            )

            # Redirect to the admin page
            return redirect("/admin/")
        return render(request, self.template_name, {"form": form})
