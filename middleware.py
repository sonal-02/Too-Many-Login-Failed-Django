from django.http import JsonResponse
from django.dispatch import receiver
from django.contrib.auth.signals import user_login_failed


class RequestMiddleware:
   
      def __init__(self,get_response, number_of_failed_attempt_count=0):
           self.get_response = get_response
           self.number_of_failed_attempt_count = number_of_failed_attempt_count
            
            
      def __call__(self, request, **kwargs):
            response = self.get_response(request)
            self.number_of_failed_attempt_count = request.session.get('failed_attempt')
            if self.number_of_failed_attempt_count > 3:
                 request.session['failed_attempt'] = 0
                 self.number_of_failed_attempt_count  = 0
                 return JsonResponse({"Warning":"To many Attempts"})  # or you can redirect to some other page
            return response
          
          
      @receiver(user_login_failed)  
      def login_failed(sender, credentials, request, **kwargs):
          if request.session.get('failed_attempt'):
              request.session['failed_attempt'] += request.session.get( 'failed_attempt')
          else:
              request.session['failed_attempt'] = 1
      
