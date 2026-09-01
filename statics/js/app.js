function updateStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('age').innerText = data.detected_age ?? '--';
            document.getElementById('alertMsg').style.display = data.alert ? 'block' : 'none';
        })
        .catch(err => console.error('Status fetch error:', err));
}

function toggleShield() {
    fetch('/toggle')
        .then(response => response.json())
        .then(data => {
            console.log('Shield active state:', data.active);
        })
        .catch(err => console.error('Toggle error:', err));
}

setInterval(updateStatus, 1000);