from django.urls import path

from parameters.views import PrivacyPolicyListView, DeliveryInformationListView, ReturnsAndRefundsListView, \
    TermsAndConditionsListView

app_name = 'parameters'

urlpatterns = [
    path('privacy-policy/', PrivacyPolicyListView.as_view(), name='privacy_policy'),
    path('delivery-information/', DeliveryInformationListView.as_view(), name='delivery_information'),

    path('returns-and-refunds/', ReturnsAndRefundsListView.as_view(), name='returns_and_refunds'),
    path('terms-and-conditions/', TermsAndConditionsListView.as_view(), name='terms_and_conditions'),
]
