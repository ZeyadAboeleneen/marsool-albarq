from django.shortcuts import render
from django.utils import timezone

from apps.accounts.permissions import require_membership
from apps.quotations.models import Quotation, QuotationStatus


@require_membership
def home(request):
    quotes = Quotation.objects.for_org(request.organization)
    today = timezone.localdate()
    month = quotes.filter(issue_date__year=today.year, issue_date__month=today.month).exclude(
        status__in=[QuotationStatus.DRAFT, QuotationStatus.CANCELLED]
    )
    ctx = {
        "my_drafts": quotes.filter(status=QuotationStatus.DRAFT, created_by=request.user)
        .select_related("customer")
        .order_by("-updated_at")[:5],
        "recent": quotes.issued().select_related("customer").order_by("-finalized_at")[:5],
        "month_count": month.count(),
        "month_accepted": month.filter(status=QuotationStatus.ACCEPTED).count(),
    }
    return render(request, "dashboard/home.html", ctx)
