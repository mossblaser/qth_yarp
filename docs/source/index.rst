``qth_yarp``: A simple reactive programming library for writing Qth clients
===========================================================================

This library implements a simplified API for writing certain types of Qth_
clients. ``qth_yarp`` uses the yarp_ library to expose a reactive programming
style interface to Qth. Clients written using ``qth_yarp`` can be just a
handful of lines and be entirely free from callbacks. For example, the
following converts a Qth temperature property from degrees Celsius to Kelvin,
storing the result in a new property:

.. _Qth: http://github.com/mossblaser/qth
.. _yarp: http://github.com/mossblaser/yarp

.. code-block:: python

    from qth_yarp import get_property, set_property, run_forever
    
    temperature_celsius = get_property("house/temperature", 19.0)
    temperature_kelvin = temperature_celsius + 273.15
    
    set_property("house/temperature-in-kelvin",
                 temperature_kelvin,
                 register=True,
                 description="Current temperature in kelvin.")
    
    run_forever()

``qth_yarp`` is not intended as a replacement for the lower-level Qth API but
rather to complement it. While it makes certain types of clients easier to
write, particularly 'if-this-then-that'-style or value-transformation focused
clients. It is not suitable for writing clients which maintain complex program
state or which need to dynamically watch, subscribe or create properties and
events. For these more complex applications, the standard Qth API should be
used.

``qth_yarp`` and the low-level Qth API can be used simultaneously within
the same client in cases where only a small proportion of the client's
functionality requires the low-level API. For example:

.. code-block:: python

    import asyncio
    from qth import Client
    from qth_yarp import watch_event, send_event
    from yarp import instantaneous_add
    
    async def main():
        c = Client("mixed-qth-and-qth_yarp-client",
                   "A client using both the qth and qth_yarp libraries.")
        
        # Regular Qth API
        def on_foo(topic, value):
            print("Event {} fired with value {}!".format(topic, value))
        await c.watch_event("example/foo", on_foo)
        
        # Also with qth_yarp (passing in the Qth Client)
        bar = watch_event("example/bar", qth_client=c)
        send_event("example/bar-plus-one",
                   value=instantaneous_add(bar, 1),
                   register=True,
                   description="Incremented version of example/bar.",
                   qth_client=c)
    
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

The ``qth_yarp`` API is documented below:

.. toctree::
   :maxdepth: 2
   
   api
