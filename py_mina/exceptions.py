################################################################################
# State
################################################################################


class StateError(Exception):
	pass


################################################################################
# Config
################################################################################


class BadConfigError(Exception):
	pass


class FetchConfigError(Exception):
	pass


class EnsureConfigError(Exception):
	pass


################################################################################
# Setup
################################################################################


class SetupError(Exception):
	pass


################################################################################
# Deploy
################################################################################


class PreDeployError(Exception):
	pass


class DeployError(Exception):
	pass


class PostDeployError(Exception):
	pass

	
class FinallizeDeployError(Exception):
	pass


################################################################################
# Launch
################################################################################


class LaunchSingletonError(Exception):
	pass


class LaunchError(Exception):
	pass

