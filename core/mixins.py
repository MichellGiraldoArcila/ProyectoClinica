from django.contrib.auth.mixins import LoginRequiredMixin


class AuthRequiredMixin(LoginRequiredMixin):
    login_url = 'cuentas:login'
