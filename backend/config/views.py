"""
Root and utility views for the ChitraBazar API.
"""

from django.conf import settings
from django.http import HttpResponse, JsonResponse


def _frontend_url():
    origins = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
    if origins:
        return origins[0]
    return "http://localhost:5173/"


def _api_index(base):
    return {
        "project": "ChitraBazar API",
        "status": "Backend is running successfully",
        "message": "Use the React app for the painting gallery storefront.",
        "frontend": _frontend_url(),
        "admin": f"{base}/admin/",
        "api": {
            "users": f"{base}/api/users/",
            "products": f"{base}/api/products/",
            "store": f"{base}/api/products/store/",
            "orders": f"{base}/api/orders/",
            "carts": f"{base}/api/carts/",
            "reviews": f"{base}/api/reviews/",
            "analytics": f"{base}/api/analytics/",
            "auth_register": f"{base}/api/users/register/",
            "auth_login": f"{base}/api/users/login/",
        },
    }


def root(request):
    """
    GET / — success page in the browser, API index as JSON otherwise.
    """
    base = request.build_absolute_uri("/").rstrip("/")
    accept = request.headers.get("Accept", "")

    if "text/html" in accept:
        frontend = _frontend_url()
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ChitraBazar API</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: system-ui, -apple-system, sans-serif;
      background: #fafaf9;
      color: #1c1917;
    }}
    .card {{
      text-align: center;
      padding: 2.5rem 2rem;
      background: #fff;
      border: 1px solid #e7e5e4;
      border-radius: 0.75rem;
      box-shadow: 0 1px 3px rgb(0 0 0 / 0.08);
      max-width: 28rem;
    }}
    h1 {{
      margin: 0 0 0.5rem;
      font-size: 1.5rem;
      color: #b45309;
    }}
    p {{ margin: 0 0 1.5rem; color: #57534e; }}
    nav {{ display: flex; flex-wrap: wrap; gap: 0.75rem; justify-content: center; }}
    a {{
      color: #92400e;
      text-decoration: none;
      font-weight: 500;
      padding: 0.5rem 1rem;
      border: 1px solid #fde68a;
      border-radius: 0.5rem;
      background: #fffbeb;
    }}
    a:hover {{ background: #fef3c7; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Backend is running successfully</h1>
    <p>ChitraBazar API is up. Open the painting gallery storefront or admin below.</p>
    <nav>
      <a href="{frontend}">Frontend app</a>
      <a href="{base}/admin/">Admin</a>
    </nav>
  </div>
</body>
</html>"""
        return HttpResponse(html)

    return JsonResponse(_api_index(base))
