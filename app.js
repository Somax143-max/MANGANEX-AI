// MANGANEX AI Frontend Engine v4.1 (Decoupled Vercel + Render Support)
let map = null;
let mapMarkersLayer = null;
let chartStatePot = null;
let chartStateShort = null;
let chartProdComp = null;
let chartRiskPie = null;
let chartSimXAI = null;

// =============================================================
// API BASE URL CONFIGURATION (Supports Vercel -> Render cross-origin)
// =============================================================
function getApiBaseUrl() {
    if (window.__MANGANEX_API_URL__) {
        return window.__MANGANEX_API_URL__.replace(/\/+$/, '');
    }
    const saved = localStorage.getItem('MANGANEX_RENDER_API_URL');
    if (saved) {
        return saved.trim().replace(/\/+$/, '');
    }
    return ''; // Same-origin relative path fallback
}

function apiUrl(path) {
    const base = getApiBaseUrl();
    const cleanPath = path.startsWith('/') ? path : '/' + path;
    return base ? `${base}${cleanPath}` : cleanPath;
}

// Update UI Badge
function updateBackendStatusBadge(status, label) {
    const dot = document.getElementById('backend-status-dot');
    const text = document.getElementById('backend-status-text');
    if (!dot || !text) return;

    if (status === 'connected') {
        dot.className = 'w-2 h-2 rounded-full bg-emerald-400';
        text.innerText = label || 'Render Backend: Connected';
        text.className = 'text-emerald-400 font-semibold text-xs';
    } else if (status === 'connecting') {
        dot.className = 'w-2 h-2 rounded-full bg-amber-400 animate-pulse';
        text.innerText = label || 'Backend: Connecting...';
        text.className = 'text-amber-400 font-semibold text-xs';
    } else {
        dot.className = 'w-2 h-2 rounded-full bg-rose-400';
        text.innerText = label || 'Backend: Disconnected';
        text.className = 'text-rose-400 font-semibold text-xs';
    }
}

async function checkBackendHealth() {
    updateBackendStatusBadge('connecting', 'Connecting...');
    try {
        const res = await fetch(apiUrl('/health'), { method: 'GET' });
        if (res.ok) {
            const data = await res.json();
            const host = getApiBaseUrl() ? new URL(getApiBaseUrl()).hostname : 'Render / Local';
            updateBackendStatusBadge('connected', `API: ${host}`);
        } else {
            updateBackendStatusBadge('error', 'API HTTP Error');
        }
    } catch (e) {
        console.warn('Backend health check failed:', e);
        updateBackendStatusBadge('error', 'Set Render URL');
    }
}

// Initialize when DOM loaded
document.addEventListener("DOMContentLoaded", () => {
    if (typeof lucide !== 'undefined') lucide.createIcons();
    checkBackendHealth();
    loadSummaryData();
    initSimXAIChart();
    runInference(); // Run default simulation
});

// Modal handlers for setting Render backend URL
function openApiConfigModal() {
    const input = document.getElementById('input-backend-url');
    if (input) input.value = getApiBaseUrl();
    const modal = document.getElementById('modal-api-config');
    if (modal) modal.classList.remove('hidden');
}

function closeApiConfigModal() {
    const modal = document.getElementById('modal-api-config');
    if (modal) modal.classList.add('hidden');
}

async function testAndSaveBackendUrl() {
    const input = document.getElementById('input-backend-url');
    const resBox = document.getElementById('api-test-result');
    const testUrl = input.value.trim().replace(/\/+$/, '');

    resBox.classList.remove('hidden', 'bg-emerald-950', 'bg-rose-950', 'text-emerald-300', 'text-rose-300', 'border-emerald-700', 'border-rose-700');
    resBox.classList.add('bg-slate-900', 'text-slate-300', 'border', 'border-slate-700');
    resBox.innerText = 'Testing connection to ' + (testUrl || 'same-origin') + '...';

    try {
        const healthEndpoint = testUrl ? `${testUrl}/health` : '/health';
        const res = await fetch(healthEndpoint);
        if (res.ok) {
            const data = await res.json();
            resBox.classList.remove('bg-slate-900', 'text-slate-300', 'border-slate-700');
            resBox.classList.add('bg-emerald-950/80', 'text-emerald-300', 'border', 'border-emerald-700');
            resBox.innerText = `✅ Connected successfully! (${data.service} v${data.version})`;

            if (testUrl) {
                localStorage.setItem('MANGANEX_RENDER_API_URL', testUrl);
            } else {
                localStorage.removeItem('MANGANEX_RENDER_API_URL');
            }

            setTimeout(() => {
                closeApiConfigModal();
                checkBackendHealth();
                loadSummaryData();
                loadGISZones();
                runInference();
            }, 800);
        } else {
            throw new Error(`HTTP status ${res.status}`);
        }
    } catch (err) {
        resBox.classList.remove('bg-slate-900', 'text-slate-300', 'border-slate-700');
        resBox.classList.add('bg-rose-950/80', 'text-rose-300', 'border', 'border-rose-700');
        resBox.innerText = `❌ Connection failed: ${err.message}. Please check CORS or URL.`;
    }
}

