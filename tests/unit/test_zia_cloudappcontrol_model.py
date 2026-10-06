"""
Testing ZIA Cloud App Control rule model parsing
"""

from zscaler.zia.models.cloudappcontrol import CloudApplicationControl


def test_cloud_app_risk_profile_object_is_parsed():
    rule = CloudApplicationControl(
        {"id": 1, "name": "rule-a", "cloudAppRiskProfile": {"id": 2724, "name": "Unsanctioned Risk 5"}}
    )

    assert rule.cloud_app_risk_profile.id == 2724
    assert rule.cloud_app_risk_profile.name == "Unsanctioned Risk 5"
    sent = rule.request_format()["cloudAppRiskProfile"]
    assert (sent["id"], sent["name"]) == (2724, "Unsanctioned Risk 5")


def test_cloud_app_risk_profile_absent():
    rule = CloudApplicationControl({"id": 1, "name": "rule-a"})

    assert rule.cloud_app_risk_profile is None
    assert rule.request_format()["cloudAppRiskProfile"] is None
