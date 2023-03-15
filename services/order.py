from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session_id = ticket["movie_session"]

            Ticket.objects.create(
                movie_session_id=movie_session_id,
                order=order,
                row=row,
                seat=seat
            )


def get_orders(
        username: str = None
) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(
            user__username=username
        )
    return queryset