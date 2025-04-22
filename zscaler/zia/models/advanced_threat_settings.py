# flake8: noqa
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


class AdvancedThreatProtectionSettings(ZscalerObject):
    """
    A class for AdvancedThreatProtectionSettings objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AdvancedThreatProtectionSettings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.risk_tolerance = config["riskTolerance"] if "riskTolerance" in config else None
            self.risk_tolerance_capture = config["riskToleranceCapture"] if "riskToleranceCapture" in config else None
            self.cmd_ctl_server_blocked = config["cmdCtlServerBlocked"] if "cmdCtlServerBlocked" in config else None
            self.cmd_ctl_server_capture = config["cmdCtlServerCapture"] if "cmdCtlServerCapture" in config else None
            self.cmd_ctl_traffic_blocked = config["cmdCtlTrafficBlocked"] if "cmdCtlTrafficBlocked" in config else None
            self.cmd_ctl_traffic_capture = config["cmdCtlTrafficCapture"] if "cmdCtlTrafficCapture" in config else None
            self.malware_sites_blocked = config["malwareSitesBlocked"] if "malwareSitesBlocked" in config else None
            self.malware_sites_capture = config["malwareSitesCapture"] if "malwareSitesCapture" in config else None
            self.active_x_blocked = config["activeXBlocked"] if "activeXBlocked" in config else None
            self.active_x_capture = config["activeXCapture"] if "activeXCapture" in config else None
            self.browser_exploits_blocked = config["browserExploitsBlocked"] if "browserExploitsBlocked" in config else None
            self.browser_exploits_capture = config["browserExploitsCapture"] if "browserExploitsCapture" in config else None
            self.file_format_vunerabilites_blocked = (
                config["fileFormatVunerabilitesBlocked"] if "fileFormatVunerabilitesBlocked" in config else None
            )
            self.file_format_vunerabilites_capture = (
                config["fileFormatVunerabilitesCapture"] if "fileFormatVunerabilitesCapture" in config else None
            )
            self.known_phishing_sites_blocked = (
                config["knownPhishingSitesBlocked"] if "knownPhishingSitesBlocked" in config else None
            )
            self.known_phishing_sites_capture = (
                config["knownPhishingSitesCapture"] if "knownPhishingSitesCapture" in config else None
            )
            self.suspected_phishing_sites_blocked = (
                config["suspectedPhishingSitesBlocked"] if "suspectedPhishingSitesBlocked" in config else None
            )
            self.suspected_phishing_sites_capture = (
                config["suspectedPhishingSitesCapture"] if "suspectedPhishingSitesCapture" in config else None
            )
            self.suspect_adware_spyware_sites_blocked = (
                config["suspectAdwareSpywareSitesBlocked"] if "suspectAdwareSpywareSitesBlocked" in config else None
            )
            self.suspect_adware_spyware_sites_capture = (
                config["suspectAdwareSpywareSitesCapture"] if "suspectAdwareSpywareSitesCapture" in config else None
            )
            self.webspam_blocked = config["webspamBlocked"] if "webspamBlocked" in config else None
            self.webspam_capture = config["webspamCapture"] if "webspamCapture" in config else None
            self.irc_tunnelling_blocked = config["ircTunnellingBlocked"] if "ircTunnellingBlocked" in config else None
            self.irc_tunnelling_capture = config["ircTunnellingCapture"] if "ircTunnellingCapture" in config else None
            self.anonymizer_blocked = config["anonymizerBlocked"] if "anonymizerBlocked" in config else None
            self.anonymizer_capture = config["anonymizerCapture"] if "anonymizerCapture" in config else None
            self.cookie_stealing_blocked = config["cookieStealingBlocked"] if "cookieStealingBlocked" in config else None
            self.cookie_stealing_pcap_enabled = (
                config["cookieStealingPCAPEnabled"] if "cookieStealingPCAPEnabled" in config else None
            )
            self.potential_malicious_requests_blocked = (
                config["potentialMaliciousRequestsBlocked"] if "potentialMaliciousRequestsBlocked" in config else None
            )
            self.potential_malicious_requests_capture = (
                config["potentialMaliciousRequestsCapture"] if "potentialMaliciousRequestsCapture" in config else None
            )
            self.blocked_countries = ZscalerCollection.form_list(
                config["blockedCountries"] if "blockedCountries" in config else [], str
            )
            self.block_countries_capture = config["blockCountriesCapture"] if "blockCountriesCapture" in config else None
            self.bit_torrent_blocked = config["bitTorrentBlocked"] if "bitTorrentBlocked" in config else None
            self.bit_torrent_capture = config["bitTorrentCapture"] if "bitTorrentCapture" in config else None
            self.tor_blocked = config["torBlocked"] if "torBlocked" in config else None
            self.tor_capture = config["torCapture"] if "torCapture" in config else None
            self.google_talk_blocked = config["googleTalkBlocked"] if "googleTalkBlocked" in config else None
            self.google_talk_capture = config["googleTalkCapture"] if "googleTalkCapture" in config else None
            self.ssh_tunnelling_blocked = config["sshTunnellingBlocked"] if "sshTunnellingBlocked" in config else None
            self.ssh_tunnelling_capture = config["sshTunnellingCapture"] if "sshTunnellingCapture" in config else None
            self.crypto_mining_blocked = config["cryptoMiningBlocked"] if "cryptoMiningBlocked" in config else None
            self.crypto_mining_capture = config["cryptoMiningCapture"] if "cryptoMiningCapture" in config else None
            self.ad_spyware_sites_blocked = config["adSpywareSitesBlocked"] if "adSpywareSitesBlocked" in config else None
            self.ad_spyware_sites_capture = config["adSpywareSitesCapture"] if "adSpywareSitesCapture" in config else None
            self.dga_domains_blocked = config["dgaDomainsBlocked"] if "dgaDomainsBlocked" in config else None
            self.alert_for_unknown_or_suspicious_c2_traffic = (
                config["alertForUnknownOrSuspiciousC2Traffic"] if "alertForUnknownOrSuspiciousC2Traffic" in config else None
            )
            self.dga_domains_capture = config["dgaDomainsCapture"] if "dgaDomainsCapture" in config else None
            self.malicious_urls_capture = config["maliciousUrlsCapture"] if "maliciousUrlsCapture" in config else None
        else:
            self.risk_tolerance = None
            self.risk_tolerance_capture = None
            self.cmd_ctl_server_blocked = None
            self.cmd_ctl_server_capture = None
            self.cmd_ctl_traffic_blocked = None
            self.cmd_ctl_traffic_capture = None
            self.malware_sites_blocked = None
            self.malware_sites_capture = None
            self.active_x_blocked = None
            self.active_x_capture = None
            self.browser_exploits_blocked = None
            self.browser_exploits_capture = None
            self.file_format_vunerabilites_blocked = None
            self.file_format_vunerabilites_capture = None
            self.known_phishing_sites_blocked = None
            self.known_phishing_sites_capture = None
            self.suspected_phishing_sites_blocked = None
            self.suspected_phishing_sites_capture = None
            self.suspect_adware_spyware_sites_blocked = None
            self.suspect_adware_spyware_sites_capture = None
            self.webspam_blocked = None
            self.webspam_capture = None
            self.irc_tunnelling_blocked = None
            self.irc_tunnelling_capture = None
            self.anonymizer_blocked = None
            self.anonymizer_capture = None
            self.cookie_stealing_blocked = None
            self.cookie_stealing_pcap_enabled = None
            self.potential_malicious_requests_blocked = None
            self.potential_malicious_requests_capture = None
            self.blocked_countries = []
            self.block_countries_capture = None
            self.bit_torrent_blocked = None
            self.bit_torrent_capture = None
            self.tor_blocked = None
            self.tor_capture = None
            self.google_talk_blocked = None
            self.google_talk_capture = None
            self.ssh_tunnelling_blocked = None
            self.ssh_tunnelling_capture = None
            self.crypto_mining_blocked = None
            self.crypto_mining_capture = None
            self.ad_spyware_sites_blocked = None
            self.ad_spyware_sites_capture = None
            self.dga_domains_blocked = None
            self.alert_for_unknown_or_suspicious_c2_traffic = None
            self.dga_domains_capture = None
            self.malicious_urls_capture = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "riskTolerance": self.risk_tolerance,
            "riskToleranceCapture": self.risk_tolerance_capture,
            "cmdCtlServerBlocked": self.cmd_ctl_server_blocked,
            "cmdCtlServerCapture": self.cmd_ctl_server_capture,
            "cmdCtlTrafficBlocked": self.cmd_ctl_traffic_blocked,
            "cmdCtlTrafficCapture": self.cmd_ctl_traffic_capture,
            "malwareSitesBlocked": self.malware_sites_blocked,
            "malwareSitesCapture": self.malware_sites_capture,
            "activeXBlocked": self.active_x_blocked,
            "activeXCapture": self.active_x_capture,
            "browserExploitsBlocked": self.browser_exploits_blocked,
            "browserExploitsCapture": self.browser_exploits_capture,
            "fileFormatVunerabilitesBlocked": self.file_format_vunerabilites_blocked,
            "fileFormatVunerabilitesCapture": self.file_format_vunerabilites_capture,
            "knownPhishingSitesBlocked": self.known_phishing_sites_blocked,
            "knownPhishingSitesCapture": self.known_phishing_sites_capture,
            "suspectedPhishingSitesBlocked": self.suspected_phishing_sites_blocked,
            "suspectedPhishingSitesCapture": self.suspected_phishing_sites_capture,
            "suspectAdwareSpywareSitesBlocked": self.suspect_adware_spyware_sites_blocked,
            "suspectAdwareSpywareSitesCapture": self.suspect_adware_spyware_sites_capture,
            "webspamBlocked": self.webspam_blocked,
            "webspamCapture": self.webspam_capture,
            "ircTunnellingBlocked": self.irc_tunnelling_blocked,
            "ircTunnellingCapture": self.irc_tunnelling_capture,
            "anonymizerBlocked": self.anonymizer_blocked,
            "anonymizerCapture": self.anonymizer_capture,
            "cookieStealingBlocked": self.cookie_stealing_blocked,
            "cookieStealingPCAPEnabled": self.cookie_stealing_pcap_enabled,
            "potentialMaliciousRequestsBlocked": self.potential_malicious_requests_blocked,
            "potentialMaliciousRequestsCapture": self.potential_malicious_requests_capture,
            "blockedCountries": self.blocked_countries,
            "blockCountriesCapture": self.block_countries_capture,
            "bitTorrentBlocked": self.bit_torrent_blocked,
            "bitTorrentCapture": self.bit_torrent_capture,
            "torBlocked": self.tor_blocked,
            "torCapture": self.tor_capture,
            "googleTalkBlocked": self.google_talk_blocked,
            "googleTalkCapture": self.google_talk_capture,
            "sshTunnellingBlocked": self.ssh_tunnelling_blocked,
            "sshTunnellingCapture": self.ssh_tunnelling_capture,
            "cryptoMiningBlocked": self.crypto_mining_blocked,
            "cryptoMiningCapture": self.crypto_mining_capture,
            "adSpywareSitesBlocked": self.ad_spyware_sites_blocked,
            "adSpywareSitesCapture": self.ad_spyware_sites_capture,
            "dgaDomainsBlocked": self.dga_domains_blocked,
            "alertForUnknownOrSuspiciousC2Traffic": self.alert_for_unknown_or_suspicious_c2_traffic,
            "dgaDomainsCapture": self.dga_domains_capture,
            "maliciousUrlsCapture": self.malicious_urls_capture,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
