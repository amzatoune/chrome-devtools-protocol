# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: Target

from __future__ import annotations
import enum
import typing
from dataclasses import dataclass
from .util import event_class, T_JSON_DICT

from . import browser
from . import page
from deprecated.sphinx import deprecated # type: ignore


class TargetID(str):
    def to_json(self) -> str:
        return self

    @classmethod
    def from_json(cls, json: str) -> TargetID:
        return cls(json)

    def __repr__(self):
        return 'TargetID({})'.format(super().__repr__())


class SessionID(str):
    '''
    Unique identifier of attached debugging session.
    '''
    def to_json(self) -> str:
        return self

    @classmethod
    def from_json(cls, json: str) -> SessionID:
        return cls(json)

    def __repr__(self):
        return 'SessionID({})'.format(super().__repr__())


@dataclass
class TargetInfo:
    target_id: TargetID

    type_: str

    title: str

    url: str

    #: Whether the target has an attached client.
    attached: bool

    #: Whether the target has access to the originating window.
    can_access_opener: bool

    #: Opener target Id
    opener_id: typing.Optional[TargetID] = None

    #: Frame id of originating window (is only set if target has an opener).
    opener_frame_id: typing.Optional[page.FrameId] = None

    browser_context_id: typing.Optional[browser.BrowserContextID] = None

    #: Provides additional details for specific target types. For example, for
    #: the type of "page", this may be set to "portal" or "prerender".
    subtype: typing.Optional[str] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['targetId'] = self.target_id.to_json()
        json['type'] = self.type_
        json['title'] = self.title
        json['url'] = self.url
        json['attached'] = self.attached
        json['canAccessOpener'] = self.can_access_opener
        if self.opener_id is not None:
            json['openerId'] = self.opener_id.to_json()
        if self.opener_frame_id is not None:
            json['openerFrameId'] = self.opener_frame_id.to_json()
        if self.browser_context_id is not None:
            json['browserContextId'] = self.browser_context_id.to_json()
        if self.subtype is not None:
            json['subtype'] = self.subtype
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetInfo:
        return cls(
            target_id=TargetID.from_json(json['targetId']),
            type_=str(json['type']),
            title=str(json['title']),
            url=str(json['url']),
            attached=bool(json['attached']),
            can_access_opener=bool(json['canAccessOpener']),
            opener_id=TargetID.from_json(json['openerId']) if json.get('openerId', None) is not None else None,
            opener_frame_id=page.FrameId.from_json(json['openerFrameId']) if json.get('openerFrameId', None) is not None else None,
            browser_context_id=browser.BrowserContextID.from_json(json['browserContextId']) if json.get('browserContextId', None) is not None else None,
            subtype=str(json['subtype']) if json.get('subtype', None) is not None else None,
        )


@dataclass
class FilterEntry:
    '''
    A filter used by target query/discovery/auto-attach operations.
    '''
    #: If set, causes exclusion of mathcing targets from the list.
    exclude: typing.Optional[bool] = None

    #: If not present, matches any type.
    type_: typing.Optional[str] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        if self.exclude is not None:
            json['exclude'] = self.exclude
        if self.type_ is not None:
            json['type'] = self.type_
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FilterEntry:
        return cls(
            exclude=bool(json['exclude']) if json.get('exclude', None) is not None else None,
            type_=str(json['type']) if json.get('type', None) is not None else None,
        )


class TargetFilter(list):
    '''
    The entries in TargetFilter are matched sequentially against targets and
    the first entry that matches determines if the target is included or not,
    depending on the value of ``exclude`` field in the entry.
    If filter is not specified, the one assumed is
    [{type: "browser", exclude: true}, {type: "tab", exclude: true}, {}]
    (i.e. include everything but ``browser`` and ``tab``).
    '''
    def to_json(self) -> typing.List[FilterEntry]:
        return self

    @classmethod
    def from_json(cls, json: typing.List[FilterEntry]) -> TargetFilter:
        return cls(json)

    def __repr__(self):
        return 'TargetFilter({})'.format(super().__repr__())


