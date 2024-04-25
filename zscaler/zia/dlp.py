# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from box import Box, BoxList
from requests import Response

from zscaler.utils import snake_to_camel
from zscaler.zia import ZIAClient


class DLPAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_dicts(self, query: str = None) -> BoxList:
        """
        Returns a list of all custom and predefined ZIA DLP Dictionaries.

        Args:
            query (str): A search string used to match against a DLP dictionary's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP Dictionaries.

        Examples:
            Print all dictionaries

            >>> for dictionary in zia.dlp.list_dicts():
            ...    pprint(dictionary)

            Print dictionaries that match the name or description 'GDPR'

            >>> pprint(zia.dlp.list_dicts('GDPR'))

        """
        payload = {"search": query}
        list = self.rest.get(path="/dlpDictionaries", params=payload)
        if isinstance(list, Response):
            return None
        return list

    def get_dict(self, dict_id: str) -> Box:
        """
        Returns the DLP Dictionary that matches the specified DLP Dictionary id.

        Args:
            dict_id (str): The unique id for the DLP Dictionary.

        Returns:
            :obj:`Box`: The ZIA DLP Dictionary resource record.

        Examples:
            >>> pprint(zia.dlp.get_dict('3'))

        """
        response = self.rest.get("/dlpDictionaries/%s" % (dict_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def add_dict(self, name: str, custom_phrase_match_type: str, dictionary_type: str, **kwargs) -> Box:
        """
        Add a new Patterns and Phrases DLP Dictionary to ZIA.

        Args:
            name (str): The name of the DLP Dictionary.
            match_type (str): The DLP custom phrase/pattern match type. Accepted values are ``all`` or ``any``.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the DLP Dictionary.
            phrases (list):
                A list of DLP phrases, with each phrase provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', 'TOP SECRET')
                    ('unique', 'COMMERCIAL-IN-CONFIDENCE')

            patterns (list):
                A list of DLP patterns, with each pattern provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', '\d{2} \d{3} \d{3} \d{3}')
                    ('unique', '[A-Z]{6}[A-Z0-9]{2,5}')

        Returns:
            :obj:`Box`: The newly created DLP Dictionary resource record.

        Examples:
            Match text found that contains an IPv4 address using patterns:

            >>> zia.dlp.add_dict(name='IPv4 Addresses',
            ...                description='Matches IPv4 address pattern.',
            ...                match_type='all',
            ...                patterns=[
            ...                    ('all', '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/(\d|[1-2]\d|3[0-2]))?')
            ...                ]))

            Match text found that contains government document caveats using phrases.

            >>> zia.dlp.add_dict(name='Gov Document Caveats',
            ...                description='Matches government classification caveats.',
            ...                match_type='any',
            ...                phrases=[
            ...                    ('all', 'TOP SECRET'),
            ...                    ('all', 'SECRET'),
            ...                    ('all', 'CONFIDENTIAL')
            ...                ]))

            Match text found that meets the criteria for a Secret Project's document markings using phrases and
            patterns:

            >>> zia.dlp.add_dict(name='Secret Project Documents',
            ...                description='Matches documents created for the Secret Project.',
            ...                match_type='any',
            ...                phrases=[
            ...                    ('all', 'Project Umbrella'),
            ...                    ('all', 'UMBRELLA')
            ...                ],
            ...                patterns=[
            ...                    ('unique', '\d{1,2}-\d{1,2}-[A-Z]{5}')
            ...                ]))

        """

        payload = {
            "name": name,
            "customPhraseMatchType": custom_phrase_match_type,
            "dictionaryType": dictionary_type,
        }

        # Process additional keyword arguments
        for key, value in kwargs.items():
            # Convert the key to camelCase and assign the value
            camel_key = snake_to_camel(key)
            payload[camel_key] = value

        response = self.rest.post("dlpDictionaries", json=payload)
        if isinstance(response, Response):
            # Handle non-successful status codes
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")

        return response

    def update_dict(self, dict_id: str, **kwargs) -> Box:
        """
        Updates the specified DLP Dictionary.

        Args:
            dict_id (str): The unique id of the DLP Dictionary.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information about the DLP Dictionary.
            match_type (str): The DLP custom phrase/pattern match type. Accepted values are ``all`` or ``any``.
            name (str): The name of the DLP Dictionary.
            phrases (list):
                A list of DLP phrases, with each phrase provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', 'TOP SECRET')
                    ('unique', 'COMMERCIAL-IN-CONFIDENCE')

            patterns (list):
                A list of DLP pattersn, with each pattern provided by a tuple following the convention
                (`action`, `pattern`). Accepted actions are ``all`` or ``unique``. E.g.

                .. code-block:: python

                    ('all', '\d{2} \d{3} \d{3} \d{3}')
                    ('unique', '[A-Z]{6}[A-Z0-9]{2,5}')

        Returns:
            :obj:`Box`: The updated DLP Dictionary resource record.

        Examples:
            Update the name of a DLP Dictionary:

            >>> zia.dlp.update_dict('3',
            ...                name='IPv4 and IPv6 Addresses')

            Update the description and phrases for a DLP Dictionary.

            >>> zia.dlp.update_dict('4',
            ...        description='Updated government caveats.'
            ...        phrases=[
            ...                    ('all', 'TOP SECRET'),
            ...                    ('all', 'SECRET'),
            ...                    ('all', 'PROTECTED')
            ...                ])

        """
        # Fetch the existing dictionary details
        existing_dict = self.get_dict(dict_id)

        # Construct the payload for update
        payload = {
            "id": dict_id,
            "name": existing_dict.get("name"),
            "customPhraseMatchType": existing_dict.get("customPhraseMatchType"),
            "dictionaryType": existing_dict.get("dictionaryType"),
        }

        # Process additional keyword arguments
        for key, value in kwargs.items():
            # Convert the key to camelCase and assign the value
            camel_key = snake_to_camel(key)
            payload[camel_key] = value

        response = self.rest.put(f"/dlpDictionaries/{dict_id}", json=payload)
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")

        # Return the updated object
        return self.get_dict(dict_id)

    def delete_dict(self, dict_id: str) -> int:
        """
        Deletes the DLP Dictionary that matches the specified DLP Dictionary id.

        Args:
            dict_id (str): The unique id for the DLP Dictionary.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.dlp.delete_dict('8')

        """
        response = self.rest.delete("/dlpDictionaries/%s" % (dict_id))
        return response.status_code

    def validate_dict(self, pattern: str) -> Box:
        """
        Validates the provided pattern for usage in a DLP Dictionary.

        Note: The ZIA API documentation doesn't provide information on how to structure a request for this API endpoint.
         This endpoint is returning a valid response but validation isn't failing for obvious wrong patterns. Use at
         own risk.

        Args:
            pattern (str): DLP Pattern for evaluation.

        Returns:
            :obj:`Box`: Information on the provided pattern.

        """
        payload = {"data": pattern}

        response = self.rest.post(path="dlpDictionaries/validateDlpPattern", json=payload)
        if isinstance(response, Response):
            return None
        return response

    # TODO: implement the remaining
    def add_dlp_engine(
        self,
        name: str,
        engine_expression=None,
        custom_dlp_engine=None,
        description=None,
    ) -> Box:
        """
        Adds a new dlp engine.
        ...
        """

        payload = {
            "name": name,
        }

        if engine_expression is not None:
            payload["engineExpression"] = engine_expression

        if custom_dlp_engine is not None:
            payload["customDlpEngine"] = custom_dlp_engine

        if description is not None:
            payload["description"] = description

        # Convert the payload keys to camelCase
        camel_payload = {snake_to_camel(key): value for key, value in payload.items()}

        response = self.rest.post("dlpEngines", json=camel_payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_dlp_engine(self, engine_id: str, **kwargs) -> Box:
        """
        Updates an existing dlp engine.

        Args:
            engine_id (str): The unique ID for the dlp engine that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The order of the rule, defaults to adding rule to bottom of list.
            description (str): The admin rank of the rule.
            engine_expression (str, optional): The logical expression defining a DLP engine by
                combining DLP dictionaries using logical operators: All (AND), Any (OR), Exclude (NOT),
                and Sum (total number of content matches).
            custom_dlp_engine (bool, optional): If true, indicates a custom DLP engine.
            description (str, optional): The DLP engine description.

        Returns:
            :obj:`Box`: The updated dlp engine resource record.

        Examples:
            Update the dlp engine:

            >>> zia.dlp.add_dlp_engine(name='new_dlp_engine',
            ...    description='TT#1965432122',
            ...    engine_expression="((D63.S > 1))",
            ...    custom_dlp_engine=False)

            Update a rule to enable custom dlp engine:

            >>> zia.dlp.add_dlp_engine('976597',
            ...    custom_dlp_engine=True,
            ...    engine_expression="((D63.S > 1))",
            ...    description="TT#1965232866")

        """
        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_dlp_engines(engine_id).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.put(f"/dlpEngines/{engine_id}", json=payload)
        if isinstance(response, Response) and response.status_code != 200:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")
        return self.get_dlp_engines(engine_id)

    def delete_dlp_engine(self, engine_id: str) -> int:
        """
        Deletes the specified dlp engine.

        Args:
            engine_id (str): The unique identifier for the dlp engine.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.dlp.delete_dlp_engine('278454')

        """
        response = self.rest.delete("/dlpEngines/%s" % (engine_id))
        return response.status_code

    def list_dlp_engines(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA DLP Engines.

        Args:
            query (str): A search string used to match against a DLP Engine's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP Engines.

        Examples:
            Print all dlp engines

            >>> for dlp engines in zia.dlp.list_dlp_engines():
            ...    pprint(engine)

            Print engines that match the name or description 'GDPR'

            >>> pprint(zia.dlp.list_dlp_engines('GDPR'))

        """
        response = self.rest.get("/dlpEngines")
        if isinstance(response, Response):
            return None
        return response

    def get_dlp_engines(self, engine_id: str) -> Box:
        """
        Returns the dlp engine details for a given DLP Engine.

        Args:
            engine_id (str): The unique identifier for the DLP Engine.

        Returns:
            :obj:`Box`: The DLP Engine resource record.

        Examples:
            >>> engine = zia.dlp.get_dlp_engines('99999')

        """
        response = self.rest.get("/dlpEngines/%s" % (engine_id))
        if isinstance(response, Response):
            return None
        return response

    def get_dlp_engine_by_name(self, name):
        engines = self.list_dlp_engines()
        for engine in engines:
            if engine.get("name") == name:
                return engine
        return None

    def list_dlp_icap_servers(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA DLP ICAP Servers.

        Args:
            query (str): A search string used to match against a DLP icap server's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP ICAP Servers.

        Examples:
            Print all icap servers

            >>> for dlp icap in zia.dlp.list_dlp_icap_servers():
            ...    pprint(icap)

            Print icaps that match the name or description 'ZS_ICAP'

            >>> pprint(zia.dlp.list_dlp_icap_servers('ZS_ICAP'))

        """
        response = self.rest.get("/icapServers")
        if isinstance(response, Response):
            return None
        return response
        # payload = {"search": query}
        # list = self.rest.get(path="/icapServers", params=payload)
        # if isinstance(list, Response):
        #     return None
        # return list

    def get_dlp_icap_servers(self, icap_server_id: str) -> Box:
        """
        Returns the dlp icap server details for a given DLP ICAP Server.

        Args:
            icap_server_id (str): The unique identifier for the DLP ICAP Server.

        Returns:
            :obj:`Box`: The DLP ICAP Server resource record.

        Examples:
            >>> icap = zia.dlp.get_dlp_icap_servers('99999')

        """
        response = self.rest.get("/icapServers/%s" % (icap_server_id))
        if isinstance(response, Response):
            return None
        return response

    def get_dlp_icap_by_name(self, name):
        icaps = self.list_dlp_icap_servers()
        for icap in icaps:
            if icap.get("name") == name:
                return icap
        return None

    def list_dlp_incident_receiver(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA DLP Incident Receiver.

        Args:
            query (str): A search string used to match against a DLP Incident Receiver's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP Incident Receiver.

        Examples:
            Print all incident receivers

            >>> for receiver in zia.dlp.list_dlp_incident_receiver():
            ...    pprint(dlp)

            Print Incident Receiver that match the name or description 'ZS_INC_RECEIVER_01'

            >>> pprint(zia.dlp.list_dlp_incident_receiver('ZS_INC_RECEIVER_01'))

        """
        response = self.rest.get("/incidentReceiverServers")
        if isinstance(response, Response):
            return None
        return response

    def get_dlp_incident_receiver(self, receiver_id: str) -> Box:
        """
        Returns the dlp incident receiver details for a given DLP Incident Receiver.

        Args:
            receiver_id (str): The unique identifier for the DLP Incident Receiver.

        Returns:
            :obj:`Box`: The DLP Incident Receiver resource record.

        Examples:
            >>> incident_receiver = zia.dlp.get_dlp_incident_receiver('99999')

        """
        response = self.rest.get("/incidentReceiverServers/%s" % (receiver_id))
        if isinstance(response, Response):
            return None
        return response

    def get_dlp_incident_receiver_by_name(self, name):
        """
        Retrieves a specific DLP Incident Receiver by its name.

        Args:
            name (str): The name of the dlp incident receiver to retrieve.

        Returns:
            :obj:`Box`: The incident receiver if found, otherwise None.

        Examples:
            >>> receiver = zia.dlp.get_dlp_incident_receiver_by_name('ZS_INC_RECEIVER_01')
            ...    pprint(receiver)
        """
        receivers = self.list_dlp_incident_receiver()
        for receiver in receivers:
            if receiver.get("name") == name:
                return receiver
        return None

    def list_dlp_idm_profiles(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA DLP IDM Profiles.

        Args:
            query (str): A search string used to match against a DLP IDM Profile's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP IDM Profiles.

        Examples:
            Print all idm profiles

            >>> for dlp idm in zia.dlp.list_dlp_idm_profiles():
            ...    pprint(idm)

            Print IDM profiles that match the name or description 'IDM_PROFILE_TEMPLATE'

            >>> pprint(zia.dlp.list_dlp_idm_profiles('IDM_PROFILE_TEMPLATE'))

        """
        payload = {"search": query}
        list = self.rest.get(path="/idmprofile", params=payload)
        if isinstance(list, Response):
            return None
        return list

    def get_dlp_idm_profiles(self, profile_id: str) -> Box:
        """
        Returns the dlp idmp profile details for a given DLP IDM Profile.

        Args:
            icap_server_id (str): The unique identifier for the DLP IDM Profile.

        Returns:
            :obj:`Box`: The DLP IDM Profile resource record.

        Examples:
            >>> idm = zia.dlp.get_dlp_idm_profiles('99999')

        """
        response = self.rest.get("/idmprofile/%s" % (profile_id))
        if isinstance(response, Response):
            return None
        return response

    def get_dlp_idm_profile_by_name(self, profile_name):
        profiles = self.list_dlp_idm_profiles()
        for profile in profiles:
            if profile.get("profile_name") == profile_name:
                return profile
        return None

    def list_dlp_templates(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA DLP Notification Templates.

        Args:
            query (str): A search string used to match against a DLP Engine's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP Engines.

        Examples:
            Print all dlp templates

            >>> for dlp templates in zia.dlp.list_dlp_templates():
            ...    pprint(engine)

            Print templates that match the name or description 'Standard_Template'

            >>> pprint(zia.dlp.list_dlp_templates('Standard_Template'))

        """
        payload = {"search": query}
        response = self.rest.get("/dlpNotificationTemplates", params=payload)
        if isinstance(response, Response):
            return None
        return response

    def get_dlp_templates(self, template_id: str) -> Box:
        """
        Returns the dlp notification template details for a given DLP template.

        Args:
            template_id (int): The unique identifer for the DLP notification template.

        Returns:
            :obj:`Box`: The DLP template resource record.

        Examples:
            >>> template = zia.dlp.get_dlp_templates('99999')

        """
        response = self.rest.get("/dlpNotificationTemplates/%s" % (template_id))
        if isinstance(response, Response):
            return None
        return response

    def add_dlp_template(self, name: str, subject: str, **kwargs) -> Box:
        """
        Adds a new DLP notification template to ZIA.

        Args:
            name (str): The name of the DLP notification template.
            subject (str): The subject line displayed within the DLP notification email.

        Keyword Args:
            attach_content (bool): If true, the content in violation is attached to the DLP notification email.
            plain_text_message (str): Template for the plain text UTF-8 message body displayed in the DLP notification email.
            html_message (str): Template for the HTML message body displayed in the DLP notification email.

        Returns:
            :obj:`Box`: The newly created DLP Notification Template resource record.

        Examples:
            Create a new DLP Notification Template:

            >>> zia.dlp.add_dlp_template(name="New DLP Template",
            ...                         subject="Alert: DLP Violation Detected",
            ...                         attach_content=True,
            ...                         plain_text_message="Text message content",
            ...                         html_message="<html><body>HTML message content</body></html>")
        """

        payload = {
            "name": name,
            "subject": subject,
        }

        # Process additional keyword arguments
        for key, value in kwargs.items():
            # Convert the key to camelCase and assign the value
            camel_key = snake_to_camel(key)
            payload[camel_key] = value

        response = self.rest.post("dlpNotificationTemplates", json=payload)
        if isinstance(response, Response):
            # Handle non-successful status codes
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")

        return response

    def update_dlp_template(self, template_id: str, **kwargs) -> Box:
        """
        Updates the specified DLP Notification Template.

        Args:
            template_id (str): The unique identifier for the DLP notification template.

        Keyword Args:
            name (str): The new name of the DLP notification template.
            subject (str): The new subject line for the DLP notification email.
            attach_content (bool): If true, updates the setting for attaching content in violation.
            plain_text_message (str): New template for the plain text UTF-8 message body.
            html_message (str): New template for the HTML message body.
            tls_enabled (bool): If true, enables TLS for the notification template.

        Returns:
            :obj:`Box`: The updated DLP Notification Template resource record.

        Examples:
            Update the name of a DLP Notification Template:

            >>> zia.dlp.update_dlp_template(template_id=4370,,
            ...                tls_enabled=True)

            Update the description and phrases for a DLP Dictionary.

            >>> zia.dlp.update_dlp_template(template_id=4370,
            ...        name='Standard DLP Template',
            ...        tls_enabled=False,
            ...        attach_content=False)
        """

        # Fetch the existing template details
        existing_template = self.get_dlp_templates(template_id)
        if not existing_template:
            raise ValueError("Template not found with the provided ID")

        # Construct the payload for update
        payload = {snake_to_camel(key): kwargs.get(key, existing_template.get(snake_to_camel(key))) for key in kwargs}

        # Ensure mandatory fields are included
        mandatory_fields = ["plainTextMessage", "htmlMessage"]
        for field in mandatory_fields:
            if field not in payload:
                payload[field] = existing_template.get(field)

        # Add the template ID
        payload["id"] = template_id

        # Make the API call
        response = self.rest.put(f"/dlpNotificationTemplates/{template_id}", json=payload)
        if isinstance(response, Response) and response.status_code != 200:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

        # Return the updated object
        return self.get_dlp_templates(template_id)

    def delete_dlp_template(self, template_id: str) -> int:
        """
        Deletes the DLP Notification Template that matches the specified Template id.

        Args:
            template_id (str): The unique id for the DLP Notification Template.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.dlp.delete_dlp_template(template_id=4370)

        """
        response = self.rest.delete("/dlpNotificationTemplates/%s" % (template_id))
        return response.status_code
