/**
 * Client application for the Cardiovascular Risk Machine Learning System.
 * Coordinates UI tabs, prediction requests, SHAP visualizations, history, and analytics.
 */

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initForm();
  initHistoryTab();
  initAnalyticsTab();
});

// ================= Tab Management =================
function initTabs() {
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabPanels = document.querySelectorAll(".tab-panel");

  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-tab");

      tabButtons.forEach((b) => b.classList.remove("active"));
      tabPanels.forEach((p) => p.classList.remove("active"));

      btn.classList.add("active");
      document.getElementById(targetId).classList.add("active");

      if (targetId === "history-tab") {
        loadHistory();
      } else if (targetId === "analytics-tab") {
        loadAnalytics();
      }
    });
  });
}

// ================= Prediction Form =================
function initForm() {
  const form = document.getElementById("patient-form");
  const btnLowRisk = document.getElementById("btn-load-low-risk");
  const btnHighRisk = document.getElementById("btn-load-high-risk");

  // Sample low-risk case
  btnLowRisk.addEventListener("click", () => {
    fillFormValues({
      age: 36,
      sex: 0,
      cp: 0,
      trestbps: 115,
      chol: 175,
      fbs: 0,
      restecg: 0,
      thalach: 178,
      exang: 0,
      oldpeak: 0.0,
      slope: 0,
      ca: 0,
      thal: 1,
    });
  });

  // Sample high-risk case
  btnHighRisk.addEventListener("click", () => {
    fillFormValues({
      age: 67,
      sex: 1,
      cp: 3,
      trestbps: 160,
      chol: 286,
      fbs: 1,
      restecg: 2,
      thalach: 108,
      exang: 1,
      oldpeak: 3.2,
      slope: 2,
      ca: 2,
      thal: 3,
    });
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await submitPrediction();
  });
}

function fillFormValues(data) {
  for (const [key, value] of Object.entries(data)) {
    const input = document.getElementById(key);
    if (input) {
      input.value = value;
    }
  }
}

async function submitPrediction() {
  const submitBtn = document.getElementById("btn-submit-prediction");
  submitBtn.disabled = true;
  submitBtn.textContent = "Analyzing Patient Biomarkers...";

  const payload = {
    age: parseInt(document.getElementById("age").value),
    sex: parseInt(document.getElementById("sex").value),
    cp: parseInt(document.getElementById("cp").value),
    trestbps: parseFloat(document.getElementById("trestbps").value),
    chol: parseFloat(document.getElementById("chol").value),
    fbs: parseInt(document.getElementById("fbs").value),
    restecg: parseInt(document.getElementById("restecg").value),
    thalach: parseFloat(document.getElementById("thalach").value),
    exang: parseInt(document.getElementById("exang").value),
    oldpeak: parseFloat(document.getElementById("oldpeak").value),
    slope: parseInt(document.getElementById("slope").value),
    ca: parseInt(document.getElementById("ca").value),
    thal: parseInt(document.getElementById("thal").value),
  };

  try {
    const response = await fetch("/api/v1/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Prediction request failed.");
    }

    const data = await response.json();
    renderPredictionResult(data);
  } catch (error) {
    alert("Error: " + error.message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Calculate Cardiovascular Risk";
  }
}

function renderPredictionResult(data) {
  const resultCard = document.getElementById("prediction-result-card");
  resultCard.style.display = "block";

  // Update probability percentage
  const probPercent = Math.round(data.probability * 100);
  document.getElementById("result-percentage").textContent = `${probPercent}%`;

  // Update SVG radial gauge
  const progressCircle = document.getElementById("gauge-progress-bar");
  const circumference = 2 * Math.PI * 65; // radius = 65
  const offset = circumference - (probPercent / 100) * circumference;
  progressCircle.style.strokeDashoffset = offset;

  // Update risk tier badge & gauge color
  const riskBadge = document.getElementById("result-risk-badge");
  riskBadge.className = "risk-badge";
  progressCircle.classList.remove("risk-low", "risk-moderate", "risk-high");

  if (data.risk_tier === "Low Risk") {
    riskBadge.classList.add("risk-low");
    progressCircle.classList.add("risk-low");
    riskBadge.textContent = "Low Cardiovascular Risk";
  } else if (data.risk_tier === "Moderate Risk") {
    riskBadge.classList.add("risk-moderate");
    progressCircle.classList.add("risk-moderate");
    riskBadge.textContent = "Moderate Cardiovascular Risk";
  } else {
    riskBadge.classList.add("risk-high");
    progressCircle.classList.add("risk-high");
    riskBadge.textContent = "High Cardiovascular Risk";
  }

  // Model details
  document.getElementById("result-model-name").textContent = `${data.model_name} (v${data.model_version})`;

  // Render local SHAP attributions
  renderLocalShapAttributions(data.feature_attributions);

  // Scroll smoothly to results
  resultCard.scrollIntoView({ behavior: "smooth" });
}

