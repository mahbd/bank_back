[website]: https://bank-mah.herokuapp.com/

# Complete Banking System

This website is hosted on Heroku. Link to the website: [website]

## Features:

* ### Transaction
    * Consistent transaction(Deposit, Withdrawal, Transfer) history
    * Transaction can not be deleted
    * Transaction amount limit is changeable from admin panel and can be adjusted per user categories(e.g. Verfied
      Email, Verified KYC)
* ### Deposit
    * Deposit money into your account
    * Balance get updated after deposit accepted and reduced if accepted deposit is canceled
* ### Withdraw
    * Withdraw money from your account
    * Balance get updated as soon as withdraw request is made and refunded if pending withdraw canceled
    * Protect against overdrafts
* ### Transfer
    * Transfer money from one account to another
    * Balance get updated after transfer is made and reduced if pending transfer is canceled
    * Protect against overdrafts
    * Protect against self-transfer

# API

## External Bank Data
* Only authorized users can access their external bank data
* Staff can access all external bank data
