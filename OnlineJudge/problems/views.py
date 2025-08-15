from django.shortcuts import render, get_object_or_404
from authentication.decorators import session_check_proceed
from django.conf import settings
from pathlib import Path
import uuid, subprocess, re, os
from problems.forms import CompilerForm
from problems.models import Submissions, Questions


# Create your views here.

@session_check_proceed
def run_submit_view(request, problem_id):
    problem = get_object_or_404(Questions, id=problem_id)
    questionkey = problem.questionkey

    submission = None           # DB Object
    status = ""
    output = "Output is displayed here."

    if request.method == 'POST':
        form = CompilerForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            language = cleaned_data['language']
            code = cleaned_data['code']
            input = cleaned_data['input']

            action = request.POST.get('action')
            if action == 'run':
                # Generate a unique prefix for our files
                filekey = f"user{request.user.id}_problem{problem.id}"
                _ , output, _ = execute_code(language, code, input, filekey)
            
            elif action == 'submit':
                status, output, filekey = judge_code(language, code, questionkey)
                # Save in DB
                submission = Submissions.objects.create(
                    user=request.user,
                    problem=problem,
                    language=language,
                    status=status,
                    filekey=filekey
                )
    else:
        form = CompilerForm()           # Initiliaze blank forms only for GET

    sample_tests = problem.test_cases.filter(is_sample=True).values('input', 'expected_output')
    context = {
        'form': form,
        'problem': problem,
        'status': status,
        'submission': submission,
        'output': output,
        'sample_tests': sample_tests,
    }
    return render(request, 'judge.html', context)



def execute_code(language, code, input, filekey):

    # Base submissions directory
    submissions_dir = Path(settings.BASE_DIR) / "submissions"
    # Subdirectories
    codes_dir = submissions_dir / "codes"
    inputs_dir = submissions_dir / "inputs"
    outputs_dir = submissions_dir / "outputs"

    # Define file paths
    code_file_path = codes_dir / f"{filekey}.{language.extension}"
    input_file_path = inputs_dir / f"{filekey}.txt"
    output_file_path = outputs_dir / f"{filekey}.txt"

    # Write the code and input to their respective files
    with open(code_file_path, "w") as code_file:
        code_file.write(code)
    with open(input_file_path, "w") as input_file:
        input_file.write(input)

    output = ""
    temp_java_path = None
    classname = None

    try:
        if language.extension == "java":     
            # Find the public class name 
            classname = detect_java_classname(code) 
            
            temp_java_path = codes_dir / f"{classname}.java"   # Java requires file name = public class name
            temp_java_path.write_text(code)                    # Create a temp symlink or copy for compilation

            # Compile
            command= ["javac", str(temp_java_path)]
            compile = subprocess.run(command, capture_output=True, text=True)
            if compile.returncode != 0:
                status = detect_error(compile.stderr, "java")
                return status, compile.stderr, filekey
            
            command = ["java", "-cp", str(codes_dir), classname]    # Command for run

        else:    
            executable_path = codes_dir / filekey
            command = language.command.format(source=str(code_file_path),executable=str(executable_path)).split()
            
            if '{executable}' in language.command:   #Compile for required languages
                # Compile
                compile = subprocess.run(command, capture_output=True, text=True)
                if compile.returncode != 0:
                    status = detect_error(compile.stderr, language.extension)
                    return status, compile.stderr, filekey
                
                command = [str(executable_path)]    # Command for run

        # Run
        with open(input_file_path, "r") as input_f, open(output_file_path, "w") as output_f:
            run = subprocess.run(
                command, stdin=input_f, stdout=output_f, stderr=subprocess.PIPE, text=True, timeout=2
            )
        if run.returncode == 0:
            status = "Accepted"
            with open(output_file_path, "r") as f:
                output = f.read()       
        else:
            status = detect_error(run.stderr, language.extension)
            output = run.stderr     

    except subprocess.TimeoutExpired:
        status = "Time Limit Exceeded"
        output = "Your code took too long to execute."
    except Exception as e:
        status = "Runtime Error"
        output = f"An unexpected error occurred: {str(e)}"
    finally:            # Delete java temp file
        if language.extension == "java" and temp_java_path:
                delete_temp_java_path(temp_java_path, codes_dir, classname)

    return status, output, filekey



