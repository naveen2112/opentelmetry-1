import msal

from hubble_report.settings import env


def load_cache(request):
    cache = msal.SerializableTokenCache()
    if request.session.get("token_cache"):
        cache.deserialize(request.session["token_cache"])
    return cache


def save_cache(request, cache):
    if cache.has_state_changed:
        request.session["token_cache"] = cache.serialize()


def get_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        env("CLIENT_ID"),
        authority=env("AUTHORITY_SIGN_ON_SIGN_OUT"),
        client_credential=env("CLIENT_SECRET"),
        token_cache=cache,
    )


def get_sign_in_flow(callback_module):
    return get_msal_app().initiate_auth_code_flow(
        scopes=["user.read"],
        redirect_uri="https://"
        + callback_module
        + env("REDIRECT_PATH"),
    )


def get_token_from_code(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)
    flow = request.session.pop("auth_flow", {})
    result = auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
    save_cache(request, cache)
    return result


def get_token(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)
    accounts = auth_app.get_accounts()
    if accounts:
        result = auth_app.acquire_token_silent(
            scopes=["user.read"], account=accounts[0]
        )
        save_cache(request, cache)
        return result["access_token"]


def remove_user_and_token(request):
    if "token_cache" in request.session:
        del request.session["token_cache"]

    if "user" in request.session:
        del request.session["user"]
