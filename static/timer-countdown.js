document.addEventListener('DOMContentLoaded', function() {
    let timerRunning = false;
    let timerInterval = null;
    let secondsRemaining = 300; // 5 minuter default
    let initialSeconds = 300;

    function updateDisplay() {
        const minutes = Math.floor(secondsRemaining / 60);
        const secs = secondsRemaining % 60;
        
        const display = String(minutes).padStart(2, '0') + ':' + 
                       String(secs).padStart(2, '0');
        
        document.querySelector('#chronoExample .values').innerHTML = display;

        if (secondsRemaining <= 0) {
            timerRunning = false;
            clearInterval(timerInterval);
            alert('Tiden är slut!');
        }
    }

    function setTimer(seconds) {
        timerRunning = false;
        clearInterval(timerInterval);
        secondsRemaining = seconds;
        initialSeconds = seconds;
        updateDisplay();
    }

    // Preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const seconds = parseInt(this.getAttribute('data-seconds'));
            setTimer(seconds);
        });
    });

    document.querySelector('#chronoExample .start-button').addEventListener('click', function() {
        if (!timerRunning && secondsRemaining > 0) {
            timerRunning = true;
            timerInterval = setInterval(function() {
                secondsRemaining--;
                updateDisplay();
            }, 1000);
        }
    });

    document.querySelector('#chronoExample .pause-button').addEventListener('click', function() {
        if (timerRunning) {
            timerRunning = false;
            clearInterval(timerInterval);
        }
    });

    document.querySelector('#chronoExample .reset-button').addEventListener('click', function() {
        timerRunning = false;
        clearInterval(timerInterval);
        secondsRemaining = initialSeconds;
        updateDisplay();
    });

    // Initial display
    updateDisplay();
});
