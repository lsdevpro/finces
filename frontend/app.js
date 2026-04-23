document.addEventListener('DOMContentLoaded', () => {
    const boton = document.getElementById('btn-obtener');
    const resultado = document.getElementById('resultado');
    const chartContainer = document.getElementById('tvchart');
    const switchAuto = document.getElementById('switch-auto');
    const selectorMoneda = document.getElementById('selector-moneda');

    const chart = LightweightCharts.createChart(chartContainer, {
        width: chartContainer.clientWidth,
        height: 400,
        layout: { backgroundColor: '#ffffff', textColor: '#333' },
        grid: { vertLines: { color: '#e0e0e0' }, horzLines: { color: '#e0e0e0' } },
    });

    const lineSeries = chart.addLineSeries({ color: '#2962ff', lineWidth: 2 });
    let intervaloId = null;

    const consultarPrecio = () => {
        const moneda = selectorMoneda.value;
        resultado.innerText = "Consultando servidor Python...";
        resultado.style.color = "#333";
        
        // Enviamos la moneda elegida al backend
        fetch(`http://127.0.0.1:5000/api/precio?moneda=${moneda}`)
            .then(response => {
                if (!response.ok) throw new Error('Error de red');
                return response.json();
            })
            .then(data => {
                if(data.precio) {
                    resultado.innerText = `¡Éxito! Precio actual de ${data.moneda.toUpperCase()}: $${data.precio} USD`;
                    resultado.style.color = "green";
                    
                    lineSeries.update({
                        time: Math.floor(Date.now() / 1000),
                        value: data.precio
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultado.innerText = "Error de conexión.";
                resultado.style.color = "red";
                
                if (switchAuto.checked) {
                    switchAuto.checked = false;
                    clearInterval(intervaloId);
                }
            });
    };

    // Al cambiar de moneda en el menú desplegable
    selectorMoneda.addEventListener('change', () => {
        lineSeries.setData([]); // Borramos el dibujo de la moneda anterior
        resultado.innerText = "Moneda seleccionada. Presiona el botón para graficar.";
        resultado.style.color = "#333";
        
        // Si el piloto automático estaba encendido, actualiza de inmediato
        if (switchAuto.checked) consultarPrecio();
    });

    boton.addEventListener('click', consultarPrecio);

    switchAuto.addEventListener('change', (evento) => {
        if (evento.target.checked) {
            consultarPrecio();
            intervaloId = setInterval(consultarPrecio, 60000);
        } else {
            clearInterval(intervaloId);
            intervaloId = null;
            resultado.innerText = "Piloto Automático Desactivado. Modo Manual.";
            resultado.style.color = "#333";
        }
    });
});
