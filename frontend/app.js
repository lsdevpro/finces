document.addEventListener('DOMContentLoaded', async () => {
    const loginView = document.getElementById('login-view');
    const appView = document.getElementById('app-view');
    const btnLogin = document.getElementById('btn-login');
    const loginError = document.getElementById('login-error');

    let supabase = null;
    let precioActual = 0;

    try {
        const configRes = await fetch('http://127.0.0.1:5000/api/config');
        const config = await configRes.json();
        supabase = window.supabase.createClient(config.supabaseUrl, config.supabaseAnonKey);
    } catch (e) {
        console.error("Error", e);
        loginError.innerText = "Error de conexión al servidor.";
        loginError.style.display = 'block';
        return;
    }

    const { data: { session } } = await supabase.auth.getSession();
    if (session) mostrarApp();

    btnLogin.addEventListener('click', async () => {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        btnLogin.innerText = "Verificando...";
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) {
            loginError.innerText = "Credenciales incorrectas.";
            loginError.style.display = 'block';
            btnLogin.innerText = "Ingresar a la Bóveda";
        } else {
            mostrarApp();
        }
    });

    function mostrarApp() {
        loginView.style.display = 'none';
        appView.style.display = 'block';

        // --- LÓGICA DEL SIDEBAR Y PÁGINAS ---
        const sidebar = document.getElementById('sidebar');
        const btnToggle = document.getElementById('btn-toggle');
        const navItems = document.querySelectorAll('.nav-item');
        const contentViews = document.querySelectorAll('.content-view');
        const btnLogoutNew = document.getElementById('btn-logout-new');

        // Toggle Sidebar
        btnToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            const icon = btnToggle.querySelector('i');
            if (sidebar.classList.contains('collapsed')) {
                icon.classList.remove('fa-chevron-left');
                icon.classList.add('fa-chevron-right');
            } else {
                icon.classList.remove('fa-chevron-right');
                icon.classList.add('fa-chevron-left');
            }

            // Resize chart when sidebar toggles
            setTimeout(() => {
                if (window.activeChart) {
                    const container = document.getElementById('tvchart');
                    window.activeChart.resize(container.clientWidth, 400);
                }
            }, 300);
        });

        // Cambio de Páginas
        navItems.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetPage = link.getAttribute('data-page');

                navItems.forEach(l => l.classList.remove('active'));
                link.classList.add('active');

                contentViews.forEach(view => {
                    view.classList.remove('active');
                    if (view.id === `view-${targetPage}`) view.classList.add('active');
                });

                // Resize chart if terminal is opened
                if (targetPage === 'terminal') {
                    setTimeout(() => {
                        if (window.activeChart) {
                            const container = document.getElementById('tvchart');
                            window.activeChart.resize(container.clientWidth, 400);
                        }
                    }, 50);
                }
            });
        });

        // Logout desde sidebar
        btnLogoutNew.addEventListener('click', async () => {
            await supabase.auth.signOut();
            window.location.reload();
        });
        // ------------------------------------------

        const boton = document.getElementById('btn-obtener');
        const resultado = document.getElementById('resultado');
        const chartContainer = document.getElementById('tvchart');
        const switchAuto = document.getElementById('switch-auto');
        const selectorMoneda = document.getElementById('selector-moneda');

        const btnGuardar = document.getElementById('btn-guardar-nota');
        const inputNota = document.getElementById('nota-texto');
        const listaNotas = document.getElementById('lista-notas');
        const labelMoneda = document.getElementById('diario-moneda-label');

        chartContainer.innerHTML = '';
        const chart = LightweightCharts.createChart(chartContainer, {
            width: chartContainer.clientWidth, height: 400,
            layout: { backgroundColor: 'transparent', textColor: '#333' },
            grid: { vertLines: { color: '#e0e0e0' }, horzLines: { color: '#e0e0e0' } },
        });
        window.activeChart = chart;
        const lineSeries = chart.addLineSeries({ color: '#2563eb', lineWidth: 2 });
        let intervaloId = null;

        async function cargarNotas() {
            const moneda = selectorMoneda.value;
            labelMoneda.innerText = selectorMoneda.options[selectorMoneda.selectedIndex].text;
            listaNotas.innerHTML = '<p style="text-align: center; opacity: 0.7;">Cargando historial...</p>';

            const { data, error } = await supabase
                .from('notas_trading')
                .select('*')
                .eq('moneda', moneda)
                .order('created_at', { ascending: false });

            if (error) {
                listaNotas.innerHTML = '<p style="color: #ef4444;">Error al cargar notas.</p>';
                return;
            }
            if (data.length === 0) {
                listaNotas.innerHTML = '<p style="text-align: center; opacity: 0.7;">No hay notas registradas para esta moneda.</p>';
                return;
            }

            listaNotas.innerHTML = '';
            data.forEach(nota => {
                const div = document.createElement('div');
                div.style = 'background: rgba(37, 99, 235, 0.05); padding: 15px; margin-bottom: 15px; border-radius: 8px; border-left: 4px solid var(--accent);';
                const fecha = new Date(nota.created_at).toLocaleString();
                div.innerHTML = `
                    <div style="font-size: 13px; opacity: 0.7; margin-bottom: 8px;"><b>${fecha}</b> | Precio registrado: <span style="color: #10b981; font-weight: bold;">$${nota.precio}</span></div>
                    <div style="font-size: 16px; line-height: 1.5; white-space: pre-wrap;">${nota.nota}</div>
                `;
                listaNotas.appendChild(div);
            });
        }

        const consultarPrecio = () => {
            const moneda = selectorMoneda.value;
            resultado.innerText = "Consultando...";
            resultado.style.color = "inherit";

            fetch(`http://127.0.0.1:5000/api/precio?moneda=${moneda}`)
                .then(res => { if (!res.ok) throw new Error('Error de red'); return res.json(); })
                .then(data => {
                    if (data.precio) {
                        precioActual = data.precio;
                        resultado.innerText = `¡Éxito! Precio actual de ${data.moneda.toUpperCase()}: $${data.precio} USD`;
                        resultado.style.color = "#10b981";
                        lineSeries.update({ time: Math.floor(Date.now() / 1000), value: data.precio });
                    }
                })
                .catch(err => {
                    resultado.innerText = "Error de conexión.";
                    resultado.style.color = "#ef4444";
                    if (switchAuto.checked) { switchAuto.checked = false; clearInterval(intervaloId); }
                });
        };

        btnGuardar.addEventListener('click', async () => {
            const texto = inputNota.value.trim();
            if (!texto) return;
            if (precioActual === 0) {
                alert("Por favor, obtén el precio del mercado antes de guardar una nota.");
                return;
            }

            btnGuardar.innerText = "Guardando...";
            const { error } = await supabase.from('notas_trading').insert([{
                moneda: selectorMoneda.value,
                precio: precioActual,
                nota: texto
            }]);

            if (error) {
                console.error(error);
                alert("Error al guardar la nota.");
            } else {
                inputNota.value = '';
                cargarNotas();
            }
            btnGuardar.innerText = "Guardar Nota";
        });

        selectorMoneda.addEventListener('change', () => {
            lineSeries.setData([]);
            precioActual = 0;
            resultado.innerText = "Moneda seleccionada. Presiona el botón para graficar.";
            resultado.style.color = "inherit";
            cargarNotas();
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

        cargarNotas();

        // --- LÓGICA MÓDULO ANÁLISIS QUANT ---
        const btnAnalizar = document.getElementById('btn-analizar');
        const tokenSelect = document.getElementById('analysis-token');
        const fiatSelect = document.getElementById('analysis-fiat');
        const yearSelect = document.getElementById('analysis-year');
        const monthSelect = document.getElementById('analysis-month');
        const tbodyAnalisis = document.getElementById('analysis-tbody');
        const valMaxAbs = document.getElementById('val-max-abs');
        const valMinAbs = document.getElementById('val-min-abs');
        const subMaxAbs = document.getElementById('sub-max-abs');
        const subMinAbs = document.getElementById('sub-min-abs');

        if(btnAnalizar) {
            btnAnalizar.addEventListener('click', async () => {
                const symbol = tokenSelect.value;
                const fiat = fiatSelect.value;
                const year = yearSelect.value;
                const month = monthSelect.value;

                // Estado UI: Procesando
                btnAnalizar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Extrayendo Datos...';
                btnAnalizar.disabled = true;
                tbodyAnalisis.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 30px;">Conectando con el Motor Cuantitativo y sincronizando bóveda...</td></tr>';

                try {
                    // Llamada al servidor Python
                    const response = await fetch('http://127.0.0.1:5000/api/analysis/monthly', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ symbol, fiat_symbol: fiat, year, month })
                    });

                    const result = await response.json();

                    if (result.status === 'success') {
                        renderQuantData(result.data);
                    } else {
                        tbodyAnalisis.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--color-bear); padding: 30px;">Error: ${result.message}</td></tr>`;
                    }
                } catch (error) {
                    console.error("Error en análisis:", error);
                    tbodyAnalisis.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--color-bear); padding: 30px;">Error de conexión con el servidor Python. ¿Está encendido?</td></tr>`;
                } finally {
                    // Restaurar botón
                    btnAnalizar.innerHTML = '<i class="fas fa-bolt"></i> Iniciar Procesador Quant';
                    btnAnalizar.disabled = false;
                }
            });
        }

        function renderQuantData(data) {
            tbodyAnalisis.innerHTML = '';
            
            let maxAbs = 0;
            let minAbs = Infinity;
            let maxAbsDate = '';
            let minAbsDate = '';

            // Extraer días y ordenar cronológicamente
            const days = Object.keys(data).sort();

            if(days.length === 0) {
                tbodyAnalisis.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 30px;">La bóveda no devolvió datos para este periodo.</td></tr>';
                valMaxAbs.innerText = "$0.00";
                valMinAbs.innerText = "$0.00";
                subMaxAbs.innerText = "---";
                subMinAbs.innerText = "---";
                return;
            }

            // Recorrer día por día para armar la tabla y buscar récords absolutos
            days.forEach(day => {
                const dayData = data[day];
                
                // Rastrear Máximos y Mínimos Absolutos
                if (dayData.max_price_mxn > maxAbs) {
                    maxAbs = dayData.max_price_mxn;
                    maxAbsDate = `${day} ${dayData.max_time.split('T')[1].substring(0,5)}`;
                }
                if (dayData.min_price_mxn < minAbs) {
                    minAbs = dayData.min_price_mxn;
                    minAbsDate = `${day} ${dayData.min_time.split('T')[1].substring(0,5)}`;
                }

                // Formatear horas
                const timeMax = dayData.max_time ? dayData.max_time.split('T')[1].substring(0,5) : '--:--';
                const timeMin = dayData.min_time ? dayData.min_time.split('T')[1].substring(0,5) : '--:--';

                // Crear fila de la tabla
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${day}</td>
                    <td style="color: var(--color-bull); font-weight: 500;">$${dayData.max_price_mxn.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                    <td style="color: var(--text-muted);">${timeMax}</td>
                    <td style="color: var(--color-bear); font-weight: 500;">$${dayData.min_price_mxn.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                    <td style="color: var(--text-muted);">${timeMin}</td>
                `;
                tbodyAnalisis.appendChild(tr);
            });

            // Actualizar Tarjetas Flotantes (Récords Absolutos)
            valMaxAbs.innerText = `$${maxAbs.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            subMaxAbs.innerText = `Registrado el: ${maxAbsDate}`;
            
            valMinAbs.innerText = `$${minAbs.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            subMinAbs.innerText = `Registrado el: ${minAbsDate}`;
        }
    }

    // --- Lógica del Sistema de Temas ---
    const themeBtns = document.querySelectorAll('.t-btn');

    const setTheme = (theme) => {
        const root = document.documentElement;
        let themeToApply = theme;

        if (theme === 'system') {
            themeToApply = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }

        root.setAttribute('data-theme', themeToApply);
        localStorage.setItem('finces-theme', theme);

        themeBtns.forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-t') === theme);
        });

        if (window.activeChart) {
            const isDark = themeToApply === 'dark';
            window.activeChart.applyOptions({
                layout: {
                    background: { color: isDark ? '#020617' : '#ffffff' },
                    textColor: isDark ? '#f1f5f9' : '#0f172a'
                },
                grid: {
                    vertLines: { color: isDark ? '#1e293b' : '#e2e8f0' },
                    horzLines: { color: isDark ? '#1e293b' : '#e2e8f0' }
                }
            });
        }
    };

    themeBtns.forEach(btn => {
        btn.addEventListener('click', () => setTheme(btn.getAttribute('data-t')));
    });

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (localStorage.getItem('finces-theme') === 'system') {
            setTheme('system');
        }
    });

    const savedTheme = localStorage.getItem('finces-theme') || 'system';
    setTheme(savedTheme);
});
