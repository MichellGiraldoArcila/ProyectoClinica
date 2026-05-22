"""Personalización global del panel de administración Django."""
from django.contrib import admin


class SaludVidaAdminSite(admin.AdminSite):
    site_header = 'IPS Salud y Vida — Historia Clínica Electrónica'
    site_title = 'HCE Salud y Vida'
    index_title = 'Panel de administración — Resolución 866/2021'
    site_url = '/'

    def each_context(self, request):
        context = super().each_context(request)
        context['site_brand'] = 'Salud y Vida'
        return context


admin_site = SaludVidaAdminSite(name='salud_vida_admin')
