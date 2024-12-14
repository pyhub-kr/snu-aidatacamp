from django.http import JsonResponse
from django.shortcuts import render


# refs: https://yalco.notion.site/AJAX-38d8749817244c71a098426827e76915
def ajax(request):
    return render(request, "showcase/ajax.html")


def ajax_data(request, code: str):
    data = DATA[code]
    return JsonResponse(
        data,
        safe=False,
    )


DATA = {
    "restapi": {
        "code": "restapi",
        "name": "REST API",
        "content": "REST (Representational State Transfer) is an architectural style for designing networked applications. It uses standard HTTP methods (GET, POST, PUT, DELETE) to interact with resources identified by URLs. REST is stateless, meaning each request contains all necessary information, enhancing scalability and performance. Data can be returned in various formats like JSON and XML. REST is simple and widely used but may require multiple requests for complex queries, which can be less efficient.",
    },
    "graphql": {
        "code": "graphql",
        "name": "GraphQL",
        "content": "GraphQL is a query language for APIs and a runtime for executing those queries with your existing data. Unlike REST, GraphQL allows clients to request only the data they need, reducing over-fetching or under-fetching of information. It uses a single endpoint for all operations, including queries, mutations, and subscriptions. This makes it highly flexible and efficient, especially for applications with complex data requirements. However, GraphQL requires a well-designed schema and can be more complex to implement compared to REST.",
    },
    "websocket": {
        "code": "websocket",
        "name": "WebSocket",
        "content": "WebSocket is a protocol providing full-duplex communication channels over a single TCP connection, ideal for real-time applications like chat and gaming. Unlike HTTP, WebSocket allows for persistent connections, enabling continuous data exchange without repeated requests. After an initial handshake, the connection stays open, allowing low-latency, bi-directional communication. This reduces overhead and improves performance for high-frequency data updates.",
    },
    "sse": {
        "code": "sse",
        "name": "SSE",
        "content": "SSE (Server-Sent Events) enables servers to push real-time updates to clients over a single, persistent HTTP connection. The client uses the EventSource interface in JavaScript to listen for updates. SSE is ideal for applications like live news feeds and stock updates. It is simple to implement and auto-reconnects if disrupted. However, SSE supports only text-based data and one-way communication, not suitable for bi-directional or binary data. Most modern browsers support SSE, making it a practical choice for many real-time web applications.",
    },
}
