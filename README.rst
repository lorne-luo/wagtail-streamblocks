=============================
wagtail_streamblocks
=============================

.. image:: https://badge.fury.io/py/wagtail_streamblocks.svg
    :target: https://badge.fury.io/py/wagtail_streamblocks

.. image:: https://travis-ci.org/lorne.luo/wagtail_streamblocks.svg?branch=master
    :target: https://travis-ci.org/lorne.luo/wagtail_streamblocks

.. image:: https://codecov.io/gh/lorne.luo/wagtail_streamblocks/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/lorne.luo/wagtail_streamblocks

wagtail_streamblocks

Documentation
-------------

The full documentation is at https://wagtail_streamblocks.readthedocs.io.

Quickstart
----------

Install wagtail_streamblocks::

    pip install wagtail_streamblocks

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtail_streamblocks.apps.WagtailStreamblocksConfig',
        ...
    )

Add wagtail_streamblocks's URL patterns:

.. code-block:: python

    from wagtail_streamblocks import urls as wagtail_streamblocks_urls


    urlpatterns = [
        ...
        url(r'^', include(wagtail_streamblocks_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
