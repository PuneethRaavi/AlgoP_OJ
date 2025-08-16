from django.apps import AppConfig
from pathlib import Path
from django.conf import settings


class CompilerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'problems'

    def ready(self):
        # Define paths for our execution/submisssions
        submissions_dir = Path(settings.BASE_DIR) / "submissions" / "files"
        testcases_dir = Path(settings.BASE_DIR) / "problems" / "testcases"

        # Subdirectories
        codes_dir = submissions_dir / "codes"
        inputs_dir = submissions_dir / "inputs"
        outputs_dir = submissions_dir / "outputs"
        test_inputs_dir = testcases_dir / "inputs"
        test_outputs_dir = testcases_dir / "outputs"

        # Create them if missing
        for directory in [codes_dir, inputs_dir, outputs_dir, test_inputs_dir, test_outputs_dir]:
            directory.mkdir(parents=True, exist_ok=True)