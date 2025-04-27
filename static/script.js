function getRecommendations() {
    const userIdElement = document.getElementById('user_id');  // Accessing the input field
    console.log(userIdElement);  // This should not be null if the element is present
    const userId = document.getElementById('user_id').value;
    if (!userId) {
        alert('Please enter a user ID!');
        return;
    }

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId }),
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsList = document.getElementById('recommendationsList');
        recommendationsList.innerHTML = '';

        if (data.recommendations.length === 0) {
            recommendationsList.innerHTML = '<li>No recommendations found.</li>';
        } else {
            data.recommendations.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.title} [Category: ${item.category}]`;
                recommendationsList.appendChild(li);
            });
        }
    })
    .catch(error => {
        console.error('Error fetching recommendations:', error);
    });
}
