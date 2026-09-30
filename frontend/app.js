// MANGANEX AI Frontend Engine
let map = null;
let mapMarkersLayer = null;
let chartStatePot = null;
let chartStateShort = null;
let chartProdComp = null;
let chartRiskPie = null;
let chartSimXAI = null;

// Initialize when DOM loaded
document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();
    loadSummaryData();
    initSimXAIChart();
    runInference(); // Run default simulation
});

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
        const res = await fetch('/api/summary');
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
// Interactive Leaflet 3D/2D Map (Zero API Key, Zero Watermarks)
// -------------------------------------------------------------
function initLeafletMap() {
    map = L.map('map', {
        center: [21.5, 80.0],
        zoom: 5,
        zoomControl: true,
    });

    // 1. ESRI Dark Gray Canvas (Clean Dark Theme, Zero Watermarks, 100% Free)
    const darkCanvas = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; Esri & OpenStreetMap contributors',
        maxZoom: 16
    });

    // 2. ESRI High-Resolution World Imagery (True Satellite View for Space Tech)
    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; Esri, Earthstar Geographics',
        maxZoom: 18
    });

    // 3. OpenStreetMap Standard (Clean Street View)
    const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    });

    // Set Default Base Layer to Dark Canvas
    darkCanvas.addTo(map);

    // Layer Switcher Control on Top-Right of the Map
    const baseMaps = {
        "🌙 Dark Geospatial Map": darkCanvas,
        "🛰️ Satellite Imagery": satelliteLayer,
        "🗺️ Standard OpenStreetMap": osmLayer
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
        const url = `/api/zones?state=${encodeURIComponent(state)}&min_prospectivity=${minScore}&min_grade=${minGrade}`;
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
            const color = z.prospectivity_score >= 0.75 ? '#10b981' :
                          z.prospectivity_score >= 0.50 ? '#00e5ff' : '#f59e0b';

            const marker = L.circleMarker([z.latitude, z.longitude], {
                radius: 6,
                fillColor: color,
                color: '#ffffff',
                weight: 1.2,
                opacity: 0.95,
                fillOpacity: 0.85
            });

            const popupContent = `
                <div style="font-size: 11px; line-height: 1.45; font-family: sans-serif;">
                    <b style="color: #38bdf8; font-size: 13px;">${z.zone_id}</b> (${z.district}, ${z.state})<br/>
                    <b>Mining Belt:</b> ${z.mining_belt}<br/>
                    <b>Formation:</b> ${z.formation}<br/>
                    <b>Prospectivity:</b> <span style="color: #10b981; font-weight: bold;">${scorePct}%</span><br/>
                    <b>Ore Grade:</b> <span style="color: #f59e0b; font-weight: bold;">${z.ore_grade_percent}% Mn</span><br/>
                    <b>Potential:</b> ${Math.round(z.predicted_manganese_reserve_tonnes).toLocaleString()} tonnes<br/>
                    <b>Operational Risk:</b> <b>${z.risk_level}</b>
                </div>
            `;
            marker.bindPopup(popupContent);
            mapMarkersLayer.addLayer(marker);
        });

        // Populate GIS Table
        const gisTable = document.getElementById('table-gis-zones');
        gisTable.innerHTML = data.zones.slice(0, 50).map(z => `
            <tr class="hover:bg-slate-800/40 transition">
                <td class="py-1.5 px-3 font-mono font-semibold text-cyan-400">${z.zone_id}</td>
                <td class="py-1.5 px-3">${z.district}</td>
                <td class="py-1.5 px-3">${z.state}</td>
                <td class="py-1.5 px-3 text-amber-400 font-mono">${z.sentinel2_ferrous_index}</td>
                <td class="py-1.5 px-3 text-amber-400 font-mono">${z.sentinel2_clay_index}</td>
                <td class="py-1.5 px-3 font-mono">${z.ndvi}</td>
                <td class="py-1.5 px-3 font-mono">${z.land_surface_temperature} °C</td>
                <td class="py-1.5 px-3 font-semibold text-slate-200">${z.ore_grade_percent}%</td>
                <td class="py-1.5 px-3 font-bold text-emerald-400">${(z.prospectivity_score * 100).toFixed(1)}%</td>
            </tr>
        `).join('');

    } catch (err) {
        console.error("Error loading GIS zones:", err);
    }
}

function updateScoreLabel(val) {
    document.getElementById('gis-score-label').innerText = `${val}%`;
}

function updateGradeLabel(val) {
    document.getElementById('gis-grade-label').innerText = `${val}%`;
}

// -------------------------------------------------------------
// Live AI Simulation & Explainable AI (XAI)
// -------------------------------------------------------------
function updateSimValue(key, val) {
    if (key === 'ferrous') document.getElementById('val-ferrous').innerText = val;
    if (key === 'clay') document.getElementById('val-clay').innerText = val;
    if (key === 'ndvi') document.getElementById('val-ndvi').innerText = val;
    if (key === 'lst') document.getElementById('val-lst').innerText = `${val} °C`;
    if (key === 'elev') document.getElementById('val-elev').innerText = `${val} m`;
    if (key === 'geo') document.getElementById('val-geo').innerText = val;
    if (key === 'grade') document.getElementById('val-grade').innerText = `${val}%`;
    if (key === 'eq') document.getElementById('val-eq').innerText = `${Math.round(val * 100)}%`;
    if (key === 'prod') document.getElementById('val-prod').innerText = `${Number(val).toLocaleString()} t`;
}

function initSimXAIChart() {
    const ctx = document.getElementById('chart-sim-xai').getContext('2d');
    chartSimXAI = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Signal Contribution',
                data: [],
                backgroundColor: ['#0284c7', '#0284c7', '#38bdf8', '#818cf8', '#6366f1'],
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1e293b' } },
                y: { ticks: { color: '#cbd5e1', font: { size: 10 } }, grid: { display: false } }
            }
        }
    });
}

async function runInference() {
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
        const res = await fetch('/api/predict', {
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
