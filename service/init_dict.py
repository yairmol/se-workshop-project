from typing import TypedDict, List, Union, Dict, Optional


class RefDict(TypedDict):
    ref: Union[str, int]


class ActionDict(TypedDict):
    user: Union[str, int]
    action: str
    params: Dict[str, Union[RefDict, str, int]]
    ref_id: Optional[Union[int, str]]


class InitDict(TypedDict):
    users: List[Union[str, int]]
    actions: List[ActionDict]