from django import forms
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView

from munera.services import ParkingService


class LoginRequiredMixin(BaseLoginRequiredMixin):
    login_url = reverse_lazy("login")
    next_page = reverse_lazy("index")


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class ParkingPermitListView(LoginRequiredMixin, TemplateView):
    template_name = "parking_permit_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service = ParkingService(self.request.user)
        context["parking_permits"] = service.list_parking_permits()

        return context


class EditForm(forms.Form):
    registration_number = forms.CharField(label=_("New registration number"))

    def __init__(self, *args, service: ParkingService, **kwargs):
        super().__init__(*args, **kwargs)
        self._service = service
        self.error_not_owned = None

    def save(self, instance):
        success = self._service.change_registration_number(instance.id, self.cleaned_data["registration_number"])
        if not success:
            self.error_not_owned = True
        return success


class ParkingPermitEditlView(LoginRequiredMixin, FormView):
    template_name = "parking_permit_edit.html"
    form_class = EditForm
    success_url = reverse_lazy("parking_permit_list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get("pk")
        service = ParkingService(self.request.user)
        return service.get_parking_permit(pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["service"] = ParkingService(self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parking_permit"] = self.object
        return context

    def form_valid(self, form: EditForm):
        success = form.save(self.object)
        if not success:
            return super().form_invalid(form)
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("index")


class LogoutView(auth_views.LogoutView):
    template_name = "logout.html"
