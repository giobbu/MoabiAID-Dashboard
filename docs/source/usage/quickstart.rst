==========
Quickstart
==========

-------
Install
-------
Follow :ref:`install` instructions

--------------------------------------
Activate environment (if using a Venv)
--------------------------------------

If using Anaconda environment instaled with environment.yml:

.. code-block:: bash

    conda activate mobiaid


----------
Migrate DB
----------
Apply migrations with 

.. code-block:: bash

    python manage.py migrate

-------------
Launch server
-------------
Luanch the server with the folowing command

.. code-block:: bash

    python manage.py runserver

If you installed *django-extentions* we recommend using:

.. code-block:: bash

    python manage.py runserver_plus