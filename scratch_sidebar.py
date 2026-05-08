import sys

css_replacement = """        /* 5. BARRA LATERAL (SIDEBAR) - ESTILO CHAINX */
        .sidebar { width: var(--sb-expanded); background: var(--bg-main); /* Usa el fondo más oscuro */ border-right: 1px solid var(--border); display: flex; flex-direction: column; transition: width var(--transition); padding: 24px 20px; flex-shrink: 0; z-index: 10; }
        .sidebar.collapsed { width: var(--sb-collapsed); padding: 24px 12px; }
        
        .sidebar-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 32px; padding: 0 4px; }
        .brand { display: flex; align-items: center; gap: 12px; font-weight: 600; font-size: 1.3rem; letter-spacing: 0.5px; color: var(--text); }
        .brand i { color: #fff; font-size: 1.4rem; }
        
        #btn-toggle { background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 0.9rem; transition: 0.2s; padding: 4px; }
        #btn-toggle:hover { color: var(--text); }

        .nav-menu { display: flex; flex-direction: column; gap: 4px; flex-grow: 1; overflow-y: auto; overflow-x: hidden; }
        .nav-menu::-webkit-scrollbar { width: 4px; }
        .nav-menu::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

        .nav-item { display: flex; align-items: center; gap: 16px; padding: 12px 16px; border-radius: 12px; color: var(--text-muted); text-decoration: none; font-weight: 500; font-size: 0.9rem; transition: all 0.2s ease; border: none !important; }
        .nav-item:hover { color: var(--text); background-color: rgba(255, 255, 255, 0.03); }
        .nav-item i { font-size: 1.1rem; min-width: 20px; text-align: center; }

        /* Píldora Activa Estilo Chainx */
        .nav-item.active { background-color: #1e2235; color: #fff; }
        .nav-item.active i { color: #818cf8; } /* Icono con ligero tono azul/púrpura */

        /* Sub-menú colapsable */
        .nav-group { display: flex; flex-direction: column; }
        .sub-menu { margin-left: 26px; padding-left: 16px; border-left: 1px solid var(--border); display: flex; flex-direction: column; gap: 12px; margin-top: 4px; margin-bottom: 8px; }
        .sub-item { font-size: 0.85rem; color: var(--text-muted); text-decoration: none; transition: 0.2s; font-weight: 400; }
        .sub-item:hover { color: var(--text); }

        /* Divisores */
        .nav-divider { height: 1px; background: var(--border); margin: 12px 0; opacity: 0.5; }

        /* Footer de Sidebar (Upgrade & Toggle) */
        .sidebar-footer { padding-top: 16px; display: flex; flex-direction: column; gap: 16px; }
        
        .upgrade-card { background: linear-gradient(135deg, #2b1b54 0%, #151136 100%); border-radius: 14px; padding: 18px 16px; border: 1px solid rgba(139, 92, 246, 0.2); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .upgrade-card h4 { font-size: 0.9rem; color: #fff; margin-bottom: 6px; display: flex; align-items: center; gap: 10px; font-weight: 600; }
        .upgrade-card p { font-size: 0.75rem; color: rgba(255, 255, 255, 0.6); line-height: 1.4; }

        .chainx-toggle-row { display: flex; justify-content: space-between; align-items: center; color: var(--text-muted); font-size: 0.85rem; padding: 0 4px; font-weight: 500; }
        .c-switch { position: relative; width: 40px; height: 22px; appearance: none; background: var(--border); border-radius: 20px; outline: none; cursor: pointer; transition: 0.3s; }
        .c-switch:checked { background: #6366f1; }
        .c-switch::after { content: ''; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; background: white; border-radius: 50%; transition: 0.3s; }
        .c-switch:checked::after { transform: translateX(18px); }

        /* Colapso de Sidebar */
        .sidebar.collapsed .brand span, .sidebar.collapsed .nav-item span, .sidebar.collapsed .sub-menu, .sidebar.collapsed .nav-item .fa-chevron-up, .sidebar.collapsed .upgrade-card, .sidebar.collapsed .chainx-toggle-row span { display: none; }
        .sidebar.collapsed .nav-item { justify-content: center; padding: 12px 0; }
        .sidebar.collapsed .chainx-toggle-row { justify-content: center; }"""

html_replacement = """            <aside id="sidebar" class="sidebar">
                <div class="sidebar-header">
                    <div class="brand"><i class="fas fa-layer-group"></i><span>Finces</span></div>
                    <button id="btn-toggle" title="Colapsar menú"><i class="fas fa-angle-double-left"></i></button>
                </div>
                
                <nav class="nav-menu">
                    <a href="#" class="nav-item" data-page="terminal"><i class="fas fa-border-all"></i><span>Dashboard</span></a>
                    <a href="#" class="nav-item" data-page="summary"><i class="fas fa-chalkboard-teacher"></i><span>Market Summary</span></a>
                    
                    <div class="nav-group">
                        <a href="#" class="nav-item" data-page="portfolio" style="justify-content: space-between;">
                            <div style="display: flex; gap: 16px; align-items: center;"><i class="fas fa-suitcase"></i><span>Portfolio</span></div>
                            <i class="fas fa-chevron-up" style="font-size: 0.7rem;"></i>
                        </a>
                        <div class="sub-menu">
                            <a href="#" class="sub-item">Stocks</a>
                            <a href="#" class="sub-item">Bonds</a>
                            <a href="#" class="sub-item">Mutual Funds</a>
                        </div>
                    </div>

                    <a href="#" class="nav-item active" data-page="analisis"><i class="fas fa-chart-line"></i><span>Analytics</span></a>
                    <a href="#" class="nav-item" data-page="wallet"><i class="fas fa-wallet"></i><span>Wallet</span></a>
                    <a href="#" class="nav-item" data-page="community"><i class="fas fa-globe"></i><span>Community</span></a>

                    <div class="nav-divider"></div>

                    <a href="#" class="nav-item" data-page="config"><i class="fas fa-cog"></i><span>Settings</span></a>
                    <a href="#" class="nav-item" data-page="help"><i class="fas fa-info-circle"></i><span>Help & Support</span></a>
                </nav>

                <div class="sidebar-footer">
                    <div class="upgrade-card">
                        <h4><i class="fas fa-shopping-basket"></i> Upgrade</h4>
                        <p>Unlock all Finces features</p>
                    </div>
                    
                    <div class="chainx-toggle-row">
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <i class="fas fa-moon"></i> <span>Dark Mode</span>
                        </div>
                        <input type="checkbox" class="c-switch" checked id="theme-toggle-switch">
                    </div>
                </div>
            </aside>"""

with open('c:/Users/52777/Desktop/Desarrollo_Fincesstrategy/fincess/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_start = content.find("/* 5. BARRA LATERAL (SIDEBAR) */")
css_end = content.find("/* 6. ÁREA DE CONTENIDO (Main View) */")

if css_start != -1 and css_end != -1:
    content = content[:css_start] + css_replacement + "\n\n        " + content[css_end:]
else:
    print("CSS block not found")
    sys.exit(1)

# 2. Update HTML
html_start = content.find('<aside id="sidebar" class="sidebar">')
html_end = content.find('</aside>', html_start) + len('</aside>')

if html_start != -1 and html_end != -1:
    content = content[:html_start] + html_replacement + content[html_end:]
else:
    print("HTML block not found")
    sys.exit(1)

with open('c:/Users/52777/Desktop/Desarrollo_Fincesstrategy/fincess/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully")
