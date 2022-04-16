## Functional Requirements

1. The store shall implement a system that would allow a user to log into the site using a username and password, which would allow the users to store account information and perform actions that require an account.
2. The store shall implement an action that would allow a user to log out from their account, which would remove access to the account from the user's end.
3. The store shall implement a system to allow users to create a new account that they can access through log in.
4. The user shall be able to delete their account which would make the account inaccessible to the user.
5. The store shall implement a cart system that stores a list of items that the customer is willing to purchase, their quantities, and the total price; the items in the cart shall be connected to a specific customer account instance and accessible through login. 
6. The customer shall be able to purchase items within their cart by providing their billing and shipping information; upon doing so an order invoice would be created and sent to the merchant for distribution. 
7. The customer shall be able to write a text based review with a numerical rating for a particular product which shall be visible on the product's page and their numerical rating shall be factored into the total rating of the item. (HP)
8. A merchant user shall be able to register a new item to the store's catalog; the merchant shall upload product images, a title, price, and description.
9. The store shall implement a home page for buyer users that will show products that the user could click on.
10. The product pages shall have a section where the uploaded images are visible and browsable. (HP)
11. The store shall have a discount system that will contain discount codes that can be applied per-item, per-category, or sitewide. Merchant users can register new discounts by selecting the products that the code applies to, the discount amount, and an expiration date. 
12. When a buyer user inputs a discount code that is valid, the discount associated shall be applied to the applicable item(s) in their cart. (HP)
13. The site shall implement a search functionality that will query available products. The search shall also support REGEX expressions. Upon recieving user input, the store shall display the search results to the user. (HP)
14. The user shall be able to change the password of their account when logged in; upon doing so, the old password cannot be used to log in while the new password can be used.
15. The store shall contain a product page that contains product images of the specified item, the name of the item, and the price, as well as a button that will allow the customer to add the item to their cart.
16. The store shall be able to display a product catalogue containing all the items in a specified product category.
17. The login system shall have separate classes for account types: merchant and customer. Upon login, merchants will be given access to a separate set of commands to a customer.

## Non-functional Requirements

1. The interface shall implement a dark mode that would change the color of the background to be dark and the text to be light.
2. The user interface shall be styled and organized using the bootstrap library. 
3. The store shall implement a navigation bar at the top of the site that will allow the user to navigate to certain categories of products, search the site, or return to the home page.
4. The store shall implement a horizontal-scrolling product catalogue for the user to browse items.

## Use Cases

1. The store shall implement a cart system that stores a list of items that the customer is willing to purchase, their quantities, and the total price; the items in the cart shall be connected to a specific customer account instance and accessible through login. 
- **Pre-condition:** The user's instance shall be logged into an active customer account.

- **Trigger:** The user clicks on a button labeled 'cart' or accesses the cart url.

- **Primary Sequence:**
  
  1. User accesses the cart website while logged into an active account.
  2. The system retrieves the cart rows that belong to the user.
  3. The system orders the rows in the cart by the earliest date that it was added to the cart.
  4. The system retrieves the name and price of the product in each of the rows.
  5. The system calculates the total price based on the summation of the prices of each of the products multiplied by their quantities.
  6. The system returns a webpage to the user that lists the rows in date order and the total price.

- **Primary Postconditions:** A webpage is displayed to the user with the information in the cart

- **Alternate Sequence:** 
  1. User accesses the cart while not logged into an account on step 1
  2. The site displays an error message and redirects the user to a site to log in or create an account.
2. The customer shall be able to write a text based review with a numerical rating for a particular product which shall be visible on the product's page and their numerical rating shall be factored into the total rating of the item.
- **Pre-condition:** The user's account has not written a review for the specific product. The user has purchased the product.

- **Trigger:** User clicks on an 'add review' button on the product page.

- **Primary Sequence:**
  
  1. User clicks on an 'add review' button on the product page.
  2. The system checks if the user is logged in, if the user has purchased the product, and if the user has not written a review.
  3. The system redirects the user to a webpage with an input for the numerical rating (number of stars), a text field for the body of the review, and a submit button.
  4. The user selects an input for the numerical rating and writes the body of the review.
  5. The user clicks the submit button.
  6. The system saves the user input as a new review.
  7. The system associates the review with the product being reviewed and makes it visible on the product page.
  8. The system redirects the user to the product page.

- **Primary Postconditions:** The user's inputted review is saved to the store and attached to the product.

- **Alternate Sequence:**
  1. User clicks on an 'add review' button on the product page.
  2. The system detects that the user has not purchased the product, has already reviewed the product, or is not logged in.
  3. The system redirects the user back to the product page.
  
3. Use Case Name (Should match functional requirement name)
- **Pre-condition:** <can be a list or short description> Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua.

- **Trigger:** <can be a list or short description> Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. 

- **Primary Sequence:**
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Et sequi incidunt 
  3. Quis aute iure reprehenderit
  4. ... 
  5. ...
  6. ...
  7. ...
  8. ...
  9. ...
  10. <Try to stick to a max of 10 steps>

- **Primary Postconditions:** <can be a list or short description> 

- **Alternate Sequence:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

- **Alternate Sequence <optional>:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

4. Use Case Name (Should match functional requirement name)
- **Pre-condition:** <can be a list or short description> Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua.

- **Trigger:** <can be a list or short description> Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. 

- **Primary Sequence:**
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Et sequi incidunt 
  3. Quis aute iure reprehenderit
  4. ... 
  5. ...
  6. ...
  7. ...
  8. ...
  9. ...
  10. <Try to stick to a max of 10 steps>

- **Primary Postconditions:** <can be a list or short description> 

- **Alternate Sequence:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

- **Alternate Sequence <optional>:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

5. Use Case Name (Should match functional requirement name)
- **Pre-condition:** <can be a list or short description> Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua.

- **Trigger:** <can be a list or short description> Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. 

- **Primary Sequence:**
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Et sequi incidunt 
  3. Quis aute iure reprehenderit
  4. ... 
  5. ...
  6. ...
  7. ...
  8. ...
  9. ...
  10. <Try to stick to a max of 10 steps>

- **Primary Postconditions:** <can be a list or short description> 

- **Alternate Sequence:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

- **Alternate Sequence <optional>:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

6. Use Case Name (Should match functional requirement name)
- **Pre-condition:** <can be a list or short description> Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua.

- **Trigger:** <can be a list or short description> Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. 

- **Primary Sequence:**
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Et sequi incidunt 
  3. Quis aute iure reprehenderit
  4. ... 
  5. ...
  6. ...
  7. ...
  8. ...
  9. ...
  10. <Try to stick to a max of 10 steps>

- **Primary Postconditions:** <can be a list or short description> 

- **Alternate Sequence:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

- **Alternate Sequence <optional>:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

1. Use Case Name (Should match functional requirement name)
- **Pre-condition:** <can be a list or short description> Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua.

- **Trigger:** <can be a list or short description> Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. 

- **Primary Sequence:**
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Et sequi incidunt 
  3. Quis aute iure reprehenderit
  4. ... 
  5. ...
  6. ...
  7. ...
  8. ...
  9. ...
  10. <Try to stick to a max of 10 steps>

- **Primary Postconditions:** <can be a list or short description> 

- **Alternate Sequence:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...

- **Alternate Sequence <optional>:** <you can have more than one alternate sequence to describe multiple issues that may arise>
  
  1. Ut enim ad minim veniam, quis nostrum e
  2. Ut enim ad minim veniam, quis nostrum e
  3. ...