def get_client_ip(request):
    """
    Retrieves the public IP address of the user, 
    even if the app is behind a proxy (like Nginx or ngrok).
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # The first IP in the list is the original client
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Fallback to the standard remote address
        ip = request.META.get('REMOTE_ADDR')
    return ip