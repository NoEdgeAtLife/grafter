try:
    from .version import VERSION as __version__  # noqa: F401
except ImportError:
    from version import VERSION as __version__  # noqa: F401

__package__ = "grafter"
__path__ = __import__("pkgutil").extend_path(__path__, __name__)
