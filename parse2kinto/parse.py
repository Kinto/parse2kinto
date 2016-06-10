import requests
from kinto_http import utils
from six import iteritems


class ParseException(Exception):
    pass


class Endpoints(object):
    endpoints = {
        'root':    '{root}/',
        'objects': '{root}/classes/{class_name}',
        'object':  '{root}/classes/{class_name}/{id}',
    }

    def __init__(self, root=''):
        self._root = root

    def get(self, endpoint, **kwargs):
        # Remove nullable values from the kwargs, and slugify the values.
        kwargs = dict((k, utils.slugify(v))
                      for k, v in iteritems(kwargs) if v)

        try:
            pattern = self.endpoints[endpoint]
            return pattern.format(root=self._root, **kwargs)
        except KeyError as e:
            msg = "Cannot get {endpoint} endpoint, {field} is missing"
            raise ParseException(msg.format(endpoint=endpoint,
                                            field=','.join(e.args)))


class ParseClient(object):

    def __init__(self, server, app_id, rest_key, class_name=None):
        self._server = server.rstrip('/').rstrip('/1')
        self._app_id = app_id
        self._rest_key = rest_key
        self._class_name = class_name
        self.endpoints = Endpoints('%s/1' % self._server)

        self.session = requests.Session()
        self.session.headers.update({
            "X-Parse-Application-Id": self._app_id,
            "X-Parse-REST-API-Key": self._rest_key,
            "Content-Type": "application/json",
        })

    def get_endpoint(self, name, class_name=None, id=None):
        """Return the endpoint with named parameters.

           Please always use the method as if it was defined like this:

               get_endpoint(self, name, *,
                            class_name=None, id=None)

           Meaning that class_name and id should always be named
           parameters.

        """
        kwargs = {
            'class_name': class_name or self._class_name,
            'id': id
        }
        return self.endpoints.get(name, **kwargs)

    def get_records(self, class_name=None):
        resp = self.session.get(self.get_endpoint('objects',
                                                  class_name=class_name))
        resp.raise_for_status()
        return resp.json()['results']


def create_client_from_args(args):
    return ParseClient(server=args.parse_server,
                       app_id=args.parse_app,
                       rest_key=args.parse_rest_key,
                       class_name=args.parse_class)
