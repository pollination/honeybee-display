if __name__ == '__main__':
    from pathlib import Path
    import json
    import os
    import pickle
    import tempfile
    import uuid

    from honeybee.model import Model
    from ladybug_geometry.geometry3d import Point3D
    from ladybug.color import Color
    from ladybug_display.visualization import ContextGeometry, DisplayPoint3D

    # inputs
    hb_model = Model.from_hbjson('model.hbjson')
    grid_data_path = 'input_data'
    active_grid_data = '{{self.active_grid_data}}'
    center_points_file = Path('center_points.json')
    output_format = '{{self.output_format}}'

    # create base vis set
    vis_set = hb_model.to_vis_set(
        color_by=None, grid_data_path=grid_data_path,
        active_grid_data=active_grid_data)

    # add DisplayPoint3D if center_points.json exists
    if center_points_file.is_file():
        geo_objs = []
        with center_points_file.open('r') as f:
            center_points = json.load(f)
        for cp in center_points:
            lb_point3d = Point3D.from_dict(cp)
            display_point3d = DisplayPoint3D(geometry=lb_point3d, color=Color(0, 0, 0))
            geo_objs.append(display_point3d)
        cg = ContextGeometry('center-points', geo_objs)
        cg.display_name = 'Center Points'
        vis_set.add_geometry(cg)

    output_file = Path(f'visualization.{output_format}')
    output_format = output_format.lower()
    if output_format in ('vsf', 'json'):
        with output_file.open('w') as f:
            json.dump(vis_set.to_dict(), f)
    elif output_format == 'pkl':
        if output_file.name != '<stdout>':
            out_folder, out_file = os.path.split(output_file.name)
            vis_set.to_pkl(out_file, out_folder)
        else:
            with output_file.open('w') as f:
                pickle.dump(vis_set.to_dict(), f)
    elif output_format in ('vtkjs', 'html'):
        if output_file.name == '<stdout>':  # get a temporary file
            out_file = str(uuid.uuid4())[:6]
            out_folder = tempfile.gettempdir()
        else:
            out_folder, out_file = os.path.split(output_file.name)
            if out_file.endswith('.vtkjs'):
                out_file = out_file[:-6]
            elif out_file.endswith('.html'):
                out_file = out_file[:-5]
        try:
            if output_format == 'vtkjs':
                vis_set.to_vtkjs(output_folder=out_folder, file_name=out_file)
            if output_format == 'html':
                vis_set.to_html(output_folder=out_folder, file_name=out_file)
        except AttributeError as ae:
            raise AttributeError(
                'Ladybug-vtk must be installed in order to use --output-format '
                'vtkjs.\n{}'.format(ae))
        if output_file.name == '<stdout>':  # load file contents to stdout
            out_file_ext = out_file + '.' + output_format
            out_file_path = os.path.join(out_folder, out_file_ext)
            if output_format == 'html':
                with open(out_file_path, encoding='utf-8') as of:
                    f_contents = of.read()
            else:  # vtkjs can only be read as binary
                with open(out_file_path, 'rb') as of:
                    f_contents = of.read()
            with output_file.open('w') as f:
                output_file.write(f_contents)
