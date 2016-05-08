from pubnub import Pubnub


class Munch(object):
    def __init__(self, p_key, s_key):
        '''
        Initialise the Munch service using Pubnub
        publish and subscribe keys
        '''
        self.pubnub = Pubnub(publish_key=p_key, subscribe_key=s_key)
        print self.pubnub.uuid

    def consumes(self, service_identifier):
        '''
        Consumer decorator definition
        '''
        print 'Registering new consumer for ' \
            'messages on channel -> {}'.format(service_identifier)

        # Modified decorator that takes the function as a parameter
        def munch_decorator(func):
            # Subscribe to the channel indicated by service_identifier
            self.pubnub.subscribe(
                channels=service_identifier,
                callback=func
            )
            # Return the function unmodified for normal execution
            return func

        return munch_decorator

    def publish(self, service_identifier, data):
        '''
        Producer function definition
        '''
        print 'Sending information from channel -> ' \
            '{}'.format(service_identifier)
        self.pubnub.publish(service_identifier, data)
