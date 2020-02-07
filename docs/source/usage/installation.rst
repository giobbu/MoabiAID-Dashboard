.. _install:

============
Installation
============

Two options are provided to install the project. First, the classical way by installing required libraries and setting up the database manually. 
This might be a lengthy and difficult process as it requires setting up a PostGIS database (see GeoDjango requirement). The second option is to use Docker.
We recommend this option as the setup in this case is automated and the real-time processing pipeline is contained in a Docker container anyway.

Common to both Projects is the first step.

-------------
Clone project
-------------

Regardless of the chosen install approach, the first step consists of cloning the project's git repository locally.

.. code-block:: bash

    git clone https://github.com/Ardillen66/MOBI-AID.git


--------------
Native Install
--------------

Requirements
============

* Python 3 (Recommended through Anaconda)
* PostgreSQL (>= 11) 
* `Django <https://docs.djangoproject.com/en/2.2/topics/install/#installing-official-release>`_ (2.2 or higher) and `GeoDjango <https://docs.djangoproject.com/en/2.2/ref/contrib/gis/install/>`_ (With PostGIS 2.5)
* Additional Python packages:

    * psycopg2 (For PostgreSQL support in Python, already used by Django)
    * `django-polymorphic <https://django-polymorphic.readthedocs.io/en/stable/quickstart.html>`_
    * *Optional:* `django-extensions <https://django-extensions.readthedocs.io/en/latest/>`_ (Remove *django_extensions* entry from INSTALLED_APPS in *settings.py* if not used)
    * See *requirements.yml* for further requiremens

Recommended: Create conda Environment Automatically
===================================================

Build a conda environment from *environment.yml*. This will install several packages, some of which are not used directly, but can prove useful in development.

.. code-block:: bash

    conda env create -f environment.yml

Import the database
===================

Load the database in PostGIS.

.. code-block:: bash

    sudo su postgres
    psql mobiaid < mobidb.sql

.. todo::
 
    Test this and verify user and database names (might be different for installer)

--------------
Docker Install
--------------

Requirements
============

* `Docker <https://www.docker.com/get-started>`_ (Recommended to take the tutorial if you are unfamiliar with it)
* `Docker Compose <https://docs.docker.com/compose/>`_

Build Docker container
======================

* Get the DockerFile and build the Image for the streaming pipeline (Ask the devs for this, Note: The image should be called *streaming*)
* Update the folowwing volumes fields in *docker-compose* file:

    * mobiaid container: Set the */streaming_files* volume to a directory on the host machine and the */map_data* volume to a directory with *shp* 
      files for communes and streets. The */map_data* volume can also be removed if the database already contains all data on streets and communes.
    * streaming container: Set the */home/guest/host* volume to a parent diredctory of the directory that was used for *streaming_files*.

Import the database
===================

.. todo::

    Either automate database setup or document how to load the database in the Docker image


