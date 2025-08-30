from django.conf import settings
from pathlib import Path
import uuid

def save_testcases(question_instance, input_file=None, output_file=None):
    try:
        # If the question doesn't have a key, generate one. This is crucial.
        if not question_instance.questionkey:
            question_instance.questionkey = str(uuid.uuid4())

        # Define the paths where the test case files will be stored
        testcases_dir = Path(settings.BASE_DIR) / "problems" / "testcases"
        inputs_dir = testcases_dir / "inputs"
        outputs_dir = testcases_dir / "outputs"
        inputs_dir.mkdir(parents=True, exist_ok=True)
        outputs_dir.mkdir(parents=True, exist_ok=True)

        # Save the uploaded input file with the questionkey as its name
        if input_file:
            input_path = inputs_dir / f"{question_instance.questionkey}.txt"
            with open(input_path, 'wb+') as destination:
                for chunk in input_file.chunks():
                    destination.write(chunk)
        
        # Save the uploaded output file with the questionkey as its name
        if output_file:
            output_path = outputs_dir / f"{question_instance.questionkey}.txt"
            with open(output_path, 'wb+') as destination:
                for chunk in output_file.chunks():
                    destination.write(chunk)
        
        # Save the question instance to persist the questionkey if it was new
        question_instance.save()
        return True

    except Exception as e:
        # In a real application, you'd want to log this error
        print(f"Error saving question files: {e}")
        return False
