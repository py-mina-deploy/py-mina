"""
Templates
"""


from py_mina.cli.template_generator import *


################################################################################
# Base
################################################################################


base_template = template_places_6.format(
    generate_head(),
    generate_settings('global'),
    generate_settings('connection'),
    generate_settings('application'),
    generate_settings('shared'),
    generate_tasks()
)


################################################################################
# Staged
################################################################################


def generate_staged_templates():
    return {
        'settings': generate_settings('global', staged=True),
        'tasks': template_places_3.format(
            generate_head(staged=True, import_subtasks=True), 
            generate_settings('shared', staged=True),
            generate_tasks(staged=True)
        ),
        'production': template_places_3.format(
            generate_head(staged=True),
            generate_settings('connection', staged='production'),
            generate_settings('application', staged='production'),
        ),
        'dev': template_places_3.format(
            generate_head(staged=True),
            generate_settings('connection', staged='dev'),
            generate_settings('application', staged='dev'),
        ),
    }
