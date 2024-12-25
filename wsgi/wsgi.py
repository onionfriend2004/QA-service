def application(environ, start_response):
    method = environ["REQUEST_METHOD"]

    params = []

    if method == "GET":
        query_string = environ["QUERY_STRING"]
        if query_string:
            params.extend(query_string.split("&"))

    if method == "POST":
        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0

        request_body = environ["wsgi.input"].read(request_body_size)
        if request_body:
            params.extend(request_body.decode("utf-8").split("&"))

    response_body = f"{method}\nParameters:\n" + "\n".join(params)

    status = "200 OK"
    response_headers = [("Content-Type", "text/plain")]
    start_response(status, response_headers)

    return [response_body.encode("utf-8")]
