import sys

css_replacement = """        /* Bento Grid Institucional (Récords KPI) */
        .bento-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .bento-card { background: var(--bg-side); border: 1px solid var(--border); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
        .bento-header { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }

        .b-block { display: flex; flex-direction: column; gap: 8px; }
        .b-block-header { display: flex; justify-content: space-between; align-items: baseline; }
        .b-title { font-size: 0.8rem; font-weight: 500; color: var(--text-muted); }
        .b-meta { font-size: 0.75rem; color: var(--text-muted); font-weight: 400; text-align: right; }

        /* Micro-Cajas para separar monedas */
        .b-values { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: var(--bg-main); padding: 10px 12px; border-radius: 8px; border: 1px solid rgba(139, 142, 159, 0.1); }
        .b-val-item { display: flex; flex-direction: column; gap: 2px; }
        .b-cur { font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
        .b-num { font-size: 0.95rem; color: var(--text); font-weight: 600; font-variant-numeric: tabular-nums; }

        /* Separador sutil entre registros de la misma tarjeta */
        .b-divider { border: none; border-top: 1px dashed var(--border); margin: 16px 0; opacity: 0.6; }"""

html_replacement = """                    <div class="bento-grid">
                        
                        <div class="bento-card">
                            <div class="bento-header"><i class="fas fa-door-open"></i> Extremos de Apertura</div>
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Apertura Máxima</span><span class="b-meta">Día 24</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 29.04</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 592.61</span></div>
                                </div>
                            </div>
                            <hr class="b-divider">
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Apertura Mínima</span><span class="b-meta">Día 14</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 24.58</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 475.75</span></div>
                                </div>
                            </div>
                        </div>

                        <div class="bento-card">
                            <div class="bento-header"><i class="fas fa-arrow-trend-down"></i> Mínimos del Periodo</div>
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Mínimo Máximo</span><span class="b-meta">Día 4 &bull; 03:46 p. m.</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 27.95</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 579.18</span></div>
                                </div>
                            </div>
                            <hr class="b-divider">
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Mínimo Absoluto</span><span class="b-meta">Día 13 &bull; 02:37 p. m.</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 23.15</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 475.66</span></div>
                                </div>
                            </div>
                        </div>

                        <div class="bento-card">
                            <div class="bento-header"><i class="fas fa-arrow-trend-up"></i> Máximos del Periodo</div>
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Máximo Absoluto</span><span class="b-meta">Día 24 &bull; 12:05 a. m.</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 29.18</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 600.54</span></div>
                                </div>
                            </div>
                            <hr class="b-divider">
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Máximo Mínimo</span><span class="b-meta">Día 14 &bull; 10:56 p. m.</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 25.48</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 498.80</span></div>
                                </div>
                            </div>
                        </div>

                        <div class="bento-card">
                            <div class="bento-header"><i class="fas fa-door-closed"></i> Extremos de Cierre</div>
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Cierre Máximo</span><span class="b-meta">Día 23</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 29.04</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 595.81</span></div>
                                </div>
                            </div>
                            <hr class="b-divider">
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Cierre Mínimo</span><span class="b-meta">Día 13</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 24.58</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 496.42</span></div>
                                </div>
                            </div>
                        </div>

                        <div class="bento-card">
                            <div class="bento-header"><i class="fas fa-water"></i> Volumen Transado</div>
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Volumen Máximo</span><span class="b-meta">Día 23</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 585,611,931</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 12,015,292,798</span></div>
                                </div>
                            </div>
                            <hr class="b-divider">
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Volumen Mínimo</span><span class="b-meta">Día 30</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 130,801,398</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 2,694,508,811</span></div>
                                </div>
                            </div>
                        </div>

                        <div class="bento-card">
                            <div class="bento-header"><i class="fas fa-coins"></i> Cap. de Mercado</div>
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Capitalización Máxima</span><span class="b-meta">Día 23</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 4,369,365,303</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 89,648,452,606</span></div>
                                </div>
                            </div>
                            <hr class="b-divider">
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Capitalización Mínima</span><span class="b-meta">Día 2</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 3,694,882,988</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 74,560,720,320</span></div>
                                </div>
                            </div>
                        </div>

                        <div class="bento-card">
                            <div class="bento-header"><i class="fas fa-wave-square"></i> Fluctuaciones</div>
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Fluctuación Máxima</span><span class="b-meta">Día 19</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 3.07</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 65.30</span></div>
                                </div>
                            </div>
                            <hr class="b-divider">
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Fluctuación Mínima</span><span class="b-meta">Día 12</span></div>
                                <div class="b-values">
                                    <div class="b-val-item"><span class="b-cur">USDT</span><span class="b-num">$ 0.73</span></div>
                                    <div class="b-val-item"><span class="b-cur">MXN</span><span class="b-num">$ 15.17</span></div>
                                </div>
                            </div>
                        </div>

                        <div class="bento-card">
                            <div class="bento-header"><i class="fas fa-exclamation-triangle"></i> Volatilidad</div>
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Volatilidad Máxima</span><span class="b-meta">Día 19</span></div>
                                <div class="b-values" style="grid-template-columns: 1fr;">
                                    <div class="b-val-item"><span class="b-cur">Porcentaje (%)</span><span class="b-num">12.00%</span></div>
                                </div>
                            </div>
                            <hr class="b-divider">
                            <div class="b-block">
                                <div class="b-block-header"><span class="b-title">Volatilidad Mínima</span><span class="b-meta">Día 13</span></div>
                                <div class="b-values" style="grid-template-columns: 1fr;">
                                    <div class="b-val-item"><span class="b-cur">Porcentaje (%)</span><span class="b-num">-10.00%</span></div>
                                </div>
                            </div>
                        </div>

                    </div>"""

with open('c:/Users/52777/Desktop/Desarrollo_Fincesstrategy/fincess/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_start = content.find("/* Bento Grid (Récords KPI) */")
css_end = content.find("/* Contenedor de la Tabla */")

if css_start != -1 and css_end != -1:
    content = content[:css_start] + css_replacement + "\n\n        " + content[css_end:]
else:
    print("CSS block not found")

# 2. Update HTML
html_start = content.find('<div class="bento-grid">')
html_end = content.find('<div class="quant-container">', html_start)

if html_start != -1 and html_end != -1:
    content = content[:html_start] + html_replacement + "\n\n                    " + content[html_end:]
else:
    print("HTML block not found")

with open('c:/Users/52777/Desktop/Desarrollo_Fincesstrategy/fincess/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch 2 applied successfully")