function renderLocalShapAttributions(attributions) {
  const container = document.getElementById("shap-attributions-list");
  container.innerHTML = "";

  if (!attributions || attributions.length === 0) {
    container.innerHTML = "<p style='color: var(--text-muted);'>No feature attributions available.</p>";
    return;
  }

  attributions.forEach((attr) => {
    const item = document.createElement("div");
    item.className = "attribution-item";

    const isRisk = attr.direction === "increases_risk";
    const barWidth = Math.min(Math.round(attr.abs_attribution * 120), 100);

    const friendlyName = getFeatureDisplayName(attr.base_feature);

    item.innerHTML = `
      <div class="attr-info">
        <span class="attr-name">${friendlyName}</span>
        <span class="attr-val">Patient value: <strong>${attr.patient_value ?? "N/A"}</strong></span>
      </div>
      <div class="attr-impact-bar">
        <span style="font-size:0.75rem; color:${isRisk ? 'var(--danger)' : 'var(--success)'}; font-weight:600;">
          ${isRisk ? '+ Risk' : '- Protective'}
        </span>
        <div class="bar-pill ${isRisk ? 'risk' : 'protective'}" style="width: ${barWidth}px;"></div>
      </div>
    `;
    container.appendChild(item);
  });
}

function getFeatureDisplayName(name) {
  const dict = {
    age: "Age",
    sex: "Biological Sex",
    cp: "Chest Pain Type",
    trestbps: "Resting Blood Pressure",
    chol: "Serum Cholesterol",
    fbs: "Fasting Blood Sugar",
    restecg: "Resting ECG",
    thalach: "Max Heart Rate",
    exang: "Exercise Angina",
    oldpeak: "ST Depression",
    slope: "ST Slope",
    ca: "Fluoroscopy Vessels",
    thal: "Thalassemia Scan",
  };
  return dict[name] || name;
}

// ================= History Tab =================
function initHistoryTab() {
  const riskFilter = document.getElementById("history-risk-filter");
  const refreshBtn = document.getElementById("btn-refresh-history");

  riskFilter.addEventListener("change", () => loadHistory());
  refreshBtn.addEventListener("click", () => loadHistory());
}

async function loadHistory() {
  const filter = document.getElementById("history-risk-filter").value;
  let url = "/api/v1/history?limit=100";
  if (filter) {
    url += `&risk_tier=${encodeURIComponent(filter)}`;
  }

  try {
    const [histResp, statsResp] = await Promise.all([
      fetch(url),
      fetch("/api/v1/history/stats"),
    ]);

    const histData = await histResp.json();
    const statsData = await statsResp.json();

    renderHistoryStats(statsData);
    renderHistoryTable(histData.items);
  } catch (err) {
    console.error("Failed to load history:", err);
  }
}

function renderHistoryStats(stats) {
  document.getElementById("stat-total-count").textContent = stats.total_assessments;
  document.getElementById("stat-low-risk").textContent = stats.low_risk_count;
  document.getElementById("stat-high-risk").textContent = stats.high_risk_count;
  document.getElementById("stat-avg-risk").textContent = `${Math.round(stats.average_predicted_risk * 100)}%`;
}

