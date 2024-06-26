from pollination.honeybee_display.abnt import AbntNbr15575DaylightVis
from queenbee.plugin.function import Function


def test_abnt_nbr_15575_daylight_vis():
    function = AbntNbr15575DaylightVis().queenbee
    assert function.name == 'abnt-nbr15575-daylight-vis'
    assert isinstance(function, Function)
