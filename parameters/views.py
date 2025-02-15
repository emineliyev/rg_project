from django.views.generic import ListView
from parameters.models import PrivacyPolicy, Contact, DeliveryInformation, ReturnsAndRefunds, TermsAndConditions


class PrivacyPolicyListView(ListView):
    model = PrivacyPolicy
    template_name = 'parameters/privacy-policy.html'
    context_object_name = 'secrets'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['contacts'] = Contact.objects.all()
        context['deliveries'] = DeliveryInformation.objects.all()
        return context


class DeliveryInformationListView(ListView):
    model = DeliveryInformation
    template_name = 'parameters/delivery-information.html'
    context_object_name = 'deliveries'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['contacts'] = Contact.objects.all()
        return context


class ReturnsAndRefundsListView(ListView):
    model = ReturnsAndRefunds
    template_name = 'parameters/returns-and-refunds.html'
    context_object_name = 'returns'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['contacts'] = Contact.objects.all()
        return context


class TermsAndConditionsListView(ListView):
    model = TermsAndConditions
    template_name = 'parameters/terms-and-conditions.html'
    context_object_name = 'terms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['contacts'] = Contact.objects.all()
        return context
