from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from contest_app.models.problem import Problem
import subprocess, tempfile, json, os

@csrf_exempt
def run_code(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    try:
        data = json.loads(request.body)
        code = data.get("code", "").strip()
        problem_id = data.get("problem_id")

        if not problem_id:
            return JsonResponse({"error": "Missing problem_id in request."}, status=400)
        if not code:
            return JsonResponse({"error": "Code cannot be empty."}, status=400)

        problem = get_object_or_404(Problem, id=problem_id)

        # Sample test case
        test_cases = [
            {"input": str(problem.sample_input or ""), "expected": str(problem.sample_output or ""), "type": "Sample"}
        ]

        # Hidden test cases
        if problem.hidden_test_cases:
            try:
                hidden_cases = json.loads(problem.hidden_test_cases)
                if isinstance(hidden_cases, list):
                    for c in hidden_cases:
                        # Ensure input/output are strings
                        tc_input = str(c.get("input", "")).replace("\\n", "\n")
                        tc_output = str(c.get("output", "")).replace("\\n", "\n")
                        test_cases.append({
                            "input": tc_input,
                            "expected": tc_output,
                            "type": "Hidden"
                        })
                else:
                    return JsonResponse({"error": "Hidden test cases should be a list of dicts."}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Hidden test cases JSON is invalid."}, status=400)

        # Write user code to temp file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
            temp.write(code.encode("utf-8"))
            temp.flush()

        results = []
        all_passed = True

        for tc in test_cases:
            try:
                result = subprocess.run(
                    ["python", temp.name],
                    input=tc["input"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                user_output = result.stdout.strip()
                expected_output = tc["expected"].strip()

                if user_output == expected_output:
                    results.append({
                        "type": tc["type"],
                        "status": "Passed",
                        "input": tc["input"],
                        "output": user_output,
                    })
                else:
                    all_passed = False
                    results.append({
                        "type": tc["type"],
                        "status": "Failed",
                        "input": tc["input"],
                        "output": user_output,
                        "expected": expected_output,
                    })
            except subprocess.TimeoutExpired:
                all_passed = False
                results.append({
                    "type": tc["type"],
                    "status": "Timeout",
                    "input": tc["input"]
                })

        score = 1 if all_passed else 0
        os.remove(temp.name)

        return JsonResponse({"results": results, "score": score})

    except Problem.DoesNotExist:
        return JsonResponse({"error": "Problem not found."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON in request."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
