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

    color_visibility = Inputs.str(
        description='A switch to note whether the color-by geometry should be hidden '
        'or shown by default. Hiding the color-by geometry is useful when the primary '
        'purpose of the visualization is to display grid data or room/face attributes '
        'but it is still desirable to have the option to turn on the geometry.',
        default='hide', spec={'type': 'string', 'enum': ['hide', 'show']}
    )

    wireframe = Inputs.str(
        description='A switch to note whether a ContextGeometry dedicated to the '
        'Model Wireframe (in DisplayLineSegment3D) should be included in the '
        'output VisualizationSet.', default='wireframe',
        spec={'type': 'string', 'enum': ['wireframe', 'exclude-wireframe']}
    )

    room_attr = Inputs.str(
        description='An optional text string of an attribute that the Model '
        'Rooms have (eg. display_name), which will be used to construct a '
        'visualization of this attribute in the resulting VisualizationSet. '
        'Room attributes input here can have . that separates the nested attributes '
        'from one another. For example, properties.energy.program_type.', default=''
    )

    face_attr = Inputs.str(
        description='An optional text string of an attribute that the Model '
        'Faces have (eg. display_name), which will be used to construct a '
        'visualization of this attribute in the resulting VisualizationSet. '
        'Face attributes input here can have . that separates the nested attributes '
        'from one another. For example, properties.energy.construction.', default=''
    )

    attr_format = Inputs.str(
        description='A switch to note whether to note whether the input room-attr '
        'and face-attr should be expressed as a colored AnalysisGeometry '
        'or a ContextGeometry as text labels.', default='text',
        spec={'type': 'string', 'enum': ['text', 'color']}
    )

    grid_display_mode = Inputs.str(
        description='Text that dictates how the ContextGeometry for Model SensorGrids '
        'should display in the resulting visualization. The Default option '
        'will draw sensor points whenever there is no grid_data_path and will not '
        'draw them at all when grid data is provided, assuming the AnalysisGeometry of '
        'the grids is sufficient. Choose from: Default, Points, Wireframe, Surface, '
        'SurfaceWithEdges, None.', default='Default',
        spec={'type': 'string', 'enum': ['Default', 'Points', 'Wireframe' 'Surface',
                                         'SurfaceWithEdges', 'None']}
    )

    grid_visibility = Inputs.str(
        description='A switch to note whether the SensorGrid ContextGeometry should '
        'be hidden or shown by default.',
        default='hide', spec={'type': 'string', 'enum': ['hide', 'show']}
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

    grid_data_display_mode = Inputs.str(
        description='Text to set the display_mode of the AnalysisGeometry that is '
        'generated from the grid_data_path above. Note that this has no effect if '
        'there are no meshes associated with the model SensorGrids. Choose from: '
        'Surface, SurfaceWithEdges, Wireframe, Points', default='Surface',
        spec={'type': 'string',
              'enum': ['Surface', 'SurfaceWithEdges', 'Wireframe', 'Points']}
    )

    active_grid_data = Inputs.str(
        description='Optional text to specify the active data in the '
        'AnalysisGeometry. This should match the name of the sub-folder '
        'within the grid_data_path that should be active. If unspecified, the '
        'first data set in the grid_data_path with be active.', default=''
    )

    output_format = Inputs.str(
        description='Text for the output format of the resulting VisualizationSet '
        'File (.vsf). Choose from: vsf, pkl, vtkjs, html. Note that vsf refers to the '
        'JSON version of the VisualizationSet File.', default='vsf',
        spec={'type': 'string', 'enum': ['vsf', 'json', 'pkl', 'vtkjs', 'html']}
    )

    @command
    def translate_model_to_vis(self):
        return 'honeybee-display model-to-vis model.hbjson ' \
            '--color-by {{self.color_by}} --{{self.color_visibility}}-color-by ' \
            '--{{self.wireframe}} --{{self.attr_format}}-attr ' \
            '--room-attr "{{self.room_attr}}" --face-attr "{{self.face_attr}}" ' \
            '--grid-display-mode {{self.grid_display_mode}} ' \
            '--{{self.grid_visibility}}-grid --grid-data input_data ' \
            '--grid-data-display-mode {{self.grid_data_display_mode}} ' \
            '--active-grid-data "{{self.active_grid_data}}" ' \
            '--output-format {{self.output_format}} ' \
            '--output-file model_vis.{{self.output_format}}'

    output_file = Outputs.file(
        description='Output visualization file.',
        path='model_vis.{{self.output_format}}'
    )
