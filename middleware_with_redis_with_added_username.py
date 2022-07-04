import redis
from django.http import JsonResponse

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

redis_instance = redis.StrictRedis(host=REDIS_HOST,
                                  port=REDIS_PORT, db=0)


class SimpleMiddlware:

    def __init__(self,get_response, number_of_failed_attempt_count=0):
        self.get_response = get_response
        self.number_of_failed_attempt_count = number_of_failed_attempt_count

    def __call__(self, request, **kwargs):
        response = self.get_response(request)
        if request.POST.get('username'):
            if redis_instance.exists(request.POST.get('username')):
                self.number_of_failed_attempt_count = int(redis_instance.get(request.POST.get('username')))
                if self.number_of_failed_attempt_count > 3:
                    redis_instance.delete(request.POST.get('username'))
                    self.number_of_failed_attempt_count  = 0
                    return JsonResponse({"message":"To many Attempts"})
        return response
      
    @receiver(user_login_failed)
    def login_failed(sender, credentials, request, **kwargs):
        if redis_instance.exists(credentials['username']):
            val = redis_instance.get(credentials['username'])
            redis_instance.set(credentials['username'], (int(val) + 1))
        else:
            redis_instance.set(credentials['username'], 1)
            
