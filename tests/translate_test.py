from pollination.honeybee_display.translate import ModelToVis
from queenbee.plugin.function import Function


def test_model_to_vis():
    function = ModelToVis().queenbee
    assert function.name == 'model-to-vis'
    assert isinstance(function, Function)
