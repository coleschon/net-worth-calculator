import plaid
from plaid.api import plaid_api
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

import locale
from plumbum import colors


locale.setlocale( locale.LC_ALL, '' )

# Plaid credentials from your account
client_id = 'REDACTED' #TODO
secret = 'REDACTED' #TODO
PLAID_ENV = 'development'
PLAID_PRODUCTS = 'auth', 'transactions'
PLAID_COUNTRY_CODES = 'US', 'CA'
PLAID_REDIRECT_URI = None

# institution IDs, retrieved via Plaid quickstart
# these can be retrieved programatically using APIS defined here https://plaid.com/docs/api/institutions/#introduction
td_ameritrade_ID = 'ins_119423'
american_express_ID = 'ins_10'
chase_ID = 'ins_3'
institution_IDs = {td_ameritrade_ID, american_express_ID, chase_ID}

# institution tokens, retrieved via public_token_exchange()
td_public_token = "REDACTED" #TODO
td_access_token = "REDACTED" #TODO
amex_public_token = 'REDACTED' #TODO
amex_access_token = 'REDACTED' #TODO
chase_public_token = 'REDACTED' #TODO
chase_access_token = 'REDACTED' #TODO

# assign globals
configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'PLAID-CLIENT-ID': client_id,
        'PLAID-SECRET': secret
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# institution endpoint
def get_by_id(id):
    request = InstitutionsGetByIdRequest(
        institution_id=id,
        country_codes=[CountryCode('US')],
        client_id=client_id,
        secret=secret
    )
    response = client.institutions_get_by_id(request)
    print(response)

# your account access tokens for institutions
def public_token_exchange(public_token):
    request = ItemPublicTokenExchangeRequest(
        public_token=public_token,
        client_id=client_id,
        secret=secret
    )
    response = client.item_public_token_exchange(request)
    print(response) # contains access_token, item_id, and request_id

def accounts_balance_get(access_token):
    request = AccountsBalanceGetRequest(
        access_token=access_token,
        client_id=client_id,
        secret=secret
    )
    response = client.accounts_balance_get(request)
    accounts = response['accounts']
#     print(response) # shows names of accounts to reference in cur_bal()
    return accounts

# helper functions
def cur_bal(accounts, name):
    for account in accounts:
        if (account['name'] == name):
            return round(account['balances']['current'], 2)

def ava_bal(accounts, name):
    for account in accounts:
        if (account['name'] == name):
            return round(account['balances']['available'], 2)

def all_ava_bal(accounts):
    total = 0
    for account in accounts:
        total += round(account['balances']['available'], 2)
    return total

# string formatting to align periods
def period(amt):
    i = len(amt)
    while (i < 10):
        print(".", end='')
        i += 1

def usd(bal):
    return str(locale.currency(bal, grouping=True))


def printout():
    # colors
    assets_color = Colors.SpringGreen3A
    liabilities_color = Colors.IndianRed1

    # institution accounts
    td_account = accounts_balance_get(td_access_token)
    chase_account = accounts_balance_get(chase_access_token)
    amex_account = accounts_balance_get(amex_access_token)

    # retrieve balances
    rsu_balance = cur_bal(td_account, 'Example RSU Account name') #TODO
    retirement_balance = cur_bal(td_account, 'Example 401(K) Account name') #TODO
    brokerage_balance = cur_bal(td_account, 'Example Brokerage Account name') #TODO
    savings_balance = cur_bal(chase_account, 'Example RSU Account name') #TODO
    checking_balance = cur_bal(chase_account, 'Example RSU Account name') #TODO
    amex_balance = cur_bal(amex_account, 'Example AMEX Account name') #TODO
    chase_visa_balance = cur_bal(amex_account, 'Example Chase Account name') #TODO
    assets = rsu_balance, retirement_balance, brokerage_balance, savings_balance, checking_balance
    liabilities = amex_balance + chase_visa_balance

    # print
    print()

    print(colors.bold | "ASSETS")
    print("  RSUs................", end='')
    period(usd(rsu_balance)
    print(assets_color | usd(rsu_bal))
    print("  401(k)..............", end='')
    period(usd(retirement_balance)
    print(assets_color | usd(retirement_balance))
    print("  Brokerage...........", end='')
    period(usd(brokerage_balance)
    print(assets_color | usd(brokerage_balance))
    print("  Savings.............", end='')
    period(usd(savings_balance)
    print(assets_color | usd(savings_balance))
    print("  Checking............", end='')
    period(usd(checking_balance)
    print(assets_color | usd(checking_balance))
    print()

    print(colors.bold | "LIABILITIES")
    print("  American Express...", end='')
    period(usd(amex_balance)
    print(liabilities_color | + '(' + usd(amex_balance) + ')')
    print("  Chase Visa.........", end='')
    period(usd(chase_visa_balance)
    print(liabilities_color | + '(' + usd(chase_visa_balance) + ')')
    print()

    print(colors.bold | "TOTAL", end='')
    print(".................", end='')
    period(usd(assets - liabilities))
    print(assets_color | usd(assets - liabilities))
    print()

def main():
    printout()
    # public_token_exchange(td_public_token)
    # print(accounts_balance_get(td_access_token))
    # accounts_balance_get(td_public_token)

if __name__ == '__main__':
    main()
