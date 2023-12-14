<script>
    var householdData = {
    labels: ['Senior Citizens', 'Pregnant/Lactating Mothers', 'Beneficiaries with Disability', 'Registered Voters', 'Total Members'],
    datasets: [{
        label: 'Household Statistics',
        data: [
            {{ total_senior_citizens }},
            {{ total_pregnant_lactating_mothers }},
            {{ total_beneficiaries_with_disability }},
            {{ total_registered_voters }},
            {{ total_members }}
        ],
        backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
        ],
        borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 1
    }]
};

var ctx = document.getElementById('householdChart').getContext('2d');
var householdChart = new Chart(ctx, {
    type: 'bar',
    data: householdData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
// Access the data from the Django context
var genderLabels = {{ gender_labels|safe }};
var genderCounts = {{ gender_counts|safe }};

// Create the pie chart
var ctx = document.getElementById('genderPieChart').getContext('2d');
var genderPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: genderLabels,
        datasets: [{
            data: genderCounts,
            backgroundColor: ['#36A2EB', '#FF6384'], // Blue for male, Red for female
        }]
    },
    options: {
        responsive: true,
        legend: {
            display: true,
            position: 'bottom',
        },
    }
});

var ageDistributionData = {
    labels: ['0-17', '18-25', '26-35', '36-50', '51-60', '60+'],
    datasets: [{
        label: 'Age Distribution',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
        data: {{ age_counts|safe }},
    }]
};

var ctx = document.getElementById('ageDistributionChart').getContext('2d');
var ageDistributionChart = new Chart(ctx, {
    type: 'bar',
    data: ageDistributionData,
    options: {
        scales: {
            y: {
                beginAtZero: true,
            }
        }
    }
});
</script>