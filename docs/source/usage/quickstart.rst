==========
Quickstart
==========

---------------------
Recommended learning
---------------------

If you are unfamiliar with any of the following technologies, we recommend following the beginner tutorials and checking out 
the documentation before proceeding.

Reccommended tutorials:

* `Django <https://docs.djangoproject.com/en/2.2/#first-steps>`_ and `GeoDjango <https://docs.djangoproject.com/en/2.2/ref/contrib/gis/tutorial/>`_
  (With PostgreSQL and PostGIS for the database)
* `PostgreSQL <https://www.postgresql.org/about/>`_ (11 recommended) and `PostGIS <http://postgis.net/>`_ (2.5 recommended) 
* `Docker <https://docs.docker.com/get-started/>`_ 
* MobilityDB (probably for later)

-------
Install
-------
Follow :ref:`install` instructions. Depending on chosen install instructions follow one of the following SetUp guides.

------
Set Up
------

^^^^^^^^^^^^^^
Native install
^^^^^^^^^^^^^^

""""""""""""""""""""""""""""""""""""""
Activate environment (if using a Venv)
""""""""""""""""""""""""""""""""""""""

If using Anaconda environment instaled with environment.yml:

.. code-block:: bash

    conda activate mobiaid

""""""""""
Migrate DB
""""""""""

Apply migrations with 

.. code-block:: bash

    python manage.py migrate

"""""""""""""
Launch server
"""""""""""""

Launch the server with the folowing command

.. code-block:: bash

    python manage.py runserver

If you installed *django-extentions* we recommend using:

.. code-block:: bash

    python manage.py runserver_plus

^^^^^^^^^^^^^^
Docker install
^^^^^^^^^^^^^^

""""""""""""""""""""""""""""
Launch the Docker containers
""""""""""""""""""""""""""""

After following the installation instructions at :ref:`docker-install`, assuming that you now have a docker container called *streaming*.

From the project root, start containers with 

.. code-block:: bash

    docker-compose up

This will build the containers for the Django web server, the PostGIS database server and the backup database server.

"""""""""""""""""""
Import the database
"""""""""""""""""""

.. todo::

    Either automate database setup or document how to load the database in the Docker image

""""""""""""""""""""""""""""""""
Launch the streaming application
""""""""""""""""""""""""""""""""

Find the id of the container for the *streaming* image. The ID is the first field when running

.. code-block:: bash

    docker container ls

To start the streaming pipeline, attatch a bash shell to the streaming image.

.. code-block:: bash

    docker exec -it <CONTAINER ID> /bin/sh -c "[ -e /bin/bash ] && /bin/bash || /bin/sh"

.. todo::
 
    When code for the pipeline is done, port it to regular python files. Optionally automate startup of the streaming pipeline with docker-compose