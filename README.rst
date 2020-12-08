=============================
wagtail_streamblocks
=============================
streamblocks for wagtail

http://tequila.butterfly.com.au/Django-packages/wagtail-streamblocks

Installation
------------

Install wagtail_streamblocks::

    pip install git+ssh://git@tequila.butterfly.com.au/Django-packages/wagtail-streamblocks.git#0.1.0

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtail_streamblocks',
        'wagtailmedia',
        'wagtail.contrib.table_block',
        ...
    )

How to Use
----------

Create stream content page

.. code-block:: python

    from wagtail_streamblocks.models import BaseStreamContentPage

    class StreamContentPage(BaseStreamContentPage):
        pass


Use stream block in template

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        {% include 'wagtail_streamblocks/stream_content_body.html' with content=page.content %}
    {% endblock %}


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l