function renderHistoryTable(records) {
  const tbody = document.getElementById("history-table-body");
  tbody.innerHTML = "";

  if (records.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:2rem;">No stored assessment records found.</td></tr>`;
    return;
  }

  records.forEach((r) => {
    const tr = document.createElement("tr");
    const d = new Date(r.created_at);
    const dateFormatted = d.toLocaleDateString() + " " + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const badgeClass = r.risk_tier === "Low Risk" ? "risk-low" : r.risk_tier === "Moderate Risk" ? "risk-moderate" : "risk-high";

    tr.innerHTML = `
      <td><strong>#${r.id}</strong></td>
      <td>${dateFormatted}</td>
      <td>${r.patient_data.age} y/o (${r.patient_data.sex === 1 ? 'M' : 'F'})</td>
      <td>${r.patient_data.trestbps} mm Hg / ${r.patient_data.chol} mg/dl</td>
      <td><strong>${Math.round(r.probability * 100)}%</strong></td>
      <td><span class="risk-badge ${badgeClass}" style="padding:0.15rem 0.6rem; font-size:0.75rem;">${r.risk_tier}</span></td>
      <td>
        <button class="btn-danger-sm" onclick="deleteRecord(${r.id})">Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function deleteRecord(id) {
  if (!confirm(`Delete assessment record #${id}?`)) return;
  try {
    const res = await fetch(`/api/v1/history/${id}`, { method: "DELETE" });
    if (res.ok) {
      loadHistory();
    }
  } catch (err) {
    alert("Delete failed: " + err.message);
  }
}

// ================= Analytics Tab =================
function initAnalyticsTab() {}

async function loadAnalytics() {
  try {
    const [infoResp, compResp, impResp, curvesResp] = await Promise.all([
      fetch("/api/v1/analytics/model-info"),
      fetch("/api/v1/analytics/model-comparison"),
      fetch("/api/v1/analytics/global-importance"),
      fetch("/api/v1/analytics/curves"),
    ]);

    const info = await infoResp.json();
    const comparison = await compResp.json();
    const importance = await impResp.json();
    const curves = await curvesResp.json();

    renderModelComparisonTable(comparison, info.model_name);
    renderTestMetricsCard(info);
    renderGlobalImportanceChart(importance);
    renderRocCurve(curves.roc_curve);
  } catch (err) {
    console.error("Failed to load analytics:", err);
  }
}

function renderModelComparisonTable(comp, activeModel) {
  const tbody = document.getElementById("comparison-table-body");
  tbody.innerHTML = "";

  for (const [modelName, m] of Object.entries(comp)) {
    const tr = document.createElement("tr");
    const isSelected = modelName === activeModel;

    tr.innerHTML = `
      <td>
        <strong>${modelName}</strong>
        ${isSelected ? '<span class="badge-best">Selected Pipeline</span>' : ''}
      </td>
      <td>${(m.cv_accuracy_mean * 100).toFixed(1)}% ± ${(m.cv_accuracy_std * 100).toFixed(1)}%</td>
      <td>${(m.cv_precision_mean * 100).toFixed(1)}%</td>
      <td>${(m.cv_recall_mean * 100).toFixed(1)}%</td>
      <td>${(m.cv_f1_mean * 100).toFixed(1)}%</td>
      <td><strong>${m.cv_roc_auc_mean.toFixed(4)}</strong> ± ${m.cv_roc_auc_std.toFixed(4)}</td>
    `;
    tbody.appendChild(tr);
  }
}

function renderTestMetricsCard(info) {
  const m = info.test_metrics;
  if (!m) return;

  document.getElementById("test-accuracy").textContent = `${(m.accuracy * 100).toFixed(1)}%`;
  document.getElementById("test-recall").textContent = `${(m.recall * 100).toFixed(1)}%`;
  document.getElementById("test-specificity").textContent = `${(m.specificity * 100).toFixed(1)}%`;
  document.getElementById("test-roc-auc").textContent = m.roc_auc.toFixed(4);
}

function renderGlobalImportanceChart(importanceList) {
  const container = document.getElementById("global-importance-container");
  container.innerHTML = "";

  if (!importanceList || importanceList.length === 0) return;

  const maxVal = Math.max(...importanceList.map((x) => x.importance));

  importanceList.slice(0, 10).forEach((item) => {
    const row = document.createElement("div");
    row.style.display = "flex";
    row.style.alignItems = "center";
    row.style.margin = "0.4rem 0";
    row.style.fontSize = "0.85rem";

    const widthPercent = (item.importance / maxVal) * 100;
    const displayName = getFeatureDisplayName(item.feature);

    row.innerHTML = `
      <div style="width: 140px; font-weight: 600; color: var(--secondary); text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
        ${displayName}
      </div>
      <div style="flex: 1; background: #e2e8f0; height: 14px; border-radius: 4px; overflow: hidden; margin: 0 0.75rem;">
        <div style="width: ${widthPercent}%; background: var(--primary); height: 100%; border-radius: 4px;"></div>
      </div>
      <div style="width: 45px; text-align: right; font-weight: 700; color: var(--text-muted);">
        ${item.importance.toFixed(3)}
      </div>
    `;
    container.appendChild(row);
  });
}

function renderRocCurve(rocData) {
  const canvas = document.getElementById("roc-canvas");
  if (!canvas || !rocData || !rocData.fpr) return;

  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  const padding = 35;

  ctx.clearRect(0, 0, w, h);

  // Background grid
  ctx.strokeStyle = "#e2e8f0";
  ctx.lineWidth = 1;
  ctx.beginPath();
  for (let i = 0; i <= 4; i++) {
    const x = padding + (i / 4) * (w - 2 * padding);
    const y = h - padding - (i / 4) * (h - 2 * padding);
    // Vertical grid
    ctx.moveTo(x, padding);
    ctx.lineTo(x, h - padding);
    // Horizontal grid
    ctx.moveTo(padding, y);
    ctx.lineTo(w - padding, y);

    // Labels
    ctx.fillStyle = "#64748b";
    ctx.font = "10px sans-serif";
    ctx.fillText((i / 4).toFixed(2), x - 10, h - padding + 15);
    ctx.fillText((i / 4).toFixed(2), padding - 28, y + 4);
  }
  ctx.stroke();

  // Diagonal chance line (FPR = TPR)
  ctx.strokeStyle = "#cbd5e1";
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  ctx.moveTo(padding, h - padding);
  ctx.lineTo(w - padding, padding);
  ctx.stroke();
  ctx.setLineDash([]);

  // Plot ROC Curve
  ctx.strokeStyle = "#0284c7";
  ctx.lineWidth = 2.5;
  ctx.beginPath();

  rocData.fpr.forEach((fpr, idx) => {
    const tpr = rocData.tpr[idx];
    const x = padding + fpr * (w - 2 * padding);
    const y = h - padding - tpr * (h - 2 * padding);

    if (idx === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.stroke();

  // Axis titles
  ctx.fillStyle = "#1e293b";
  ctx.font = "11px sans-serif";
  ctx.fillText("False Positive Rate (1 - Specificity)", w / 2 - 80, h - 5);
  ctx.save();
  ctx.translate(12, h / 2 + 50);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText("True Positive Rate (Sensitivity)", 0, 0);
  ctx.restore();
}
