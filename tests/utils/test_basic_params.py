from utils.basic_params import duration


def test_duration():
    assert duration(4229, 8867) == "01:17:18"
