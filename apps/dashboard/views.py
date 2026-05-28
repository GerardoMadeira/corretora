from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):

        context = {"usuario": request.user}

        return render(request, "dashboard/dashboard.html", context)
