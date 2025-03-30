from subprocess import check_output


def get_system_fonts() -> [str]:
    output = check_output(['fc-list'])
    
    return [s.decode('utf-8').split(':')[0] for s in output.splitlines()]


def get_font_metadata(path: str, fileds: [str]) -> {str: str}:
    return {field: check_output(['fc-query', path, '--format=%{' + field + '}']).decode('utf-8') for field in fileds}
