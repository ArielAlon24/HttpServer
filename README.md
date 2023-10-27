# HTTP Server Library

A simple HTTP server library for Python, designed to make it easy to create web applications and serve HTTP requests. This library allows you to define routes and handlers for different HTTP endpoints, making it a useful tool for building RESTful APIs, serving web pages, or handling various HTTP requests.

## Table of Contents

- [Usage](#usage)
  - [Defining Routes](#defining-routes)
  - [Injecting Parameters and Headers](#injecting-parameters-and-headers)
  - [Using Templates with `[variable]` Markup](#using-templates-with-variable-markup)
  - [Accessing Parameters as Arguments](#accessing-parameters-as-arguments)
- [License](#license)

## Usage
### Defining Routes
To use the HTTP server library, follow these steps:

Import the necessary modules:

```python
from http_server import HttpServer
from enums.content_types import ContentType
from utils import file
```
Create an instance of the HttpServer class:

```python
app = HttpServer()
```

Define routes using the @app.route decorator and specify the content type for each route:

```python
@app.route(path="/favicon.ico", content_type=ContentType.IMAGE)
def favicon() -> bytes:
    # Define the response logic for this route
    return file.read(path="resources/favicon.ico")
```

Start the HTTP server using the `app.run()` method:

```python
if __name__ == "__main__":
    app.run()
```

### Injecting Payload and Headers
You can inject the payload or the headers (or both) into the handler function by modifying the function's signature to accept additional parameters. For example:

```python
@app.route(path="/", content_type=ContentType.HTML)
def index(payload: str, headers: Dict[str, str]) -> bytes:
    # Use payload and headers in your response logic
    response_content = f"Payload: {payload}<br>Headers: {headers}"
    return file.template(
        path="resources/index.html", payload=response_content
    )
```

The `index` function will receive on runtime both the request's payload and headers.

### Using Templates with [variable] Markup
As we saw in the previous example, you can use templates with placeholders like `[variable]` by creating an HTML template file with placeholders. They will be replaced with actual key-word arguments passed in the `file.template`.

```html
<!DOCTYPE html>
<html>
<head>
    <title>HTTP Server Template</title>
</head>
<body>
    <h1>Welcome to my HTTP Server</h1>
    <p>Payload: [payload]</p>
    <p>Headers: [headers]</p>
</body>
</html>
```
### Accessing Request's Parameters
To access parameters sent in the request, simply define function arguments with the same names as the parameters in the URL. For example:

```python
@app.route(path="/add", content_type=ContentType.HTML)
def add(a: str, b: str) -> str:
    result = int(a) + int(b)
    return f"<h1> Result = {result} </h1>"
```
This function will accept URL of the type: `www.example.com/add?a=<a>&b=<b>`. Note that the parameters passed in must be strings.

## License
This HTTP server library is open-source and available under the MIT License.