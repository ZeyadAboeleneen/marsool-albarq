from django.shortcuts import render

from apps.accounts.permissions import require_membership


@require_membership
def home(request):
    return render(request, "dashboard/home.html")
