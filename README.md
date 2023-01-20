# net-worth-calculator
See all your financial account totals from the CLI using Plaid's bank APIs.

### Motivation
Do you have a note keeping track of your financials? Is it taking valuable time out of your day to keep this updated? \
Well look no further, net-worth-calculator is a clean and minimalistic CLI tool to visualize all of your updated \
account totals with the press of a button.

#### Example
![alt-text](https://github.com/coleschon/net-worth-calculator/blob/main/example-screenshot.png?raw=true)

### Steps
1. Create a Plaid account and Development environment at https://plaid.com. A Dev environment is free and \
gives you access to up to 100 banking accounts, which is more than enough for the average Joe.
2. Use your new Dev client_id and secret key with Plaid's Quickstart app, found at https://plaid.com/docs/quickstart/. \
Clone the app and follow along with the video to use Plaid Link (the client-side component) to search for and connect \
to one of your banking accounts. More info at https://plaid.com/docs/link/.
3. When you're done connecting to your bank, you'll get back a public token. Input this token in \
   `public_token_exchange()` to generate a persistent access token for that account. You can then use this access \
   token to start making calls against Plaid's banking APIs (i.e. for this program to function properly).
4. Repeat steps 2 and 3 to retrieve access tokens for all of your desired banking accounts.
5. Populate these tokens in `main.py`, and change all other necessary credentials. See lines marked with `#TODO`.
6. Happy banking :)