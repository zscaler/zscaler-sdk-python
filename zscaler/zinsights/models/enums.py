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

from enum import Enum


class ActionStatus(str, Enum):
    """Supported action types for filtering."""
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"


class Aggregation(str, Enum):
    """Aggregation types for data queries."""
    SUM = "SUM"
    COUNT = "COUNT"
    AVG = "AVG"


class ApplicationCategoryType(str, Enum):
    """Supported application category types."""
    FILE = "FILE"


class CasbDocType(str, Enum):
    """Supported document types for CASB incidents."""
    ANY = "ANY"
    NONE = "NONE"
    DOC_TYPE_DMV = "DOC_TYPE_DMV"
    DOC_TYPE_FINANCIAL = "DOC_TYPE_FINANCIAL"
    DOC_TYPE_TECHNICAL = "DOC_TYPE_TECHNICAL"
    DOC_TYPE_MEDICAL = "DOC_TYPE_MEDICAL"
    DOC_TYPE_REAL_ESTATE = "DOC_TYPE_REAL_ESTATE"
    DOC_TYPE_HR = "DOC_TYPE_HR"
    DOC_TYPE_INVOICE = "DOC_TYPE_INVOICE"
    DOC_TYPE_INSURANCE = "DOC_TYPE_INSURANCE"
    DOC_TYPE_TAX = "DOC_TYPE_TAX"
    DOC_TYPE_LEGAL = "DOC_TYPE_LEGAL"
    DOC_TYPE_COURT_FORM = "DOC_TYPE_COURT_FORM"
    DOC_TYPE_CORPORATE_LEGAL = "DOC_TYPE_CORPORATE_LEGAL"
    DOC_TYPE_IMMIGRATION = "DOC_TYPE_IMMIGRATION"
    DOC_TYPE_SOURCE_CODE = "DOC_TYPE_SOURCE_CODE"
    DOC_TYPE_ID_CARD = "DOC_TYPE_ID_CARD"
    DOC_TYPE_SATELLITE_DATA = "DOC_TYPE_SATELLITE_DATA"
    DOC_TYPE_SCHEMATIC_DATA = "DOC_TYPE_SCHEMATIC_DATA"
    DOC_TYPE_MEDICAL_IMAGING = "DOC_TYPE_MEDICAL_IMAGING"
    DOC_TYPE_OTHERS_TEXT = "DOC_TYPE_OTHERS_TEXT"
    DOC_TYPE_NO_TEXT = "DOC_TYPE_NO_TEXT"
    DOC_TYPE_CREDIT_CARD_IMAGE = "DOC_TYPE_CREDIT_CARD_IMAGE"
    DOC_TYPE_UNKNOWN = "DOC_TYPE_UNKNOWN"


class CasbIncidentType(str, Enum):
    """Supported CASB incident types."""
    DLP = "DLP"
    MALWARE = "MALWARE"


class DlpEngineFilter(str, Enum):
    """Supported DLP engines for filtering."""
    ANY = "ANY"
    NONE = "NONE"
    HIPAA = "HIPAA"
    CYBER_BULLY_ENG = "CYBER_BULLY_ENG"
    GLBA = "GLBA"
    PCI = "PCI"
    OFFENSIVE_LANGUAGE = "OFFENSIVE_LANGUAGE"
    EXTERNAL = "EXTERNAL"


class IncidentsCategorizeBy(str, Enum):
    """Supported incident categorization fields."""
    LOCATION_ID = "LOCATION_ID"
    APP_ID = "APP_ID"
    USER_ID = "USER_ID"
    DEPARTMENT_ID = "DEPARTMENT_ID"
    URL_CATEGORY_ID = "URL_CATEGORY_ID"
    THREAT_CATEGORY_ID = "THREAT_CATEGORY_ID"
    SOURCE_COUNTRY = "SOURCE_COUNTRY"
    DESTINATION_COUNTRY = "DESTINATION_COUNTRY"
    TIME_STAMP = "TIME_STAMP"


class IncidentsGroupBy(str, Enum):
    """Supported incident grouping fields."""
    THREAT_CATEGORY_ID = "THREAT_CATEGORY_ID"
    APP_ID = "APP_ID"
    TIME = "TIME"
    USER_ID = "USER_ID"
    SRC_COUNTRY = "SRC_COUNTRY"


class IncidentsWithIdGroupBy(str, Enum):
    """Supported incident grouping fields with IDs."""
    LOCATION_ID = "LOCATION_ID"


class RecordType(str, Enum):
    """Supported record types."""
    EMAILDLP_DLP_INCIDENT = "EMAILDLP_DLP_INCIDENT"


class SortOrder(str, Enum):
    """Sort order for query results."""
    ASC = "ASC"
    DESC = "DESC"


class ThreatClass(str, Enum):
    """Supported threat class values."""
    VIRUS_SPYWARE = "VIRUS_SPYWARE"
    ADVANCED = "ADVANCED"
    BEHAVIORAL_ANALYSIS = "BEHAVIORAL_ANALYSIS"


class ThreatClassSummarizeBy(str, Enum):
    """Threat class summarization options."""
    LOCATION = "LOCATION"
    USER = "USER"


class TrendInterval(str, Enum):
    """Supported trend intervals for time-series data."""
    DAY = "DAY"
    HOUR = "HOUR"


class WebTrafficUnits(str, Enum):
    """Supported web traffic measurement units."""
    TRANSACTIONS = "TRANSACTIONS"
    BYTES = "BYTES"


# Export all enums
__all__ = [
    "ActionStatus",
    "Aggregation",
    "ApplicationCategoryType",
    "CasbDocType",
    "CasbIncidentType",
    "DlpEngineFilter",
    "IncidentsCategorizeBy",
    "IncidentsGroupBy",
    "IncidentsWithIdGroupBy",
    "RecordType",
    "SortOrder",
    "ThreatClass",
    "ThreatClassSummarizeBy",
    "TrendInterval",
    "WebTrafficUnits",
]
