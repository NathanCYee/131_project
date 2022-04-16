## <remove all of the example text and notes in < > such as this one>

## Functional Requirements

1. The store shall implement a system that would allow a user to log into the site using a username and password. The store shall offer the option to register as either a merchant or a buyer. Upon doing so, actions such as adding to cart or purchasing would become tied to the account and account information such as shipping address would become visible to the user. Actions specific to the type of user, such as managing inventory, shall be visible only to that of the type of user.
2. The store shall implement an action that would allow a user to log out from the site. Upon doing so, the user's actions would no longer be tied to an account nor will the user be able to access portions of the site that require an account. 
3. The store shall implement a system to be able to register a new user to the site. Upon registration, the user would be able to log in, log out, and perform account actions such as managing user information or adding purchases that are tied to the user's account.
4. The user shall be able to delete their account should they choose to. Upon doing so, the account would no longer be accessible to the user through login.
5. The store shall implement a cart system that stores a list of items that the user is willing to purchase, their quantities, and the total price. The user shall be able to add new items to the cart and remove items listed in the cart before checking out. The user shall be able to check out all items in the cart within one transaction.
6. The user shall be able to purchase items within their cart and individually. The checkout system would allow the user to input their billing information as well as the delivery address in order to receive the item. 
7. The user shall be able to write a text based review with a numerical rating for a particular item. Upon doing so, their review shall be visible on the product's page and their numerical rating shall be factored into the total rating of the item. (HP)
8. A merchant user shall be able to register a new item to the store. The merchant user shall be able to upload product images and input a title, price, and description. Upon completion, the product page containing such information and user reviews shall be present on the site and accessible through links or search.
9. The store shall implement a home page for buyer users that will show products that the user could click on.
10. The product pages shall have a section where the uploaded images are visible and browsable. (HP)
11. The store shall have a discount system that will contain discount codes that can be applied per-item, per-category, or sitewide. Merchant users can register new discounts by selecting the products that the code applies to, the discount amount, and an expiration date. When a buyer user inputs a code, the stored discount would be applied to the item(s) in their cart. (HP)
12. The site shall implement a search functionality that will query available products. The search shall also support REGEX expressions. Upon recieving user input, the store shall display the search results to the user. (HP)

## Non-functional Requirements

1. The interface shall implement a dark mode that would change the color of the background to be dark and the text to be light.
2. The user interface shall be styled and organized using the bootstrap library. 
3. The store shall implement a navigation bar at the top of the site that will allow the user to navigate to certain categories of products, search the site, or return to the home page.
4. The store shall implement a horizontal-scrolling product catalogue for the user to browse items.

## Use Cases

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
2. Use Case Name (Should match functional requirement name)
   ...
