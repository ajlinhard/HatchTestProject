
class MessageRegistry:
    """
    A registry for chat Message.
    """
    
    _providers = {}

    @classmethod
    def register(cls, provider_name):
        """
        Register a new provider.
        """
        def decorator(subclass):
            cls._providers[provider_name] = subclass
            return subclass
        return decorator

    @classmethod
    def get_provider(cls, provider_name):
        """
        Get a provider by name.
        """
        provider = cls._providers.get(provider_name)
        if provider is None:
            raise ValueError(f"Provider '{provider_name}' not found.")
        return provider

    @classmethod
    def list_providers(cls):
        """
        List all registered providers.
        """
        return list(cls._providers.keys())