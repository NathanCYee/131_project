## Functional Requirements

1. The store shall implement a system that would allow a user to log into the site using a username and password, which would allow the users to store account information and perform actions that require an account.
2. The store shall implement an action that would allow a user to log out from their account, which would remove access to the account from the user's end.
3. The store shall implement a system to allow users to create a new account that they can access through log in.
4. The user shall be able to delete their account which would make the account inaccessible to the user.
5. The store shall implement a cart system that stores a list of items that the customer is willing to purchase, their quantities, and the total price; the items in the cart shall be connected to a specific customer account instance and accessible through login. 
6. The customer shall be able to purchase items within their cart by providing their billing and shipping information; upon doing so an order invoice would be created and sent to the merchant for distribution. 
7. Merchant users shall be able to view their orders, and change their fulfillment status.
8. The customer shall be able to write a review for a product and include a numerical rating which shall be visible on the product's page; that numerical rating shall be factored into the total rating of the item.
9. A merchant user shall be able to register a new item to the store's catalog; the merchant shall upload product images, a title, price, and description.
10. The store shall implement a home page for buyer users that will show products that the user could click on.
11. The product pages shall have a section where the uploaded images are visible and browsable. (HP)
12. The store shall have a discount system that will contain discount codes that can be applied by the customer per-item, per-category, or sitewide. (HP)
13. Merchant users shall be able to register new discount codes that contain information about their expiration, discount amount, and applicable products. 
14. When a buyer user inputs a discount code that is valid, the discount associated shall be applied to the applicable item(s) in their cart. (HP)
15. The site shall implement a search functionality that will query available products. The search shall also support REGEX expressions. Upon receiving user input, the store shall display the search results to the user. (HP)
16. The user shall be able to change the password of their account when logged in; upon doing so, the old password cannot be used to log in while the new password can be used.
17. The store shall contain a product page that contains product images of the specified item, the name of the item, and the price, as well as a button that will allow the customer to add the item to their cart.
18. The store shall be able to display a product catalogue containing all the items in a specified product category.
19. The login system shall have separate classes for account types: merchant and customer. Upon login, merchants will be given access to a separate set of commands to a customer.

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
  
3. When a buyer user inputs a discount code that is valid, the discount associated shall be applied to the applicable item(s) in their cart.
- **Pre-condition:** The user is logged into an account and has applicable items in their cart.

- **Trigger:** User loads the cart website

- **Primary Sequence:**
  
  1. User inputs a discount code into the discount code field in the cart website.
  2. User clicks submit.
  3. The system retrieves the discount amount and applicable products that correspond to the discount code.
  4. The system checks the current date against the expiration date of the discount code and validates that the current date is before the expiration date.
  5. The system loops through the user's cart items and applies the discount to the applicable items.
  6. The system sums the total discount and subtracts it from the user's cart value.
  7. The system returns a cart website with the updated prices to the user.

- **Primary Postconditions:** A discount is applied to the user's cart. The prices of the items are adjusted for the user according to the discount amount.

- **Alternate Sequence:** 
  
  1. The user inputs an invalid discount code on step 1
  2. User clicks submit
  3. The system fails to retrieve a discount code
  4. The system returns a cart website to the user with an error message "ERROR: Code not valid"

- **Alternate Sequence:** 
  
  1. The user inputs a discount code that is out of date on step 1
  2. User clicks submit
  3. The system retrieves the discount amount and applicable products that correspond to the discount code.
  4. The system checks the current date against the expiration date of the discount code and finds that the date is past.
  5. The system returns a cart website to the user with an error message "ERROR: Code is expired"

4. The store shall be able to display a product catalogue containing all the items in a specified product category.
- **Pre-condition:** A category with the correct name exists and products are classified in that category

- **Trigger:** User clicks on the category's label in the navigation bar or accesses the url of the category

- **Primary Sequence:**
  
  1. User hovers over the category label in the navigation bar and selects a product category
  2. The system receive the user request for a product category and fetches all products belonging to the category
  3. System renders a website containing product pictures and links to each of the products in the category
  4. System returns the rendered website to the user
  5. User is able to use the product catalog to navigate to a desired product

- **Primary Postconditions:** User receive an up-to-date list of all the items within a specific category

- **Alternate Sequence:** 
  
  1. User accesses the URL of an invalid product catalog in step 1
  2. System returns an error

5. Merchant users shall be able to register new discount codes that contain information about their expiration, discount amount, and applicable products. 
- **Pre-condition:** Specific discount code name has not already been used, user is logged in as a merchant

- **Trigger:** Merchant user clicks on an 'create new promotion' button

- **Primary Sequence:**
  
  1. Merchant user clicks on an 'create new promotion' button
  2. System redirects the user to a page with fields to input the code name, select applicable products, the discount amount, and expiration date.
  3. Merchant enters their desired code name, selects the products that apply to the promotion, inputs a discount amount, and inputs an expiration date.
  4. Merchant clicks submit
  5. System checks if the code name has been used before
  6. System adds the discount to be able to be used by customers
  7. System displays a success message to the merchant user

- **Primary Postconditions:** A new discount is created that is usable by customers.

- **Alternate Sequence:** 
  
  1. System detects that the desired code name is already in use by another discount on step 5
  2. System redirects the merchant to a site containing an error message and an option to resubmit the discount with a different code
  3. Merchant inputs a different code
  4. Merchant clicks submit
  5. Primary sequence resumes on step 5

6. Merchant users shall be able to view their orders, and change their fulfillment status.
- **Pre-condition:** Merchant has products that have been purchased by a customer

- **Trigger:** Merchant clicks on a "view unfulfilled orders" button on their home page

- **Primary Sequence:**
  
  1. System retrieves all orders attached to the specific merchant that have the status 'unfulfilled'
  2. System returns a website to the merchant that lists the orders, the product in the order, the quantity of products, and the shipping address as well as a button to 'Complete order'
  3. Merchant user clicks 'Complete order' for a specific order
  4. System updates the status of the order to complete and refreshes the site, returning the same site without the completed order

- **Primary Postconditions:** Order status is changed to fulfilled and can be viewed by the customer