django-uuid-pk
==============


.. image:: https://secure.travis-ci.org/saxix/django-uuid-pk.png?branch=develop
   :target: http://travis-ci.org/saxix/django-django-uuid-pk/


django uuidfield that can be used as primary key

The reason of this project is that any other UUDField implementation that I found
does not reflect the expected behaviour when used as primary-key,
if the save() fails for any reason the value of the field persist so that checking `obj.pk`
cannot be used anymore to check if the object is stored or not.

The code is mainly based on the dcramer's implementation that can be found at
https://github.com/dcramer/django-uuidfield
