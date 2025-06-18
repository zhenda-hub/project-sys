class AdminRegisterMiddleware:
    # useless middleware
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.path == '/admin/register/':
            return self.get_response(request)
        return self.get_response(request)