@dataclass
class RemoteLocation:
    host: str

    port: int

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['host'] = self.host
        json['port'] = self.port
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RemoteLocation:
        return cls(
            host=str(json['host']),
            port=int(json['port']),
        )


def activate_target(
        target_id: TargetID
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Activates (focuses) the target.

    :param target_id:
    '''
    params: T_JSON_DICT = dict()
    params['targetId'] = target_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.activateTarget',
        'params': params,
    }
    json = yield cmd_dict


def attach_to_target(
        target_id: TargetID,
        flatten: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,SessionID]:
    '''
    Attaches to the target with given id.

    :param target_id:
    :param flatten: *(Optional)* Enables "flat" access to the session via specifying sessionId attribute in the commands. We plan to make this the default, deprecate non-flattened mode, and eventually retire it. See crbug.com/991325.
    :returns: Id assigned to the session.
    '''
    params: T_JSON_DICT = dict()
    params['targetId'] = target_id.to_json()
    if flatten is not None:
        params['flatten'] = flatten
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.attachToTarget',
        'params': params,
    }
    json = yield cmd_dict
    return SessionID.from_json(json['sessionId'])


def attach_to_browser_target() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,SessionID]:
    '''
    Attaches to the browser target, only uses flat sessionId mode.

    **EXPERIMENTAL**

    :returns: Id assigned to the session.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.attachToBrowserTarget',
    }
    json = yield cmd_dict
    return SessionID.from_json(json['sessionId'])


def close_target(
        target_id: TargetID
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,bool]:
    '''
    Closes the target. If the target is a page that gets closed too.

    :param target_id:
    :returns: Always set to true. If an error occurs, the response indicates protocol error.
    '''
    params: T_JSON_DICT = dict()
    params['targetId'] = target_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.closeTarget',
        'params': params,
    }
    json = yield cmd_dict
    return bool(json['success'])


def expose_dev_tools_protocol(
        target_id: TargetID,
        binding_name: typing.Optional[str] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Inject object to the target's main frame that provides a communication
    channel with browser target.

    Injected object will be available as ``window[bindingName]``.

    The object has the follwing API:
    - ``binding.send(json)`` - a method to send messages over the remote debugging protocol
    - ``binding.onmessage = json => handleMessage(json)`` - a callback that will be called for the protocol notifications and command responses.

    **EXPERIMENTAL**

    :param target_id:
    :param binding_name: *(Optional)* Binding name, 'cdp' if not specified.
    '''
    params: T_JSON_DICT = dict()
    params['targetId'] = target_id.to_json()
    if binding_name is not None:
        params['bindingName'] = binding_name
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.exposeDevToolsProtocol',
        'params': params,
    }
    json = yield cmd_dict


def create_browser_context(
        dispose_on_detach: typing.Optional[bool] = None,
        proxy_server: typing.Optional[str] = None,
        proxy_bypass_list: typing.Optional[str] = None,
        origins_with_universal_network_access: typing.Optional[typing.List[str]] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,browser.BrowserContextID]:
    '''
    Creates a new empty BrowserContext. Similar to an incognito profile but you can have more than
    one.

    **EXPERIMENTAL**

    :param dispose_on_detach: *(Optional)* If specified, disposes this context when debugging session disconnects.
    :param proxy_server: *(Optional)* Proxy server, similar to the one passed to --proxy-server
    :param proxy_bypass_list: *(Optional)* Proxy bypass list, similar to the one passed to --proxy-bypass-list
    :param origins_with_universal_network_access: *(Optional)* An optional list of origins to grant unlimited cross-origin access to. Parts of the URL other than those constituting origin are ignored.
    :returns: The id of the context created.
    '''
    params: T_JSON_DICT = dict()
    if dispose_on_detach is not None:
        params['disposeOnDetach'] = dispose_on_detach
    if proxy_server is not None:
        params['proxyServer'] = proxy_server
    if proxy_bypass_list is not None:
        params['proxyBypassList'] = proxy_bypass_list
    if origins_with_universal_network_access is not None:
        params['originsWithUniversalNetworkAccess'] = [i for i in origins_with_universal_network_access]
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.createBrowserContext',
        'params': params,
    }
    json = yield cmd_dict
    return browser.BrowserContextID.from_json(json['browserContextId'])


def get_browser_contexts() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List[browser.BrowserContextID]]:
    '''
    Returns all browser contexts created with ``Target.createBrowserContext`` method.

    **EXPERIMENTAL**

    :returns: An array of browser context ids.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.getBrowserContexts',
    }
    json = yield cmd_dict
    return [browser.BrowserContextID.from_json(i) for i in json['browserContextIds']]


