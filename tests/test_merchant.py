import datetime

from sqlalchemy.orm import sessionmaker

from app.models import User, UserRole, Product, Category, Order, OrderRow, Discount


def test_merchant_denial(client):
    with client:
        response = client.get('/merchant')
        assert response.status_code == 302  # successfully reached the test


def test_merchant_register(db, client):
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        # check to see if the user is in the database

        response = client.get('/merchant/account_test')
        assert response.status_code == 200  # successfully reached the test

        response = client.get('/merchant')
        assert response.status_code == 200  # successfully reached the test

        users = User.query.filter(User.roles.any(id=2)).filter_by(username=username)
        assert users.count() == 1  # should only have 1 matching user

        # check props of user to make sure they are inserted correctly
        user = users.first()
        assert user.username == username
        assert user.email == email
        assert user.check_password(password)

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_bad_register(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    improper_email = "testmail"
    new_username = "Test2"

    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        client.get('/logout')  # call the logout

        # test for improperly formatted email (not verified)
        response = client.post('/merchant/register',
                               data={'username': new_username, 'email': improper_email, 'password': password,
                                     'submit': True})
        assert response.status_code == 200  # 200, did not redirect

        # test for an already existing account
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 200  # 200, did not redirect
        assert b"Username is already taken" in response.data

        # test for an already existing email
        response = client.post('/register',
                               data={'username': new_username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 200  # 200, did not redirect
        assert b"Email has already been used" in response.data

        # check to see if the user is in the database
        users = User.query.filter_by()
        assert users.count() == 1  # should only have 1 matching user

        # check props of user to make sure they are inserted correctly
        user = users.first()
        assert user.username == username
        assert user.email == email
        assert user.check_password(password)

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_good_login(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        client.get('/logout')  # call the logout

        response = client.post('/merchant/login',
                               data={'username': username, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        response = client.get('/merchant/account_test')
        assert response.status_code == 200  # successfully reached the test

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_bad_login(db, client):
    # test params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    wrong_password = "pass-1"
    wrong_username = "test1"

    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        client.get('/logout')  # call the logout

        # test bad password
        response = client.post('/merchant/login',
                               data={'username': username, 'password': wrong_password, 'submit': True})
        assert response.status_code == 200  # 200 response ok, did not redirect
        # test bad username
        response = client.post('/merchant/login',
                               data={'username': wrong_username, 'password': password, 'submit': True})
        assert response.status_code == 200  # 200 response ok, did not redirect
    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_prevent_merchant(db, client):
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"
    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page
        # check to see if the user is in the database

        response = client.get('/merchant/account_test')
        assert response.status_code == 200  # successfully reached the test

        response = client.get('/')
        assert response.status_code == 302  # redirected from home

    # clean up any changes
    User.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_add_product(db, client):
    # test account params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # test product params
    name = "iPhone"
    price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."
    category = Category.query.filter_by(name="Electronics").first()
    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        user = User.query.filter_by(username=username).first()

        response = client.post('/merchant/new_product',
                               data={'merchant_id': user.id, 'name': name, 'price': price, 'description': description,
                                     'category': category.name, 'pictures': [], 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to product page

        products = Product.query.filter_by(name=name)
        assert products.count() == 1

    # clean up any changes
    User.query.delete()
    Product.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_product_page(db, client):
    # test account params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # test product params
    name = "iPhone"
    price = 999.99
    description = "The brand new iPhone. Lorem ipsum sit amet."
    category = Category.query.filter_by(name="Electronics").first()
    with client:
        response = client.post('/merchant/register',
                               data={'username': username, 'email': email, 'password': password, 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to home page

        user = User.query.filter_by(username=username).first()

        response = client.post('/merchant/new_product',
                               data={'merchant_id': user.id, 'name': name, 'price': price, 'description': description,
                                     'category': category.name, 'pictures': [], 'submit': True})
        assert response.status_code == 302  # 302 successful redirect to product page

        products = Product.query.filter_by(name=name)
        assert products.count() == 1
        response = client.post('/')
        product = products.first()
        response = client.get(f'/product/{product.id}', follow_redirects=True)
        assert bytes(product.name, 'utf-8') in response.data
        assert bytes(product.description, 'utf-8') in response.data
    # clean up any changes
    User.query.delete()
    Product.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_merchant_fill_orders(db, client):
    # test merchant account params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    # test customer params
    cust_username = "customer_test"
    cust_email = "test2@mail.com"
    cust_password = "Pass-1"
    cust_address = "123 Sesame Street."

    Session = sessionmaker(db.engine)
    with Session() as session:
        # create the customer
        customer = User(username=cust_username, email=cust_email)
        customer.set_password(cust_password)
        session.add(customer)

        # test product params
        name = "iPhone"
        price = 999.99
        description = "The brand new iPhone. Lorem ipsum sit amet."
        category = Category.query.filter_by(name="Electronics").first()
        with client:
            response = client.post('/merchant/register',
                                   data={'username': username, 'email': email, 'password': password, 'submit': True})
            print(response.data)
            assert response.status_code == 302  # 302 successful redirect to home page

            user = User.query.filter_by(username=username).first()

            # test params
            name = "iPhone 1000"
            product_price = 999.99
            description = "The brand new iPhone. Lorem ipsum sit amet."

            # create the product
            product = Product(merchant_id=user.id, name=name, price=product_price, description=description,
                              category_id=category.id)
            session.add(product)
            session.commit()

            test_order = Order(user_id=customer.id, ship_address=cust_address)
            session.add(test_order)
            session.commit()
            test_row = OrderRow(id=test_order.id, product_id=product.id, quantity=1, product_price=product.price)
            session.add(test_row)
            session.commit()

            # check if the merchant can see their orders
            response = client.get('/merchant/orders')
            assert response.status_code == 200  # 302 successful redirect to product page
            # check to see if info from the order is in the page
            assert bytes(product.name, 'utf-8') in response.data
            assert bytes(str(test_row.quantity), 'utf-8') in response.data
            assert bytes(f'{test_row.product_price:.2f}', 'utf-8') in response.data
            assert bytes(test_order.ship_address, 'utf-8') in response.data
            assert bytes(customer.username, 'utf-8') in response.data

            # merchant fills their order
            response = client.post('/merchant/orders',
                                   data={'merchant_id': user.id, 'order_id': test_row.id, 'submit': True})
            assert response.status_code == 302  # redirect back to the homepage
            # check to see if info from the order removed from the page
            response = client.get('/merchant/orders')
            assert bytes(product.name, 'utf-8') not in response.data
            find_row = OrderRow.query.filter_by(id=test_row.id).first()
            assert find_row.filled

            # check to see if the order is seen as filled by the merchant
            response = client.get('/merchant/orders/filled')
            assert bytes(product.name, 'utf-8') in response.data

    # clean up any changes
    User.query.delete()
    Product.query.delete()
    Order.query.delete()
    OrderRow.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_merchant_discount(db, client):
    # test merchant account params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    promo_name = "CODE10"
    discount = 10

    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # test product params
        name = "iPhone"
        product_price = 999.99
        description = "The brand new iPhone. Lorem ipsum sit amet."
        category = Category.query.filter_by(name="Electronics").first()
        with client:
            response = client.post('/merchant/register',
                                   data={'username': username, 'email': email, 'password': password, 'submit': True})
            print(response.data)
            assert response.status_code == 302  # 302 successful redirect to home page

            user = User.query.filter_by(username=username).first()

            # create the product
            product = Product(merchant_id=user.id, name=name, price=product_price, description=description,
                              category_id=category.id)
            session.add(product)
            session.commit()

            applicable_products = [product.id]

            # post a response to the new promo site
            response = client.post('/merchant/promo',
                                   data={'code': promo_name, 'amount': discount, 'products': applicable_products,
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)
            assert b"Successfully created discount" in response.data

            discounts = Discount.query.filter_by(code=promo_name)
            assert discounts.count() == 1
            discount = discounts.all()[0]
            assert discount.code == promo_name
            assert discount.is_valid()

    User.query.delete()
    Product.query.delete()
    Discount.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()


def test_merchant_percentage_discount(db, client):
    # test merchant account params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    promo_name = "CODE10"
    discount = 10

    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # test product params
        name = "iPhone"
        product_price = 999.99
        description = "The brand new iPhone. Lorem ipsum sit amet."
        category = Category.query.filter_by(name="Electronics").first()
        with client:
            response = client.post('/merchant/register',
                                   data={'username': username, 'email': email, 'password': password, 'submit': True})
            print(response.data)
            assert response.status_code == 302  # 302 successful redirect to home page

            user = User.query.filter_by(username=username).first()

            # create the product
            product = Product(merchant_id=user.id, name=name, price=product_price, description=description,
                              category_id=category.id)
            session.add(product)
            session.commit()

            applicable_products = [product.id]

            # post a response to the new promo site
            response = client.post('/merchant/promo/percentage',
                                   data={'code': promo_name, 'amount': discount, 'products': applicable_products,
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)
            assert b"Successfully created discount" in response.data

            discounts = Discount.query.filter_by(code=promo_name)
            assert discounts.count() == 1
            discount = discounts.all()[0]
            assert discount.code == promo_name
            assert discount.is_valid()

    User.query.delete()
    Product.query.delete()
    Discount.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()

def test_bad_merchant_discount(db, client):
    # test merchant account params
    username = "Test1"
    email = "test@mail.com"
    password = "Pass-1"

    promo_name = "CODE10"
    promo_name2 = "CODE5"
    discount = 10
    big_discount = 10000

    expiration_date = datetime.date.today() + datetime.timedelta(days=10)

    Session = sessionmaker(db.engine)
    with Session() as session:
        # test product params
        name = "iPhone"
        product_price = 999.99
        description = "The brand new iPhone. Lorem ipsum sit amet."
        category = Category.query.filter_by(name="Electronics").first()
        with client:
            response = client.post('/merchant/register',
                                   data={'username': username, 'email': email, 'password': password, 'submit': True})
            print(response.data)
            assert response.status_code == 302  # 302 successful redirect to home page

            user = User.query.filter_by(username=username).first()

            # create the product
            product = Product(merchant_id=user.id, name=name, price=product_price, description=description,
                              category_id=category.id)
            session.add(product)
            session.commit()

            applicable_products = [product.id]

            # post a good promo
            response = client.post('/merchant/promo',
                                   data={'code': promo_name, 'amount': discount, 'products': applicable_products,
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)
            assert b"Successfully created discount" in response.data

            discounts = Discount.query.filter_by(code=promo_name)
            assert discounts.count() == 1
            discount = discounts.all()[0]
            assert discount.code == promo_name
            assert discount.is_valid()

            # post a promo with the same code
            response = client.post('/merchant/promo',
                                   data={'code': promo_name, 'amount': discount, 'products': applicable_products,
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)
            assert b"Code has already been used" in response.data

            discounts = Discount.query.filter_by(code=promo_name)
            assert discounts.count() == 1

            # post a promo with a large value
            response = client.post('/merchant/promo',
                                   data={'code': promo_name2, 'amount': big_discount, 'products': applicable_products,
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)
            assert b"Discount amount is greater than the price" in response.data

            discounts = Discount.query.filter_by(code=promo_name2)
            assert discounts.count() == 0

            # post a promo with a large percentage value
            response = client.post('/merchant/promo/percentage',
                                   data={'code': promo_name2, 'amount': big_discount, 'products': applicable_products,
                                         'expiration_date': expiration_date, 'submit': True}, follow_redirects=True)
            assert b"Invalid percentage" in response.data

            discounts = Discount.query.filter_by(code=promo_name2)
            assert discounts.count() == 0

    User.query.delete()
    Product.query.delete()
    Discount.query.delete()
    db.session.query(UserRole).delete()
    db.session.commit()
    db.session.flush()
