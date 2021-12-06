from typing import Dict, Any, List, Optional

from virtualstudio.common.logging import logengine

GROUPS: Dict[str, Dict[str, List[Any]]] = {}

GROUP_TYPE_SOURCE_VISIBILITY = "src_visibility"

logger = logengine.getLogger()

def addToGroup(gtype: str, gname: str, element: Any):
    if gtype not in GROUPS:
        logger.info("Group Type Created: {}".format(gtype))
        GROUPS[gtype] = {}

    if gname not in GROUPS[gtype]:
        logger.info("Group Created: {}".format(gname))
        GROUPS[gtype][gname] = []

    logger.info("Object added to Group {} of Type {}".format(gtype, gname))
    GROUPS[gtype][gname].append(element)


def removeFromGroup(gtype: str, gname: str, element):
    if gtype not in GROUPS:
        return

    if gname not in GROUPS[gtype]:
        return

    if element in GROUPS[gtype][gname]:
        logger.info("Object removed from Group {} of Type {}".format(gtype, gname))
        GROUPS[gtype][gname].remove(element)

def getGroupNames(gtype: str):
    if gtype not in GROUPS:
        return None

    return list(GROUPS[gtype].keys())


def getGroup(gtype: str, gname: str) -> Optional[List[Any]]:
    if gtype not in GROUPS:
        logger.info("No Groups with Type {} found. Valid Types: {}".format(gtype, list(GROUPS.keys())))
        return None

    if gname not in GROUPS[gtype]:
        logger.info("No Groups with Name {} found. Valid Names: {}".format(gname, list(GROUPS[gtype].keys())))
        return None

    return GROUPS[gtype][gname]