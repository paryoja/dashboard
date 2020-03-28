import abc
import json
import typing

from django.conf import settings

VERSION = getattr(settings, "VERSION", "0.0.1")
NAV_ITEM_JSON = getattr(settings, "NAV_ITEM_JSON", None)
if NAV_ITEM_JSON:
    nav_config = json.load(open(NAV_ITEM_JSON, encoding="utf-8"))
else:
    nav_config = None


class NavBase:
    """
    Navigation 항목의 base 가 되는 class
    """

    description: str
    icon: str

    __metaclass__ = abc.ABCMeta

    def __init__(
        self,
        description: str,
        icon: str,
        has_child: bool,
        should_superuser: bool = False,
    ):
        self.description = description
        self.icon = icon
        self.has_child = has_child
        self.should_superuser = should_superuser

    @abc.abstractmethod
    def is_active(self, current_page: str):
        pass

    @abc.abstractmethod
    def get_active_set(self):
        pass


class NavCollection(NavBase):
    """
    Child 를 가지는 Navigation
    """

    collection: str
    child: typing.List[NavBase]
    active_set: typing.Set[str]

    def __init__(
        self,
        description: str,
        icon: str,
        collection: str,
        child_info: dict,
        should_superuser=False,
    ):
        super().__init__(
            description=description,
            icon=icon,
            has_child=True,
            should_superuser=should_superuser,
        )

        self.collection = collection
        self.child = []
        self.active_set = set()

        self._set_child(child_info)

    def get_active_set(self) -> typing.Set[str]:
        if not self.active_set:
            for child in self.child:
                self.active_set.update(child.get_active_set())
        return self.active_set

    def _set_child(self, child_info: dict):
        for child in child_info:
            self.child.append(NavigationFactory.get_navigation_item(child))

    def is_active(self, current_page):
        return current_page in self.get_active_set()


class NavItem(NavBase):
    """
    말단 Navigation 노드
    """

    template: str
    suffix: typing.Optional[str]

    def __init__(
        self,
        description: str,
        icon: str,
        template: str,
        argument: typing.Dict[str, str] = None,
        external: bool = False,
        should_superuser: bool = False,
        login_state: str = "always",
        active_override: str = None,
    ):
        super().__init__(
            description=description,
            icon=icon,
            has_child=False,
            should_superuser=should_superuser,
        )

        if external:
            self.template = template
            self.active = {""}
        else:
            self.template = f"book:{template}"
            if active_override:
                self.active = {active_override}
            else:
                self.active = {template}

        if argument:
            self.suffix = "?" + "&".join([f"{k}={v}" for k, v in argument.items()])
        else:
            self.suffix = None
        self.argument = argument
        self.external = external
        self.login_state = login_state

    def is_active(self, current_page: str):
        return self.template == current_page

    def get_active_set(self) -> typing.Set[str]:
        return self.active


class NavigationFactory:
    """
    주어진 dictionary 를 적절한 Navigation 노드로 변환한다.
    """

    @staticmethod
    def get_navigation_item(info: dict) -> NavBase:
        if "collection" in info:
            return NavCollection(**info)
        else:
            return NavItem(**info)


class Sidebar:
    """
    Navigation 의 모든 정보를 가진 클래스
    """

    def __init__(self, config: typing.List[dict]):
        self.items = []
        for block_config in config:
            for k, v in block_config.items():
                nav_items = []
                for nav_item in v:
                    nav_items.append(NavigationFactory.get_navigation_item(nav_item))
                self.items.append((k, nav_items))


sidebar = Sidebar(nav_config)


def get_render_dict(current_page: str) -> dict:
    render_dict = {"current_page": current_page}
    return render_dict
