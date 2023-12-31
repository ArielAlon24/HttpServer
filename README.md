# HttpServer

A simple HTTP server library for Python.

## Usage
### Defining Routes
To use the HTTP server library, follow these steps:

1. Import the necessary modules:

```python
from http_server import Server
from http_server.enums import ContentType
from http_server.utils import FileUtils
```
2. Create an instance of the HttpServer class:

```python
app = Server()
```

3. Define routes using the `@app.route` decorator and specify the content type for each route:

```python
@app.route(path="/favicon.ico", content_type=ContentType.IMAGE)
def favicon() -> bytes:
    return file.read(path="resources/favicon.ico")
```
Alternatively, you can add routes with the `app.add_route`:

```python
def favicon() -> bytes:
    return file.read(path="resources/favicon.ico")

app.add_route(
    function=favicon,
    path="/favicon.ico",
    content_type=ContentType.IMAGE,
)
```

or in case the resource if a file use the `app.add_file_route` (which is best suited for our example):
```python
app.add_file_route(
    file_path="resources/favicon.ico",
    content_type=ContentType.IMAGE,
    path="/favicon.ico",
)
```

4. Start the HTTP server using the `app.run()` method:

```python
if __name__ == "__main__":
    app.run()
```

### Injecting Payload and Headers
You can inject the payload or the headers (or both) into the handler function by modifying the function's signature to accept additional parameters. For example:

```python
@app.route(path="/", content_type=ContentType.HTML)
def index(payload: str, headers: Dict[str, str]) -> bytes:
    return file.template(
        path="resources/index.html", payload=payload, headers=repr(headers)
    )
```

The `index` function will receive on runtime both the request's payload and headers.

### Using Templates with [variable] Markup
As we saw in the previous example, you can use templates with placeholders like `[variable]` by creating an HTML template file with placeholders. They will be replaced with key-word arguments passed in the `file.template` function.

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

### Accessing Request Parameters
To access parameters sent in the request, simply define function arguments with the same names as the parameters in the URL. For example:

```python
@app.route(path="/add", content_type=ContentType.HTML)
def add(a: str, b: str) -> str:
    result = int(a) + int(b)
    return f"<h1> Result = {result} </h1>"
```
This function will accept URLs of the type: `www.example.com/add?a=<a>&b=<b>`. 
- **Note** that the parameters passed in must be strings.

### Adding Specific Error Pages

To add a unique error page, based on the returned error status code, use the `error` decorator or `add_error_route` function. For example:
```python
@app.error(status=status_code.NOT_FOUND)
def not_found() -> str:
    return "<h1> Oops not found... </h1>"
```

This `not_found` function will occur only when the server encountered a `status_code.NOT_FOUND` error. In a case where the `not_found` funtion fails, the server will search for an `status_code.INTERNAL_SERVER_ERROR` resource, if it fails, it will return a defualt error handling resource.

## License
This HttpServer library is open-source and available under the MIT License.
