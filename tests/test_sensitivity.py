import pytest

def test_sensitivity():
    from src.backend.sensitivity import Sensitivity
    from src.configs.config import Config
    from astropy import constants
    import astropy.units as u
    from pathlib import Path

    CONFIG_PATH = Path(__file__).resolve().parents[0]
    
    config = Config.from_yaml(CONFIG_PATH / "test_user_inputs.yaml")

    calculator = Sensitivity(config)
    assert calculator.sensitivity(config.t_int).value == pytest.approx(0.00724, abs=0.00001)

def test_integration():
    from src.backend.sensitivity import Sensitivity
    from src.configs.config import Config
    from astropy import constants
    import astropy.units as u
    from pathlib import Path
    
    CONFIG_PATH = Path(__file__).resolve().parents[0]
    
    config = Config.from_yaml(CONFIG_PATH / "test_user_inputs.yaml")

    calculator = Sensitivity(config)
    assert calculator.t_integration(config.sensitivity).value == pytest.approx(0.5246, abs=0.0001)

def test_consistency():
    from src.backend.sensitivity import Sensitivity
    from src.configs.config import Config
    from astropy import constants
    import astropy.units as u
    from pathlib import Path
    
    CONFIG_PATH = Path(__file__).resolve().parents[0]
    
    config = Config.from_yaml(CONFIG_PATH / "test_user_inputs.yaml")

    calculator = Sensitivity(config)
    t = calculator.t_integration(config.sensitivity)
    assert calculator.sensitivity(t).to(u.mJy).value == pytest.approx(config.sensitivity.to(u.mJy).value, abs=0.01)