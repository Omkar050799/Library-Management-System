from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import AnonRateThrottle

class AnonymousUserAPIThrottle(AnonRateThrottle):
    scope = 'high'
    rate = '20/minute'

class LoginAPIThrottle(UserRateThrottle):
    scope = 'high'
    rate = '10/minute'

class LightRateLimit(UserRateThrottle):
    scope = 'high'
    rate = '60/minute'

class MediumRateLimit(UserRateThrottle):
    scope = 'high'
    rate = '30/minute'

class HeavyRatLimit(UserRateThrottle):
    scope = 'high'
    rate = '15/minute'