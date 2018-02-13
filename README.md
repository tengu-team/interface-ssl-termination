
# Overview
This interface is used for charms who want to set up a ssl-termination proxy.

# Usage
## Requires
By requiring the `ssl-termination` interface, your charm requests ssl-termination.

This interface layer will set the following states, as appropriate:
- `endpoint.{relation-name}.available` indicates that at least one upstream is connected. This state is automatically removed.
- `endpoint.{relation-name}.update` is set whenever a change happened. This is triggered when a providing charm sends new/updated info or when a relation departs. This state needs to be manually removed.

Use the `send_cert_info(request)` method to create a request. A request has the following format:
```
{
    'fqdn': ['example.com', 'blog.example.com'],
    'contact-email': '',
    'credentials': 'user pass',
    'upstreams': [{
        'hostname': 'x.x.x.x',
        'port': 'XXXX'
    }]
}
```

Use `get_status` to retrieve info about the request. It returns a status report with the following format:
```
{
    'status': {},
    'remote_unit_name': 'ssl-termination-proxy/0'
}
```

## Provides

By providing the `ssl-termination` interface, your charm is providing ssl-termination. 

This interface layer will set the following states, as appropriate:
- `endpoint.{relation-name}.available` indicates that at least one ssl-termination relation is active. This state is automatically removed.
- `endpoint.{relation-name}.update` indicates that a change has occured, either a relation departed or there is a change in ssl-termination requests.

Use `get_cert_requests()` to receive all ssl-termination requests.
Use `send_status(status)` to send a status update about the request.


## Authors

This software was created in the [IDLab research group](https://www.ugent.be/ea/idlab) of [Ghent University](https://www.ugent.be) in Belgium. This software is used in [Tengu](https://tengu.io), a project that aims to make experimenting with data frameworks and tools as easy as possible.

 - Sander Borny <sander.borny@ugent.be>

