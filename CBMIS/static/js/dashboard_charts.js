

    document.addEventListener('DOMContentLoaded', function() {
        const municipalLabels = {{ municipal_labels|safe }};
        const residentCounts = {{ municipal_residents|safe }};

        const ctx = document.getElementById('residentChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: municipalLabels,
                datasets: [{
                    label: 'Total Residents',
                    data: residentCounts,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    });