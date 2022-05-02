## Meetings

### 2022-04-12 at 15:00
- Attendees: Nicholas, Nathan, Sarah
- Team Brainstorm (<=1hr)
  All three attendees collaborated to form a general blueprint of the project. We discussed what functional and non-functional requirements we wanted to implement. We also tried to determine which requirements (functional and non-functional) could be deemed as HP. Further discussion on Discord to organize a meeting time that worked for all four members.
  - <Nathan> Add name/username to readme file. Flesh out requirements file and add required packages.
  - <Nicholas> Add name/username to readme file. Implement custom css and bootstrap. Add main block content.
  - <Sarah> Add name/username to readme file. Update meetings file.
  - <Selim> Add name/username to readme file.

  - No pair-programming to report
  - Group was able to come to a consensus on the overall layout and functionality of the website. Ensured that we had enough functional and non-functional requirements to satisfy Milestone 1. Determined a day which all four members could meet. No prior updates available since this was the first meeting.

  ### 2022-04-22 at 12:00
- Attendees: Nicholas, Nathan, Sarah, Selim
- Touch Base and Project Updates (20min>)
  All four teammates gave updates on what they've accomplished in the past week. A couple members had midterms and could not get much done which is understandable. No one had any questions. We discussed methods for testing and decided to implement "Travis CI". We also were planning on fleshing out our Readme file further to include documentation for our website. We plan on including a brief description of how the Python elements work with the backend. We plan on including a Docstring for the functions to explain what each function does as well.
  - <Nathan> Working on implementing a login/logout system . Will allow the user to input a username and password which will give them access to their account. Planning to implement a register user system. If the user does not have an account already, a user can make a username and password which will make them an account. Implemented Travis CI testing and code coverage for the entire project. 
  - <Nicholas> Working on the index and base templates for html. Fixed issue when index template was returning the base html file. Working on implementing a functioning navbar. Users will be able to navigate the entire site. Working on designing and implementing a functioning homepage. 
  - <Sarah> Working on implementing a cart system. Initially working on adding item to cart function. When a user is logged in and adds an item to their cart, a row will be added to the CartItem table which records the user, the product, and the quantity. Planning to work on further cart functionalities (eg. purchase cart, discount application, register/add discounts)
  - <Selim> Working on implementing features where the vendor can update the status on their products as well as add new products to their "page". Planning on including a page where the users can leave reviews on certain products. Planning on implementing a search function which will allow whoever accesses the site to navigate quicker.

  - No pair-programming to report
  - Group was able to give small updates on their progress for each person's respective tasks. We came to an agreement on testing for each task we plan on implementing as well. Each member specified what they planned on completing in the following week.

  ### 2022-04-29 at 12:00
- Attendees: Nicholas, Nathan, Sarah, Selim
- Project Updates, Testing, GitHub Etiquette (30min>)
  All four teammates gave updates on what they've accomplished in the past week. We discussed how writing the tests for each route and model should work, and how to go about pytest when we submit our pull requests on GitHub. We also went over GitHub etiquette. We agreed that we should often pull from origin master to have the latest changes as well as commit often to our remote branches so changes will not have to be made all at once.
  - <Nathan> Finished implementing login/logout system that will allow the user to input a username and password which will give them access to their account. Also finished implementing a register user system that allows a new user to create an account. Finished implementing a delete account system that allows a user to get rid of their account. Also implemented a search system using REGEX for users to search a specific item. Also implemented a secondary account system for merchants to log in and sell/list new items. Included tests to ensure that the login/logout/register/delete account functionalities are working correctly. Has completed all of his requirements for the project. 
  - <Nicholas> Implemented a functioning homepage.html. Currently working on the product.html which will list all items for sale on the website. Working on implementing category + subcategory display as well as adding pop-overs for functions such as the add_cart. This will display the message "item added to cart" when user adds an item. Working on integrating the backend functionality with the frontend.  
  - <Sarah> Implemented cart system. Customers can add products to cart for purchase. The cart will display the image, name, and price of the product. It will calculate price based off of the products initial price multiplied by the quantitiy. Working on checkout/place order system. This will calculate the total price of the cart by adding up all the product prices. This system will also take in the users address to "ship" said order as well as the users billing information so the user can pay for their items.
  - <Selim> Implemented features where the users can leave a review of the product on the product's page. There will be a numerical value and description associated with each review. A total numerical value will be assigned to each product based off of the reviews for that one product. the average of all the numerical values from the product's reviews will be added to the product's page.

  - No pair-programming to report
  - Group was able to give small updates on their progress for each person's respective tasks. We discussed how testing should be done and agreed upon the GitHub etiquette for the project moving forward. 