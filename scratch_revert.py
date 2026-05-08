import sys

css_replacement = """        /* 5. BARRA LATERAL (SIDEBAR) */
        .sidebar {
            width: var(--sb-expanded);
            background: var(--bg-side);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            transition: width var(--transition);
            padding: 24px 16px;
            flex-shrink: 0;
            z-index: 10;
        }

        .sidebar.collapsed {
            width: var(--sb-collapsed);
            padding: 24px 8px;
        }

        .sidebar-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 40px;
            padding: 0 8px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 500;
            font-size: 1.25rem;
            letter-spacing: 0.5px;
        }

        .brand i {
            color: var(--accent);
            font-size: 1.5rem;
        }

        #btn-toggle {
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 1rem;
            transition: 0.2s;
        }

        #btn-toggle:hover {
            color: var(--text);
        }

        .nav-menu {
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex-grow: 1;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 12px 16px;
            border-radius: 12px;
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 400;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            border-left: 3px solid transparent;
            white-space: nowrap;
        }

        .nav-item:hover {
            color: var(--text);
            background-color: rgba(36, 33, 217, 0.05);
        }

        .nav-item i {
            font-size: 1.1rem;
            min-width: 20px;
            text-align: center;
        }

        /* Píldora Activa */
        .nav-item.active {
            background-color: rgba(36, 33, 217, 0.15);
            color: var(--text);
            border-left: 3px solid var(--accent);
        }

        .nav-item.active i {
            color: var(--accent);
        }

        /* Sidebar Footer & Theme Controls */
        .sidebar-footer {
            border-top: 1px solid var(--border);
            padding-top: 24px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .theme-controls {
            display: flex;
            gap: 8px;
            background: var(--bg-main);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid var(--border);
        }

        .t-btn {
            flex: 1;
            background: none;
            border: none;
            color: var(--text-muted);
            padding: 8px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
            font-size: 1rem;
        }

        .t-btn:hover {
            color: var(--text);
        }

        .t-btn.active {
            background: var(--bg-side);
            color: var(--accent);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        #btn-logout-new {
            background: none;
            border: none;
            font-family: inherit;
            width: 100%;
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 12px 16px;
            border-radius: 12px;
            color: var(--color-bear);
            font-weight: 400;
            font-size: 0.95rem;
            cursor: pointer;
            transition: 0.2s;
            white-space: nowrap;
        }

        #btn-logout-new:hover {
            background-color: rgba(239, 68, 68, 0.1);
        }

        #btn-logout-new i {
            font-size: 1.1rem;
            min-width: 20px;
            text-align: center;
        }

        /* Sidebar Colapsada */
        .sidebar.collapsed .brand span,
        .sidebar.collapsed .nav-item span,
        .sidebar.collapsed #btn-logout-new span {
            display: none;
        }

        .sidebar.collapsed .nav-item {
            justify-content: center;
            padding: 12px 0;
        }

        .sidebar.collapsed .theme-controls {
            flex-direction: column;
        }

        .sidebar.collapsed #btn-logout-new {
            justify-content: center;
            padding: 12px 0;
        }"""

html_replacement = """            <aside id="sidebar" class="sidebar">
                <div class="sidebar-header">
                    <div class="brand"><i class="fas fa-layer-group"></i><span>Finces</span></div>
                    <button id="btn-toggle"><i class="fas fa-chevron-left"></i></button>
                </div>
                <nav class="nav-menu">
                    <a href="#" class="nav-item active" data-page="terminal"><i
                            class="fas fa-chart-line"></i><span>Terminal</span></a>
                    <a href="#" class="nav-item" data-page="portfolio"><i
                            class="fas fa-wallet"></i><span>Portafolio</span></a>
                    <a href="#" class="nav-item" data-page="analisis"><i class="fas fa-microchip"></i><span>Análisis
                            Quant</span></a>
                    <a href="#" class="nav-item" data-page="config"><i
                            class="fas fa-sliders-h"></i><span>Ajustes</span></a>
                </nav>
                <div class="sidebar-footer">
                    <div class="theme-controls">
                        <button class="t-btn" data-t="light" title="Modo Claro"><i class="fas fa-sun"></i></button>
                        <button class="t-btn" data-t="dark" title="Modo Oscuro"><i class="fas fa-moon"></i></button>
                        <button class="t-btn" data-t="system" title="Tema del Sistema"><i
                                class="fas fa-desktop"></i></button>
                    </div>
                    <button id="btn-logout-new"><i class="fas fa-sign-out-alt"></i><span>Desconectar</span></button>
                </div>
            </aside>"""

with open('c:/Users/52777/Desktop/Desarrollo_Fincesstrategy/fincess/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_start = content.find("/* 5. BARRA LATERAL (SIDEBAR) - ESTILO CHAINX */")
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

print("Revert applied successfully")
