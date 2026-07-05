from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order, OrderItem
from inventory.models import BookCopy


class Command(BaseCommand):
    help = 'Automatically release reservations that have expired'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_orders = Order.objects.filter(
            status=Order.Status.RESERVED,
            reserved_until__lt=now
        )

        count = 0
        for order in expired_orders:
            self.stdout.write(self.style.WARNING(f"Processing expired Order #{order.id} for user {order.client.username}"))
            
            # Cancel order items and set copies back to available
            for item in order.items.all():
                item.status = OrderItem.Status.CANCELED
                item.save()
                
                # Make the physical copy available again
                copy = item.copy
                copy.status = BookCopy.Status.AVAILABLE
                copy.save()
                self.stdout.write(f"  - Released copy [{copy.barcode}] ({copy.book.title})")
                
            # Cancel the order itself
            order.status = Order.Status.CANCELED
            order.save()
            count += 1

        if count > 0:
            self.stdout.write(self.style.SUCCESS(f"Successfully released {count} expired reservations."))
        else:
            self.stdout.write(self.style.SUCCESS("No expired reservations found."))
