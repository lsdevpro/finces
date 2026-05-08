import sys

css_replacement = """        /* 8. MÓDULO ANÁLISIS QUANT (BENTO DASHBOARD PRO) */
        
        /* Panel de Control Premium */
        .quant-header-group { margin-bottom: 24px; }
        .quant-header-title h1 { font-size: 1.8rem; margin-bottom: 4px; font-weight: 500; }
        .quant-header-title p { color: var(--text-muted); font-size: 0.9rem; }
        
        .pro-controls-wrapper { background: var(--bg-side); border: 1px solid var(--border); border-radius: 16px; padding: 20px 24px; margin-bottom: 24px; display: flex; flex-wrap: wrap; gap: 24px; justify-content: space-between; align-items: flex-end; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
        .pro-control-group { display: flex; flex-direction: column; gap: 10px; }
        .pro-control-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); font-weight: 600; display: flex; align-items: center; gap: 6px; }
        .pro-inputs { display: flex; gap: 10px; }
        
        .finces-select { height: 42px; appearance: none; background-color: var(--bg-main); border: 1px solid var(--border); color: var(--text); padding: 0 36px 0 16px; border-radius: 8px; font-size: 0.85rem; cursor: pointer; outline: none; font-family: 'Inter', sans-serif; background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238b8e9f' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e"); background-repeat: no-repeat; background-position: right 12px center; background-size: 14px; transition: all 0.2s ease; }
        .finces-select:focus, .finces-select:hover { border-color: var(--accent); }
        
        .btn-execute { height: 42px; background: var(--accent); color: white; border: none; padding: 0 24px; border-radius: 8px; font-weight: 500; font-size: 0.9rem; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.2s; font-family: 'Inter', sans-serif; }
        .btn-execute:hover { background: var(--accent-hover); box-shadow: 0 4px 15px rgba(36, 33, 217, 0.25); }

        /* Bento Grid (Récords KPI) */
        .bento-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .bento-card { background: var(--bg-side); border: 1px solid var(--border); border-radius: 16px; padding: 20px; transition: 0.2s; }
        .bento-card:hover { border-color: var(--text-muted); }
        .bento-title { color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--border); padding-bottom: 12px; }
        .bento-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid rgba(139, 142, 159, 0.1); }
        .bento-item:last-child { border-bottom: none; padding-bottom: 0; }
        .bento-label { font-size: 0.8rem; color: var(--text); display: flex; flex-direction: column; gap: 2px; }
        .bento-label span { color: var(--text-muted); font-size: 0.65rem; }
        
        .bento-val { display: flex; align-items: center; gap: 10px; font-variant-numeric: tabular-nums; font-size: 0.9rem; font-weight: 600; }
        .b-max { color: #2563eb; } .b-min { color: #db2777; }
        [data-theme="dark"] .b-max { color: #60a5fa; } [data-theme="dark"] .b-min { color: #f472b6; }
        .b-badge { background: var(--bg-main); border: 1px solid var(--border); padding: 3px 6px; border-radius: 6px; font-size: 0.65rem; color: var(--text-muted); font-weight: 500; letter-spacing: 0.5px; }

        /* Contenedor de la Tabla */
        .quant-container { width: 100%; overflow-x: auto; overflow-y: auto; max-height: 600px; background: var(--bg-side); border: 1px solid var(--border); border-radius: 16px; }
        .quant-container::-webkit-scrollbar { height: 8px; width: 8px; }
        .quant-container::-webkit-scrollbar-track { background: transparent; }
        .quant-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }

        .quant-table { width: max-content; border-collapse: separate; border-spacing: 0; text-align: right; font-family: 'Inter', sans-serif; font-size: 0.85rem; }
        .quant-table.tabular { font-variant-numeric: tabular-nums; }
        
        /* Cabeceras Limpias */
        .quant-table thead { position: sticky; top: 0; z-index: 20; background: var(--bg-side); box-shadow: 0 4px 10px rgba(0,0,0,0.03); }
        .quant-table th { color: var(--text-muted); padding: 14px 16px; border-bottom: 1px solid var(--border); font-weight: 500; font-size: 0.75rem; letter-spacing: 0.5px; text-transform: uppercase; white-space: nowrap; text-align: center; }
        .quant-table th.th-group { border-bottom: 1px solid rgba(139, 142, 159, 0.2); color: var(--text); font-weight: 600; }
        .quant-table th i { font-size: 0.65rem; margin-left: 4px; opacity: 0.4; cursor: pointer; transition: 0.2s; }
        
        .quant-table th:not(:last-child), .quant-table td:not(:last-child) { border-right: 1px solid rgba(139, 142, 159, 0.1); }
        .quant-table td { padding: 12px 16px; border-bottom: 1px solid rgba(139, 142, 159, 0.1); white-space: nowrap; color: var(--text); background: var(--bg-main); transition: background 0.2s; }
        .quant-table tbody tr:hover td { filter: brightness(1.1); }
        .col-free { font-weight: 600; text-align: center; background-color: var(--bg-side) !important; color: var(--text-muted) !important; }

        /* Mapas de Calor y Barras */
        .heat-bull { background-color: rgba(16, 185, 129, 0.1) !important; color: #10b981 !important; font-weight: 500; text-align: center !important; }
        .heat-bear { background-color: rgba(239, 68, 68, 0.1) !important; color: #ef4444 !important; font-weight: 500; text-align: center !important; }
        .bar-cell { position: relative; z-index: 1; }
        .bar-fill { position: absolute; top: 2px; bottom: 2px; left: 2px; background: rgba(36, 33, 217, 0.08); z-index: -1; border-radius: 4px; }
        [data-theme="dark"] .bar-fill { background: rgba(96, 165, 250, 0.15); }
"""

