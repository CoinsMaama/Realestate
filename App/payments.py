import razorpay
import os

def create_razorpay_order(amount_in_paise):
    try:
        client = razorpay.Client(auth=(
            os.getenv("RAZORPAY_KEY"), 
            os.getenv("RAZORPAY_SECRET"))
        )
        
        order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1
        })
        return order
    except Exception as e:
        print(f"Payment error: {e}")
        return None
