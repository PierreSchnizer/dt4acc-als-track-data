from collections import defaultdict
from typing import Sequence, Dict

from bluesky.protocols import Reading


def all_data_in_one_dict(data: Sequence[Dict[str, Reading]]) -> Dict[str, Reading]:
    """
    Todo: does bluesky provide that ?
    """
    d = {}
    for elem in data:
        for key, value in elem.items():
            if d.get(key, None) is None:
                d[key] = value
            else:
                logger.warning(f"Duplicate key {key} in data, ignoring this occurence")
    return d


def group_data(
    data: Dict[str, Reading]
) -> (Dict[str, Reading], Dict[str, Dict[str, Reading]]):
    bpm_data = {}
    non_bpm_data = {}
    for k, v in data.items():
        if "BPM" in k:
            bpm_data[k] = v
        else:
            non_bpm_data[k] = v
    bpm_data = group_bpm_data(bpm_data)
    return non_bpm_data, bpm_data


def group_bpm_data(data: Sequence[Reading]) -> Dict[str, Dict[str, Reading]]:
    d = defaultdict(dict)
    for k, v in data.items():
        bpm_name, coor = map(str, k.split("-"))
        assert coor in ["x", "y", "sum"]
        d[bpm_name][coor] = v
    r = dict(d)
    for v in r.values():
        # check that these entries exist
        v["x"]
        v["y"]
        v["sum"]
    return r
