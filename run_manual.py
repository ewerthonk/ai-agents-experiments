import langwatch
try:
    with langwatch.trace(name="TestTrace") as trace:
        print("Trace created!")
        trace.update(input="test input")
        trace.update(output="test output")
        print("Trace updated!")
except Exception as e:
    print(f"Error: {e}")
