parse2kinto
===========

parse2kinto is a little utility that let you migrate your Parse APP
objects into Kinto records.


Glossary
--------

Parse is talking about ``classes`` where kinto is talking about ``collections``

Let's say you have a ``Game`` app with a ``score`` class on Parse, you
will endup with a ``Game`` bucket and a ``score`` collection.

All the object you have created in the ``score`` class will became
``records`` of the ``score`` collection in Kinto.


Install
-------

.. code-block:: bash

    pip install parse2kinto


Usage
-----

.. code-block:: bash

    parse2kinto --parse-server https://api.parse.com --parse-app app_id --parse-class score --parse-rest-key REST_key \
	            --server http://localhost:8888/v1 --bucket Game --collection score

It will take a bit of time because of parse requests number limitation
but you will eventually get back all of your records :)
