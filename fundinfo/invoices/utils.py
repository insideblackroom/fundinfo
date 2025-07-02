def get_user_ip(request):
    ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if not ip:
        ip = request.META.get("REMOTE_ADDR")
    return ip