def create_target(
        url: str,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        browser_context_id: typing.Optional[browser.BrowserContextID] = None,
        enable_begin_frame_control: typing.Optional[bool] = None,
        new_window: typing.Optional[bool] = None,
        background: typing.Optional[bool] = None,
        for_tab: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,TargetID]:
    '''
    Creates a new page.

    :param url: The initial URL the page will be navigated to. An empty string indicates about:blank.
    :param width: *(Optional)* Frame width in DIP (headless chrome only).
    :param height: *(Optional)* Frame height in DIP (headless chrome only).
    :param browser_context_id: **(EXPERIMENTAL)** *(Optional)* The browser context to create the page in.
    :param enable_begin_frame_control: **(EXPERIMENTAL)** *(Optional)* Whether BeginFrames for this target will be controlled via DevTools (headless chrome only, not supported on MacOS yet, false by default).
    :param new_window: *(Optional)* Whether to create a new Window or Tab (chrome-only, false by default).
    :param background: *(Optional)* Whether to create the target in background or foreground (chrome-only, false by default).
    :param for_tab: **(EXPERIMENTAL)** *(Optional)* Whether to create the target of type "tab".
    :returns: The id of the page opened.
    '''
    params: T_JSON_DICT = dict()
    params['url'] = url
    if width is not None:
        params['width'] = width
    if height is not None:
        params['height'] = height
    if browser_context_id is not None:
        params['browserContextId'] = browser_context_id.to_json()
    if enable_begin_frame_control is not None:
        params['enableBeginFrameControl'] = enable_begin_frame_control
    if new_window is not None:
        params['newWindow'] = new_window
    if background is not None:
        params['background'] = background
    if for_tab is not None:
        params['forTab'] = for_tab
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.createTarget',
        'params': params,
    }
    json = yield cmd_dict
    return TargetID.from_json(json['targetId'])


def detach_from_target(
        session_id: typing.Optional[SessionID] = None,
        target_id: typing.Optional[TargetID] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Detaches session with given id.

    :param session_id: *(Optional)* Session to detach.
    :param target_id: **(DEPRECATED)** *(Optional)* Deprecated.
    '''
    params: T_JSON_DICT = dict()
    if session_id is not None:
        params['sessionId'] = session_id.to_json()
    if target_id is not None:
        params['targetId'] = target_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.detachFromTarget',
        'params': params,
    }
    json = yield cmd_dict


def dispose_browser_context(
        browser_context_id: browser.BrowserContextID
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Deletes a BrowserContext. All the belonging pages will be closed without calling their
    beforeunload hooks.

    **EXPERIMENTAL**

    :param browser_context_id:
    '''
    params: T_JSON_DICT = dict()
    params['browserContextId'] = browser_context_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.disposeBrowserContext',
        'params': params,
    }
    json = yield cmd_dict


def get_target_info(
        target_id: typing.Optional[TargetID] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,TargetInfo]:
    '''
    Returns information about a target.

    **EXPERIMENTAL**

    :param target_id: *(Optional)*
    :returns: 
    '''
    params: T_JSON_DICT = dict()
    if target_id is not None:
        params['targetId'] = target_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.getTargetInfo',
        'params': params,
    }
    json = yield cmd_dict
    return TargetInfo.from_json(json['targetInfo'])


