.. module:: qth_yarp

``qth_yarp`` API
================

Qth to Value Functions
----------------------

The following functions can be used to fetch a :py:class:`yarp.Value`
representing Qth properties or event.

.. autofunction:: get_property

.. autofunction:: watch_event

The next two functions use a :py:class:`yarp.Value` to set or send a Qth
property or event.

.. autofunction:: set_property

.. autofunction:: send_event

In all cases, the Values will not be updated, nor will value changes be sent to
Qth until the :py:mod:`asyncio` mainloop is started. See
:py:func:`run_forever`.

Specifying the Qth Client
-------------------------

The functions defined above accept a ``qth_client`` parameter giving the
:py:class:`qth.Client` object to use. The following function can be used
(before any calls to the ``qth_yarp`` functions) to specify a specific
:py:class:`qth.Client` instance to use.

.. autofunction:: set_default_qth_client

If this function is not called, a Qth :py:class:`qth.Client` will be created
automatically. To fetch the Qth instance used, call:

.. autofunction:: get_default_qth_client


Main-loop utility function
--------------------------

As a convenience for simple scripts, the :py:mod:`asyncio` event loop can be
run forever using the following function.

.. autofunction:: run_forever
