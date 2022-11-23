from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class ModelToVis(Function):
    """Translate a Honeybee Model to a visualization format.

    This can be either a VisualizationSet File (.vsf) in JSON or binary Pkl format
    or it can be a VTKJS file.
    """

    model = Inputs.file(
        description='Honeybee model in JSON or Pkl format.', path='model.hbjson',
        extensions=['hbjson', 'json', 'hbpkl', 'pkl']
    )

    color_by = Inputs.str(
        description='Text for the property that dictates the colors of '
        'the Model geometry. Choose from: type, boundary_condition, none. '
        'If none, only a wireframe of the Model will be generated, assuming the '
        '--exclude-wireframe option is not uses. None is useful when the primary '
        'purpose of the visualization is to display results in relation to the Model '
        'geometry or display some room_attr or face_attr as an AnalysisGeometry '
        'or Text labels.', default='type',
        spec={'type': 'string', 'enum': ['type', 'boundary_condition', 'none']}
    )

    wireframe = Inputs.str(
        description='A switch to note whether a ContextGeometry dedicated to the '
        'Model Wireframe (in DisplayLineSegment3D) should be included in the '
        'output VisualizationSet.', default='wireframe',
        spec={'type': 'string', 'enum': ['wireframe', 'exclude-wireframe']}
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
        path='input_data', optional=True
    )

    grid_display_mode = Inputs.str(
        description='Text to set the display_mode of the AnalysisGeometry that is '
        'generated from the grid_data_path above. Note that this has no effect if '
        'there are no meshes associated with the model SensorGrids. Choose from: '
        'Surface, SurfaceWithEdges, Wireframe, Points', default='Surface',
        spec={'type': 'string',
              'enum': ['Surface', 'SurfaceWithEdges', 'Wireframe', 'Points']}
    )

    output_format = Inputs.str(
        description='Text for the output format of the resulting VisualizationSet '
        'File (.vsf). Choose from: json, pkl, vtkjs.', default='vtkjs',
        spec={'type': 'string', 'enum': ['vtkjs', 'json', 'pkl']}
    )

    @command
    def model_modifiers_from_constructions(self):
        return 'honeybee-display model-to-vis model.hbjson ' \
            '--color-by {{self.color_by}} --{{self.wireframe}} ' \
            '--grid-data {{self.grid_data}} ' \
            '--grid-display-mode {{self.grid_display_mode}} ' \
            '--output-format {{self.output_format}} ' \
            '--output-file model_vis.vtkjs'

    new_model = Outputs.file(
        description='Output visualization file.', path='model.{{self.output_format}}'
    )
