document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    let sentimentChart;

    async function fetchMetrics() {
        const response = await fetch('/feedbacks/metrics');
        const data = await response.json();
        return data;
    }

    function updateChart(data) {
        if (sentimentChart) sentimentChart.destroy();
    
        sentimentChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Positivo', 'Neutro', 'Negativo'],
                datasets: [{
                    data: [data.sentiments.positive, data.sentiments.neutral, data.sentiments.negative],
                    backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
                }]
            }
        });
    }
    

    function updateTopFeatures(data) {
        const featuresList = document.getElementById('top-features-list');
        featuresList.innerHTML = '';
        
        data.top_features.forEach(f => {
            const li = document.createElement('li');
            li.textContent = `${f.code} (${f.count} pedidos)`;
            featuresList.appendChild(li);
        });
    }

    async function updateMetrics() {
        const data = await fetchMetrics();
        updateChart(data);
        updateTopFeatures(data);
    }

    document.getElementById('refresh-btn').addEventListener('click', updateMetrics);

    updateMetrics();
});
