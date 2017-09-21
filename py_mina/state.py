"""
Deploy state manager
"""


from py_mina.utils import _AttributeDict
from py_mina.exceptions import StateError


state = _AttributeDict({
	'pre': None,	
	'deploy': None,	
	'post': None,	
	'finallize': None,
	'launch': None,
})

def set(key, value):
	if value in [True, False]:
		if key in state.keys():
			state[key] = value
		else:
			raise StateError('State "%s" is not defined' % key)
	else:
		raise StateError('State value must be "True" or "False"')


# Alias to prevent conflict when importing "py_mina.config" and "py_mina.state"
set_state = set