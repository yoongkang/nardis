# Nardis

A web framework based on ASGI. This is inspired by the Express framework for node.js.

# Current status

Still not production-ready.

This API is currently experimental, and is subject to change at any time.

As such, please don't use this for production applications yet.

However, please do play around with it. Any feedback at this stage is welcome as the API becomes more stable.


# Requirements

Python 3.6+

# Installation

## Via pip

Run the following:

```
$ pip install nardis
```

## From source

To build from source, clone this repo, and then:

```
$ python setup.py install
```

# Example

Here's a quick example you can use. Create an `application.py` and copy and paste this:

```python
from nardis.asgi import main
from nardis.routing import Get as get, Post as post
import asyncio


template_start = """
<!doctype html>
<head><title>example</title></head>
<body>
"""

template_end = """
</body>
"""

async def index(req, res):
    """
    This just demonstrates that you can write async code. Don't actually write this in production.
    """
    await res.send(template_start, more=True)
    for x in range(10, 0, -1):
        await res.send(f"<p>{x}!</p>", more=True)
        await asyncio.sleep(1)
    await res.send("<p>liftoff!</p>", more=True)
    await res.send(template_end)


async def hello(req, res):
    """
    Try going to http://127.0.0.1:8000/hello/your_name/

    You'll see "Hello, your_name!"
    """
    name = req.params.get('name', 'world')
    await res.send(f"<h1>Hello, {name}!</h1>")


routes = [
    get(r"^/?$", index),
    get(r"^/hello/(?P<name>\w+)/?$", hello),
]

config = {
    'routes': routes,
}

app = main(config)  # this is the ASGI application

if __name__ == '__main__':
    from uvicorn.run import run
    run(app, '127.0.0.1', 8000)
```

And then:

```
$ python application.py
```

Alternatively, you could also do the following:

```
$ uvicorn application:app
```

This should start a server on http://127.0.0.1:8000


# Using other web servers

Currently, Uvicorn is a dependency of Nardis.

The codebase doesn't actually use Uvicorn, but this dependency allows you to run your application quickly (see above example). This dependency might be removed in the future.

Nardis should also work with other ASGI-based web servers, like Daphne.

To get Daphne working with the example code above, you could do the following:

```
$ daphne application:app
```

