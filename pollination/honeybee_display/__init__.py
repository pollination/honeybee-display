"""Plugin for Pollination containing all honeybee extensions."""
from pollination_dsl.common import get_docker_image_from_dependency

# set the version for docker image dynamically based on honeybee-display version
# in dependencies
image_id = get_docker_image_from_dependency(
    __package__, 'honeybee-display', 'ladybugtools'
)

__pollination__ = {
    'config': {
        'docker': {
            'image': image_id,
            'workdir': '/home/ladybugbot/run'
        }
    }
}
