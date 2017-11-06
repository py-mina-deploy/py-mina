"""
Deploy state manager
"""


from py_mina.utils import _AttributeDict


################################################################################
# Default state
################################################################################


state = _AttributeDict({
    'pre_deploy': None, 
    'deploy': None, 
    'post_deploy': None,    
    'finalize': None,
    'success': None,
    'on_success': None,
})


################################################################################
# Set state
################################################################################


def set(key, value):
    if key in state.keys():
        state[key] = value
    else:
        raise Exception('State "%s" is not defined' % key)


# Alias to prevent conflict when importing "py_mina.config" and "py_mina.state"
set_state = set
