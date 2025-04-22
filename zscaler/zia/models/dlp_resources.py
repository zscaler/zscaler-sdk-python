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


class DLPICAPServer(ZscalerObject):
    """
    A class representing DLP ICAP Server objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.url = config["url"] if "url" in config else None
            self.status = config["status"] if "status" in config else None
        else:
            self.id = None
            self.name = None
            self.url = None
            self.status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "status": self.status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DLPIDMProfile(ZscalerObject):
    """
    A class representing DLP IDM Profile objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.profile_id = config["profileId"] if "profileId" in config else None
            self.profile_name = config["profileName"] if "profileName" in config else None
            self.profile_type = config["profileType"] if "profileType" in config else None
            self.port = config["port"] if "port" in config else None
            self.schedule_type = config["scheduleType"] if "scheduleType" in config else None
            self.schedule_day = config["scheduleDay"] if "scheduleDay" in config else None
            self.schedule_time = config["scheduleTime"] if "scheduleTime" in config else None
            self.schedule_disabled = config["scheduleDisabled"] if "scheduleDisabled" in config else False
            self.upload_status = config["uploadStatus"] if "uploadStatus" in config else None
            self.version = config["version"] if "version" in config else None
            self.idm_client = config["idmClient"] if "idmClient" in config else None
            self.volume_of_documents = config["volumeOfDocuments"] if "volumeOfDocuments" in config else None
            self.num_documents = config["numDocuments"] if "numDocuments" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
        else:
            self.profile_id = None
            self.profile_name = None
            self.profile_type = None
            self.port = None
            self.schedule_type = None
            self.schedule_day = None
            self.schedule_time = None
            self.schedule_disabled = False
            self.upload_status = None
            self.version = None
            self.idm_client = None
            self.volume_of_documents = None
            self.num_documents = None
            self.last_modified_time = None
            self.modified_by = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "profileId": self.profile_id,
            "profileName": self.profile_name,
            "profileType": self.profile_type,
            "port": self.port,
            "scheduleType": self.schedule_type,
            "scheduleDay": self.schedule_day,
            "scheduleTime": self.schedule_time,
            "scheduleDisabled": self.schedule_disabled,
            "uploadStatus": self.upload_status,
            "version": self.version,
            "idmClient": self.idm_client,
            "volumeOfDocuments": self.volume_of_documents,
            "numDocuments": self.num_documents,
            "lastModifiedTime": self.last_modified_time,
            "modifiedBy": self.modified_by,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DLPEDMSchema(ZscalerObject):
    """
    A class representing DLP EDM Schema objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.schema_id = config["schemaId"] if "schemaId" in config else None
            self.edm_client = config["edmClient"] if "edmClient" in config else None
            self.project_name = config["projectName"] if "projectName" in config else None
            self.revision = config["revision"] if "revision" in config else None
            self.filename = config["filename"] if "filename" in config else None
            self.original_filename = config["originalFileName"] if "originalFileName" in config else None
            self.file_upload_status = config["fileUploadStatus"] if "fileUploadStatus" in config else None
            self.schema_status = config["schemaStatus"] if "schemaStatus" in config else None
            self.orig_col_count = config["origColCount"] if "origColCount" in config else None
            self.last_modified_by = config["lastModifiedBy"] if "lastModifiedBy" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.created_by = config["createdBy"] if "createdBy" in config else None
            self.cells_used = config["cellsUsed"] if "cellsUsed" in config else None
            self.schema_active = config["schemaActive"] if "schemaActive" in config else None

            # Handling the tokenList using ZscalerCollection
            self.token_list = ZscalerCollection.form_list(config.get("tokenList", []), dict)

            self.schedule_present = config["schedulePresent"] if "schedulePresent" in config else False
        else:
            self.schema_id = None
            self.edm_client = None
            self.project_name = None
            self.revision = None
            self.filename = None
            self.original_filename = None
            self.file_upload_status = None
            self.schema_status = None
            self.orig_col_count = None
            self.last_modified_by = None
            self.last_modified_time = None
            self.created_by = None
            self.cells_used = None
            self.schema_active = None
            self.token_list = []
            self.schedule_present = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "schemaId": self.schema_id,
            "edmClient": self.edm_client,
            "projectName": self.project_name,
            "revision": self.revision,
            "filename": self.filename,
            "originalFileName": self.original_filename,
            "fileUploadStatus": self.file_upload_status,
            "schemaStatus": self.schema_status,
            "origColCount": self.orig_col_count,
            "lastModifiedBy": self.last_modified_by,
            "lastModifiedTime": self.last_modified_time,
            "createdBy": self.created_by,
            "cellsUsed": self.cells_used,
            "schemaActive": self.schema_active,
            "tokenList": self.token_list,
            "schedulePresent": self.schedule_present,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