function resetBackendUrl() {
    localStorage.removeItem('MANGANEX_RENDER_API_URL');
    const input = document.getElementById('input-backend-url');
    if (input) input.value = '';
    testAndSaveBackendUrl();
}

// Tab Navigation
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.getElementById(tabId).classList.remove('hidden');

    document.querySelectorAll('.nav-tab').forEach(btn => {
        btn.classList.remove('bg-cyan-600', 'text-white', 'shadow');
        btn.classList.add('text-slate-400');
    });

    const activeBtn = document.getElementById(tabId.replace('tab-', 'nav-'));
    if (activeBtn) {
        activeBtn.classList.add('bg-cyan-600', 'text-white', 'shadow');
        activeBtn.classList.remove('text-slate-400');
    }

    // Refresh map if switching to GIS tab
    if (tabId === 'tab-gis') {
        setTimeout(() => {
            if (!map) {
                initLeafletMap();
            } else {
                map.invalidateSize();
            }
        }, 150);
    }
}

// -------------------------------------------------------------
// Load Summary & Charts
// -------------------------------------------------------------
async function loadSummaryData() {
    try {
        const res = await fetch(apiUrl('/api/summary'));
        const data = await res.json();

        // Update KPIs
        document.getElementById('kpi-potential').innerText = `${data.kpis.total_potential_mt} M t`;
        document.getElementById('kpi-historical').innerText = `${data.kpis.total_historical_mt} M t`;
        document.getElementById('kpi-predicted').innerText = `${data.kpis.total_predicted_mt} M t`;
        document.getElementById('kpi-shortfall').innerText = `${data.kpis.total_shortfall_mt} M t`;
        document.getElementById('kpi-gap').innerText = `-${data.kpis.national_gap_pct}% Deficit Gap`;
        document.getElementById('kpi-tier1').innerText = data.kpis.tier1_zones_count;

        // Render State Potential Bar Chart
        const potCtx = document.getElementById('chart-state-potential').getContext('2d');
        const potLabels = Object.keys(data.state_potential_mt);
        const potValues = Object.values(data.state_potential_mt);
        if (chartStatePot) chartStatePot.destroy();
        chartStatePot = new Chart(potCtx, {
            type: 'bar',
            data: {
                labels: potLabels,
                datasets: [{
                    label: 'Potential (Million Tonnes)',
                    data: potValues,
                    backgroundColor: '#0284c7',
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { display: false } },
                    y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1e293b' } }
                }
            }
        });

        // Render State Shortfall Bar Chart
        const shortCtx = document.getElementById('chart-state-shortfall').getContext('2d');
        const shortLabels = Object.keys(data.state_shortfall_kt);
        const shortValues = Object.values(data.state_shortfall_kt);
        if (chartStateShort) chartStateShort.destroy();
        chartStateShort = new Chart(shortCtx, {
            type: 'bar',
            data: {
                labels: shortLabels,
                datasets: [{
                    label: 'Shortfall (Thousand Tonnes)',
                    data: shortValues,
                    backgroundColor: '#f97316',
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { display: false } },
                    y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1e293b' } }
                }
            }
        });

        // Render Production Comparison Bar Chart
        const prodCtx = document.getElementById('chart-prod-comparison').getContext('2d');
        if (chartProdComp) chartProdComp.destroy();
        chartProdComp = new Chart(prodCtx, {
            type: 'bar',
            data: {
                labels: ['Historical Baseline', 'AI Forecasted Output', 'Predicted Shortfall'],
                datasets: [{
                    data: [data.kpis.total_historical_tonnes, data.kpis.total_predicted_tonnes, data.kpis.total_shortfall_tonnes],
                    backgroundColor: ['#0284c7', '#38bdf8', '#ef4444'],
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
                    y: { ticks: { color: '#94a3b8', callback: v => (v / 1e6).toFixed(1) + 'M t' }, grid: { color: '#1e293b' } }
                }
            }
        });

        // Render Risk Doughnut
        const riskCtx = document.getElementById('chart-risk-pie').getContext('2d');
        if (chartRiskPie) chartRiskPie.destroy();
        chartRiskPie = new Chart(riskCtx, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: [data.risk_distribution['Low'] || 0, data.risk_distribution['Medium'] || 0, data.risk_distribution['High'] || 0],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderColor: '#111827',
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#cbd5e1', boxWidth: 12, font: { size: 11 } } }
                }
            }
        });

        // Populate Top Targets Table
        const targetTable = document.getElementById('table-top-targets');
        targetTable.innerHTML = data.top_targets.map(t => `
            <tr class="hover:bg-slate-800/40 transition">
                <td class="py-2.5 px-3 font-semibold text-cyan-400 font-mono">${t.zone_id}</td>
                <td class="py-2.5 px-3">${t.state}</td>
                <td class="py-2.5 px-3">${t.district}</td>
                <td class="py-2.5 px-3 text-slate-400">${t.mining_belt}</td>
                <td class="py-2.5 px-3 font-semibold text-amber-400">${t.ore_grade_percent}%</td>
                <td class="py-2.5 px-3 font-bold text-emerald-400">${(t.prospectivity_score * 100).toFixed(1)}%</td>
                <td class="py-2.5 px-3">${Math.round(t.predicted_manganese_reserve_tonnes).toLocaleString()} t</td>
                <td class="py-2.5 px-3">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold ${
                        t.risk_level === 'High' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                        t.risk_level === 'Medium' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                        'bg-emerald-950 text-emerald-300 border border-emerald-800'
                    }">${t.risk_level}</span>
                </td>
            </tr>
        `).join('');

        // Populate Shortfall Hotspots Table
        const shortTable = document.getElementById('table-shortfall-hotspots');
        shortTable.innerHTML = data.top_targets.map(t => `
            <tr class="hover:bg-slate-800/40 transition">
                <td class="py-2 px-3 font-semibold text-cyan-400 font-mono">${t.zone_id}</td>
                <td class="py-2 px-3">${t.state}</td>
                <td class="py-2 px-3">${t.district}</td>
                <td class="py-2 px-3">${Math.round(t.historical_production_tonnes).toLocaleString()}</td>
                <td class="py-2 px-3">${Math.round(t.predicted_production_tonnes).toLocaleString()}</td>
                <td class="py-2 px-3 font-bold text-rose-400">${Math.round(t.production_shortfall_tonnes).toLocaleString()} t</td>
                <td class="py-2 px-3 font-semibold text-rose-400">-${t.production_gap_percent}%</td>
                <td class="py-2 px-3">${(t.equipment_efficiency * 100).toFixed(0)}%</td>
                <td class="py-2 px-3">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold ${
                        t.risk_level === 'High' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                        t.risk_level === 'Medium' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                        'bg-emerald-950 text-emerald-300 border border-emerald-800'
                    }">${t.risk_level}</span>
                </td>
            </tr>
        `).join('');

    } catch (err) {
        console.error("Error loading summary data:", err);
    }
}

