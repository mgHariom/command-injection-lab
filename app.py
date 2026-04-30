from flask import Flask, render_template_string, request
import re
import subprocess

app = Flask(__name__)

# Fixed the name to be consistent (ALL CAPS)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Network Health Dashboard</title></head>
<body>
    <h2>Network Ping Tool</h2>
    <form method='POST'>
        <input type='text' name='target' placeholder='Enter IP address (e.g. 8.8.8.8)'>
        <input type='submit' value='Ping'>
    </form>
    <pre>{{ result }}</pre>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        target = request.form.get('target', '')

        # VULNERABLE LINE: user input is directly passed to the shell command without sanitization
        # command = f"ping -c 4 {target}"
        # import os
        # result = os.popen(command).read()

        # 1. Regex check
        if not re.match(r"^[0-9.]+$", target):
            result = "Invalid characters detected! Only numbers and dots allowed."
        else:
            # 2. Try the secure subprocess call
            try:
                output = subprocess.check_output(
                    ["ping", "-c", "4", target],
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=10
                )
                result = output
            except subprocess.CalledProcessError as e:
                result = e.output
            except Exception as e:
                result = f"An error occurred: {str(e)}"

    # We use 'result' consistently here
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)