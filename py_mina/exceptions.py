################################################################################
# State
################################################################################


class StateError(Exception):
	pass


################################################################################
# Config
################################################################################


class ConfigError(Exception):
	pass


class BadConfigError(ConfigError):
	pass


class FetchConfigError(ConfigError):
	pass


class EnsureConfigError(ConfigError):
	pass


################################################################################
# Setup
################################################################################


class SetupError(Exception):
	pass


################################################################################
# Deploy
################################################################################


class DeployError(Exception):
	pass


class OnPreDeployError(DeployError):
	pass


class OnDeployError(DeployError):
	pass


class OnPostDeployError(DeployError):
	pass

	
class OnFinallizeDeployError(DeployError):
	pass


class OnDeploySuccessError(DeployError):
	pass
