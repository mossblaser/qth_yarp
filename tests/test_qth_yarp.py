import pytest

from mock import Mock

import asyncio

import qth
from yarp import NoValue, Value

import qth_yarp


@pytest.fixture
def qth_client():
    m = Mock()
    
    async def async_nop(*a, **kw): pass
    
    m.register.side_effect = async_nop
    m.watch_property.side_effect = async_nop
    m.set_property.side_effect = async_nop
    m.watch_event.side_effect = async_nop
    m.send_event.side_effect = async_nop
    
    qth_yarp.set_default_qth_client(m)
    return m

@pytest.mark.asyncio
async def test_get_property(qth_client, event_loop):
    a = qth_yarp.get_property("foo/bar", 123,
                              qth_client=qth_client,
                              loop=event_loop)
    
    # Default value should be provided initially
    assert a.value == 123
    
    # Allow asyncio functions to run...
    await asyncio.sleep(0.1, loop=event_loop)
    
    # But not written to qth
    assert len(qth_client.set_property.mock_calls) == 0
    
    # Watch should be setup
    assert len(qth_client.watch_property.mock_calls) == 1
    assert qth_client.watch_property.mock_calls[0][1][0] == "foo/bar"
    cb = qth_client.watch_property.mock_calls[0][1][1]
    
    # The registered callback should cause the Value to be changed
    cb("foo/bar", 321)
    assert a.value == 321

@pytest.mark.asyncio
async def test_get_property_register(qth_client, event_loop):
    a = qth_yarp.get_property("foo/bar", 123,
                              register=True,
                              description="Something",
                              qth_client=qth_client,
                              loop=event_loop)
    
    # Default value should be provided initially
    assert a.value == 123
    
    # Allow asyncio functions to run...
    await asyncio.sleep(0.1, loop=event_loop)
    
    # And should have made it to Qth
    qth_client.set_property.assert_called_once_with("foo/bar", 123)
    
    # Registration should have been sent
    qth_client.register.assert_called_once_with(
        "foo/bar",
        qth.PROPERTY_MANY_TO_ONE,
        "Something",
        delete_on_unregister=True,
    )
    
    # Watch should be setup
    assert len(qth_client.watch_property.mock_calls) == 1
    assert qth_client.watch_property.mock_calls[0][1][0] == "foo/bar"
    cb = qth_client.watch_property.mock_calls[0][1][1]
    
    # The registered callback should cause the Value to be changed
    cb("foo/bar", 321)
    assert a.value == 321

@pytest.mark.asyncio
async def test_watch_event(qth_client, event_loop):
    a = qth_yarp.watch_event("foo/bar",
                             qth_client=qth_client,
                             loop=event_loop)
    
    on_value_change = Mock()
    a.on_value_changed(on_value_change)
    
    # Should be instantaneous (so no continuous value)
    assert a.value is NoValue
    
    # Allow asyncio functions to run...
    await asyncio.sleep(0.1, loop=event_loop)
    
    # Watch should be setup
    assert len(qth_client.watch_event.mock_calls) == 1
    assert qth_client.watch_event.mock_calls[0][1][0] == "foo/bar"
    cb = qth_client.watch_event.mock_calls[0][1][1]
    
    # The registered callback should cause the Value to be changed
    cb("foo/bar", 321)
    assert a.value is NoValue
    on_value_change.assert_called_once_with(321)

@pytest.mark.asyncio
async def test_watch_event_register(qth_client, event_loop):
    a = qth_yarp.watch_event("foo/bar", register=True, description="Something",
                             qth_client=qth_client,
                             loop=event_loop)
    on_value_change = Mock()
    a.on_value_changed(on_value_change)
    
    # Not a continuous value...
    assert a.value is NoValue
    
    # Allow asyncio functions to run...
    await asyncio.sleep(0.1, loop=event_loop)
    
    # Registration should have been sent
    qth_client.register.assert_called_once_with(
        "foo/bar",
        qth.EVENT_MANY_TO_ONE,
        "Something",
    )
    
    # Watch should be setup
    assert len(qth_client.watch_event.mock_calls) == 1
    assert qth_client.watch_event.mock_calls[0][1][0] == "foo/bar"
    cb = qth_client.watch_event.mock_calls[0][1][1]
    
    # The registered callback should cause the Value to be changed
    cb("foo/bar", 321)
    assert a.value is NoValue
    on_value_change.assert_called_once_with(321)

