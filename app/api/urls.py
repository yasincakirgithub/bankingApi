from django.urls import path
from .views import (
    CustomerListCreateAPIView,
    AccountCreateAPIView,
    AccountListAPIView,
    AccountDetailAPIView,
    DepositListCreateAPIView,
    WithdrawListCreateAPIView,
    TransferAPIView,
    AccountTransfersAPIView
)

urlpatterns = [

    # POST Create New Costumer
    # GET All Customers
    path('customer/', CustomerListCreateAPIView.as_view(), name='list-create-customer'),

    # GET All accounts with filter (open_date,type,customer__id)
    path('account/', AccountListAPIView.as_view(), name='list-account'),

    # GET       Retrieve balances for a given account
    # DELETE    Delete Account
    # PUT       Update Account
    path('account/<int:id>', AccountDetailAPIView.as_view(), name='detail-account'),

    # GET Account transfer transactions
    path('account/<int:id>/transfers', AccountTransfersAPIView.as_view(), name='detail-account-transfer'),

    # POST Create a new bank account for a customer with an initial deposit amount
    path('account/create', AccountCreateAPIView.as_view(), name='create-account'),

    # POST Transfer amounts between any two accounts
    # GET Retrieve transfer history for a given account -> All transfers with filter (account_id,processing_date_start,processing_date_end)
    path('transfer/', TransferAPIView.as_view(), name='transfer'),

    # POST Deposit Money
    path('deposit/', DepositListCreateAPIView.as_view(), name='deposit'),

    # POST Withdraw Money
    path('withdraw/', WithdrawListCreateAPIView.as_view(), name='withdraw'),

]
