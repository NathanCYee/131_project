Welcome to E-Buy's documentation!
=================================
E-Buy is a revolutionary E-Commerce website that connects merchants with customers.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Contents
--------

.. toctree::
   app

Setup and Install
--------

Please make sure python 3 is installed (working on python 3.8).

* Download the library as a zip or by cloning it using ::

    $ git clone https://github.com/NathanCYee/131_project.git

* Navigate to the folder in which the project is stored (e.g. `cd 131_project`)
* Install the prerequisites using::

    $ pip install .

* Setup and create the database by running the create_db.py file using::

    $ python3 create_db.py

* Run the webapp by running::

    $ python3 run.py

* If run on a local machine, site will be accessible at `localhost:5000` or `http://127.0.0.1:5000/` from a browser

If errors occur with jinja, try to manually upgrade flask by using `pip install --upgrade Flask`.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
