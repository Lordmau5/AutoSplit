from cv2 import (
    Error as Error, data as data, gapi as gapi, mat_wrapper as mat_wrapper, misc as misc, utils as utils,
    version as version,
)
from cv2.cv2 import *  # noqa: F403
from cv2.mat_wrapper import Mat as WrappedMat, _NDArray
from typing_extensions import TypeAlias

__all__: list[str] = []


def bootstrap() -> None: ...


Mat: TypeAlias = WrappedMat | _NDArray
# TODO: Make Mat generic with int or float
_MatF: TypeAlias = WrappedMat | _NDArray  # noqa: Y047