// -------------------------------------------------------------
// Interactive Leaflet Map (Guaranteed 100% Free Open Layers)
// -------------------------------------------------------------
function initLeafletMap() {
    map = L.map('map', {
        center: [21.5, 80.0],
        zoom: 5,
        zoomControl: true,
    });

    // 1. OpenStreetMap
    const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    });

    // 2. ESRI Dark Gray Canvas
    const darkLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; Esri, HERE, Garmin, METI/NASA, USGS',
        maxZoom: 16
    });

    // 3. ESRI Satellite Imagery
    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; Esri, Maxar, Earthstar Geographics',
        maxZoom: 18
    });

    darkLayer.addTo(map);

    const baseMaps = {
        "🌑 Dark Theme Map": darkLayer,
        "🗺️ Standard OpenStreetMap": osmLayer,
        "🛰️ Space Satellite Imagery": satelliteLayer
    };
    L.control.layers(baseMaps, null, { position: 'topright' }).addTo(map);

    mapMarkersLayer = L.layerGroup().addTo(map);
    loadGISZones();
}

async function loadGISZones() {
    if (!map) return;
    const state = document.getElementById('gis-filter-state').value;
    const minScore = document.getElementById('gis-filter-score').value;
    const minGrade = document.getElementById('gis-filter-grade').value;

    try {
        const url = apiUrl(`/api/zones?state=${encodeURIComponent(state)}&min_prospectivity=${minScore}&min_grade=${minGrade}`);
        const res = await fetch(url);
        const data = await res.json();

        // Populate State dropdown if needed
        const stateSelect = document.getElementById('gis-filter-state');
        if (stateSelect.options.length <= 1 && data.available_states) {
            stateSelect.innerHTML = data.available_states.map(s => `<option value="${s}">${s}</option>`).join('');
            stateSelect.value = state;
        }

        document.getElementById('gis-matching-count').innerText = data.total_matching;

        // Clear existing markers
        mapMarkersLayer.clearLayers();

        data.zones.forEach(z => {
            const scorePct = (z.prospectivity_score * 100).toFixed(1);
            const color = z.prospectivity_score >= 0.75 ? '#059669' :
                          z.prospectivity_score >= 0.50 ? '#0284c7' : '#d97706';

            const circle = L.circleMarker([z.latitude, z.longitude], {
                radius: z.prospectivity_score >= 0.75 ? 8 : 6,
                fillColor: color,
                color: '#ffffff',
                weight: 1.5,
                opacity: 0.9,
                fillOpacity: 0.85
            });

            circle.bindPopup(`
                <div class="p-1 space-y-1.5 text-xs">
                    <div class="font-bold text-sm text-cyan-400 border-b border-slate-700 pb-1 flex justify-between">
                        <span>${z.zone_id}</span>
                        <span class="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">${z.state}</span>
                    </div>
                    <div><strong>Mining Belt:</strong> <span class="text-slate-300">${z.mining_belt}</span></div>
                    <div><strong>Ore Grade:</strong> <span class="text-amber-400 font-bold">${z.ore_grade_percent}% Mn</span></div>
                    <div><strong>Prospectivity:</strong> <span class="text-emerald-400 font-bold">${scorePct}%</span></div>
                    <div><strong>Estimated Potential:</strong> <span class="text-slate-200">${Math.round(z.predicted_manganese_reserve_tonnes).toLocaleString()} tonnes</span></div>
                    <div><strong>Operational Risk:</strong> <span class="font-bold ${
                        z.risk_level === 'High' ? 'text-rose-400' : z.risk_level === 'Medium' ? 'text-amber-400' : 'text-emerald-400'
                    }">${z.risk_level}</span></div>
                    <button onclick="fillSimulatorWithZone(${JSON.stringify(z).replace(/"/g, '&quot;')})" class="w-full mt-2 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-1 rounded text-center block transition">
                        ⚡ Load into AI Simulator
                    </button>
                </div>
            `);

            mapMarkersLayer.addLayer(circle);
        });

    } catch (err) {
        console.error("Error loading GIS zones:", err);
    }
}

