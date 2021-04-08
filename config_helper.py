import json
import os
import time

import boto3


class AppConfigHelper:

    def __init__(
        self,
        appconfig_application: str,
        appconfig_environment: str,
        appconfig_profile: str,
        expire: int,
        client_id: str,
    ) -> None:

        self._client = boto3.client("appconfig",
                                    region_name=os.environ['AWS_DEFAULT_REGION'])
        self._appconfig_profile = appconfig_profile
        self._appconfig_environment = appconfig_environment
        self._appconfig_application = appconfig_application
        self.expire = expire
        self._client_id = client_id
        self._configuration_version = "null"
        self._last_update_time = 0.0
        self._config = None

    @property
    def appconfig_profile(self) -> str:
        """The profile in use."""
        return self._appconfig_profile

    @property
    def appconfig_environment(self) -> str:
        """The environment in use."""
        return self._appconfig_environment

    @property
    def appconfig_application(self) -> str:
        """The application in use."""
        return self._appconfig_application

    @property
    def config_version(self) -> str:
        """The configuration version last received."""
        return self._configuration_version

    @property
    def config(self) -> dict:
        return self._config

    def update_config(self, force: bool = False) -> bool:
        """Request the latest configration.
        Returns True if a new version of configuration was received. False
        indicates that no attempt was made, or that no new version was found.
        """
        if (
            time.time() - self._last_update_time < self.expire
        ) and not force:
            return False

        response = self._client.get_configuration(
            Application=self._appconfig_application,
            Environment=self._appconfig_environment,
            Configuration=self._appconfig_profile,
            ClientId=self._client_id,
            ClientConfigurationVersion=self._configuration_version,
        )

        if response["ConfigurationVersion"] == self._configuration_version:
            self._last_update_time = time.time()
            return False

        content = response["Content"].read()
        try:
            self._config = json.loads(content.decode("utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(error.msg) from error

        self._last_update_time = time.time()
        self._configuration_version = response["ConfigurationVersion"]
        return True