def get_targets(
        filter_: typing.Optional[TargetFilter] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List[TargetInfo]]:
    '''
    Retrieves a list of available targets.

    :param filter_: **(EXPERIMENTAL)** *(Optional)* Only targets matching filter will be reported. If filter is not specified and target discovery is currently enabled, a filter used for target discovery is used for consistency.
    :returns: The list of targets.
    '''
    params: T_JSON_DICT = dict()
    if filter_ is not None:
        params['filter'] = filter_.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.getTargets',
        'params': params,
    }
    json = yield cmd_dict
    return [TargetInfo.from_json(i) for i in json['targetInfos']]


@deprecated(version="1.3")
def send_message_to_target(
        message: str,
        session_id: typing.Optional[SessionID] = None,
        target_id: typing.Optional[TargetID] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Sends protocol message over session with given id.
    Consider using flat mode instead; see commands attachToTarget, setAutoAttach,
    and crbug.com/991325.

    .. deprecated:: 1.3

    :param message:
    :param session_id: *(Optional)* Identifier of the session.
    :param target_id: **(DEPRECATED)** *(Optional)* Deprecated.
    '''
    params: T_JSON_DICT = dict()
    params['message'] = message
    if session_id is not None:
        params['sessionId'] = session_id.to_json()
    if target_id is not None:
        params['targetId'] = target_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.sendMessageToTarget',
        'params': params,
    }
    json = yield cmd_dict


def set_auto_attach(
        auto_attach: bool,
        wait_for_debugger_on_start: bool,
        flatten: typing.Optional[bool] = None,
        filter_: typing.Optional[TargetFilter] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Controls whether to automatically attach to new targets which are considered to be related to
    this one. When turned on, attaches to all existing related targets as well. When turned off,
    automatically detaches from all currently attached targets.
    This also clears all targets added by ``autoAttachRelated`` from the list of targets to watch
    for creation of related targets.

    **EXPERIMENTAL**

    :param auto_attach: Whether to auto-attach to related targets.
    :param wait_for_debugger_on_start: Whether to pause new targets when attaching to them. Use ```Runtime.runIfWaitingForDebugger``` to run paused targets.
    :param flatten: *(Optional)* Enables "flat" access to the session via specifying sessionId attribute in the commands. We plan to make this the default, deprecate non-flattened mode, and eventually retire it. See crbug.com/991325.
    :param filter_: **(EXPERIMENTAL)** *(Optional)* Only targets matching filter will be attached.
    '''
    params: T_JSON_DICT = dict()
    params['autoAttach'] = auto_attach
    params['waitForDebuggerOnStart'] = wait_for_debugger_on_start
    if flatten is not None:
        params['flatten'] = flatten
    if filter_ is not None:
        params['filter'] = filter_.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.setAutoAttach',
        'params': params,
    }
    json = yield cmd_dict


def auto_attach_related(
        target_id: TargetID,
        wait_for_debugger_on_start: bool,
        filter_: typing.Optional[TargetFilter] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Adds the specified target to the list of targets that will be monitored for any related target
    creation (such as child frames, child workers and new versions of service worker) and reported
    through ``attachedToTarget``. The specified target is also auto-attached.
    This cancels the effect of any previous ``setAutoAttach`` and is also cancelled by subsequent
    ``setAutoAttach``. Only available at the Browser target.

    **EXPERIMENTAL**

    :param target_id:
    :param wait_for_debugger_on_start: Whether to pause new targets when attaching to them. Use ```Runtime.runIfWaitingForDebugger``` to run paused targets.
    :param filter_: **(EXPERIMENTAL)** *(Optional)* Only targets matching filter will be attached.
    '''
    params: T_JSON_DICT = dict()
    params['targetId'] = target_id.to_json()
    params['waitForDebuggerOnStart'] = wait_for_debugger_on_start
    if filter_ is not None:
        params['filter'] = filter_.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.autoAttachRelated',
        'params': params,
    }
    json = yield cmd_dict


def set_discover_targets(
        discover: bool,
        filter_: typing.Optional[TargetFilter] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Controls whether to discover available targets and notify via
    ``targetCreated/targetInfoChanged/targetDestroyed`` events.

    :param discover: Whether to discover available targets.
    :param filter_: **(EXPERIMENTAL)** *(Optional)* Only targets matching filter will be attached. If ```discover```` is false, ````filter``` must be omitted or empty.
    '''
    params: T_JSON_DICT = dict()
    params['discover'] = discover
    if filter_ is not None:
        params['filter'] = filter_.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.setDiscoverTargets',
        'params': params,
    }
    json = yield cmd_dict


