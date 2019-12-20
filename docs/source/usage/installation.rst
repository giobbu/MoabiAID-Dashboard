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

.. code-block:: bash

    git clone https://github.com/Ardillen66/MOBI-AID.git


-------------
Local Install
-------------

Requirements
============

* Python (3.6 or higher. Recommended through Anaconda)
* `Django <https://docs.djangoproject.com/en/2.2/topics/install/#installing-official-release>`_ (2.2 or higher)
* `GeoDjango <https://docs.djangoproject.com/en/2.2/ref/contrib/gis/install/>`_ (With PostGIS)
* `django-polymorphic <https://django-polymorphic.readthedocs.io/en/stable/quickstart.html>`_
* *Optional:* `django-extensions <https://django-extensions.readthedocs.io/en/latest/>`_ (Remove *django_extensions* entry from INSTALLED_APPS in *settings.py* if not used)
* See *requirements.yml* for further requiremens

Recommended: Create conda Environment Automatically
===================================================

Build a conda environment from *environment.yml*. This will install several packages, some of which are not used directly, but can prove useful in development.

.. code-block:: bash

    conda env create -f environment.yml

--------------
Docker Install
--------------

Requirements
============

* `Docker <https://www.docker.com/get-started>`_ (Recommended to take the tutorial if you are unfamiliar with it)
* `Docker Compose <https://docs.docker.com/compose/>`_

Setup
=====

* Get the DockerFile and build the Image for the streaming pipeline (Ask the devs for this, Note: The image should be called *streaming*)
* Update the folowwing volumes fields in *docker-compose* file:
    * mobiaid container: Set the */streaming_files* volume to a directory on the host machine and the */map_data* volume to a directory with *shp* 
    files for communes and streets. The */map_data* volume can also be removed if the database already contains all data on streets and communes.
    * streaming container: Set the */home/guest/host* volume to a parent diredctory of the directory that was used for *streaming_files*.
* Run :command:`docker-compose up` from the root of the directory 
* Import the database (TODO)


