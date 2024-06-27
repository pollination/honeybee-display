import inspect
from pollination_dsl.function import Function, script, Inputs, Outputs
from dataclasses import dataclass

from .scripts import abnt_nbr_15575_visualization


@dataclass
class AbntNbr15575DaylightVis(Function):
    """Translate a Honeybee Model to a visualization format for a ABNT NBR
    15575 daylight visualization.

    This can be either a VisualizationSet File (.vsf) in JSON or binary Pkl format
    or it can be a VTKJS file.
    """
    model = Inputs.file(
        description='Honeybee model in JSON or Pkl format.', path='model.hbjson',
        extensions=['hbjson', 'json', 'hbpkl', 'pkl']
    )

    grid_data = Inputs.folder(
        description='An optional path to a folder containing data that '
        'aligns with the SensorGrids in the model. Any sub folder within this path '
        'that contains a grids_into.json (and associated CSV files) will be '
        'converted to an AnalysisGeometry in the resulting VisualizationSet. '
        'If a vis_metadata.json file is found within this sub-folder, the '
        'information contained within it will be used to customize the '
        'AnalysisGeometry. Note that it is acceptable if data and '
        'grids_info.json exist in the root of this grid_data_path. Also '
        'note that this argument has no impact if honeybee-radiance is not '
        'installed and SensorGrids cannot be decoded.',
        path='input_data'
    )

    active_grid_data = Inputs.str(
        description='Optional text to specify the active data in the '
        'AnalysisGeometry. This should match the name of the sub-folder '
        'within the grid_data_path that should be active. If unspecified, the '
        'first data set in the grid_data_path with be active.', default='4_930AM'
    )

    center_points = Inputs.file(
        description='A JSON file with Ladybug Point3D objects to be visualized. '
        'These will be displayed as DisplaySphere.',
        path='center_points.json', optional=True)
    
    point_radius = Inputs.float(
        description='Radius of the spheres at the center points.',
        default=0.05, spec={'type': 'number', 'minimum': 0.01}
    )

    output_format = Inputs.str(
        description='Text for the output format of the resulting VisualizationSet '
        'File (.vsf). Choose from: vsf, pkl, vtkjs, html. Note that vsf refers to the '
        'JSON version of the VisualizationSet File.', default='vsf',
        spec={'type': 'string', 'enum': ['vsf', 'json', 'pkl', 'vtkjs', 'html']}
    )

    @script
    def run_create_visualization(self):
        return inspect.getsource(abnt_nbr_15575_visualization)

    output_file = Outputs.file(path='visualization.{{self.output_format}}')
