from typing import List, Type, TypeVar, Any

T = TypeVar('T')


class ZscalerCollection:
    "Class to build lists composed of ZscalerObject datatypes"

    @staticmethod
    def form_list(collection: List[Any], data_type: Type[T]) -> List[T]:
        if not collection:
            # If empty list or None
            return []
        for index in range(len(collection)):
            if not ZscalerCollection.is_formed(collection[index], data_type):
                collection[index] = data_type(collection[index])
        return collection

    @staticmethod
    def is_formed(value: Any, data_type: Type[T]) -> bool:
        return isinstance(value, data_type)
