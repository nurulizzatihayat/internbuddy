const ctx = document.getElementById('statusChart');

const statusCounts = {
    listed: parseInt(ctx.dataset.listed, 10) || 0,
    applied: parseInt(ctx.dataset.applied, 10) || 0,
    interview: parseInt(ctx.dataset.interview, 10) || 0,
    offered: parseInt(ctx.dataset.offered, 10) || 0,
    rejected: parseInt(ctx.dataset.rejected, 10) || 0,
    accepted: parseInt(ctx.dataset.accepted, 10) || 0
};

new Chart(ctx, {
    type: 'bar',

    data: {
        labels: [
            'Listed',
            'Applied',
            'Interview',
            'Offered',
            'Rejected',
            'Accepted'
        ],

        datasets: [{
            label: 'Applications',
            data: [
                statusCounts.listed,
                statusCounts.applied,
                statusCounts.interview,
                statusCounts.offered,
                statusCounts.rejected,
                statusCounts.accepted
            ],

            backgroundColor: [
                '#8D6E63',  // Taupe brown - Listed
                '#795548',  // Brown - Applied
                '#A1887F',  // Light brown - Interview
                '#6D4C41',  // Dark brown - Offer
                '#5D4037',  // Deep brown - Rejected
                '#BCAAA4'   // Soft brown - Accepted
            ],

            borderColor: 'rgba(60, 40, 30, 0.25)',
            borderWidth: 2
        }]
    },

    options: {
        responsive: true,

        plugins: {
            legend: {
                position: 'right',
                labels: {
                    color: '#ffffff'
                }
            }
        }
    }
});