// Load a clicked zone into the simulator
function fillSimulatorWithZone(z) {
    switchTab('tab-simulator');
    document.getElementById('sim-ferrous').value = z.sentinel2_ferrous_index || 1.45;
    document.getElementById('sim-clay').value = z.sentinel2_clay_index || 1.30;
    document.getElementById('sim-ndvi').value = z.ndvi || 0.28;
    document.getElementById('sim-lst').value = z.land_surface_temperature || 34.5;
    document.getElementById('sim-elev').value = z.elevation_m || 480;
    document.getElementById('sim-geo').value = z.geological_score || 0.85;
    document.getElementById('sim-grade').value = z.ore_grade_percent || 42.5;
    document.getElementById('sim-prod').value = z.historical_production_tonnes || 32000;
    document.getElementById('sim-eq').value = z.equipment_efficiency || 0.72;

    updateSliderLabels();
    runInference();
}

function updateSliderLabels() {
    document.getElementById('val-sim-ferrous').innerText = parseFloat(document.getElementById('sim-ferrous').value).toFixed(2);
    document.getElementById('val-sim-clay').innerText = parseFloat(document.getElementById('sim-clay').value).toFixed(2);
    document.getElementById('val-sim-ndvi').innerText = parseFloat(document.getElementById('sim-ndvi').value).toFixed(2);
    document.getElementById('val-sim-lst').innerText = `${parseFloat(document.getElementById('sim-lst').value).toFixed(1)} °C`;
    document.getElementById('val-sim-elev').innerText = `${parseInt(document.getElementById('sim-elev').value)} m`;
    document.getElementById('val-sim-geo').innerText = parseFloat(document.getElementById('sim-geo').value).toFixed(2);
    document.getElementById('val-sim-grade').innerText = `${parseFloat(document.getElementById('sim-grade').value).toFixed(1)}%`;
    document.getElementById('val-sim-prod').innerText = `${parseInt(document.getElementById('sim-prod').value).toLocaleString()} t`;
    document.getElementById('val-sim-eq').innerText = `${(parseFloat(document.getElementById('sim-eq').value) * 100).toFixed(0)}%`;
}

