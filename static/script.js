
        function getRecommendations(event) {
            event.preventDefault();

            const userId = document.getElementById('user_id').value;
            if (!userId) {
                alert('Please enter a valid User ID!');
                return;
            }

            // Make an AJAX request to fetch recommendations
            fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);

                    const recommendationsList = document.getElementById('recommendationsList');
                    recommendationsList.innerHTML = ''; // Clear previous recommendations

                    data.recommendations.forEach(item => {
                        const row = document.createElement('tr');

                        // Create title and category cells
                        const titleCell = document.createElement('td');
                        const categoryCell = document.createElement('td');

                        // The first element of `item` is the title and the second is the category
                        titleCell.textContent = item[0];  // Title is the first element in the array
                        categoryCell.textContent = item[1];  // Category is the second element in the array

                        // Append cells to the row
                        row.appendChild(titleCell);
                        row.appendChild(categoryCell);

                        // Append the row to the table
                        recommendationsList.appendChild(row);
                    });


                    // Display user and recommendation details
                    document.getElementById('user_categories').textContent = data.user_categories.join(', ');
                    document.getElementById('recommended_categories').textContent = data.recommended_categories.join(', ');
                    document.getElementById('matching_categories').textContent = data.matching_categories.join(', ');
                    document.getElementById('accuracy').textContent = data.accuracy + '%';

                    // Show the recommendations and results sections
                    document.getElementById('recommendationsSection').style.display = 'block';
                    document.getElementById('resultsSection').style.display = 'block';
                })
                .catch(error => {
                    console.error('Error fetching recommendations:', error);
                });
        }


        async function showClicksVsAccuracy() {
            try {
                const response = await fetch('/clicks_vs_accuracy');  // New API route
                const data = await response.json();
        
                const ctx = document.getElementById('clicksAccuracyChart').getContext('2d');
                document.getElementById('chartSection').style.display = 'block';
        
                new Chart(ctx, {
                    type: 'scatter',
                    data: {
                        datasets: [{
                            label: 'Clicks vs Accuracy',
                            data: data.map(d => ({ x: d.clicks, y: d.accuracy })),
                            backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Number of Clicks'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Accuracy (%)'
                                },
                                min: 0,
                                max: 100
                            }
                        }
                    }
                });
        
            } catch (error) {
                console.error('Error fetching clicks vs accuracy:', error);
            }
        }