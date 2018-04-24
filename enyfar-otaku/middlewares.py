from django.utils import timezone
from accounts.models import User
from transaction.models import Order

class DeleteMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        users = User.objects.filter(social_confirm_deadline__lte= timezone.now())
        orders = Order.objects.filter(status_deadline__lte=timezone.now())
        users.delete()
        orders.delete()

        return response
