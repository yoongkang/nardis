# Nardis

A web framework based on ASGI. This is inspired by the Express framework for node.js.

# Current status

This API is *extremely* experimental, and is subject to change at any time.

I do not recommend using it for production purposes, but I would love to get feedback.


# Requirements

Written with Python 3.7, no guarantee it will work on earlier versions (although I think 3.6 would work fine).

# Installation

Clone this repo, and then:

```
$ python setup.py install
```

# Example

Here's a quick example you can use. Create an `application.py` and copy and paste this:

```python
from nardis.asgi import main
from nardis.routing import Get, Post
import asyncio


template_start = """
<!doctype html>
<head><title>example</title></head>
<body>
  <h1>He's down!</h1>
"""

template_end = """
</body>
"""

async def index(req, res):
    await res.send(template_start, more=True)
    for x in range(10, 0, -1):
        await res.send(f"<p>{x}!</p>", more=True)
        await asyncio.sleep(1)
    await res.send("<p>It's over. TKO!</p>", more=True)
    await res.send(template_end)


routes = [
    Get("/", index),
]

app = main(routes)  # this is the ASGI application

if __name__ == '__main__':
    from uvicorn.run import run
    run(app, '127.0.0.1', 8000)
```

And then:

```
$ python application.py
```

This should start a server on http://127.0.0.1


# Using other web servers

Uvicorn is currently a dependency of Nargis for local development.

Nargis should also work with other ASGI-based web servers, like Daphne.

To get Daphne working with the example code above, you could do the following:

```
$ daphne application:app
```
