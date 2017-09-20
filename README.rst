YUI
===

.. image:: https://travis-ci.org/item4/item4.net.svg?branch=master
   :target: https://travis-ci.org/item4/item4.net

website of `innocent`_\.

.. _`innocent`: http://item4.net


Requirements
------------

- Git
- Python 3.6 or higher


Installation
------------

.. code-block:: bash

   $ git clone https://github.com/item4/item4.net.git
   $ cd item4.net
   $ pip install -e .



Configuration
-------------

You need ``innocent/settings.py`` which is regular django config.
You can see example file in same path.
If you use example file, you must change some values like secret key.


Database migration
------------------

.. code-block:: bash

   $ python manage.py migrate


Run server
----------

.. code-block:: bash

   $ python manage.py runserver


Test
----

.. code-block:: bash

   $ pip install -e .[tests]
   $ pytest tests
   $ mypy api innocent tests


Contributing
------------

.. code-block:: bash

   $ mkdir -p .git/hooks/
   $ ln -s $(pwd)/hooks/pre-commit .git/hooks


License
-------

AGPLv3 or higher