@pytest.mark.asyncio
async def test_set_property(qth_client, event_loop):
    a = Value(123)
    qth_yarp.set_property("foo/bar", a, qth_client=qth_client, loop=event_loop)
    
    # Allow asyncio functions to run...
    await asyncio.sleep(0.1, loop=event_loop)
    
    # Initial should have been sent to Qth
    qth_client.set_property.assert_called_once_with("foo/bar", 123)
    
    # No registration should be made
    assert len(qth_client.register.mock_calls) == 0
    
    # Setting the qth value should update Qth
    a.value = 321
    await asyncio.sleep(0.1, loop=event_loop)
    qth_client.set_property.assert_called_with("foo/bar", 321)
    
    # And again...
    a.value = 1234
    await asyncio.sleep(0.1, loop=event_loop)
    qth_client.set_property.assert_called_with("foo/bar", 1234)

@pytest.mark.asyncio
async def test_set_property_register(qth_client, event_loop):
    a = Value(123)
    qth_yarp.set_property("foo/bar", a,
                          register=True,
                          description="Something",
                          qth_client=qth_client,
                          loop=event_loop)
    
    # Allow asyncio functions to run...
    await asyncio.sleep(0.1, loop=event_loop)
    
    # Initial should have been sent to Qth
    qth_client.set_property.assert_called_once_with("foo/bar", 123)
    
    # Registration should have been sent
    qth_client.register.assert_called_once_with(
        "foo/bar",
        qth.PROPERTY_ONE_TO_MANY,
        "Something",
        delete_on_unregister=True,
    )
    
    # Setting the qth value should update Qth
    a.value = 321
    await asyncio.sleep(0.1, loop=event_loop)
    qth_client.set_property.assert_called_with("foo/bar", 321)
    
    # And again...
    a.value = 1234
    await asyncio.sleep(0.1, loop=event_loop)
    qth_client.set_property.assert_called_with("foo/bar", 1234)

@pytest.mark.asyncio
async def test_send_event(qth_client, event_loop):
    a = Value()
    qth_yarp.send_event("foo/bar", a, qth_client=qth_client, loop=event_loop)
    
    # Allow asyncio functions to run...
    await asyncio.sleep(0.1, loop=event_loop)
    
    # No initial value should have been sent to Qth
    assert len(qth_client.send_event.mock_calls) == 0
    
    # No registration should be made
    assert len(qth_client.register.mock_calls) == 0
    
    # Setting the qth value should update Qth
    a.set_instantaneous_value(321)
    await asyncio.sleep(0.1, loop=event_loop)
    qth_client.send_event.assert_called_with("foo/bar", 321)
    
    # And again...
    a.set_instantaneous_value(1234)
    await asyncio.sleep(0.1, loop=event_loop)
    qth_client.send_event.assert_called_with("foo/bar", 1234)


@pytest.mark.asyncio
async def test_send_event_register(qth_client, event_loop):
    a = Value()
    qth_yarp.send_event("foo/bar", a,
                        register=True,
                        description="Something",
                        qth_client=qth_client,
                        loop=event_loop)
    
    # Allow asyncio functions to run...
    await asyncio.sleep(0.1, loop=event_loop)
    
    # No initial value should have been sent to Qth
    assert len(qth_client.send_event.mock_calls) == 0
    
    # No registration should be made
    # Registration should have been sent
    qth_client.register.assert_called_once_with(
        "foo/bar",
        qth.EVENT_ONE_TO_MANY,
        "Something",
    )
    
    # Setting the qth value should update Qth
    a.set_instantaneous_value(321)
    await asyncio.sleep(0.1, loop=event_loop)
    qth_client.send_event.assert_called_with("foo/bar", 321)
    
    # And again...
    a.set_instantaneous_value(1234)
    await asyncio.sleep(0.1, loop=event_loop)
    qth_client.send_event.assert_called_with("foo/bar", 1234)
