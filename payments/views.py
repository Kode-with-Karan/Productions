from django.shortcuts import render
from .models import Transaction, Withdrawal, Earnings
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user.profile)
    return render(request, 'payments/transactions.html', {'transactions': transactions})





stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def earnings(request):

    


    user = request.user

    # Create a Stripe Express account for the user
    account = stripe.Account.create(
        type="express",
        email="l.ilym.a.nde.rs.on81.3@gmail.com",
        capabilities={
        "transfers": {"requested": True}  # Enable Transfers Capability
    }
    )

    # Store the account ID in the user's profile
    user.profile.stripe_account_id = account.id
    user.profile.save()
    account = stripe.Account.retrieve(user.profile.stripe_account_id)
    if account.capabilities.get("transfers") == "active":
        print("Transfers are enabled ✅")
    else:
        print("Transfers are NOT enabled ❌, please complete onboarding.")

    # Generate an account link for onboarding
    account_link = stripe.AccountLink.create(
        account=account.id,
        refresh_url="https://yourwebsite.com/stripe/refresh/",
        return_url="https://yourwebsite.com/dashboard/",
        type="account_onboarding",
    )


    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        user = request.user

        # Check if user has enough balance
        if user.profile.total_earnings >= amount:
            if not user.profile.stripe_account_id:  
                # If user has no Stripe account ID, show a message
                Notification.objects.create(user=user, message="Withdrawal failed: No Stripe account connected.")
                messages.error(request, "You need to connect a Stripe account before withdrawing funds.")
                return redirect("withdrawal_page")

            try:
                # Transfer money to user's Stripe account
                transfer = stripe.Transfer.create(
                    amount=int(amount * 100),  # Convert to cents
                    currency="usd",
                    destination=user.profile.stripe_account_id,
                    # destination="hello",
                    description="Withdrawal Request"
                )

                # Deduct amount from user's total_earnings
                user.profile.total_earnings -= amount
                user.profile.save()

                # Save withdrawal record
                Withdrawal.objects.create(user=user, amount=amount, status="Completed")

                # Save success notification
                Notification.objects.create(user=user, message=f"Your withdrawal of ${amount} was successful.")

                messages.success(request, "Withdrawal successful!")
            except stripe.error.StripeError as e:
                Notification.objects.create(user=user, message="Withdrawal failed due to payment gateway error.")
                messages.error(request, f"Error: {e.user_message}")
        else:
            Notification.objects.create(user=user, message="Withdrawal failed due to insufficient balance.")
            messages.error(request, "Insufficient funds for withdrawal.")

        return redirect("home")

    return render(request, "payments/earnings.html")

# @login_required
# def earnings(request):
#     user = request.user
#     earnings = Earnings.objects.filter(user=user)
#     withdrawals = WithdrawalRequest.objects.filter(user=user)

#     if request.method == "POST":
#         amount = request.POST.get("amount")
#         method = request.POST.get("method")
#         if float(amount) > 0:
#             WithdrawalRequest.objects.create(user=user, amount=amount, method=method, status="Pending")
    
#     return render(request, "payments/earnings.html", {"earnings": earnings, "withdrawals": withdrawals})