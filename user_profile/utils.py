from django.utils import timezone
from django.conf import settings

def set_jwt_token_cookie(response, token=None):
    """
    Util method to set the token in cookie
    @param response: Response object
    @param token: token to be set in cookie
    @return: None
    """
    if token['refresh']:
        expires_in = timezone.now() + settings.SIMPLE_JWT[
            'REFRESH_TOKEN_LIFETIME']
        response.set_cookie(
            key=settings.AUTH_COOKIE_REFRESH,
            value=token['refresh'],
            expires=expires_in,
            secure=False,
            httponly=False,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            domain=settings.TOKEN_COOKIE_DOMAIN
        )


def add_access_token_validity_cookie(response):
    """
    Method for updating access token expiry cookie
    """
    expires_in = timezone.now() + settings.SIMPLE_JWT[
        'ACCESS_TOKEN_LIFETIME']

    response.set_cookie(
        key='access_token_expiry',
        value=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        expires=expires_in,
        secure=False,
        httponly=False,
        domain=settings.TOKEN_COOKIE_DOMAIN,
    )


def fetch_token_from_header(request):
    """
    Method used to fetch authorization token from request header
    :param request: request object
    :return authorized_token: token fetched from request
    """
    header_token = request.META.get('HTTP_AUTHORIZATION')
    authorized_token = (header_token.split(' ')[1]
                        if header_token.startswith('Bearer ')
                        else header_token)
    return authorized_token
