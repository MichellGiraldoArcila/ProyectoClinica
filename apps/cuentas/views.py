from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.cuentas.forms import RegistroUsuarioForm


class LoginUsuarioView(LoginView):
    template_name = 'cuentas/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('cuentas:dashboard')


class RegistroUsuarioView(FormView):
    template_name = 'cuentas/registro.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('cuentas:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('cuentas:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            f'Cuenta creada correctamente. Bienvenido, {user.get_username()}.',
        )
        return super().form_valid(form)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('cuentas:login')
    return render(request, 'cuentas/dashboard.html')


def logout_usuario(request):
    logout(request)
    return redirect('cuentas:login')
