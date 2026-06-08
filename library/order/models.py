import time
from django.db import models

from authentication.models import CustomUser
from book.models import Book


def current_timestamp():
    return int(time.time())


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )
    created_at = models.IntegerField(default=current_timestamp)
    end_at = models.IntegerField(null=True, blank=True)
    plated_end_at = models.IntegerField(default=current_timestamp)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} {self.book} {self.user} {self.created_at} {self.end_at} {self.plated_end_at}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "book": self.book.id if self.book else None,
            "user": self.user.id if self.user else None,
            "created_at": self.created_at,
            "end_at": self.end_at,
            "plated_end_at": self.plated_end_at,
        }

    @staticmethod
    def create(user, book, plated_end_at):
        order = Order(user=user, book=book, plated_end_at=plated_end_at)
        order.save()
        return order

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at

        self.save()

    @staticmethod
    def get_all():
        return Order.objects.all()

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at__isnull=True)

    @staticmethod
    def delete_by_id(order_id):
        order = Order.get_by_id(order_id)
        if order:
            order.delete()
            return True
        return False