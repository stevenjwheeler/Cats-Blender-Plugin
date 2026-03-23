
import sys
from unittest.mock import MagicMock

# Mock bpy
bpy = MagicMock()
sys.modules['bpy'] = bpy

# Mock translations
def t(key):
    return f"Translated: {key}"

# The function to test (copied from __init__.py)
def check_unsupported_blender_versions():
    # Don't allow Blender versions older than 5.1
    if bpy.app.version < (5, 1):
        # unregister() # Skipping unregister for mock test
        sys.tracebacklimit = 0
        raise ImportError(t('Main.error.29unsupportedVersion'))
     
    # Don't allow 5.2+
    if bpy.app.version >= (5, 2):
        sys.tracebacklimit = 0
        raise ImportError(t('Main.error.40unsupportedVersion'))

def test_version(version):
    bpy.app.version = version
    print(f"Testing version: {version}")
    try:
        check_unsupported_blender_versions()
        print(f"  Result: Allowed")
    except ImportError as e:
        print(f"  Result: Blocked - {e}")

if __name__ == "__main__":
    test_version((4, 2, 0)) # Should be blocked
    test_version((5, 0, 0)) # Should be blocked
    test_version((5, 1, 0)) # Should be allowed
    test_version((5, 1, 1)) # Should be allowed
    test_version((5, 2, 0)) # Should be blocked
