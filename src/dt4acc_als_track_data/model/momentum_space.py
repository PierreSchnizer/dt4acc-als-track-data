from dataclasses import dataclass
from typing import Literal

import at

Branch = Literal["upper", "lower"]


@dataclass(frozen=True)
class TwissParametersForPlane:
    beta: float
    alpha: float


@dataclass(frozen=True)
class MomentumSpaceForPlane:
    twiss: TwissParametersForPlane
    emittance: float


@dataclass(frozen=True)
class MomentumSpace:
    x: MomentumSpaceForPlane
    y: MomentumSpaceForPlane

    def sigma_matrix(self):
        return at.sigma_matrix(
            betax=self.x.twiss.beta,
            alphax=self.x.twiss.alpha,
            emitx=self.x.emittance,
            betay=self.y.twiss.beta,
            alphay=self.y.twiss.alpha,
            emity = self.y.emittance,
        )


def get_branch_as_flag(branch: Branch) -> Literal[-1, 1]:
    if branch == "upper":
        return 1
    if branch == "lower":
        return -1
    raise ValueError(f"Invalid branch: {branch!r}")
