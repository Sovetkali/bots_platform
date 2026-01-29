class BotContainer:
    def __init__(self):
        self._services = {}
        self._configs = {}

    def register_bot(self, name, config):
        self._configs[name] = config

    def get_bot(self, name):
        config = self._configs[name]

        if name not in self._services:
            service = config['service_class'](**config.get('dependencies', {}))
            router = config['router_class'](service)
            client = config['client_class'](router.router)
            self._services[name] = client

        return self._services[name]

container = BotContainer()
