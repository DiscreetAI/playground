# # Not using this at the moment, but it was hard to find.
# # Source: https://dammit.nl/20141111-disabling-csrf-checking-in-django-rest-framework-to-enable-replay.html
#
# class DisableCSRF(object):
#     def process_request(self, request):
#             setattr(request, '_dont_enforce_csrf_checks', True)
