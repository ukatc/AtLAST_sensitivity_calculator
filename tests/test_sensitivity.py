import pytest

def test_sensitivity():
    from atlast_sc.sensitivity import Sensitivity
    from atlast_sc.configs.config import Config
    from pathlib import Path

    CONFIG_PATH = Path(__file__).resolve().parents[0]
    
    config = Config.from_yaml(CONFIG_PATH / "test_user_inputs.yaml")

    calculator = Sensitivity(config)
    assert calculator.sensitivity(config.t_int).value == pytest.approx(0.007675, abs=0.00001)

def test_integration():
    from atlast_sc.sensitivity import Sensitivity
    from atlast_sc.configs.config import Config
    from pathlib import Path
    
    CONFIG_PATH = Path(__file__).resolve().parents[0]
    
    config = Config.from_yaml(CONFIG_PATH / "test_user_inputs.yaml")

    calculator = Sensitivity(config)
    assert calculator.t_integration(config.sensitivity).value == pytest.approx(0.5892, abs=0.0001)

def test_consistency():
    from atlast_sc.sensitivity import Sensitivity
    from atlast_sc.configs.config import Config
    import astropy.units as u
    from pathlib import Path
    
    CONFIG_PATH = Path(__file__).resolve().parents[0]
    
    config = Config.from_yaml(CONFIG_PATH / "test_user_inputs.yaml")

    calculator = Sensitivity(config)
    t = calculator.t_integration(config.sensitivity)
    assert calculator.sensitivity(t).to(u.mJy).value == pytest.approx(config.sensitivity.to(u.mJy).value, abs=0.01)