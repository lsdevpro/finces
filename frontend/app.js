document.addEventListener('DOMContentLoaded', async () => {
    const loginView = document.getElementById('login-view');
    const appView = document.getElementById('app-view');
    const btnLogin = document.getElementById('btn-login');
    const btnLogout = document.getElementById('btn-logout');
    const loginError = document.getElementById('login-error');
    
    let supabaseClient = null;

    // 1. Obtener llaves del backend e inicializar Supabase
    try {
        const configRes = await fetch('http://127.0.0.1:5000/api/config');
        const config = await configRes.json();
        // Usar window.supabase para evitar chocar con la variable local nula
        supabaseClient = window.supabase.createClient(config.supabaseUrl, config.supabaseAnonKey);
    } catch (e) {
        console.error("Error cargando configuración", e);
        loginError.innerText = "Error de conexión al servidor.";
        loginError.style.display = 'block';
        return;
    }

    // 2. Comprobar sesión activa
    const { data: { session } } = await supabaseClient.auth.getSession();
    if (session) {
        mostrarApp();
    }

    // 3. Lógica de Inicio de Sesión
    btnLogin.addEventListener('click', async () => {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        btnLogin.innerText = "Verificando...";
        
        const { data, error } = await supabaseClient.auth.signInWithPassword({ email, password });
        
        if (error) {
            loginError.innerText = "Credenciales incorrectas.";
            loginError.style.display = 'block';
            btnLogin.innerText = "Ingresar a la Bóveda";
        } else {
            mostrarApp();
        }
    });

    // 4. Lógica de Cierre de Sesión
    btnLogout.addEventListener('click', async () => {
        await supabaseClient.auth.signOut();
        loginView.style.display = 'flex';
        appView.style.display = 'none';
        document.getElementById('login-email').value = '';
        document.getElementById('login-password').value = '';
    });

    // --- LÓGICA DEL PANEL DE TRADING (Solo se inicia si hay acceso) ---
    function mostrarApp() {
        loginView.style.display = 'none';
        appView.style.display = 'block';
        
        // (Resto de tu código de gráficas)
        const boton = document.getElementById('btn-obtener');
        const resultado = document.getElementById('resultado');
        const chartContainer = document.getElementById('tvchart');
        const switchAuto = document.getElementById('switch-auto');
        const selectorMoneda = document.getElementById('selector-moneda');

        chartContainer.innerHTML = ''; // Limpiar contenedor por si acaso
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
            resultado.innerText = "Consultando...";
            resultado.style.color = "#333";
            
            fetch(`http://127.0.0.1:5000/api/precio?moneda=${moneda}`)
                .then(res => { if (!res.ok) throw new Error('Error de red'); return res.json(); })
                .then(data => {
                    if(data.precio) {
                        resultado.innerText = `¡Éxito! Precio actual de ${data.moneda.toUpperCase()}: $${data.precio} USD`;
                        resultado.style.color = "green";
                        lineSeries.update({ time: Math.floor(Date.now() / 1000), value: data.precio });
                    }
                })
                .catch(err => {
                    resultado.innerText = "Error de conexión.";
                    resultado.style.color = "red";
                    if (switchAuto.checked) { switchAuto.checked = false; clearInterval(intervaloId); }
                });
        };

        selectorMoneda.addEventListener('change', () => {
            lineSeries.setData([]); 
            resultado.innerText = "Moneda seleccionada. Presiona el botón para graficar.";
            resultado.style.color = "#333";
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
                resultado.innerText = "Piloto Automático Desactivado.";
            }
        });
    }
});
