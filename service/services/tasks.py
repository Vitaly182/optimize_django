from celery import shared_task
from django.db.models import F


@shared_task
def set_price(subscription_id):
    from services.models import Subscription

    subscription = Subscription.objects.filter(id=subscription_id).annotate(
        anntated_price=F('service__full_price') -
                       F('service__full_price') * F('plan__discount_percent') / 100.00).first()
    subscription.price = subscription.anntated_price
    subscription.save()
