document.addEventListener('DOMContentLoaded', () => {
    const searchTermInput = document.getElementById('search-term');
    const submitSearchTermButton = document.getElementById('submit-search-term');
    const filterQuestions = document.getElementById('filter-questions');
    const status = document.getElementById('status');
    let currentQuestion = 1;

    submitSearchTermButton.addEventListener('click', () => {
        const searchTerm = searchTermInput.value.trim();
        if (searchTerm) {
            fetch('/api/search-term', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ searchTerm }),
            })
            .then(response => response.json())
            .then(data => {
                status.textContent = data.message;
                filterQuestions.style.display = 'block'; // Show the first filter question
                document.getElementById('question-1').style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                status.textContent = 'An error occurred.';
            });
        } else {
            alert('Please enter a search term.');
        }
    });

    document.querySelectorAll('.response-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const response = event.target.getAttribute('data-response');
            const questionNumber = parseInt(event.target.getAttribute('data-question'), 10);
            fetch('/api/filter-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ questionNumber, response }),
            })
            .then(response => response.json())
            .then(data => {
                status.textContent = data.message;
                document.getElementById(`question-${questionNumber}`).style.display = 'none';
                currentQuestion++;
                if (currentQuestion <= 5) {
                    document.getElementById(`question-${currentQuestion}`).style.display = 'block';
                } else {
                    status.textContent = 'All questions answered. Scraping will proceed.';
                    // Optionally trigger scraping here
                }
            })
            .catch(error => {
                console.error('Error:', error);
                status.textContent = 'An error occurred.';
            });
        });
    });
});
