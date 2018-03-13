`qth_yarp`: Reactive-ish bindings for Qth
=========================================

[![Build Status](https://travis-ci.org/mossblaser/qth_yarp.svg?branch=master)](https://travis-ci.org/mossblaser/qth_yarp)

[Documentation](http://qth-yarp.readthedocs.io/en/latest/)

An alternative API for writing [Qth](http://github.com/mossblaser/qth) clients
based on the [`yarp`](http://github.com/mossblaser/yarp) library for
reactive(-ish) programming in Python. This library is not intended as a
replacement for the standard Qth API but rather a complementrary option. In
exchange for some flexibility, the `qth_yarp` API makes writing certain types
of Qth client far simpler to write.

For example, here's a simple `qth_yarp` application which converts a
temperature Qth property from degrees celsius into a new Qth property whose
value is in kelvin.

    from qth_yarp import get_property, set_property, run_forever
    
    temperature_celsius = get_property("house/temperature", 19.0)
    temperature_kelvin = temperature_celsius + 273.15
    
    set_property("house/temperature-in-kelvin",
                 temperature_kelvin,
                 register=True,
                 description="Current temperature in kelvin.")
    
    run_forever()

In this example `temperature_celsius` is a `yarp.Value` representing the
current value of the Qth property `house/temperature`. Adding 273.15 converts
the temperature from degrees celsius to kelvin yielding a new `yarp.Value`.
This is finally assigned to a newly registered Qth property
`house/temperature-in-kelvin`. Whenever the `house/temperature` property
changes, `yqrp` automatically reevaluates everything and the
`house/temperature-in-kelvin` property is changed accordingly.

`qth_yarp` can also be used alongside the regular Qth API, for example:

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

