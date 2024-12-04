import logging
from django.utils.timezone import now

logger = logging.getLogger('django')

class RequestLogMiddleware:
    """
    Atılan isteğin IP adresi, endpoint bilgisi ve dönen yanıtı loglar.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # İstekten önceki işlemler
        ip = self.get_client_ip(request)
        method = request.method
        path = request.get_full_path()
        body = request.body.decode('utf-8') if request.body else "Boş İstek"

        # Loglama: İstek detayları
        logger.info(f"[{now()}] IP: {ip} METHOD: {method} PATH: {path} BODY: {body}")

        # Yanıt oluştur
        response = self.get_response(request)

        # Loglama: Yanıt detayları
        logger.info(f"[{now()}] IP: {ip} RESPONSE: {response.status_code} DATA: {response.content.decode('utf-8')}")

        return response

    def get_client_ip(self, request):
        """
        Kullanıcının IP adresini alır.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip