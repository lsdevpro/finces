document.addEventListener('DOMContentLoaded', () => {
    const boton = document.getElementById('btn-obtener');
    const resultado = document.getElementById('resultado');

    boton.addEventListener('click', () => {
        resultado.innerText = "Consultando servidor Python...";
        resultado.style.color = "#333";
        
        fetch('http://127.0.0.1:5000/api/precio')
            .then(response => {
                if (!response.ok) throw new Error('Error en la comunicación con el backend');
                return response.json();
            })
            .then(data => {
                if(data.bitcoin && data.bitcoin.usd) {
                    const precio = data.bitcoin.usd;
                    resultado.innerText = `¡Éxito! Precio actual: $${precio} USD`;
                    resultado.style.color = "green";
                } else {
                    throw new Error('Datos incompletos de CoinGecko');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultado.innerText = "Error: ¿El servidor Python está encendido?";
                resultado.style.color = "red";
            });
    });
});
