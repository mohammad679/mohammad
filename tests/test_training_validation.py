from training.validation import should_promote_model


def test_should_promote_model_pass() -> None:
    assert should_promote_model(f1_score_value=0.92, threshold=0.90)


def test_should_promote_model_fail() -> None:
    assert not should_promote_model(f1_score_value=0.89, threshold=0.90)