def judge_code(language, code, questionkey): 
    temp_java_path = None
    classname = None

    try:
        try:
            question = Questions.objects.get(questionkey=questionkey)
        except Questions.DoesNotExist:
            return "System Error", "Question not found.", None
        time_limit = question.time_limit  

        # Base directory
        submissions_dir = Path(settings.BASE_DIR) / "submissions"
        testcases_dir = Path(settings.BASE_DIR) / "problems" / "testcases"
        # Subdirectories
        codes_dir = submissions_dir / "codes"
        test_inputs_dir = testcases_dir / "inputs"
        test_outputs_dir = testcases_dir / "outputs"

        # Generate a unique prefix for our files
        filekey = str(uuid.uuid4())

        # Code file 
        code_file_path = codes_dir / f"{filekey}.{language.extension}"
        with open(code_file_path, "w") as code_file:
            code_file.write(code)


        # Complile for neccessary programs
        if language.extension == "java":
            # Find the public class name 
            classname = detect_java_classname(code)

            temp_java_path = codes_dir / f"{classname}.java"   # Java requires file name = public class name
            temp_java_path.write_text(code)    

            # Compile
            command= ["javac", str(temp_java_path)]
            compile = subprocess.run(command, capture_output=True, text=True)
            if compile.returncode != 0:
                status = detect_error(compile.stderr, "java")
                return status, compile.stderr, filekey
            
            # Run
            command = ["java", "-cp", str(codes_dir), classname]

        else:
            executable_path = codes_dir / filekey
            command = language.command.format(source=str(code_file_path),executable=str(executable_path)).split()
            if '{executable}' in language.command:
                compile = subprocess.run(command, capture_output=True, text=True)
                if compile.returncode != 0:
                    status = detect_error(compile.stderr, language.extension)
                    return status, compile.stderr, filekey
                command = [str(executable_path)]

        #Read and check test cases
        try:
            input_file_path = test_inputs_dir / f"{questionkey}.txt"
            expected_output_file_path = test_outputs_dir / f"{questionkey}.txt" 

            with open(input_file_path, 'r') as f:
                test_inputs = [block.strip() for block in f.read().strip().split("\n\n") if block.strip()]

            with open(expected_output_file_path, 'r') as f:
                test_outputs = [block.strip() for block in f.read().strip().split("\n\n") if block.strip()]

            if not test_inputs or not test_outputs:
                return "System Error", "Test case files are empty.", filekey

            if len(test_inputs) != len(test_outputs):
                return "System Error", "Mismatch in number of test input and output blocks.", filekey

        except FileNotFoundError:
            return "System Error", "Main test case files not found.", filekey
        
        #Run code and check if all output, test_output match
        for i, (test_input, test_output) in enumerate(zip(test_inputs, test_outputs), 1):
            try:
                # Execute the code against a single test case
                run = subprocess.run(
                    command,input=test_input,capture_output=True,text=True,timeout=time_limit+1
                )
                if run.returncode != 0:
                    status = detect_error(run.stderr, language.extension)
                    return status, run.stderr, filekey

                user_output = run.stdout.strip()
                if user_output != test_output.strip():
                    output = (
                        f"Test Case #{i} Failed\n"
                        f"Your Output:\n----------\n{user_output}\n\n"
                        f"Expected Output:\n----------\n{test_output}"
                    )
                    return "Wrong Answer", output, filekey
                
            except subprocess.TimeoutExpired:
                status = "Time Limit Exceeded"
                output = f"Test Case #{i} took too long."
                return status, output, filekey

            except Exception as e:
                status = "Runtime Error"
                output = f"An unexpected error occurred: {e}"
                return status, output, filekey
            
        return "Accepted", "All test cases passed successfully!", filekey
    
    finally:            # Delete java temp file
        if language.extension == "java" and temp_java_path:
                delete_temp_java_path(temp_java_path, codes_dir, classname)




def detect_error(txt, language_extension):
    txt = txt.lower()

    if language_extension == "py":
        if "syntaxerror" in txt:
            return "Syntax Error"
        elif "indentationerror" in txt:
            return "Indentation Error"
        elif "nameerror" in txt:
            return "Name Error"
        elif "typeerror" in txt:
            return "Type Error"
        elif "valueerror" in txt:
            return "Value Error"
        return "Runtime Error"

    elif language_extension == "cpp":
        # GCC/Clang error patterns
        if "expected" in txt and ";" in txt:
            return "Syntax Error"
        elif "undeclared" in txt:
            return "Name Error"
        elif "no matching function" in txt:
            return "Type Error"
        elif "cannot convert" in txt:
            return "Type Error"
        return "Compilation Error"

    return "Runtime Error"



def detect_java_classname(code_str):
    match = re.search(r'public\s+class\s+([A-Za-z_][A-Za-z0-9_]*)', code_str)
    return match.group(1) if match else "Main"
def delete_temp_java_path(temp_java_path, codes_dir, classname):
    os.remove(temp_java_path)
    class_file = codes_dir / f"{classname}.class"
    if class_file.exists():
        os.remove(class_file)