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

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class DLPDictionary(ZscalerObject):
    """
    A class for Dictionary objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.confidence_threshold = config["confidenceThreshold"] if "confidenceThreshold" in config else None
            self.custom_phrase_match_type = config["customPhraseMatchType"] if "customPhraseMatchType" in config else None
            self.name_l10n_tag = config["nameL10nTag"] if "nameL10nTag" in config else False
            self.dictionary_type = config["dictionaryType"] if "dictionaryType" in config else None
            self.exact_data_match_details = config["exactDataMatchDetails"] if "exactDataMatchDetails" in config else []
            self.idm_profile_match_accuracy_details = (
                config["idmProfileMatchAccuracyDetails"] if "idmProfileMatchAccuracyDetails" in config else []
            )
            self.proximity = config["proximity"] if "proximity" in config else 0
            self.predefined_phrases = config["predefinedPhrases"] if "predefinedPhrases" in config else []
            self.ignore_exact_match_idm_dict = (
                config["ignoreExactMatchIdmDict"] if "ignoreExactMatchIdmDict" in config else False
            )
            self.include_bin_numbers = config["includeBinNumbers"] if "includeBinNumbers" in config else False
            self.predefined_clone = config["predefinedClone"] if "predefinedClone" in config else False
            self.threshold_allowed = config["thresholdAllowed"] if "thresholdAllowed" in config else False
            self.hierarchical_identifiers = config["hierarchicalIdentifiers"] if "hierarchicalIdentifiers" in config else []
            self.proximity_enabled_for_custom_dictionary = (
                config["proximityEnabledForCustomDictionary"] if "proximityEnabledForCustomDictionary" in config else False
            )
            self.include_ssn_numbers = config["includeSsnNumbers"] if "includeSsnNumbers" in config else False
            self.unicode_phrase_matching_enabled = (
                config["unicodePhraseMatchingEnabled"] if "unicodePhraseMatchingEnabled" in config else False
            )
            self.dictionary_cloning_enabled = (
                config["dictionaryCloningEnabled"] if "dictionaryCloningEnabled" in config else False
            )
            self.confidence_level_for_predefined_dict = (
                config["confidenceLevelForPredefinedDict"] if "confidenceLevelForPredefinedDict" in config else None
            )
            self.custom = config["custom"] if "custom" in config else False
            self.proximity_length_enabled = config["proximityLengthEnabled"] if "proximityLengthEnabled" in config else False
            self.custom_phrase_supported = config["customPhraseSupported"] if "customPhraseSupported" in config else False
            self.hierarchical_dictionary = config["hierarchicalDictionary"] if "hierarchicalDictionary" in config else False

            self.phrases = ZscalerCollection.form_list(config["phrases"] if "phrases" in config else [], DictionaryPhrases)

            self.patterns = ZscalerCollection.form_list(config["patterns"] if "patterns" in config else [], DictionaryPattern)

        else:
            self.id = None
            self.name = None
            self.description = None
            self.confidence_threshold = None
            self.phrases = []
            self.patterns = []
            self.custom_phrase_match_type = None
            self.name_l10n_tag = False
            self.dictionary_type = None
            self.exact_data_match_details = []
            self.idm_profile_match_accuracy_details = []
            self.proximity = 0
            self.predefined_phrases = []
            self.ignore_exact_match_idm_dict = False
            self.include_bin_numbers = False
            self.predefined_clone = False
            self.threshold_allowed = False
            self.hierarchical_identifiers = []
            self.proximity_enabled_for_custom_dictionary = False
            self.include_ssn_numbers = False
            self.unicode_phrase_matching_enabled = False
            self.dictionary_cloning_enabled = False
            self.confidence_level_for_predefined_dict = None
            self.custom = False
            self.proximity_length_enabled = False
            self.custom_phrase_supported = False
            self.hierarchical_dictionary = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "confidenceThreshold": self.confidence_threshold,
            "phrases": self.phrases,
            "patterns": self.patterns,
            "customPhraseMatchType": self.custom_phrase_match_type,
            "nameL10nTag": self.name_l10n_tag,
            "dictionaryType": self.dictionary_type,
            "exactDataMatchDetails": self.exact_data_match_details,
            "idmProfileMatchAccuracyDetails": self.idm_profile_match_accuracy_details,
            "proximity": self.proximity,
            "predefinedPhrases": self.predefined_phrases,
            "ignoreExactMatchIdmDict": self.ignore_exact_match_idm_dict,
            "includeBinNumbers": self.include_bin_numbers,
            "predefinedClone": self.predefined_clone,
            "thresholdAllowed": self.threshold_allowed,
            "hierarchicalIdentifiers": self.hierarchical_identifiers,
            "proximityEnabledForCustomDictionary": self.proximity_enabled_for_custom_dictionary,
            "includeSsnNumbers": self.include_ssn_numbers,
            "unicodePhraseMatchingEnabled": self.unicode_phrase_matching_enabled,
            "dictionaryCloningEnabled": self.dictionary_cloning_enabled,
            "confidenceLevelForPredefinedDict": self.confidence_level_for_predefined_dict,
            "custom": self.custom,
            "proximityLengthEnabled": self.proximity_length_enabled,
            "customPhraseSupported": self.custom_phrase_supported,
            "hierarchicalDictionary": self.hierarchical_dictionary,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DictionaryPhrases(ZscalerObject):
    """
    A class for DictionaryPhrases objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the DictionaryPhrases model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.action = config["action"] if "action" in config else None
            self.phrase = config["phrase"] if "phrase" in config else None

        else:
            self.action = None
            self.phrase = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "phrase": self.phrase,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DictionaryPattern(ZscalerObject):
    """
    A class for DictionaryPattern objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the DictionaryPattern model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.action = config["action"] if "action" in config else None
            self.pattern = config["pattern"] if "pattern" in config else None

        else:
            self.action = None
            self.pattern = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "action": self.action,
            "pattern": self.pattern,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DLPPatternValidation(ZscalerObject):
    """
    A class representing the response from validating a DLP Pattern.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.status = config["status"] if "status" in config else None
            self.err_position = config["errPosition"] if "errPosition" in config else None
            self.err_msg = config["errMsg"] if "errMsg" in config else None
            self.err_parameter = config["errParameter"] if "errParameter" in config else None
            self.err_suggestion = config["errSuggestion"] if "errSuggestion" in config else None
            self.id_list = config["idList"] if "idList" in config else []
        else:
            self.status = None
            self.err_position = None
            self.err_msg = None
            self.err_parameter = None
            self.err_suggestion = None
            self.id_list = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
            "errPosition": self.err_position,
            "errMsg": self.err_msg,
            "errParameter": self.err_parameter,
            "errSuggestion": self.err_suggestion,
            "idList": self.id_list,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
