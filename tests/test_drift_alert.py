from drift.alert import trigger_alert


def test_trigger_alert_no_exception_without_webhook() -> None:
    trigger_alert("drift exceeded")
