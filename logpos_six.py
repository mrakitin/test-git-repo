import os
from pyOlog.ophyd_tools import _normalize_positioners, _print_pos


def log_pos(positioners=None, extra_msg=None, objlen=200):
    """Get the current position of Positioners and make a logbook entry.
    Print to the screen the position of the positioners and make a logbook text
    entry. This routine also creates session information in the logbook so
    positions can be recovered.
    Parameters
    ----------
    positioners : Positioner, list of Positioners or None
    Returns
    -------
    int
        The ID of the logbook entry returned by the logbook.log method.
    """
    if os.getenv("TEST"):
        print('Testing')
        return
    positioners = _normalize_positioners(positioners)
    logbook = get_logbook()
    if extra_msg:
        msg = extra_msg + '\n'
    else:
        msg = ''

    with closing(StringIO()) as sio:
        msg += sio.getvalue()

    # Add the text representation of the positioners

    # Create the property for storing motor posisions
    pdict = {}
    pdict['values'] = {}

    msg += logbook_add_objects(positioners)

    for p in positioners:
        try:
            pdict['values'][p.name] = p.position
        except DisconnectedError:
            pdict['values'][p.name] = DISCONNECTED

    pdict['objects'] = repr(positioners)
    print(f"{len(pdict['objects']) = }")
    print(f"{len(pdict['values']) = }")
    pdict['objects'] = pdict['objects'][:objlen]
    pdict['values'] = repr(pdict['values'])

    import pprint
    pprint.pprint(pdict)
    print(f"{msg = }")

    if logbook:
        id_ = logbook.log(msg, properties={'OphydPositioners': pdict},
                          ensure=True)

        print('Logbook positions added as Logbook ID {}'.format(id_))
        return id_