// -------------------------------------------------------------
// AI Mineral Simulator & XAI Inference
// -------------------------------------------------------------
function initSimXAIChart() {
    const ctx = document.getElementById('chart-sim-xai').getContext('2d');
    chartSimXAI = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Geological', 'Ferrous (SWIR)', 'Clay (SWIR)', 'Canopy Stress', 'Thermal LST'],
            datasets: [{
                label: 'Signal Contribution',
                data: [0.30, 0.22, 0.14, 0.12, 0.08],
                backgroundColor: ['#38bdf8', '#0284c7', '#6366f1', '#10b981', '#f59e0b'],
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { min: 0, max: 0.45, ticks: { color: '#94a3b8' }, grid: { color: '#1e293b' } },
                y: { ticks: { color: '#cbd5e1', font: { size: 11 } }, grid: { display: false } }
            }
        }
    });
}

async function runInference() {
    updateSliderLabels();

    const payload = {
        sentinel2_ferrous_index: parseFloat(document.getElementById('sim-ferrous').value),
        sentinel2_clay_index: parseFloat(document.getElementById('sim-clay').value),
        ndvi: parseFloat(document.getElementById('sim-ndvi').value),
        land_surface_temperature: parseFloat(document.getElementById('sim-lst').value),
        elevation_m: parseFloat(document.getElementById('sim-elev').value),
        geological_score: parseFloat(document.getElementById('sim-geo').value),
        ore_grade_percent: parseFloat(document.getElementById('sim-grade').value),
        historical_production_tonnes: parseFloat(document.getElementById('sim-prod').value),
        equipment_efficiency: parseFloat(document.getElementById('sim-eq').value),
        rainfall_mm: 1150.0
    };

    try {
        const res = await fetch(apiUrl('/api/predict'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const pred = await res.json();

        // Update Simulator Output KPIs
        document.getElementById('sim-res-score').innerText = `${pred.prospectivity_percent}%`;
        document.getElementById('sim-res-conf').innerText = `Confidence: ${pred.confidence_score}%`;
        document.getElementById('sim-res-pot').innerText = `${Math.round(pred.estimated_reserve_tonnes).toLocaleString()} t`;
        document.getElementById('sim-res-short').innerText = `${Math.round(pred.predicted_shortfall_tonnes).toLocaleString()} t`;
        document.getElementById('sim-res-gap').innerText = `-${pred.production_gap_percent}% Deficit Gap`;
        document.getElementById('sim-res-risk').innerText = pred.risk_level;

        // Update XAI Chart
        if (chartSimXAI && pred.prospectivity_signals) {
            chartSimXAI.data.labels = pred.prospectivity_signals.map(s => s.Signal);
            chartSimXAI.data.datasets[0].data = pred.prospectivity_signals.map(s => s.Contribution);
            chartSimXAI.update();
        }

        // Update Recommendations Box
        const recBox = document.getElementById('sim-recommendations');
        recBox.innerHTML = pred.recommendations.map(r => `
            <div class="p-2.5 rounded-lg border text-xs leading-relaxed ${
                r.includes('Warning') || r.includes('Deficit') || r.includes('High Operational Risk') ?
                'bg-rose-950/40 border-rose-800/80 text-rose-200' :
                'bg-cyan-950/40 border-cyan-800/80 text-cyan-200'
            }">
                <strong>▶</strong> ${r}
            </div>
        `).join('');

    } catch (err) {
        console.error("Inference failed:", err);
    }
}