def set_remote_locations(
        locations: typing.List[RemoteLocation]
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enables target discovery for the specified locations, when ``setDiscoverTargets`` was set to
    ``true``.

    **EXPERIMENTAL**

    :param locations: List of remote locations.
    '''
    params: T_JSON_DICT = dict()
    params['locations'] = [i.to_json() for i in locations]
    cmd_dict: T_JSON_DICT = {
        'method': 'Target.setRemoteLocations',
        'params': params,
    }
    json = yield cmd_dict


@event_class('Target.attachedToTarget')
@dataclass
class AttachedToTarget:
    '''
    **EXPERIMENTAL**

    Issued when attached to target because of auto-attach or ``attachToTarget`` command.
    '''
    #: Identifier assigned to the session used to send/receive messages.
    session_id: SessionID
    target_info: TargetInfo
    waiting_for_debugger: bool

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AttachedToTarget:
        return cls(
            session_id=SessionID.from_json(json['sessionId']),
            target_info=TargetInfo.from_json(json['targetInfo']),
            waiting_for_debugger=bool(json['waitingForDebugger'])
        )


@event_class('Target.detachedFromTarget')
@dataclass
class DetachedFromTarget:
    '''
    **EXPERIMENTAL**

    Issued when detached from target for any reason (including ``detachFromTarget`` command). Can be
    issued multiple times per target if multiple sessions have been attached to it.
    '''
    #: Detached session identifier.
    session_id: SessionID
    #: Deprecated.
    target_id: typing.Optional[TargetID]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> DetachedFromTarget:
        return cls(
            session_id=SessionID.from_json(json['sessionId']),
            target_id=TargetID.from_json(json['targetId']) if json.get('targetId', None) is not None else None
        )


@event_class('Target.receivedMessageFromTarget')
@dataclass
class ReceivedMessageFromTarget:
    '''
    Notifies about a new protocol message received from the session (as reported in
    ``attachedToTarget`` event).
    '''
    #: Identifier of a session which sends a message.
    session_id: SessionID
    message: str
    #: Deprecated.
    target_id: typing.Optional[TargetID]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ReceivedMessageFromTarget:
        return cls(
            session_id=SessionID.from_json(json['sessionId']),
            message=str(json['message']),
            target_id=TargetID.from_json(json['targetId']) if json.get('targetId', None) is not None else None
        )


@event_class('Target.targetCreated')
@dataclass
class TargetCreated:
    '''
    Issued when a possible inspection target is created.
    '''
    target_info: TargetInfo

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetCreated:
        return cls(
            target_info=TargetInfo.from_json(json['targetInfo'])
        )


@event_class('Target.targetDestroyed')
@dataclass
class TargetDestroyed:
    '''
    Issued when a target is destroyed.
    '''
    target_id: TargetID

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetDestroyed:
        return cls(
            target_id=TargetID.from_json(json['targetId'])
        )


@event_class('Target.targetCrashed')
@dataclass
class TargetCrashed:
    '''
    Issued when a target has crashed.
    '''
    target_id: TargetID
    #: Termination status type.
    status: str
    #: Termination error code.
    error_code: int

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetCrashed:
        return cls(
            target_id=TargetID.from_json(json['targetId']),
            status=str(json['status']),
            error_code=int(json['errorCode'])
        )


@event_class('Target.targetInfoChanged')
@dataclass
class TargetInfoChanged:
    '''
    Issued when some information about a target has changed. This only happens between
    ``targetCreated`` and ``targetDestroyed``.
    '''
    target_info: TargetInfo

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TargetInfoChanged:
        return cls(
            target_info=TargetInfo.from_json(json['targetInfo'])
        )
