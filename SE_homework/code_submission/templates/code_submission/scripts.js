document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('generateTestCodeButton').addEventListener('click', generateTestCode);
});

async function generateTestCode() {
    const codeContent = document.getElementById('code').value;
    if (!codeContent) {
        alert('Please enter the code to test.');
        return;
    }

    document.getElementById('loading-indicator').style.display = 'block';

    const response = await fetch('/code/generate_test_code/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({code: codeContent})
    });

    document.getElementById('loading-indicator').style.display = 'none';

    if (response.ok) {
        const data = await response.json();
        document.getElementById('test_code').value = data.test_code;
    } else {
        const errorText = await response.text();
        document.getElementById('output').innerText = 'Failed to generate test code: ' + errorText;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function autoDebug() {
    const code = document.getElementById('code').value;
    const test_code = document.getElementById('test_code').value;
    const error_message = document.getElementById('output').textContent;

    fetch('/code/auto_debug/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            code: code,
            test_code: test_code,
            error_message: error_message
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('code').value = data.debugged_code;
        document.getElementById('output').textContent = "Auto-Debug Completed";
    })
    .catch(error => {
        console.error('Error during auto-debug:', error);
        document.getElementById('output').textContent = 'Auto-Debug Failed';
    });
}
