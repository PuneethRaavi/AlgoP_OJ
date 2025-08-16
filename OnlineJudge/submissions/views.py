from django.shortcuts import render, get_object_or_404
from django.conf import settings
from pathlib import Path
from submissions.models import Submissions
from authentication.decorators import session_check_proceed

# Create your views here.

@session_check_proceed
def submission_detail_view(request, filekey):
    submission = get_object_or_404(
        Submissions.objects.select_related('problem', 'language', 'problem__author'),
        filekey=filekey,
        user=request.user
    )

    sample_tests = submission.problem.test_cases.filter(is_sample=True).values('input', 'expected_output')

    code = "Error: The code for this submission could not be retrieved."
    try:
        # Construct the path to the stored code file
        code_file_path = (
            Path(settings.BASE_DIR) / "submissions" / "files" / "codes" /
            f"{submission.filekey}.{submission.language.extension}"
        )

        if code_file_path.exists():
            with open(code_file_path, 'r') as f:
                code = f.read()
    except Exception as e:
        print(f"Error reading submission file for filekey {filekey}: {e}")

    context = {
        'submission': submission,
        'problem': submission.problem,
        'code': code,
        'sample_tests': sample_tests,
        'user': request.user
    }
    return render(request, 'submissiondetail.html', context)