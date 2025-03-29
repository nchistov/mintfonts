from subprocess import check_output


def get_system_fonts() -> [str]:
    output = check_output(['fc-list'])
    
    return [s.decode('utf-8').split(':')[0] for s in output.splitlines()]


def get_font_metadata(path: str) -> {str: str}:
    family = check_output(['fc-query', path, '--format=%{family}']).decode('utf-8')
    style = check_output(['fc-query', path, '--format=%{style}']).decode('utf-8')

    return {'family': family, 'style': style}
