"""API 에서 사용할 Inspector."""

from drf_yasg import openapi
from drf_yasg.inspectors import SerializerInspector


class ExampleInspector(SerializerInspector):
    """예제가 제공되면 이를 삽입하는 Inspector."""

    def process_result(self, result, method_name, obj, **kwargs):
        """Meta.examples 를 이용하여 제공."""
        # obj.Meta.examples 에 접근할 수 없다면 예시를 넣을 수 없습니다.
        has_examples = hasattr(obj, "Meta") and hasattr(obj.Meta, "examples")
        if isinstance(result, openapi.Schema.OR_REF) and has_examples:
            schema = openapi.resolve_ref(result, self.components)
            # properties가 정의되지 않은 경우엔 할 수 있는게 없습니다.
            if "properties" in schema:
                properties = schema["properties"]
                for name in properties.keys():
                    # 예시를 정해둔 필드만 손댑니다.
                    if name in obj.Meta.examples:
                        properties[name]["example"] = obj.Meta.examples[name]

        # schema 를 return 하면 안 됩니다.
        # 위에서 schema 를 수정해도 reference 되어서 result 에 반영됩니다.
        return result
