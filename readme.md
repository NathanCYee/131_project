# E-Buy

[![CircleCI](https://circleci.com/gh/NathanCYee/131_project/tree/master.svg?style=svg)](https://circleci.com/gh/NathanCYee/131_project/tree/master)
[![codecov](https://codecov.io/gh/NathanCYee/131_project/branch/master/graph/badge.svg?token=G6YR4ZSL9J)](https://codecov.io/gh/NathanCYee/131_project)
[![Last Commit](https://img.shields.io/github/last-commit/NathanCYee/131_project)](https://github.com/NathanCYee/131_project/commits/)
![Built by SJSU Students](https://badgen.net/badge/Built%20by/SJSU%20Students/yellow)
[![Trello](https://img.shields.io/badge/Trello-%23026AA7.svg?style=flat&logo=Trello&logoColor=white)
](https://trello.com/b/1UQLG3ci/team-13)

A store page that allows merchants to post products and customers to purchase them.

## Features

- Login and register account functionality accessible through `/login` and `/register`
- Account information, delete account, and password change form accessible through `/account_info`
- Merchant portal accessible through `/merchant`
    - Merchant login/register accessible through `/merchant/login` and `/merchant/register`
    - Create a new product accessible through `/merchant/new_product`
- Product pages with the url `/product/<id>`
    - Add to cart functionality on product pages
- Product catalogs with the url `/catalog/<id>`
- Cart located at `/cart` for logged in users

## Setup and Install

- Download the library as a zip or by cloning it using `git clone https://github.com/NathanCYee/131_project.git`
- Navigate to the folder in which the project is stored
- Install the prerequisites using `pip install .`
- Setup and create the database by running the create_db.py file using ``python3 create_db.py``
- Run the webapp by running `python3 run.py`

## Team Members

- Sarah Singh-LEAD (@SarahS16)
- Selim Ishakbeyoglu (@SelimIshakb)
- Nicholas (@StickOnAStick)
- Nathan Yee (@NathanCYee)

---
![Your Repository's Stats](https://contrib.rocks/image?repo=NathanCYee/131_project)

## Libraries Used

- [Bootstrap](https://getbootstrap.com/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [ForEvolve/bootstrap-dark](https://github.com/ForEvolve/bootstrap-dark)