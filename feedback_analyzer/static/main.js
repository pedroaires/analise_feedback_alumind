document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    let sentimentChart;

    async function fetchMetrics() {
        const response = await fetch('/feedbacks/metrics');
        return await response.json();
    }

    async function fetchFeedbacks(id = '') {
        const url = id ? `/feedbacks/${id}` : '/feedbacks';
        const response = await fetch(url);
        return await response.json();
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

    function populateFeedbackTable(data) {
        const tableBody = document.getElementById('feedback-table-body');
        tableBody.innerHTML = '';

        if (!Array.isArray(data)) data = [data]; // se for apenas um feedback, coloca em array

        data.forEach(feedback => {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${feedback.id}</td>
                <td>${feedback.feedback}</td>
                <td>${feedback.sentiment}</td>
                <td>${feedback.requested_features.map(f => f.code).join(', ')}</td>
            `;

            tableBody.appendChild(tr);
        });
    }

    async function updateDashboard() {
        const metrics = await fetchMetrics();
        const feedbacks = await fetchFeedbacks();

        updateChart(metrics);
        updateTopFeatures(metrics);
        populateFeedbackTable(feedbacks);
    }

    document.getElementById('search-feedback-btn').addEventListener('click', async () => {
        const id = document.getElementById('feedback-id-input').value.trim();
        if (!id) {
            alert('Por favor, informe o ID do feedback.');
            return;
        }

        try {
            const feedback = await fetchFeedbacks(id);
            populateFeedbackTable(feedback);
        } catch {
            alert('Feedback não encontrado ou ocorreu um erro.');
        }
    });

    updateDashboard();
});
