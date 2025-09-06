import subprocess
import sys

TEST_SCRIPTS = [
    "sb_queue_smoke_test.py",
    "sb_topic_smoke_test.py",
    "sb_topic_dynamic_smoke_test.py",
    "sb_pubsub_smoke_test.py",
    "sb_large_message_test.py",
    "sb_batch_test.py",
    "sb_deadletter_test.py",
    "sb_duplicate_test.py",
    "sb_concurrent_consumer_test.py",
    "sb_delayed_delivery_test.py"
]

def run_test(script):
    print(f"\n=== Running {script} ===")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    print(f"Exit code: {result.returncode}")
    return result.returncode

def main():
    failures = 0
    failed_tests = []
    for script in TEST_SCRIPTS:
        code = run_test(script)
        if code != 0:
            print(f"Test {script} FAILED.")
            failures += 1
            failed_tests.append(script)
        else:
            print(f"Test {script} PASSED.")
    print(f"\nSummary: {len(TEST_SCRIPTS) - failures} passed, {failures} failed.")
    if failed_tests:
        print("Failed tests:")
        for name in failed_tests:
            print(f"- {name}")
    sys.exit(failures)

if __name__ == "__main__":
    main()
