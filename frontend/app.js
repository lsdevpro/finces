document.addEventListener('DOMContentLoaded', async () => {
  const loginView = document.getElementById('login-view');
  const appView = document.getElementById('app-view');
  const btnLogin = document.getElementById('btn-login');
  const loginError = document.getElementById('login-error');

  // Inicialización de la Bóveda (Supabase)
  const supabaseUrl = 'https://qxavafkcfmkjvsvhubpr.supabase.co';
  const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4YXZhZmtjZm1ranZzdmh1YnByIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5NjY0OTEsImV4cCI6MjA5MjU0MjQ5MX0.iMar-iKp2YvEC2mg8g98DFrU6iObzUCNVw7soGISzPQ';
  const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
  let precioActual = 0;

  // Verificación de Sesión Inicial
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
      // Conexión eliminada
      resultado.innerText = "Consultas desactivadas temporalmente.";
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


  }

  // --- Lógica del Sistema de Temas (Switch Chainx) ---
  const themeSwitch = document.getElementById('theme-toggle-switch');

  const setTheme = (isDark) => {
    const root = document.documentElement;
    const theme = isDark ? 'dark' : 'light';

    root.setAttribute('data-theme', theme);
    localStorage.setItem('finces-theme', theme);
    if (themeSwitch) themeSwitch.checked = isDark;

    if (window.activeChart) {
      window.activeChart.applyOptions({
        layout: {
          background: { color: isDark ? '#0f1015' : '#ffffff' },
          textColor: isDark ? '#ffffff' : '#0f172a'
        },
        grid: {
          vertLines: { color: isDark ? '#2a2b36' : '#e2e8f0' },
          horzLines: { color: isDark ? '#2a2b36' : '#e2e8f0' }
        }
      });
    }
  };

  if (themeSwitch) {
    themeSwitch.addEventListener('change', (e) => {
      setTheme(e.target.checked);
    });
  }

  // Cargar tema guardado
  const savedTheme = localStorage.getItem('finces-theme');
  if (savedTheme) {
    setTheme(savedTheme === 'dark');
  } else {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(prefersDark);
  }

  /* =========================================
     MÓDULO MARKET SUMMARY — CoinGecko API
  ========================================= */
  let marketSummaryInitialized = false;

  // --- GLOBAL MARKET STATE (Elevated for accessibility) ---
  let coinsData = [];
  let favorites = JSON.parse(localStorage.getItem('finces-favorites') || '[]');
  let customLists = JSON.parse(localStorage.getItem('finces-custom-lists') || '[]');

  // Migration from old watchlist if needed
  if (customLists.length === 0) {
    let oldWatchlist = JSON.parse(localStorage.getItem('finces-watchlist') || '[]');
    if (oldWatchlist.length > 0) {
      customLists.push({ id: 'list-general', name: 'General', coins: oldWatchlist });
      localStorage.setItem('finces-custom-lists', JSON.stringify(customLists));
    }
  }

  function isCoinInAnyList(coinId) {
    return customLists.some(list => list.coins.includes(coinId));
  }

  let filterFavorites = false;
  let filterWatchlist = false;
  let revealFavs = false;
  let revealWatch = false;

  async function initMarketSummary() {
    if (marketSummaryInitialized) return;
    marketSummaryInitialized = true;

    const tbody = document.getElementById('mercados-tbody');
    const statusEl = document.getElementById('mercados-status');
    const headers = document.querySelectorAll('#mercados-table th[data-sort]');

    let sortKey = 'market_cap';
    let sortDir = 'desc';
    let usdtMxnRate = 20.00;
    let currentPeriod = '24h';
    let searchFilter = '';

    let activeFilters = {
      priceMin: null, priceMax: null,
      mcapMin: null, mcapMax: null,
      changeMin: null, changeMax: null
    };

    let currentPage = 1;
    let totalCoins = 15978; // Estimación oficial de CoinGecko
    const perPage = 100;

    let searchTimeout;
    const searchTrigger = document.getElementById('m-search-trigger');
    const searchPopup = document.getElementById('m-search-popup');
    const searchBackdrop = document.getElementById('m-search-backdrop');
    const searchClose = document.getElementById('m-search-close');
    const searchClear = document.getElementById('m-search-clear');
    const popupInput = document.getElementById('m-popup-input');
    const popupResults = document.getElementById('m-popup-results');

    function openSearch() {
      searchPopup.classList.add('visible');
      searchBackdrop.classList.add('visible');
      setTimeout(() => popupInput.focus(), 100);
    }

    function closeSearch() {
      searchPopup.classList.remove('visible');
      searchBackdrop.classList.remove('visible');
      // Limpiar al cerrar
      if (popupInput) {
        popupInput.value = '';
        resetSearchResults();
      }
    }

    function resetSearchResults() {
      if (popupResults) {
        popupResults.innerHTML = `
                <div style="padding:40px; text-align:center; color:var(--text-muted); font-size:0.9rem;">
                    <i class="fa-solid fa-search" style="font-size: 1.5rem; margin-bottom: 15px; opacity: 0.5;"></i><br>
                    Escribe para buscar entre más de 10,000 monedas...
                </div>`;
      }
    }

    if (searchTrigger) {
      searchTrigger.addEventListener('click', openSearch);
    }

    if (searchBackdrop) {
      searchBackdrop.addEventListener('click', closeSearch);
    }

    if (searchClose) {
      searchClose.addEventListener('click', closeSearch);
    }

    // --- ACCIONES DE TABLA (EVENT DELEGATION) ---
    if (tbody) {
      tbody.addEventListener('click', (e) => {
        const target = e.target;
        if (target.classList.contains('star-toggle')) {
          const id = target.getAttribute('data-id');
          if (favorites.includes(id)) {
            favorites = favorites.filter(fid => fid !== id);
          } else {
            favorites.push(id);
          }
          localStorage.setItem('finces-favorites', JSON.stringify(favorites));
          renderTable();
        } else if (target.classList.contains('watch-toggle')) {
          const id = target.getAttribute('data-id');
          openWatchlistModal(id);
        }
      });
    }

    // --- FILTROS GLOBALES (CABECERA) ---
    const favTrigger = document.getElementById('m-fav-trigger');
    const watchTrigger = document.getElementById('m-watchlist-trigger');

    if (favTrigger) {
      const favEye = favTrigger.querySelector('.m-eye-badge');
      favTrigger.onclick = () => {
        filterFavorites = !filterFavorites;
        filterWatchlist = false;
        if (watchTrigger) watchTrigger.classList.remove('active');
        favTrigger.classList.toggle('active', filterFavorites);
        renderTable();
      };
      if (favEye) {
        favEye.onclick = (e) => {
          e.stopPropagation();
          revealFavs = !revealFavs;
          revealWatch = false; // Solo uno a la vez
          const watchEye = watchTrigger?.querySelector('.m-eye-badge');
          if (watchEye) watchEye.classList.remove('reveal-active');
          favEye.classList.toggle('reveal-active', revealFavs);
          renderTable();
        };
      }
    }
    if (watchTrigger) {
      const watchEye = watchTrigger.querySelector('.m-eye-badge');
      watchTrigger.onclick = () => {
        filterWatchlist = !filterWatchlist;
        filterFavorites = false;
        if (favTrigger) favTrigger.classList.remove('active');
        watchTrigger.classList.toggle('active', filterWatchlist);
        renderTable();
      };
      if (watchEye) {
        watchEye.onclick = (e) => {
          e.stopPropagation();
          revealWatch = !revealWatch;
          revealFavs = false; // Solo uno a la vez
          const favEye = favTrigger?.querySelector('.m-eye-badge');
          if (favEye) favEye.classList.remove('reveal-active');
          watchEye.classList.toggle('reveal-active', revealWatch);
          renderTable();
        };
      }
    }

    if (searchClear) {
      searchClear.addEventListener('click', () => {
        if (popupInput) {
          popupInput.value = '';
          popupInput.focus();
          resetSearchResults();
        }
      });
    }

    // --- ADVANCED FILTERS LOGIC ---
    const filterTrigger = document.getElementById('m-filter-trigger');
    const filterDropdown = document.getElementById('m-filter-dropdown');
    const btnFilterApply = document.getElementById('btn-filter-apply');
    const btnFilterReset = document.getElementById('btn-filter-reset');

    if (filterTrigger) {
      filterTrigger.addEventListener('click', (e) => {
        e.stopPropagation();
        const isVisible = filterDropdown.style.display === 'flex';
        filterDropdown.style.display = isVisible ? 'none' : 'flex';
      });
    }

    document.addEventListener('click', (e) => {
      if (filterDropdown && !filterDropdown.contains(e.target)) {
        filterDropdown.style.display = 'none';
      }
    });

    if (btnFilterApply) {
      btnFilterApply.onclick = () => {
        const pMin = document.getElementById('filter-price-min').value;
        const pMax = document.getElementById('filter-price-max').value;
        const mMin = document.getElementById('filter-mcap-min').value;
        const mMax = document.getElementById('filter-mcap-max').value;
        const cMin = document.getElementById('filter-change-min').value;
        const cMax = document.getElementById('filter-change-max').value;

        activeFilters.priceMin = pMin ? parseFloat(pMin) : null;
        activeFilters.priceMax = pMax ? parseFloat(pMax) : null;
        activeFilters.mcapMin = mMin ? parseFloat(mMin) : null;
        activeFilters.mcapMax = mMax ? parseFloat(mMax) : null;
        activeFilters.changeMin = cMin ? parseFloat(cMin) : null;
        activeFilters.changeMax = cMax ? parseFloat(cMax) : null;

        renderTable();
        filterDropdown.style.display = 'none';

        // Indicate filters are active
        const hasFilters = Object.values(activeFilters).some(v => v !== null);
        filterTrigger.style.borderColor = hasFilters ? 'var(--accent)' : 'var(--border)';
        filterTrigger.style.color = hasFilters ? 'var(--accent)' : 'var(--text-muted)';
      };
    }

    if (btnFilterReset) {
      btnFilterReset.onclick = () => {
        document.getElementById('filter-price-min').value = '';
        document.getElementById('filter-price-max').value = '';
        document.getElementById('filter-mcap-min').value = '';
        document.getElementById('filter-mcap-max').value = '';
        document.getElementById('filter-change-min').value = '';
        document.getElementById('filter-change-max').value = '';

        activeFilters = { priceMin: null, priceMax: null, mcapMin: null, mcapMax: null, changeMin: null, changeMax: null };
        currentPage = 1;
        fetchMarkets(); // Refresh data with page 1
        filterTrigger.style.borderColor = 'var(--border)';
        filterTrigger.style.color = 'var(--text-muted)';
      };
    }

    // Cerrar con Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeSearch();
    });

    if (popupInput) {
      popupInput.addEventListener('input', (e) => {
        searchFilter = e.target.value.toLowerCase().trim();

        if (searchFilter.length === 0) {
          popupResults.innerHTML = `
                <div style="padding:40px; text-align:center; color:var(--text-muted); font-size:0.9rem;">
                    <i class="fa-solid fa-search" style="font-size: 1.5rem; margin-bottom: 15px; opacity: 0.5;"></i><br>
                    Escribe para buscar entre más de 10,000 monedas...
                </div>`;
          return;
        }

        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          globalSearch(searchFilter);
        }, 400);
      });
    }

    async function globalSearch(query) {
      if (!query) return;
      try {
        popupResults.innerHTML = '<div style="padding:40px; text-align:center;"><i class="fa-solid fa-circle-notch fa-spin"></i> Buscando en todo el mercado...</div>';

        const sRes = await fetch(`https://api.coingecko.com/api/v3/search?query=${query}`);
        const sData = await sRes.json();

        if (sData && sData.coins && sData.coins.length > 0) {
          const ids = sData.coins.slice(0, 10).map(c => c.id).join(',');
          const BASE = 'http://127.0.0.1:5000/api/market/coins';
          const params = `vs_currency=usd&ids=${ids}&order=market_cap_desc&sparkline=false`;

          const mRes = await fetch(`${BASE}?${params}`);
          const mData = await mRes.json();

          if (Array.isArray(mData)) {
            renderSearchResults(mData);
          } else {
            popupResults.innerHTML = '<div style="padding:40px; text-align:center; color:var(--text-muted);">No se encontraron detalles de mercado.</div>';
          }
        } else {
          popupResults.innerHTML = '<div style="padding:40px; text-align:center; color:var(--text-muted);">Sin resultados para "' + query + '"</div>';
        }
      } catch (e) {
        console.error('Global search error:', e);
        popupResults.innerHTML = '<div style="padding:40px; text-align:center; color:var(--color-bear);">Error de conexión con la API de búsqueda.</div>';
      }
    }

    function renderSearchResults(results) {
      if (!popupResults) return;
      if (results.length === 0) {
        popupResults.innerHTML = '<div style="padding:40px; text-align:center; color:var(--text-muted);">Sin resultados detallados.</div>';
        return;
      }

      popupResults.innerHTML = results.map(c => {
        const change = c.price_change_percentage_24h ?? 0;
        const changeClass = change >= 0 ? 'heat-bull' : 'heat-bear';
        const arrow = change >= 0 ? '<i class="fa-solid fa-caret-up"></i>' : '<i class="fa-solid fa-caret-down"></i>';
        const price = c.current_price.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
        const rank = c.market_cap_rank ? `<span class="search-result-rank">${c.market_cap_rank}</span>` : '';

        return `
                <div class="search-result-item" onclick="window.location.hash='#view-mercados'; document.getElementById('m-search-popup').classList.remove('visible'); document.getElementById('m-search-backdrop').classList.remove('visible');">
                    <img src="${c.image}" class="search-result-icon" onerror="this.style.display='none'">
                    <div class="search-result-info">
                        <div class="search-result-name">${c.name} ${rank}</div>
                        <span class="search-result-ticker">${c.symbol}</span>
                    </div>
                    <div class="search-result-data">
                        <span class="search-result-price">${price}</span>
                        <span class="search-result-change ${changeClass}">${arrow} ${Math.abs(change).toFixed(2)}%</span>
                    </div>
                </div>
              `;
      }).join('');
    }

    // Stats Panel Logic
    const statsPanel = document.getElementById('mercados-stats-panel');
    const btnGainers = document.getElementById('btn-top-gainers');
    const btnLosers = document.getElementById('btn-top-losers');
    const btnTrending = document.getElementById('btn-top-trending');
    const btnNews = document.getElementById('btn-top-news');
    const btnNew = document.getElementById('btn-top-new');
    let activeStatsType = null;
    let statsRows = 1;
    let trendingData = [];
    let newData = [];
    const newsData = [
      { title: "Bitcoin consolida su posición tras el halving", source: "Finces Insight", time: "hace 2h" },
      { title: "Solana rompe récords de actividad en la red", source: "Market Update", time: "hace 4h" },
      { title: "Ethereum: Vitalik propone nuevas mejoras de escalabilidad", source: "Tech News", time: "hace 6h" },
      { title: "Binance anuncia soporte para nuevos pares RWA", source: "Exchange News", time: "hace 8h" },
      { title: "Inversión institucional en cripto crece un 20% este trimestre", source: "Finance Report", time: "hace 12h" }
    ];

    async function fetchTrending() {
      try {
        const res = await fetch('https://api.coingecko.com/api/v3/search/trending');
        const data = await res.json();
        if (data && Array.isArray(data.coins)) {
          trendingData = data.coins.map(c => ({
            name: c.item.name,
            symbol: c.item.symbol,
            image: c.item.large,
            current_price_usd: c.item.data.price || 0,
            price_change_percentage_24h: c.item.data.price_change_percentage_24h?.usd || 0
          }));
        }
      } catch (e) { console.error('Trending error:', e); }

      // Fallback para Trending
      if (trendingData.length === 0) {
        trendingData = [
          { name: "Bitcoin", symbol: "btc", image: "https://assets.coingecko.com/coins/images/1/large/bitcoin.png", current_price_usd: 81000, price_change_percentage_24h: 0.5 },
          { name: "Ethereum", symbol: "eth", image: "https://assets.coingecko.com/coins/images/279/large/ethereum.png", current_price_usd: 3100, price_change_percentage_24h: 1.2 },
          { name: "Solana", symbol: "sol", image: "https://assets.coingecko.com/coins/images/4128/large/solana.png", current_price_usd: 210, price_change_percentage_24h: 4.5 },
          { name: "Pepe", symbol: "pepe", image: "https://assets.coingecko.com/coins/images/29850/large/pepe-token.png", current_price_usd: 0.00001, price_change_percentage_24h: 12.3 },
          { name: "Sui", symbol: "sui", image: "https://assets.coingecko.com/coins/images/26375/large/sui_asset.png", current_price_usd: 2.34, price_change_percentage_24h: -2.1 }
        ];
      }
    }

    async function fetchNew() {
      try {
        // Proxy para monedas nuevas usando orden por ID descendente
        const res = await fetch('http://127.0.0.1:5000/api/market/coins?vs_currency=usd&order=id_desc&per_page=20');
        const data = await res.json();
        if (Array.isArray(data)) {
          newData = data;
        } else {
          console.warn('New coins API did not return an array:', data);
          newData = [];
        }
      } catch (e) {
        console.error('New coins error:', e);
        newData = [];
      }

      // Fallback si la API falla o regresa vacío (evitar que se vea vacío)
      if (newData.length === 0) {
        newData = [
          { name: "EigenLayer", symbol: "eigen", image: "https://assets.coingecko.com/coins/images/37166/large/EIGEN.png", current_price_usd: 3.42, price_change_percentage_24h: 2.5 },
          { name: "Hamster Kombat", symbol: "hmstr", image: "https://assets.coingecko.com/coins/images/38118/large/HMSTR.png", current_price_usd: 0.005, price_change_percentage_24h: -1.2 },
          { name: "Catizen", symbol: "cati", image: "https://assets.coingecko.com/coins/images/39906/large/cati.png", current_price_usd: 0.45, price_change_percentage_24h: 5.8 },
          { name: "Dogs", symbol: "dogs", image: "https://assets.coingecko.com/coins/images/39564/large/dogs.png", current_price_usd: 0.0008, price_change_percentage_24h: -3.4 },
          { name: "Scroll", symbol: "scr", image: "https://assets.coingecko.com/coins/images/31818/large/scroll.png", current_price_usd: 1.10, price_change_percentage_24h: 0.5 }
        ];
      }
    }

    async function renderStats() {
      if (!statsPanel || !activeStatsType) {
        if (statsPanel) statsPanel.style.display = 'none';
        return;
      }

      let items = [];
      let title = '';
      let icon = '';
      let colorStyle = '';

      if (activeStatsType === 'gainers' || activeStatsType === 'losers') {
        const sorted = [...coinsData].sort((a, b) => {
          const ca = a.price_change_percentage_24h ?? 0;
          const cb = b.price_change_percentage_24h ?? 0;
          return activeStatsType === 'gainers' ? cb - ca : ca - cb;
        });
        items = sorted;
        title = activeStatsType === 'gainers' ? 'Top Ganadoras (24h)' : 'Top Perdedoras (24h)';
        icon = activeStatsType === 'gainers' ? 'fa-arrow-trend-up' : 'fa-arrow-trend-down';
        colorStyle = `color:var(--color-${activeStatsType === 'gainers' ? 'bull' : 'bear'})`;
      } else if (activeStatsType === 'trending') {
        if (trendingData.length === 0) await fetchTrending();
        items = trendingData;
        title = 'Tendencias Mundiales';
        icon = 'fa-fire';
        colorStyle = 'color:#ff9800';
      } else if (activeStatsType === 'news') {
        items = newsData;
        title = 'Noticias Destacadas';
        icon = 'fa-newspaper';
        colorStyle = 'color:var(--text)';
      } else if (activeStatsType === 'new') {
        if (newData.length === 0) await fetchNew();
        items = newData;
        title = 'Nuevos Listados';
        icon = 'fa-wand-magic-sparkles';
        colorStyle = 'color:#9c27b0';
      }

      const limit = statsRows * 5;
      const topItems = items.slice(0, limit);

      let gridHtml = '';
      if (activeStatsType === 'news') {
        gridHtml = topItems.map(n => `
            <div class="stat-card" style="justify-content:space-between;">
              <div style="display:flex; flex-direction:column; gap:8px;">
                <span style="font-size:0.8rem; font-weight:600; line-height:1.4; color:var(--text);">${n.title}</span>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px;">
                   <span style="font-size:0.65rem; color:var(--accent); font-weight:600;">${n.source}</span>
                   <span style="font-size:0.65rem; color:var(--text-muted);">${n.time}</span>
                </div>
              </div>
            </div>
          `).join('');
      } else {
        gridHtml = topItems.map(c => {
          const chg = c.price_change_percentage_24h ?? 0;
          const pxMxn = (typeof c.current_price_usd === 'number' ? c.current_price_usd : 0) * usdtMxnRate;
          return `
              <div class="stat-card">
                <div class="stat-card-top">
                  <img src="${c.image}" class="stat-card-img" onerror="this.style.display='none'">
                  <div class="stat-card-info">
                    <span class="stat-card-symbol">${c.symbol.toUpperCase()}</span>
                    <span class="stat-card-name">${c.name}</span>
                  </div>
                </div>
                <div class="stat-card-price-row">
                  <span class="stat-card-price-usd">${formatNum(c.current_price_usd)}</span>
                  <span class="stat-card-price-mxn">${formatNum(pxMxn)}</span>
                </div>
                <div class="stat-card-pct ${chg >= 0 ? 'pct-bull' : 'pct-bear'}">
                  ${(chg >= 0 ? '+' : '') + chg.toFixed(2)}%
                </div>
              </div>
            `;
        }).join('');
      }

      statsPanel.innerHTML = `
          <div class="stats-panel-header">
            <div class="stats-panel-title">
              <i class="fa-solid ${icon}" style="${colorStyle}"></i> ${title}
            </div>
          </div>
          <div class="stats-grid">
            ${gridHtml}
          </div>
          <div class="stats-panel-footer">
            <button class="stats-expand-btn" id="btn-stats-expand" title="Ver más">
              <i class="fa-solid fa-chevron-down"></i>
            </button>
          </div>
        `;
      statsPanel.style.display = 'block';

      const exBtn = document.getElementById('btn-stats-expand');
      if (exBtn) exBtn.onclick = () => { statsRows++; renderStats(); };
    }

    const toggleStats = (type) => {
      if (activeStatsType === type) {
        activeStatsType = null;
      } else {
        activeStatsType = type;
      }
      statsRows = 1;
      [btnGainers, btnLosers, btnTrending, btnNews, btnNew].forEach(b => {
        if (b) b.classList.toggle('active', b.id.includes(activeStatsType));
      });
      renderStats();
    };

    if (btnGainers) btnGainers.onclick = () => toggleStats('gainers');
    if (btnLosers) btnLosers.onclick = () => toggleStats('losers');
    if (btnTrending) btnTrending.onclick = () => toggleStats('trending');
    if (btnNews) btnNews.onclick = () => toggleStats('news');
    if (btnNew) btnNew.onclick = () => toggleStats('new');

    async function fetchMarkets() {
      if (!statusEl) return;
      statusEl.textContent = 'Sincronizando con el servidor local...';
      try {
        const res = await fetch(`http://127.0.0.1:5000/api/market/coins?vs_currency=usd&order=market_cap_desc&per_page=100&page=${currentPage}&sparkline=false&price_change_percentage=24h`);
        const data = await res.json();
        if (Array.isArray(data)) {
          coinsData = data;
          statusEl.textContent = 'Mercado en vivo';
          renderTable();
          renderPagination();
        } else {
          statusEl.textContent = 'Error: Respuesta inesperada del servidor.';
        }
      } catch (e) {
        console.error('Fetch markets error:', e);
        statusEl.textContent = 'Error de conexión con el Backend Proxy.';
      }
    }

    async function updateMarketSentiment() {
      // Conexiones eliminadas para reset total
    }

    function formatNum(n, decimals = 2) {
      if (n === null || n === undefined) return '—';
      return '$' + n.toLocaleString('es-MX', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
      });
    }

    function renderTable() {
      if (!tbody) return;

      const table = document.getElementById('mercados-table');
      if (table) {
        table.classList.toggle('reveal-favs', revealFavs);
        table.classList.toggle('reveal-watch', revealWatch);
      }

      let filtered = coinsData;

      // Filtros globales (Favoritos / Watchlist)
      if (filterFavorites) {
        filtered = filtered.filter(c => favorites.includes(c.id));
      }
      if (filterWatchlist) {
        filtered = filtered.filter(c => isCoinInAnyList(c.id));
      }

      if (searchFilter) {
        filtered = coinsData.filter(c =>
          c.name.toLowerCase().includes(searchFilter) ||
          c.symbol.toLowerCase().includes(searchFilter)
        );
      }

      // Apply Advanced Filters
      if (activeFilters.priceMin !== null) filtered = filtered.filter(c => c.current_price_usd >= activeFilters.priceMin);
      if (activeFilters.priceMax !== null) filtered = filtered.filter(c => c.current_price_usd <= activeFilters.priceMax);
      if (activeFilters.mcapMin !== null) filtered = filtered.filter(c => c.market_cap >= activeFilters.mcapMin);
      if (activeFilters.mcapMax !== null) filtered = filtered.filter(c => c.market_cap <= activeFilters.mcapMax);
      if (activeFilters.changeMin !== null) {
        const ck = currentPeriod === '24h' ? 'price_change_percentage_24h' : `price_change_percentage_${currentPeriod}_in_currency`;
        filtered = filtered.filter(c => (c[ck] ?? c.price_change_percentage_24h ?? 0) >= activeFilters.changeMin);
      }
      if (activeFilters.changeMax !== null) {
        const ck = currentPeriod === '24h' ? 'price_change_percentage_24h' : `price_change_percentage_${currentPeriod}_in_currency`;
        filtered = filtered.filter(c => (c[ck] ?? c.price_change_percentage_24h ?? 0) <= activeFilters.changeMax);
      }

      const sorted = [...filtered].sort((a, b) => {
        let actualSortKey = sortKey;
        // Si el usuario quiere ordenar por cambio, usamos la llave del periodo actual
        if (sortKey === 'price_change_percentage_24h') {
          actualSortKey = currentPeriod === '24h' ? 'price_change_percentage_24h' : `price_change_percentage_${currentPeriod}_in_currency`;
        }

        const valA = a[actualSortKey] ?? 0;
        const valB = b[actualSortKey] ?? 0;

        if (typeof valA === 'string') return sortDir === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
        return sortDir === 'asc' ? valA - valB : valB - valA;
      });

      // Limit the rows only if NOT searching
      let finalData = sorted;
      if (!searchFilter && !filterFavorites && !filterWatchlist) {
        const limitSelect = document.getElementById('mercados-limit-select');
        const currentLimit = parseInt(limitSelect ? limitSelect.value : '50');
        finalData = sorted.slice(0, currentLimit);
      }

      tbody.innerHTML = finalData.map((c, i) => {
        const rank = (currentPage - 1) * parseInt(document.getElementById('mercados-limit-select')?.value || 100) + i + 1;

        // Lógica de Ranking Badge
        const isDefaultSort = (sortKey === 'market_cap' && sortDir === 'desc');
        const rankBadgeHtml = !isDefaultSort ? `<span class="rank-badge" title="Ranking de Capitalización">#${c.market_cap_rank || '—'}</span>` : '';

        // Estados de Favoritos y Watchlist
        const isFav = favorites.includes(c.id);
        const isWatch = isCoinInAnyList(c.id);

        const changeKey = currentPeriod === '24h' ? 'price_change_percentage_24h' : `price_change_percentage_${currentPeriod}_in_currency`;
        const change = c[changeKey] ?? c.price_change_percentage_24h ?? 0;
        const changeClass = change >= 0 ? 'bull-text' : 'bear-text';
        const changeStr = (change >= 0 ? '+' : '') + change.toFixed(2) + '%';
        const priceMxn = c.current_price_usd * usdtMxnRate;
        const volMxn = c.total_volume * usdtMxnRate;
        const capMxn = c.market_cap * usdtMxnRate;

        return `<tr class="${isFav ? 'is-favorite' : ''} ${isWatch ? 'is-watchlist' : ''}">
            <td class="col-free">
              <span class="row-number">${rank}</span>
              <div class="row-hover-actions">
                <i class="fa-regular fa-star row-action-icon star-toggle ${isFav ? 'active' : ''}" 
                   data-id="${c.id}" title="${isFav ? 'Quitar de Favoritos' : 'Añadir a Favoritos'}"></i>
                <i class="fa-regular fa-bookmark row-action-icon watch-toggle ${isWatch ? 'active' : ''}" 
                   data-id="${c.id}" title="${isWatch ? 'Quitar de Lista' : 'Añadir a Lista'}"></i>
              </div>
            </td>
            <td>
              <div class="mercados-coin-name">
                <img src="${c.image}" alt="${c.symbol}"
                  onerror="this.style.display='none'">
                <div class="mercados-coin-info">
                  <span class="mercados-coin-ticker">
                    ${c.symbol.toUpperCase()}
                  </span>
                  <span class="mercados-coin-fullname">${c.name}</span>
                  ${rankBadgeHtml}
                </div>
              </div>
            </td>
            <td>
              <div class="cell-stack">
                <span class="val-primary">
                  ${formatNum(c.current_price_usd)}
                </span>
                <span class="val-secondary">${formatNum(priceMxn)}</span>
              </div>
            </td>
            <td class="${changeClass}" style="font-weight: 500;">${changeStr}</td>
            <td>
              <div class="cell-stack">
                <span class="val-primary">
                  ${formatNum(c.total_volume)}
                </span>
                <span class="val-secondary">${formatNum(volMxn)}</span>
              </div>
            </td>
            <td>
              <div class="cell-stack">
                <span class="val-primary">
                  ${formatNum(c.market_cap)}
                </span>
                <span class="val-secondary">${formatNum(capMxn)}</span>
              </div>
            </td>
          </tr>`;
      }).join('');
    }

    function renderPagination() {
      const infoEl = document.getElementById('pagination-info');
      const controlsEl = document.getElementById('pagination-controls');
      if (!infoEl || !controlsEl) return;

      const currentLimit = parseInt(document.getElementById('mercados-limit-select')?.value || 100);
      const totalPages = Math.ceil(totalCoins / currentLimit);

      // Update Info
      const start = (currentPage - 1) * currentLimit + 1;
      const end = Math.min(currentPage * currentLimit, totalCoins);
      infoEl.textContent = `Mostrando ${start} - ${end} de ${totalCoins}`;

      // Update Controls
      let html = `
            <div class="pagination-btn ${currentPage === 1 ? 'disabled' : ''}" id="prev-page-action">
              <i class="fa-solid fa-chevron-left pagination-arrow"></i>
            </div>
          `;

      const maxVisible = 6;
      for (let i = 1; i <= Math.min(totalPages, maxVisible); i++) {
        html += `<div class="pagination-btn page-num ${i === currentPage ? 'active' : ''}" data-page="${i}">${i}</div>`;
      }

      if (totalPages > maxVisible) {
        html += `<div class="pagination-ellipsis">...</div>`;
        html += `<div class="pagination-btn page-num ${currentPage === totalPages ? 'active' : ''}" data-page="${totalPages}">${totalPages}</div>`;
      }

      html += `
            <div class="pagination-btn ${currentPage === totalPages ? 'disabled' : ''}" id="next-page-action">
              <i class="fa-solid fa-chevron-right pagination-arrow"></i>
            </div>
          `;

      controlsEl.innerHTML = html;

      // Listeners
      controlsEl.querySelectorAll('.page-num').forEach(btn => {
        btn.onclick = () => {
          const p = parseInt(btn.dataset.page);
          if (p !== currentPage) {
            currentPage = p;
            fetchMarkets();
            scrollToTableTop();
          }
        };
      });

      const prev = document.getElementById('prev-page-action');
      const next = document.getElementById('next-page-action');

      if (prev) prev.onclick = () => {
        if (currentPage > 1) {
          currentPage--;
          fetchMarkets();
          scrollToTableTop();
        }
      };

      if (next) next.onclick = () => {
        if (currentPage < totalPages) {
          currentPage++;
          fetchMarkets();
          scrollToTableTop();
        }
      };
    }

    function scrollToTableTop() {
      const container = document.getElementById('mercados-scroll-container');
      if (container) container.scrollTo({ top: 0, behavior: 'smooth' });
      const main = document.querySelector('.main-content');
      if (main) {
        const tools = document.querySelector('.mercados-table-tools');
        if (tools) tools.scrollIntoView({ behavior: 'smooth' });
      }
    }

    headers.forEach(th => {
      th.addEventListener('click', () => {
        const key = th.getAttribute('data-sort');
        if (sortKey === key) { sortDir = sortDir === 'asc' ? 'desc' : 'asc'; }
        else { sortKey = key; sortDir = 'desc'; }
        headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
        th.classList.add(sortDir === 'asc' ? 'sort-asc' : 'sort-desc');
        renderTable();
      });
    });


    let autoInterval = null;

    function startAutoRefresh() {
      const selectEl = document.getElementById('mercados-interval-select');
      if (!selectEl) return;
      const ms = parseInt(selectEl.value || '60000');
      stopAutoRefresh();
      autoInterval = setInterval(fetchMarkets, ms);
    }

    function stopAutoRefresh() {
      if (autoInterval) {
        clearInterval(autoInterval);
        autoInterval = null;
      }
    }

    // Manual refresh button
    const btnRefresh = document.getElementById(
      'mercados-btn-refresh'
    );
    if (btnRefresh) {
      btnRefresh.addEventListener('click', async () => {
        btnRefresh.classList.add('spinning');
        await fetchMarkets();
        setTimeout(() =>
          btnRefresh.classList.remove('spinning'), 650);
      });
    }

    // Auto-update toggle
    const autoToggle = document.getElementById(
      'mercados-auto-toggle'
    );
    if (autoToggle) {
      autoToggle.addEventListener('change', () => {
        if (autoToggle.checked) {
          startAutoRefresh();
        } else {
          stopAutoRefresh();
        }
      });
    }

    // Interval selector
    const intervalSelect = document.getElementById(
      'mercados-interval-select'
    );
    if (intervalSelect) {
      intervalSelect.addEventListener('change', () => {
        if (autoToggle && autoToggle.checked) {
          startAutoRefresh();
        }
      });
    }

    // Limit selector (rows)
    const limitSelect = document.getElementById('mercados-limit-select');
    if (limitSelect) {
      limitSelect.addEventListener('change', () => {
        fetchMarkets();
      });
    }

    // Initial load + start auto-refresh
    await fetchMarkets();
    startAutoRefresh();

    // --- WATCHLIST MULTI-LIST MODAL LOGIC (Refactored & Stabilized) ---
    const watchModal = document.getElementById('watchlist-modal');
    const watchBackdrop = document.getElementById('watchlist-modal-backdrop');
    const watchItemsContainer = document.getElementById('watchlist-modal-items');
    const watchClose = document.getElementById('close-watchlist-modal');
    const createListBtn = document.getElementById('create-list-btn');
    const newListInput = document.getElementById('new-watchlist-input');
    const watchCoinTitle = document.getElementById('watchlist-modal-coin-name');

    let currentActiveCoinId = null;

    function openWatchlistModal(coinId) {
      currentActiveCoinId = coinId;
      const coin = coinsData.find(c => c.id === coinId);
      if (watchCoinTitle) watchCoinTitle.textContent = coin ? `${coin.name} (${coin.symbol.toUpperCase()})` : 'Cargando...';

      renderWatchlistModalItems();

      watchBackdrop.style.display = 'block';
      watchModal.style.display = 'flex';
      setTimeout(() => {
        watchBackdrop.classList.add('visible');
        watchModal.classList.add('visible');
      }, 10);
    }

    function closeWatchlistModal() {
      if (watchBackdrop) watchBackdrop.classList.remove('visible');
      if (watchModal) watchModal.classList.remove('visible');
      setTimeout(() => {
        if (watchBackdrop) watchBackdrop.style.display = 'none';
        if (watchModal) watchModal.style.display = 'none';
      }, 300);
    }

    function renderWatchlistModalItems() {
      if (!watchItemsContainer) return;
      watchItemsContainer.innerHTML = customLists.map((list, index) => {
        const isActive = list.coins.includes(currentActiveCoinId);
        return `
                <div class="watchlist-item ${isActive ? 'active' : ''}" 
                     data-list-id="${list.id}" 
                     data-index="${index}"
                     draggable="true">
                    <div class="watchlist-item-top">
                        <i class="fa-solid fa-grip-vertical drag-handle" title="Arrastrar para reordenar"></i>
                        <div class="w-checkbox ${isActive ? 'checked' : ''}" data-action="toggle">
                            <i class="fa-solid fa-check"></i>
                        </div>
                        <span class="watchlist-item-name">${list.name}</span>
                    </div>
                    <div class="watchlist-item-bottom">
                        <div class="watchlist-item-actions">
                            <button class="w-main-action-btn ${isActive ? 'remove' : 'add'}" data-action="quick-toggle">
                                ${isActive ? 'Quitar' : 'Añadir'}
                            </button>
                            <button class="w-action-btn edit" title="Renombrar" data-action="edit">
                                <i class="fa-solid fa-pen"></i>
                            </button>
                            <button class="w-action-btn delete" title="Eliminar" data-action="delete">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        </div>
                        <span class="watchlist-item-count">${list.coins.length} ${list.coins.length === 1 ? 'activo' : 'activos'}</span>
                    </div>
                </div>
            `;
      }).join('');

      setupDragAndDrop();
    }

    let draggedIndex = null;

    function setupDragAndDrop() {
      const items = watchItemsContainer.querySelectorAll('.watchlist-item');
      items.forEach((item, index) => {
        const handle = item.querySelector('.drag-handle');

        handle.addEventListener('dragstart', (e) => {
          draggedIndex = index;
          item.classList.add('dragging');
          e.dataTransfer.effectAllowed = 'move';
          e.dataTransfer.setData('text/plain', index);

          // Set a small delay to add class that disables pointer events on children
          setTimeout(() => {
            watchItemsContainer.classList.add('is-sorting');
          }, 0);
        });

        item.addEventListener('dragend', () => {
          item.classList.remove('dragging');
          watchItemsContainer.classList.remove('is-sorting');
          items.forEach(i => i.classList.remove('drag-over'));
          draggedIndex = null;
        });

        item.addEventListener('dragover', (e) => {
          e.preventDefault();
          e.dataTransfer.dropEffect = 'move';

          const targetIndex = parseInt(item.dataset.index);
          if (draggedIndex !== null && draggedIndex !== targetIndex) {
            // Live swap!
            const listToMove = customLists[draggedIndex];
            customLists.splice(draggedIndex, 1);
            customLists.splice(targetIndex, 0, listToMove);

            draggedIndex = targetIndex; // Update for next comparison
            localStorage.setItem('finces-custom-lists', JSON.stringify(customLists));
            renderWatchlistModalItems(); // Re-render to show new order

            // Re-apply dragging state to the new item at the new index
            const newItems = watchItemsContainer.querySelectorAll('.watchlist-item');
            newItems[targetIndex].classList.add('dragging');
          }
        });

        item.addEventListener('drop', (e) => {
          e.preventDefault();
          if (typeof renderTable === 'function') renderTable();
        });
      });
    }

    function toggleCoinInList(listId, shouldClose = true) {
      const list = customLists.find(l => l.id === listId);
      if (!list) return;

      if (list.coins.includes(currentActiveCoinId)) {
        list.coins = list.coins.filter(id => id !== currentActiveCoinId);
      } else {
        list.coins.push(currentActiveCoinId);
      }

      localStorage.setItem('finces-custom-lists', JSON.stringify(customLists));
      renderWatchlistModalItems();
      if (typeof renderTable === 'function') renderTable();

      if (shouldClose) {
        setTimeout(closeWatchlistModal, 150);
      }
    }

    function deleteList(listId) {
      const list = customLists.find(l => l.id === listId);
      if (!list) return;

      if (confirm(`¿Estás seguro de que deseas eliminar la lista "${list.name}"?`)) {
        customLists = customLists.filter(l => l.id !== listId);
        localStorage.setItem('finces-custom-lists', JSON.stringify(customLists));
        renderWatchlistModalItems();
        if (typeof renderTable === 'function') renderTable();
      }
    }

    function renameList(listId) {
      const list = customLists.find(l => l.id === listId);
      if (!list) return;

      const newName = prompt('Nuevo nombre para la lista:', list.name);
      if (newName && newName.trim() !== '' && newName !== list.name) {
        list.name = newName.trim();
        localStorage.setItem('finces-custom-lists', JSON.stringify(customLists));
        renderWatchlistModalItems();
      }
    }

    // Event delegation for items and actions
    if (watchItemsContainer) {
      watchItemsContainer.addEventListener('click', (e) => {
        const actionBtn = e.target.closest('.w-action-btn');
        const mainActionBtn = e.target.closest('.w-main-action-btn');
        const checkbox = e.target.closest('.w-checkbox');
        const item = e.target.closest('.watchlist-item');

        if (!item) return;
        const listId = item.dataset.listId;

        if (actionBtn) {
          e.stopPropagation();
          const action = actionBtn.dataset.action;
          if (action === 'delete') deleteList(listId);
          if (action === 'edit') renameList(listId);
        } else if (checkbox) {
          e.stopPropagation();
          toggleCoinInList(listId, false); // Multi-selection: stay open
        } else if (mainActionBtn) {
          e.stopPropagation();
          toggleCoinInList(listId, true); // Quick toggle: close
        }
      });
    }

    if (createListBtn) {
      createListBtn.addEventListener('click', () => {
        const name = newListInput.value.trim();
        if (!name) return;

        const newList = {
          id: 'list-' + Date.now(),
          name: name,
          coins: [currentActiveCoinId]
        };

        customLists.push(newList);
        localStorage.setItem('finces-custom-lists', JSON.stringify(customLists));

        // Success Feedback
        const originalHTML = createListBtn.innerHTML;
        createListBtn.innerHTML = '<i class="fa-solid fa-check"></i> ¡Lista Creada!';
        createListBtn.classList.add('success-state');

        newListInput.value = '';
        renderWatchlistModalItems();
        if (typeof renderTable === 'function') renderTable();

        setTimeout(() => {
          createListBtn.innerHTML = originalHTML;
          createListBtn.classList.remove('success-state');
          closeWatchlistModal(); // Close after success feedback
        }, 800);
      });

      if (newListInput) {
        newListInput.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') createListBtn.click();
        });
      }
    }

    if (watchClose) watchClose.onclick = closeWatchlistModal;
    if (watchBackdrop) watchBackdrop.onclick = closeWatchlistModal;

    // --- SMART ANCHOR SCROLL SYSTEM (Sequential Priority + Dynamic Handover) ---
    const mainContent = document.querySelector('.main-content');
    const tableContainer = document.getElementById('mercados-scroll-container');
    const tableTools = document.querySelector('.mercados-table-tools');

    if (mainContent && tableContainer && tableTools) {
      mainContent.addEventListener('wheel', (e) => {
        if (document.getElementById('view-mercados').classList.contains('active')) {
          const rect = tableTools.getBoundingClientRect();
          const isAtTop = rect.top <= 10;

          if (isAtTop) {
            if (e.deltaY > 0) {
              const isTableAtBottom = tableContainer.scrollHeight - tableContainer.scrollTop <= tableContainer.clientHeight + 1;
              if (!isTableAtBottom) {
                e.preventDefault();
                tableContainer.scrollTop += e.deltaY;
              }
            }
            else if (e.deltaY < 0) {
              const isTableAtTop = tableContainer.scrollTop <= 0;
              if (!isTableAtTop) {
                e.preventDefault();
                tableContainer.scrollTop += e.deltaY;
              }
            }
          }
        }
      }, { passive: false });
    }

    // Trigger al navegar a Market Summary
    document.querySelectorAll('.nav-item').forEach(link => {
      link.addEventListener('click', (e) => {
        const targetPage = link.getAttribute('data-page') || link.dataset.page;
        if (targetPage === 'mercados') {
          initMarketSummary();
        }
      });
    });

    // Auto-inicializar si ya estamos en mercados (ej. al refrescar)
    if (document.getElementById('view-mercados')?.classList.contains('active')) {
      initMarketSummary();
    }
  } // Cierre de mostrarApp
}); // Final de DOMContentLoaded

/* MERCADOS — Tabs & Tags interactivity */
document.addEventListener('click', function (e) {

  // Tab switching
  if (e.target.closest('.mercados-tab')) {
    document.querySelectorAll('.mercados-tab')
      .forEach(t => t.classList.remove('active'));
    e.target.closest('.mercados-tab')
      .classList.add('active');
  }

  // Tag switching
  if (e.target.closest('.mercados-tag')) {
    document.querySelectorAll('.mercados-tag')
      .forEach(t => t.classList.remove('active'));
    e.target.closest('.mercados-tag')
      .classList.add('active');
  }

  // Description expand/collapse toggle
  if (e.target.id === 'mercados-desc-toggle') {
    const desc = document.getElementById(
      'mercados-desc-text'
    );
    const toggle = e.target;
    if (desc.style.webkitLineClamp === '2') {
      desc.style.webkitLineClamp = 'unset';
      desc.style.overflow = 'visible';
      toggle.textContent = 'Menos';
    } else {
      desc.style.webkitLineClamp = '2';
      desc.style.overflow = 'hidden';
      desc.style.display = '-webkit-box';
      desc.style.webkitBoxOrient = 'vertical';
      toggle.textContent = 'Más';
    }
  }
});
