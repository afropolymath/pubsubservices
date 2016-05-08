import sys
import os
import signal

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from munch import Munch

'''
Signals

munch.subscription.create  -> Create a new subscription
munch.subscription.delete  -> Deletes an existing subscription
munch.subscription.update  -> Updates an existing subscription
munch.subscription.list    -> Returns a list of all the available subscriptions

munch.appInstanceId.subscriptions.ui     -> Notifies UI about events that have happened in the backend
'''

'''
Notifications

Message Format -> JSON

Sample Incoming Message
{
    appInstanceId: 'XXXXX'
    data: {
        id: ...
        username: ...
    }
}

Sample Notification Message
{
    status: 1,
    message: 'Some context information'
    data: {

    }
}
'''

# Create instance of munch using your publish and subscribe keys
munch = Munch(
    'pub-c-a2ca7a5e-f2c4-4682-93fa-4d95929e2c3f',
    'sub-c-c84d1450-0df9-11e6-bbd9-02ee2ddab7fe'
)


@munch.consumes('munch.subscription.list')
def list_subscriptions(data, channel):
    # List subscriptions
    instance_id = data['appInstanceId']
    uic = 'munch.{}.subscriptions.ui'.format(instance_id)
    munch.publish(uic, {'some': 'data'})
    print "Listing subscriptions"


@munch.consumes('munch.subscription.create')
def create_subscription(data, channel):
    # List subscriptions
    print "Creating subscription with the following data"
    print data
    channel_id = 'munch.{}.subscriptions.ui'.format('SOME_RANDOM_STRING')
    munch.publish(channel_id, data)
