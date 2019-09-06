.. _install:

============
Installation
============

--------------------------------------
Create conda environment automatically
--------------------------------------
Build a conda environment from *environment.yml*. This will install several packages, some of which are not used directly, but can prove useful in development.

.. note:: This method is currently untested and may not work. Manually install requirements listed below in this case

------------
Requirements
------------
* Python (3.6 or higher)
* `Django <https://docs.djangoproject.com/en/2.2/topics/install/#installing-official-release>`_ (2.2 or higher)
* `GeoDjango <https://docs.djangoproject.com/en/2.2/ref/contrib/gis/install/>`_ (With PostGIS)
* `django-polymorphic <https://django-polymorphic.readthedocs.io/en/stable/quickstart.html>`_
* *Optional:* `django-extensions <https://django-extensions.readthedocs.io/en/latest/>`_ (Remove *django_extensions* entry from INSTALLED_APPS in *settings.py* if not used)

-------------
Clone project
-------------

.. code-block:: bash

    git clone https://github.com/Ardillen66/MOBI-AID.git


