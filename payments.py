import os
import razorpay

def create_razorpay_link(amount_paise):
    client = razorpay.Client(auth=(
        os.getenv("RAZORPAY_KEY"),
        os.getenv("RAZORPAY_SECRET")
    ))
    
    payment = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })
    return payment.get("short_url", "https://razorpay.com/payment-link")