html_replacement = """                    <div class="quant-header-group">
                        <div class="quant-header-title">
                            <h1>Análisis Cuantitativo</h1>
                            <p>Ethereum Classic (ETC/USDT) | Panel de Extracción y Modelado</p>
                        </div>
                    </div>

                    <div class="pro-controls-wrapper">
                        <div class="pro-control-group">
                            <div class="pro-control-label"><i class="fas fa-coins"></i> Activo y Mercado</div>
                            <div class="pro-inputs">
                                <select id="analysis-token" class="finces-select">
                                    <option value="BTCUSDT">Bitcoin (BTC)</option>
                                    <option value="ETCUSDT" selected>Ethereum Classic (ETC)</option>
                                </select>
                                <select id="analysis-fiat" class="finces-select"><option value="USDTMXN">Par: USDT/MXN</option></select>
                            </div>
                        </div>
                        
                        <div class="pro-control-group">
                            <div class="pro-control-label"><i class="fas fa-calendar-alt"></i> Periodo de Análisis</div>
                            <div class="pro-inputs">
                                <select id="analysis-year" class="finces-select"><option value="2025">Año: 2025</option></select>
                                <select id="analysis-month" class="finces-select"><option value="1">Mes: Enero</option></select>
                            </div>
                        </div>

                        <div class="pro-control-group">
                            <div class="pro-control-label"><i class="fas fa-sort-amount-down"></i> Motor de Ordenamiento</div>
                            <div class="pro-inputs">
                                <select class="finces-select"><option>Criterio: Predeterminado</option></select>
                                <select class="finces-select"><option>Dirección: Ascendente ↑</option><option>Dirección: Descendente ↓</option></select>
                            </div>
                        </div>

                        <button id="btn-analizar" class="btn-execute"><i class="fas fa-microchip"></i> Procesar Datos</button>
                    </div>

                    <div class="bento-grid">
                        <div class="bento-card">
                            <div class="bento-title"><i class="fas fa-door-open"></i> Extremos de Apertura</div>
                            <div class="bento-item"><div class="bento-label">Apertura Máx <span>USDT / MXN</span></div><div class="bento-val b-max"><span class="b-badge">Día 24</span> $ 29.04 / $ 592.61</div></div>
                            <div class="bento-item"><div class="bento-label">Apertura Mín <span>USDT / MXN</span></div><div class="bento-val b-min"><span class="b-badge">Día 14</span> $ 24.58 / $ 475.75</div></div>
                        </div>
                        <div class="bento-card">
                            <div class="bento-title"><i class="fas fa-door-closed"></i> Extremos de Cierre</div>
                            <div class="bento-item"><div class="bento-label">Cierre Máx <span>USDT / MXN</span></div><div class="bento-val b-max"><span class="b-badge">Día 23</span> $ 29.04 / $ 595.81</div></div>
                            <div class="bento-item"><div class="bento-label">Cierre Mín <span>USDT / MXN</span></div><div class="bento-val b-min"><span class="b-badge">Día 13</span> $ 24.58 / $ 496.42</div></div>
                        </div>
                        <div class="bento-card">
                            <div class="bento-title"><i class="fas fa-arrow-trend-down"></i> Mínimos del Periodo</div>
                            <div class="bento-item"><div class="bento-label">Mínimo Máx <span>Día 4 (03:46 pm)</span></div><div class="bento-val b-max">$ 27.95 / $ 579.18</div></div>
                            <div class="bento-item"><div class="bento-label">Mínimo Absoluto <span>Día 13 (02:37 pm)</span></div><div class="bento-val b-min">$ 23.15 / $ 475.66</div></div>
                        </div>
                        <div class="bento-card">
                            <div class="bento-title"><i class="fas fa-arrow-trend-up"></i> Máximos del Periodo</div>
                            <div class="bento-item"><div class="bento-label">Máximo Absoluto <span>Día 24 (12:05 am)</span></div><div class="bento-val b-max">$ 29.18 / $ 600.54</div></div>
                            <div class="bento-item"><div class="bento-label">Máximo Mín <span>Día 14 (10:56 pm)</span></div><div class="bento-val b-min">$ 25.48 / $ 498.80</div></div>
                        </div>
                        <div class="bento-card">
                            <div class="bento-title"><i class="fas fa-water"></i> Liquidez de Mercado</div>
                            <div class="bento-item"><div class="bento-label">Volumen USDT <span>Máx / Mín</span></div><div class="bento-val" style="color:var(--text);"><span class="b-badge">D23</span> $ 585M / <span class="b-badge">D30</span> $ 130M</div></div>
                            <div class="bento-item"><div class="bento-label">Capitalización MXN <span>Máx / Mín</span></div><div class="bento-val" style="color:var(--text);"><span class="b-badge">D23</span> $ 89.6B / <span class="b-badge">D2</span> $ 74.5B</div></div>
                        </div>
                        <div class="bento-card">
                            <div class="bento-title"><i class="fas fa-exclamation-triangle"></i> Riesgo y Rendimiento</div>
                            <div class="bento-item"><div class="bento-label">Volatilidad (%) <span>Máx / Mín</span></div><div class="bento-val" style="color:var(--text);"><span class="b-badge">D19</span> 12.00% / <span class="b-badge">D13</span> -10.00%</div></div>
                            <div class="bento-item"><div class="bento-label">Fluctuación USDT <span>Máx / Mín</span></div><div class="bento-val" style="color:var(--text);"><span class="b-badge">D19</span> $ 3.07 / <span class="b-badge">D12</span> $ 0.73</div></div>
                        </div>
                    </div>

                    <div class="quant-container">
                        <table class="quant-table tabular">
                            <thead>
                                <tr>
                                    <th rowspan="2" class="col-free">Nº <i class="fas fa-sort"></i></th>
                                    <th colspan="2" class="th-group">APERTURA</th>
                                    <th colspan="3" class="th-group">MÍNIMO</th>
                                    <th colspan="3" class="th-group">MÁXIMO</th>
                                    <th colspan="2" class="th-group">CIERRE</th>
                                    <th class="th-group">VOLAT.</th>
                                    <th colspan="2" class="th-group">FLUCTUACIONES</th>
                                    <th colspan="2" class="th-group">VOLUMEN</th>
                                    <th colspan="2" class="th-group">CAPITALIZACIÓN</th>
                                    <th rowspan="2" class="th-group" style="vertical-align: middle;">SUMINISTRO <br> CIRCULANTE</th>
                                </tr>
                                <tr>
                                    <th>USDT <i class="fas fa-sort"></i></th><th>MXN <i class="fas fa-sort"></i></th>
                                    <th>Temporalidad <i class="fas fa-sort"></i></th><th>USDT <i class="fas fa-sort"></i></th><th>MXN <i class="fas fa-sort"></i></th>
                                    <th>Temporalidad <i class="fas fa-sort"></i></th><th>USDT <i class="fas fa-sort"></i></th><th>MXN <i class="fas fa-sort"></i></th>
                                    <th>USDT <i class="fas fa-sort"></i></th><th>MXN <i class="fas fa-sort"></i></th>
                                    <th>% <i class="fas fa-sort"></i></th>
                                    <th>USDT <i class="fas fa-sort"></i></th><th>MXN <i class="fas fa-sort"></i></th>
                                    <th>USDT <i class="fas fa-sort"></i></th><th>MXN <i class="fas fa-sort"></i></th>
                                    <th>USDT <i class="fas fa-sort"></i></th><th>MXN <i class="fas fa-sort"></i></th>
                                </tr>
                            </thead>
                            <tbody id="analysis-tbody">
                                <tr><td class="col-free">31</td><td>$ 26.29</td><td>$ 544.46</td><td class="heat-bull">04:58:00 a. m.</td><td>$ 25.95</td><td>$ 537.41</td><td class="heat-bull">04:04:00 p. m.</td><td>$ 27.59</td><td>$ 571.32</td><td>$ 26.82</td><td>$ 555.48</td><td>6.31%</td><td>$ 1.64</td><td>$ 33.90</td><td class="bar-cell"><div class="bar-fill" style="width: 35%;"></div>$ 209,846,372.06</td><td class="bar-cell"><div class="bar-fill" style="width: 35%;"></div>$ 4,345,918,365.36</td><td>$ 4,038,584,949.29</td><td>$ 83,639,094,299.80</td><td>150,570,927</td></tr>
                                <tr><td class="col-free">30</td><td>$ 25.51</td><td>$ 525.54</td><td class="heat-bull">12:34:00 a. m.</td><td>$ 25.41</td><td>$ 523.46</td><td class="heat-bull">03:25:00 p. m.</td><td>$ 26.64</td><td>$ 548.76</td><td>$ 26.29</td><td>$ 541.57</td><td>4.83%</td><td>$ 1.23</td><td>$ 25.30</td><td class="bar-cell"><div class="bar-fill" style="width: 22%;"></div>$ 130,801,398.60</td><td class="bar-cell"><div class="bar-fill" style="width: 22%;"></div>$ 2,694,508,811.16</td><td>$ 3,958,167,369.61</td><td>$ 81,538,247,813.97</td><td>150,558,475</td></tr>
                                <tr><td class="col-free">29</td><td>$ 24.97</td><td>$ 513.04</td><td class="heat-bear">07:31:00 p. m.</td><td>$ 24.87</td><td>$ 510.96</td><td class="heat-bear">10:40:00 p. m.</td><td>$ 25.99</td><td>$ 533.97</td><td>$ 25.51</td><td>$ 524.17</td><td>4.50%</td><td>$ 1.12</td><td>$ 23.01</td><td class="bar-cell"><div class="bar-fill" style="width: 28%;"></div>$ 171,347,009.73</td><td class="bar-cell"><div class="bar-fill" style="width: 28%;"></div>$ 3,520,752,682.43</td><td>$ 3,840,429,714.20</td><td>$ 78,911,229,552.52</td><td>150,544,493</td></tr>
                                <tr><td class="col-free">28</td><td>$ 25.95</td><td>$ 535.67</td><td class="heat-bear">10:13:00 p. m.</td><td>$ 24.65</td><td>$ 508.93</td><td class="heat-bear">05:52:00 a. m.</td><td>$ 26.26</td><td>$ 542.11</td><td>$ 24.97</td><td>$ 515.41</td><td>-6.12%</td><td>$ 1.61</td><td>$ 33.18</td><td class="bar-cell"><div class="bar-fill" style="width: 24%;"></div>$ 140,825,839.68</td><td class="bar-cell"><div class="bar-fill" style="width: 24%;"></div>$ 2,906,997,395.59</td><td>$ 3,758,535,567.22</td><td>$ 77,585,570,446.34</td><td>150,531,587</td></tr>
                                <tr><td class="col-free">27</td><td>$ 26.24</td><td>$ 542.35</td><td class="heat-bear">10:55:00 a. m.</td><td>$ 24.74</td><td>$ 511.46</td><td class="heat-bear">12:40:00 a. m.</td><td>$ 26.62</td><td>$ 550.40</td><td>$ 25.95</td><td>$ 536.45</td><td>-7.08%</td><td>$ 1.88</td><td>$ 38.94</td><td class="bar-cell"><div class="bar-fill" style="width: 46%;"></div>$ 278,891,230.31</td><td class="bar-cell"><div class="bar-fill" style="width: 46%;"></div>$ 5,765,378,958.58</td><td>$ 3,905,960,950.87</td><td>$ 80,745,977,756.86</td><td>150,518,534</td></tr>
                                <tr><td class="col-free">26</td><td>$ 27.05</td><td>$ 553.44</td><td class="heat-bear">11:37:00 p. m.</td><td>$ 26.16</td><td>$ 535.27</td><td class="heat-bear">05:17:00 a. m.</td><td>$ 27.12</td><td>$ 554.85</td><td>$ 26.24</td><td>$ 536.77</td><td>-3.53%</td><td>$ 0.96</td><td>$ 19.58</td><td class="bar-cell"><div class="bar-fill" style="width: 24%;"></div>$ 145,662,157.43</td><td class="bar-cell"><div class="bar-fill" style="width: 24%;"></div>$ 2,980,247,741.02</td><td>$ 3,948,544,900.70</td><td>$ 80,787,228,668.32</td><td>150,505,378</td></tr>
                                <tr><td class="col-free">25</td><td>$ 27.35</td><td>$ 557.98</td><td class="heat-bear">08:34:00 a. m.</td><td>$ 26.67</td><td>$ 544.16</td><td class="heat-bear">12:29:00 a. m.</td><td>$ 27.51</td><td>$ 561.18</td><td>$ 27.05</td><td>$ 551.81</td><td>-3.03%</td><td>$ 0.83</td><td>$ 17.02</td><td class="bar-cell"><div class="bar-fill" style="width: 27%;"></div>$ 163,962,237.91</td><td class="bar-cell"><div class="bar-fill" style="width: 27%;"></div>$ 3,344,829,653.36</td><td>$ 4,070,716,472.77</td><td>$ 83,042,616,044.51</td><td>150,492,243</td></tr>
                                <tr><td class="col-free">24</td><td>$ 29.04</td><td>$ 592.61</td><td class="heat-bear">11:46:00 p. m.</td><td>$ 27.33</td><td>$ 557.77</td><td class="heat-bear">12:05:00 a. m.</td><td>$ 29.18</td><td>$ 595.50</td><td>$ 27.35</td><td>$ 558.19</td><td>-6.34%</td><td>$ 1.85</td><td>$ 37.73</td><td class="bar-cell"><div class="bar-fill" style="width: 55%;"></div>$ 329,890,937.65</td><td class="bar-cell"><div class="bar-fill" style="width: 55%;"></div>$ 6,732,249,310.09</td><td>$ 4,115,920,991.05</td><td>$ 83,995,657,624.85</td><td>150,479,128</td></tr>
                                <tr><td class="col-free">23</td><td>$ 26.81</td><td>$ 550.07</td><td class="heat-bull">01:52:00 a. m.</td><td>$ 26.66</td><td>$ 547.08</td><td class="heat-bull">11:42:00 p. m.</td><td>$ 29.17</td><td>$ 598.44</td><td>$ 29.04</td><td>$ 595.81</td><td>9.39%</td><td>$ 2.50</td><td>$ 51.36</td><td class="bar-cell"><div class="bar-fill" style="width: 100%;"></div>$ 585,611,931.19</td><td class="bar-cell"><div class="bar-fill" style="width: 100%;"></div>$ 12,015,292,798.19</td><td>$ 4,369,365,303.10</td><td>$ 89,648,452,606.35</td><td>150,464,423</td></tr>
                                <tr><td class="col-free">22</td><td>$ 27.12</td><td>$ 559.56</td><td class="heat-bear">08:40:00 a. m.</td><td>$ 26.50</td><td>$ 546.77</td><td class="heat-bear">01:01:00 a. m.</td><td>$ 27.64</td><td>$ 570.31</td><td>$ 26.81</td><td>$ 553.23</td><td>-4.13%</td><td>$ 1.14</td><td>$ 23.55</td><td class="bar-cell"><div class="bar-fill" style="width: 33%;"></div>$ 197,826,521.50</td><td class="bar-cell"><div class="bar-fill" style="width: 33%;"></div>$ 4,082,150,271.15</td><td>$ 4,033,589,785.67</td><td>$ 83,233,125,227.30</td><td>150,448,051</td></tr>
                                <tr><td class="col-free">21</td><td>$ 25.78</td><td>$ 536.60</td><td class="heat-bull">04:38:00 a. m.</td><td>$ 24.98</td><td>$ 519.85</td><td class="heat-bull">06:55:00 p. m.</td><td>$ 27.80</td><td>$ 578.64</td><td>$ 27.12</td><td>$ 564.37</td><td>11.31%</td><td>$ 2.82</td><td>$ 58.78</td><td class="bar-cell"><div class="bar-fill" style="width: 41%;"></div>$ 246,412,600.39</td><td class="bar-cell"><div class="bar-fill" style="width: 41%;"></div>$ 5,128,462,245.62</td><td>$ 4,079,460,918.09</td><td>$ 84,903,780,357.75</td><td>150,439,448</td></tr>
                                <tr><td class="col-free">20</td><td>$ 25.37</td><td>$ 533.96</td><td class="heat-bull">12:51:00 a. m.</td><td>$ 24.84</td><td>$ 522.75</td><td class="heat-bull">07:10:00 a. m.</td><td>$ 27.85</td><td>$ 586.13</td><td>$ 25.78</td><td>$ 542.67</td><td>12.12%</td><td>$ 3.01</td><td>$ 63.38</td><td class="bar-cell"><div class="bar-fill" style="width: 66%;"></div>$ 397,501,769.16</td><td class="bar-cell"><div class="bar-fill" style="width: 66%;"></div>$ 8,366,418,486.40</td><td>$ 3,878,359,543.29</td><td>$ 81,629,772,487.40</td><td>150,423,370</td></tr>
                                <tr><td class="col-free">19</td><td>$ 26.92</td><td>$ 572.35</td><td class="heat-bull">11:58:00 a. m.</td><td>$ 24.97</td><td>$ 530.69</td><td class="heat-bull">08:10:00 p. m.</td><td>$ 28.04</td><td>$ 596.00</td><td>$ 25.37</td><td>$ 539.30</td><td>12.30%</td><td>$ 3.07</td><td>$ 65.30</td><td class="bar-cell"><div class="bar-fill" style="width: 68%;"></div>$ 408,248,982.79</td><td class="bar-cell"><div class="bar-fill" style="width: 68%;"></div>$ 8,678,352,751.66</td><td>$ 3,815,841,130.96</td><td>$ 81,115,242,841.38</td><td>150,408,956</td></tr>
                                <tr><td class="col-free">18</td><td>$ 28.29</td><td>$ 591.97</td><td class="heat-bear">08:55:00 p. m.</td><td>$ 26.38</td><td>$ 551.84</td><td class="heat-bear">01:04:00 a. m.</td><td>$ 28.47</td><td>$ 595.76</td><td>$ 26.92</td><td>$ 563.34</td><td>-7.37%</td><td>$ 2.10</td><td>$ 43.92</td><td class="bar-cell"><div class="bar-fill" style="width: 35%;"></div>$ 214,817,140.25</td><td class="bar-cell"><div class="bar-fill" style="width: 35%;"></div>$ 4,494,511,616.88</td><td>$ 4,049,448,160.96</td><td>$ 84,724,579,147.69</td><td>150,397,635</td></tr>
                                <tr><td class="col-free">17</td><td>$ 26.70</td><td>$ 557.31</td><td class="heat-bull">12:01:00 a. m.</td><td>$ 26.70</td><td>$ 557.20</td><td class="heat-bull">08:52:00 p. m.</td><td>$ 28.63</td><td>$ 597.64</td><td>$ 28.29</td><td>$ 590.55</td><td>7.26%</td><td>$ 1.94</td><td>$ 40.44</td><td class="bar-cell"><div class="bar-fill" style="width: 35%;"></div>$ 210,508,021.17</td><td class="bar-cell"><div class="bar-fill" style="width: 35%;"></div>$ 4,393,828,671.87</td><td>$ 4,254,937,827.79</td><td>$ 88,811,189,810.55</td><td>150,386,642</td></tr>
                                <tr><td class="col-free">16</td><td>$ 27.13</td><td>$ 563.85</td><td class="heat-bear">09:08:00 a. m.</td><td>$ 26.11</td><td>$ 542.64</td><td class="heat-bear">05:40:00 p. m.</td><td>$ 27.31</td><td>$ 567.73</td><td>$ 26.70</td><td>$ 554.97</td><td>4.63%</td><td>$ 1.21</td><td>$ 25.10</td><td class="bar-cell"><div class="bar-fill" style="width: 33%;"></div>$ 199,956,645.06</td><td class="bar-cell"><div class="bar-fill" style="width: 33%;"></div>$ 4,156,098,867.57</td><td>$ 4,015,072,650.20</td><td>$ 83,453,285,034.41</td><td>150,373,353</td></tr>
                                <tr><td class="col-free">15</td><td>$ 25.39</td><td>$ 522.69</td><td class="heat-bull">11:35:00 a. m.</td><td>$ 24.91</td><td>$ 512.72</td><td class="heat-bull">11:56:00 p. m.</td><td>$ 27.14</td><td>$ 558.77</td><td>$ 27.13</td><td>$ 558.42</td><td>8.98%</td><td>$ 2.24</td><td>$ 46.05</td><td class="bar-cell"><div class="bar-fill" style="width: 33%;"></div>$ 202,325,674.76</td><td class="bar-cell"><div class="bar-fill" style="width: 33%;"></div>$ 4,164,974,014.92</td><td>$ 4,079,909,561.52</td><td>$ 83,964,332,729.90</td><td>150,361,959</td></tr>
                                <tr><td class="col-free">14</td><td>$ 24.58</td><td>$ 507.45</td><td class="heat-bull">12:19:00 a. m.</td><td>$ 24.47</td><td>$ 505.30</td><td class="heat-bull">10:56:00 p. m.</td><td>$ 25.48</td><td>$ 526.16</td><td>$ 25.39</td><td>$ 524.31</td><td>4.13%</td><td>$ 1.01</td><td>$ 20.86</td><td class="bar-cell"><div class="bar-fill" style="width: 17%;"></div>$ 103,456,128.90</td><td class="bar-cell"><div class="bar-fill" style="width: 17%;"></div>$ 2,135,334,500.10</td><td>$ 3,817,543,900.20</td><td>$ 78,832,100,500.80</td><td>150,351,100</td></tr>
                                <tr><td class="col-free">13</td><td>$ 25.26</td><td>$ 527.07</td><td class="heat-bear">02:37:00 p. m.</td><td>$ 23.15</td><td>$ 483.10</td><td class="heat-bear">12:38:00 a. m.</td><td>$ 25.79</td><td>$ 538.09</td><td>$ 24.58</td><td>$ 513.11</td><td>-10.23%</td><td>$ 2.64</td><td>$ 54.99</td><td class="bar-cell"><div class="bar-fill" style="width: 50%;"></div>$ 305,456,789.20</td><td class="bar-cell"><div class="bar-fill" style="width: 50%;"></div>$ 6,375,110,400.50</td><td>$ 3,694,882,988.12</td><td>$ 77,112,450,100.30</td><td>150,340,200</td></tr>
                                <tr><td class="col-free">12</td><td>$ 25.55</td><td>$ 533.43</td><td class="heat-bear">10:29:00 p. m.</td><td>$ 25.01</td><td>$ 522.20</td><td class="heat-bear">02:41:00 a. m.</td><td>$ 25.74</td><td>$ 537.37</td><td>$ 25.26</td><td>$ 527.42</td><td>-2.83%</td><td>$ 0.73</td><td>$ 15.17</td><td class="bar-cell"><div class="bar-fill" style="width: 25%;"></div>$ 150,330,440.10</td><td class="bar-cell"><div class="bar-fill" style="width: 25%;"></div>$ 3,137,450,220.80</td><td>$ 3,797,110,500.40</td><td>$ 79,245,660,110.20</td><td>150,331,100</td></tr>
                                <tr><td class="col-free">11</td><td>$ 25.69</td><td>$ 536.42</td><td class="heat-bear">08:56:00 a. m.</td><td>$ 25.17</td><td>$ 525.55</td><td class="heat-bear">09:25:00 p. m.</td><td>$ 25.91</td><td>$ 540.92</td><td>$ 25.55</td><td>$ 533.50</td><td>-2.86%</td><td>$ 0.74</td><td>$ 15.37</td><td class="bar-cell"><div class="bar-fill" style="width: 20%;"></div>$ 120,440,550.30</td><td class="bar-cell"><div class="bar-fill" style="width: 20%;"></div>$ 2,513,440,200.50</td><td>$ 3,840,440,110.20</td><td>$ 80,185,440,220.10</td><td>150,320,500</td></tr>
                                <tr><td class="col-free">10</td><td>$ 24.87</td><td>$ 515.00</td><td class="heat-bull">12:28:00 a. m.</td><td>$ 24.85</td><td>$ 514.53</td><td class="heat-bull">08:13:00 p. m.</td><td>$ 25.88</td><td>$ 535.90</td><td>$ 25.69</td><td>$ 532.10</td><td>4.14%</td><td>$ 1.03</td><td>$ 21.37</td><td class="bar-cell"><div class="bar-fill" style="width: 28%;"></div>$ 168,550,220.40</td><td class="bar-cell"><div class="bar-fill" style="width: 28%;"></div>$ 3,518,440,100.20</td><td>$ 3,861,550,440.10</td><td>$ 80,014,550,200.80</td><td>150,311,200</td></tr>
                                <tr><td class="col-free">9</td><td>$ 25.27</td><td>$ 520.20</td><td class="heat-bear">08:40:00 p. m.</td><td>$ 24.37</td><td>$ 501.56</td><td class="heat-bear">01:31:00 a. m.</td><td>$ 25.57</td><td>$ 526.20</td><td>$ 24.87</td><td>$ 511.20</td><td>-4.69%</td><td>$ 1.20</td><td>$ 24.64</td><td class="bar-cell"><div class="bar-fill" style="width: 32%;"></div>$ 188,440,110.50</td><td class="bar-cell"><div class="bar-fill" style="width: 32%;"></div>$ 3,934,550,600.10</td><td>$ 3,738,110,500.20</td><td>$ 76,890,440,100.50</td><td>150,300,100</td></tr>
                                <tr><td class="col-free">8</td><td>$ 25.94</td><td>$ 530.75</td><td class="heat-bear">05:40:00 p. m.</td><td>$ 24.39</td><td>$ 498.95</td><td class="heat-bear">12:52:00 a. m.</td><td>$ 26.27</td><td>$ 537.49</td><td>$ 25.27</td><td>$ 516.40</td><td>-7.15%</td><td>$ 1.88</td><td>$ 38.54</td><td class="bar-cell"><div class="bar-fill" style="width: 40%;"></div>$ 240,110,550.80</td><td class="bar-cell"><div class="bar-fill" style="width: 40%;"></div>$ 5,012,440,100.20</td><td>$ 3,798,220,110.50</td><td>$ 77,654,110,200.40</td><td>150,290,400</td></tr>
                                <tr><td class="col-free">7</td><td>$ 26.88</td><td>$ 555.28</td><td class="heat-bear">07:44:00 a. m.</td><td>$ 26.62</td><td>$ 550.03</td><td class="heat-bear">11:07:00 p. m.</td><td>$ 28.46</td><td>$ 587.99</td><td>$ 25.94</td><td>$ 535.10</td><td>-6.47%</td><td>$ 1.84</td><td>$ 37.96</td><td class="bar-cell"><div class="bar-fill" style="width: 36%;"></div>$ 215,440,110.20</td><td class="bar-cell"><div class="bar-fill" style="width: 36%;"></div>$ 4,498,550,200.10</td><td>$ 3,898,440,100.50</td><td>$ 80,456,110,300.20</td><td>150,281,500</td></tr>
                                <tr><td class="col-free">6</td><td>$ 28.12</td><td>$ 578.74</td><td class="heat-bear">01:22:00 a. m.</td><td>$ 27.78</td><td>$ 571.80</td><td class="heat-bear">04:34:00 p. m.</td><td>$ 29.18</td><td>$ 600.54</td><td>$ 26.88</td><td>$ 553.40</td><td>-4.97%</td><td>$ 1.40</td><td>$ 28.74</td><td class="bar-cell"><div class="bar-fill" style="width: 45%;"></div>$ 265,110,400.80</td><td class="bar-cell"><div class="bar-fill" style="width: 45%;"></div>$ 5,456,110,200.50</td><td>$ 4,039,550,200.10</td><td>$ 83,145,220,100.40</td><td>150,270,100</td></tr>
                                <tr><td class="col-free">5</td><td>$ 28.39</td><td>$ 590.51</td><td class="heat-bear">02:19:00 p. m.</td><td>$ 27.48</td><td>$ 571.56</td><td class="heat-bear">12:16:00 a. m.</td><td>$ 28.56</td><td>$ 594.02</td><td>$ 28.12</td><td>$ 584.10</td><td>-3.79%</td><td>$ 1.08</td><td>$ 22.46</td><td class="bar-cell"><div class="bar-fill" style="width: 29%;"></div>$ 170,440,500.10</td><td class="bar-cell"><div class="bar-fill" style="width: 29%;"></div>$ 3,546,110,200.80</td><td>$ 4,225,110,400.50</td><td>$ 87,845,110,200.10</td><td>150,260,800</td></tr>
                                <tr><td class="col-free">4</td><td>$ 28.43</td><td>$ 589.02</td><td class="heat-bear">03:46:00 p. m.</td><td>$ 27.95</td><td>$ 579.18</td><td class="heat-bear">01:17:00 p. m.</td><td>$ 28.75</td><td>$ 595.72</td><td>$ 28.39</td><td>$ 588.10</td><td>-2.78%</td><td>$ 0.80</td><td>$ 16.54</td><td class="bar-cell"><div class="bar-fill" style="width: 22%;"></div>$ 130,110,400.50</td><td class="bar-cell"><div class="bar-fill" style="width: 22%;"></div>$ 2,694,110,500.20</td><td>$ 4,266,440,100.80</td><td>$ 88,412,550,100.40</td><td>150,250,400</td></tr>
                                <tr><td class="col-free">3</td><td>$ 26.88</td><td>$ 555.28</td><td class="heat-bull">07:44:00 a. m.</td><td>$ 26.62</td><td>$ 550.03</td><td class="heat-bull">11:07:00 p. m.</td><td>$ 28.46</td><td>$ 587.99</td><td>$ 28.43</td><td>$ 587.20</td><td>6.85%</td><td>$ 1.84</td><td>$ 37.96</td><td class="bar-cell"><div class="bar-fill" style="width: 38%;"></div>$ 225,110,400.20</td><td class="bar-cell"><div class="bar-fill" style="width: 38%;"></div>$ 4,698,550,100.50</td><td>$ 4,271,440,500.10</td><td>$ 88,245,110,400.80</td><td>150,240,100</td></tr>
                                <tr><td class="col-free">2</td><td>$ 25.76</td><td>$ 475.75</td><td class="heat-bull">12:01:00 a. m.</td><td>$ 25.75</td><td>$ 475.66</td><td class="heat-bull">11:49:00 a. m.</td><td>$ 27.01</td><td>$ 498.80</td><td>$ 26.88</td><td>$ 496.40</td><td>4.85%</td><td>$ 1.26</td><td>$ 23.14</td><td class="bar-cell"><div class="bar-fill" style="width: 25%;"></div>$ 145,110,500.80</td><td class="bar-cell"><div class="bar-fill" style="width: 25%;"></div>$ 3,015,440,200.10</td><td>$ 4,038,110,400.50</td><td>$ 74,560,720,320.00</td><td>150,230,500</td></tr>
                                <tr><td class="col-free">1</td><td>$ 25.01</td><td>$ 523.80</td><td class="heat-bull">11:08:00 a. m.</td><td>$ 24.63</td><td>$ 515.76</td><td class="heat-bull">09:37:00 p. m.</td><td>$ 25.89</td><td>$ 542.21</td><td>$ 25.76</td><td>$ 539.10</td><td>5.11%</td><td>$ 1.26</td><td>$ 26.45</td><td class="bar-cell"><div class="bar-fill" style="width: 20%;"></div>$ 118,440,200.10</td><td class="bar-cell"><div class="bar-fill" style="width: 20%;"></div>$ 2,456,110,500.80</td><td>$ 3,869,440,500.20</td><td>$ 80,985,440,100.50</td><td>150,220,100</td></tr>
                            </tbody>
                        </table>
                    </div>
"""

with open('c:/Users/52777/Desktop/Desarrollo_Fincesstrategy/fincess/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_start = content.find("/* 8. MÓDULO ANÁLISIS QUANT")
css_end = content.find("</style>")

if css_start != -1 and css_end != -1:
    content = content[:css_start] + css_replacement + "    " + content[css_end:]

# 2. Update HTML
html_start = content.find('<div class="quant-header-group">')
html_end = content.find('</section>', html_start)

if html_start != -1 and html_end != -1:
    content = content[:html_start] + html_replacement + "                " + content[html_end:]

with open('c:/Users/52777/Desktop/Desarrollo_Fincesstrategy/fincess/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully")
