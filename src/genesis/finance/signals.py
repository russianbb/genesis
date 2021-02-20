# from django.db import transaction
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import CostCenter, ServiceOrder


# def create_costcenter(instance):
#     cost_center = CostCenter(description=instance.description)
#     cost_center.save()


# @receiver(post_save, sender=ServiceOrder)
# def receiver_signal_serviceorder_created(sender, instance, **kwargs):
#     if kwargs["created"]:
#         transaction.on_commit(create_costcenter(instance))
