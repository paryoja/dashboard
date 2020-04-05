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

    :param description: Navigation bar 에 나타날 string
    :type description: str
    :param icon: Navigation bar 에 나타날 icon
    :type icon: str
    :param has_child: Nav Element 의 하위 항목 존재 여부
    :type has_child: str
    :param should_superuser: Superuser 에게만 보이게 설정
    :type should_superuser: bool
    """

    description: str
    icon: str
    has_child: bool
    should_superuser: bool

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
    def is_active(self, current_page: str) -> bool:
        """
        :param current_page: 현재 page 이름
        :return: 현재 page 에 관련 있으면 True, 없으면 False
        """
        pass

    @abc.abstractmethod
    def get_active_set(self) -> typing.Set[str]:
        pass


class NavCollection(NavBase):
    """
    Child 를 가지는 Navigation

    :param collection: Collapse 를 동작 시킬 때 collection 을 구별할 변수
    :type collection: str
    :param child: child element
    :type child: List[NavBase]
    :param active_set: active 로 표시될 current page 의 set
    :type active_set: typing.Set[str]
    """

    collection: str
    child: typing.List[NavBase]
    active_set: typing.Set[str]

    def __init__(self, collection: str, child_info: dict, **kwargs):
        super().__init__(has_child=True, **kwargs)

        self.collection = collection
        self.child = []
        self.active_set = set()

        self._set_child(child_info)

    def get_active_set(self) -> typing.Set[str]:
        if not self.active_set:
            for child in self.child:
                self.active_set.update(child.get_active_set())
        return self.active_set

    def _set_child(self, child_info: dict) -> None:
        for child in child_info:
            self.child.append(NavigationFactory.get_navigation_item(child))

    def is_active(self, current_page) -> bool:
        return current_page in self.get_active_set()


class NavItem(NavBase):
    """
    말단 Navigation 노드

    :param template: Link 눌렀을 때 이동할 link
    :type template: str
    :param suffix: Get Argument 로 적을 내용
    :type suffix: typing.Optional[str]
    """

    template: str
    suffix: typing.Optional[str]

    def __init__(
        self,
        template: str,
        argument: typing.Dict[str, str] = None,
        external: bool = False,
        login_state: str = "always",
        active_override: str = None,
        **kwargs,
    ):
        """
        :param template: template 명 혹은 url 링크
        :param argument: template 에 argument 를 전달하기 위함
        :param external: 외부 링크 여부, 내부인 경우 "book" namespace 사용
        :param login_state: Login 에 따라 보여줄 지 말지 선택 옵션은 "always", "login", "logout"
        :param active_override: active 를 기본적으로는 template 과 같은지를 보지만,
                                argument 에 따라서 선택 할 수 있도록 override
        """
        super().__init__(has_child=False, **kwargs)

        if external:
            self.template = template
            # external link 의 경우 active 한 state 가 없음
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
        """

        :param info: navigation item 을 구성할 정보
        :return: collection element 를 이용하여 Collection 인지, 말단 node 인지 구분
        """
        if "collection" in info:
            return NavCollection(**info)
        else:
            return NavItem(**info)


class Sidebar:
    """
    Navigation 의 모든 정보를 가진 클래스

    :param items: Navigation 정보를 가진 List, 각 항목당 horizontal line 으로 구분 됨
    :type  items: typing.List[typing.Tuple]
    """

    items: typing.List[typing.Tuple]

    def __init__(self, config: typing.List[dict]):
        """
        :param config: Navigation 설정
        """
        self.items = []
        for block_config in config:
            for k, v in block_config.items():
                nav_items = []
                for nav_item in v:
                    nav_items.append(NavigationFactory.get_navigation_item(nav_item))
                self.items.append((k, nav_items))


sidebar = Sidebar(nav_config)


def get_render_dict(current_page: str) -> dict:
    """
    context 에 current_page 를 만들어 주는 함수

    :param current_page: 현재 page string
    :type current_page: str
    :return:
    """
    render_dict = {"current_page": current_page}
    return render_dict
