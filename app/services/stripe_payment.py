import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_payment_intent(amount: float, currency: str = "pkr"):
    """
    Creates a Stripe Payment Intent in Pakistani Rupees (PKR).
    'amount' should be a float (e.g., 1500.00)
    """
    try:
        amount_in_paisa = int(amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_in_paisa,
            currency=currency, 
            metadata={"integration_check": "accept_a_payment"},
            description="CommerceCore Order Payment"
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id
        }
    except Exception as e:
        print(f"Stripe Error: {str(e)}")
        return None