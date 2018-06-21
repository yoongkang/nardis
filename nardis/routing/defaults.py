from nardis.http import Request, Response


template_404 = """
<!doctype html>
<head>
  <title>URL not found</title>
</head>
<body>
  <h1>URL not found</h1>
</body>
"""

template_500 = """
<!doctype html>
<head>
  <title>Internal Server Error</title>
</head>
<body>
  <h1>Internal Server Error</h1>
</body>
"""


async def default_404(req: Request, res: Response):
    res.status(404)
    await res.send(template_404)


async def default_500(req: Request, res: Response):
    res.status(500)
    await res.send(template_500)
