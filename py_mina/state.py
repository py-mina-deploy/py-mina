from py_mina.utils import _AttributeDict
from py_mina.exceptions import StateError

state = _AttributeDict({
	'pre_deploy': None,	
	'deploy': None,	
	'post_deploy': None,	
	'launch': None,	
})

def set(key, value):
	if value in [True, False]:
		if key in state.keys():
			state[key] = value
		else:
			raise StateError('State "%s" is not defined')
	else:
		raise StateError('State value must be "True" or "False"')
