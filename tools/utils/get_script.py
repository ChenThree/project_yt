from .. import scripts


def get_script(analyze_type):
    """get specific script for different analyze type

    Args:
        analyze_type (int): analyze type to get script

    Raises:
        AttributeError: 'Invalid analyze type {analyze_type}'

    Returns:
        script
    """
    try:
        script = getattr(scripts, f'script_{analyze_type}')
    except Exception:
        raise AttributeError(f'Invalid analyze type: {analyze_type}')
    return script
