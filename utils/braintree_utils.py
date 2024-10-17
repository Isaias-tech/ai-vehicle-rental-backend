import braintree
from django.conf import settings


def get_braintree_gateway():
    return braintree.BraintreeGateway(
        braintree.Configuration(
            (
                braintree.Environment.Sandbox
                if settings.BRAINTREE_ENVIRONMENT == "Sandbox"
                else braintree.Environment.Production
            ),
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )
    )
