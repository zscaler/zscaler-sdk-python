"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from zscaler.aiguard.llm_application_credentials import LLMApplicationCredentialsAPI
from zscaler.aiguard.llm_applications import LLMApplicationsAPI
from zscaler.aiguard.llm_provider_credentials import LLMProviderCredentialsAPI
from zscaler.aiguard.llm_providers import LLMProvidersAPI
from zscaler.aiguard.policies import PoliciesAPI
from zscaler.aiguard.policy_match_rules import PolicyMatchRulesAPI
from zscaler.request_executor import RequestExecutor


class AIGuardService:
    """
    AI Guard Service client, exposing the AI Guard configuration APIs over OneAPI.

    Policy detection (``/v1/detection/*``) is **not** available through OneAPI and is
    therefore not exposed here -- use ``LegacyAIGuardClient(...).aiguard.policy_detection``.
    """

    def __init__(self, request_executor: RequestExecutor) -> None:
        self._request_executor = request_executor

    @property
    def policies(self) -> PoliciesAPI:
        """
        The interface object for the :ref:`AI Guard Detection Policies interface <aiguard-policies>`.

        """
        return PoliciesAPI(self._request_executor)

    @property
    def policy_match_rules(self) -> PolicyMatchRulesAPI:
        """
        The interface object for the :ref:`AI Guard Policy Match Rules interface <aiguard-policy_match_rules>`.

        """
        return PolicyMatchRulesAPI(self._request_executor)

    @property
    def llm_providers(self) -> LLMProvidersAPI:
        """
        The interface object for the :ref:`AI Guard LLM Providers interface <aiguard-llm_providers>`.

        """
        return LLMProvidersAPI(self._request_executor)

    @property
    def llm_provider_credentials(self) -> LLMProviderCredentialsAPI:
        """
        The interface object for the :ref:`AI Guard LLM Provider Credentials interface <aiguard-llm_provider_credentials>`.

        """
        return LLMProviderCredentialsAPI(self._request_executor)

    @property
    def llm_applications(self) -> LLMApplicationsAPI:
        """
        The interface object for the :ref:`AI Guard LLM Applications interface <aiguard-llm_applications>`.

        """
        return LLMApplicationsAPI(self._request_executor)

    @property
    def llm_application_credentials(self) -> LLMApplicationCredentialsAPI:
        """
        The interface object for the
        :ref:`AI Guard LLM Application Credentials interface <aiguard-llm_application_credentials>`.

        """
        return LLMApplicationCredentialsAPI(self._request_executor)
