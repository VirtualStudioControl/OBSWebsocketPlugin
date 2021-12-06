FILTER_DATA_ACTIONS = []


def addFilterDataAction(action):
    FILTER_DATA_ACTIONS.append(action)


def removeFilterDataAction(action):
    FILTER_DATA_ACTIONS.remove(action)


def updateFilterDataActions():
    for action in FILTER_DATA_ACTIONS:
        action.updateFilterValues()
