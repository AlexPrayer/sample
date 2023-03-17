import inspect
from collections import OrderedDict
from typing import Dict, Iterable, List, Tuple, Type


class DirectoryItem(str):

    def __new__(cls, value, *args, **kwargs):
        return super(DirectoryItem, cls).__new__(cls, value)

    def __init__(self, value, description):
        assert value == self
        self._description = description or value
        super(DirectoryItem, self).__init__()

    @property
    def description(self) -> str:
        return self._description


def _attr_filer(key, value):
    if key.startswith("_") or key == "auto":
        return False
    if inspect.isroutine(value) or inspect.isdatadescriptor(value):
        return False
    return True


class DirectoryMeta(type):

    def __new__(mcs, name, bases, attrs):
        items = OrderedDict()
        for key, value in attrs.items():
            if not _attr_filer(key, value):
                continue

            if not isinstance(value, DirectoryItem):
                value = DirectoryItem(key, value)

            attrs[key] = value
            items[value] = value.description

        assert '_items' not in attrs, "'_items' attribute can't be overwritten"
        attrs['_items'] = OrderedDict(items)

        return super(DirectoryMeta, mcs).__new__(mcs, name, bases, attrs)

    def __contains__(cls: Type["Directory"], item: str):
        return item in cls.items()


class Directory(str, metaclass=DirectoryMeta):
    """
    Build set of values with description which can be used as enumeration and choice for django field.

    Usage:
    ```
    class Verification(Directory):
        VERIFIED = "valid contract was found"
        UNVERIFIED = "can't find contract"
        CUSTOM = Directory.custom("my_field")
    ```

    Special value: `Directory.custom` build custom value and set value explicitly

    Operations:
    * get attribute: `Verification.VERIFIED` -> "VERIFIED"
    * get attribute description: `Verification.VERIFIED.description` -> "valid contract was found"
    * get all attributes: `Verification.items()` -> ["VERIFIED", "UNVERIFIED", "my_field"]
    * get all attributes with descriptions: `Verification.dict()`-> dict: key -> descriptions
    """
    _items: Dict[DirectoryItem, str]
    auto: str = None

    def __new__(cls, *args, **kwargs):
        assert 1 <= len(args) <= 2 and not kwargs, "unknown args or kwargs"
        result = super(Directory, cls).__new__(cls, args[0])
        result.description = args[1] if len(args) == 2 else args[0]
        return result

    @classmethod
    def dict(cls) -> Dict[str, str]:
        return cls._items

    @classmethod
    def items(cls) -> List[str]:
        return list(cls.dict().keys())

    @classmethod
    def choices(cls, key_tmpl: str = "{0}", value_tmpl="{0.description}",
                exclude: Iterable[str] = None, include: Iterable[str] = None) -> List[Tuple[str, str]]:
        """
        Build choices for django field. You can customize templates for display value as well as build only subset.

        :param key_tmpl: template for key value
        :param value_tmpl: template for display value
        :param include: include only listed values
        :param exclude: doesn't include listed values
        """
        exclude = list(exclude) if exclude is not None else None
        include = list(include) if include is not None else None
        assert exclude is None or all(i in cls for i in exclude), "exclude contains unknown values"
        assert include is None or all(i in cls for i in include), "include contains unknown values"

        def filter_value(value):
            if include is not None and value not in include:
                return False
            if exclude is not None and value in exclude:
                return False
            return True

        return [(key_tmpl.format(i), value_tmpl.format(i)) for i in cls._items if filter_value(i)]

    @staticmethod
    def custom(value: str, description: str = None) -> str:
        """
        Overwrite default behaviour and set custom field value and description
        """
        return DirectoryItem(value, description)
