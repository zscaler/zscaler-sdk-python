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


from box import Box

from zscaler.zia import ZIAClient


class AuditLogsAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def status(self) -> Box:
        """
        Get the status of a request for an audit log report.

        Returns:
            :obj:`Box`: Audit log report request status.

        Examples:
            >>> print(zia.audit_logs.status())

        """
        return self.rest.get("auditlogEntryReport")

    def create(self, start_time: str, end_time: str) -> int:
        """
        Creates an audit log report for the specified time period and saves it as a CSV file. The report
        includes audit information for every call made to the cloud service API during the specified time period.
        Creating a new audit log report will overwrite a previously-generated report.

        Args:
            start_time (str):
                The timestamp, in epoch, of the admin's last login.
            end_time (str):
                The timestamp, in epoch, of the admin's last logout.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.audit_logs.create(start_time='1627221600000',
            ...    end_time='1627271676622')

        """
        payload = {
            "startTime": start_time,
            "endTime": end_time,
        }
        return self.rest.post("auditlogEntryReport", json=payload, box=False).status_code

    def cancel(self) -> int:
        """
        Cancels the request to create an audit log report.

        Returns:
            :obj:`int`: The operation response code.

        Examples:
            >>> zia.audit_logs.cancel()

        """
        return self.rest.delete("auditlogEntryReport", box=False).status_code

    def get_report(self) -> str:
        """
        Returns the most recently created audit log report.

        Returns:
            :obj:`str`: String representation of CSV file.

        Examples:
            Write report to CSV file:

            >>> with open("audit_log.csv", "w+") as fh:
            ...    fh.write(zia.audit_logs.get_report())

        """
        return self.rest.get("auditlogEntryReport/download").text
