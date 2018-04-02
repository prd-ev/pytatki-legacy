from config import CONFIG

def test_config():
    assert CONFIG.is_ok() == True