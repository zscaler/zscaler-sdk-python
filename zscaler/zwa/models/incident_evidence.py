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


class IncidentEvidence(ZscalerObject):
    """
    A class for IncidentEvidence objects.
    """

    def __init__(self, config=None):
        """
        Initialize the IncidentEvidence model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.file_name = config["fileName"] if "fileName" in config else None
            self.file_type = config["fileType"] if "fileType" in config else None
            self.additional_info = config["additionalInfo"] if "additionalInfo" in config else None
            self.evidence_u_r_l = config["evidenceURL"] if "evidenceURL" in config else None
        else:
            self.file_name = None
            self.file_type = None
            self.additional_info = None
            self.evidence_u_r_l = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "fileName": self.file_name,
            "fileType": self.file_type,
            "additionalInfo": self.additional_info,
            "evidenceURL": self.evidence_u_r_l,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
