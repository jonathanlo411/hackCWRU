$.ajax({
    method: "GET",
    url: "http://127.0.0.1:8000/api/data",
    success: (response) => {
        const data = {
            labels: ["Thu", "Fri", "Sat", "Sun"],
            datasets: [{
            label: 'Spending',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 120, 70],
            }]
        };

        const config = {
            type: 'line',
            data: data,
            options: {}
        };
        
        const myChart = new Chart(
            document.getElementById('myChart'),
            config
        );

    },
    error: (response) => {
        console.log("Something went wrong!")
    }
})

