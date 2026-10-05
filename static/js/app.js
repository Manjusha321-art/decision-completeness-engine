/**
 * High-Performance Frontend Controller for The Decision Completeness Engine (DCE)
 * Optimized for sub-50ms execution, instant rendering, and zero UI latency.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global State & Client Cache
  let currentScenarioId = 'vendor_procurement';
  let pipelineRunning = false;
  const scenariosCache = {};

  // DOM Elements
  const scenarioSelectorContainer = document.getElementById('scenario-selector-container');
  const btnRunFull = document.getElementById('btn-run-full');
  const btnStepNext = document.getElementById('btn-step-next');
  const btnReset = document.getElementById('btn-reset');
  const pipelineStatusText = document.getElementById('pipeline-status-text');
  const speedModeSelect = document.getElementById('speed-mode-select');
  const autoHitlCheck = document.getElementById('auto-hitl-check');

  // Request Info
  const reqDomainBadge = document.getElementById('req-domain-badge');
  const reqTitle = document.getElementById('req-title');
  const reqId = document.getElementById('req-id');
  const reqSummary = document.getElementById('req-summary');
  const reqRequester = document.getElementById('req-requester');
  const reqDept = document.getElementById('req-dept');
  const reqAmount = document.getElementById('req-amount');

  // Completeness & Gatekeeper
  const completenessScoreBadge = document.getElementById('completeness-score-badge');
  const completenessProgressBar = document.getElementById('completeness-progress-bar');
  const gatekeeperStatusBox = document.getElementById('gatekeeper-status-box');
  const gateIcon = document.getElementById('gate-icon');
  const gateTitle = document.getElementById('gate-title');
  const gateDesc = document.getElementById('gate-desc');
  const metricVerified = document.getElementById('metric-verified');
  const metricHealed = document.getElementById('metric-healed');
  const metricMissing = document.getElementById('metric-missing');

  // Evidence Table
  const evidenceTableBody = document.getElementById('evidence-table-body');

  // Verdict Container
  const verdictContainer = document.getElementById('verdict-container');
  const verdictBadge = document.getElementById('verdict-badge');
  const verdictTitle = document.getElementById('verdict-title');
  const verdictConfidence = document.getElementById('verdict-confidence');
  const verdictId = document.getElementById('verdict-id');
  const verdictSummary = document.getElementById('verdict-summary');
  const verdictReasoningList = document.getElementById('verdict-reasoning-list');
  const actionsList = document.getElementById('actions-list');

  // HITL Elements
  const hitlTabBadge = document.getElementById('hitl-tab-badge');
  const hitlTargetRole = document.getElementById('hitl-target-role');
  const hitlTargetEmail = document.getElementById('hitl-target-email');
  const hitlVerifiedSummary = document.getElementById('hitl-verified-summary');
  const hitlMissingItem = document.getElementById('hitl-missing-item');
  const hitlActionRequired = document.getElementById('hitl-action-required');
  const hitlNotesInput = document.getElementById('hitl-notes-input');
  const btnHitlApprove = document.getElementById('btn-hitl-approve');
  const btnHitlUpload = document.getElementById('btn-hitl-upload');
  const btnHitlReject = document.getElementById('btn-hitl-reject');

  // Tabs
  const navTabs = document.querySelectorAll('.nav-tab');
  const tabPanes = document.querySelectorAll('.tab-pane');

  // Custom Modal
  const btnCustomModal = document.getElementById('btn-custom-modal');
  const customModal = document.getElementById('custom-modal');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const btnCancelModal = document.getElementById('btn-cancel-modal');
  const btnSubmitModal = document.getElementById('btn-submit-modal');

  // -------------------------------------------------------------
  // Initial Setup (Parallel Non-Blocking Fetch)
  // -------------------------------------------------------------
  Promise.all([
    fetchScenarios(),
    fetchSources(),
    fetchAnalytics()
  ]);

  // Tab switching with instant CSS transition
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.dataset.tab;
      navTabs.forEach(t => {
        t.classList.remove('active', 'border-indigo-500', 'text-white');
        t.classList.add('border-transparent', 'text-slate-400');
      });
      tab.classList.add('active', 'border-indigo-500', 'text-white');
      tab.classList.remove('border-transparent', 'text-slate-400');

      tabPanes.forEach(pane => pane.classList.add('hidden'));
      const activePane = document.getElementById(targetId);
      if (activePane) activePane.classList.remove('hidden');
    });
  });

  // -------------------------------------------------------------
  // Scenario Loading with Client Cache
  // -------------------------------------------------------------
  async function fetchScenarios() {
    try {
      const res = await fetch('/api/scenarios');
      if (!res.ok) throw new Error('API unavailable');
      const data = await res.json();
      Object.assign(scenariosCache, data.scenarios);
      renderScenarioButtons(data.scenarios, data.current);
    } catch (err) {
      console.warn('API offline. Using embedded dataset for static 24/7 hosting:', err);
      if (window.DCE_STATIC_DATA && window.DCE_STATIC_DATA.scenarios) {
        Object.assign(scenariosCache, window.DCE_STATIC_DATA.scenarios);
        renderScenarioButtons(window.DCE_STATIC_DATA.scenarios, currentScenarioId);
      }
    }
  }

  function renderScenarioButtons(scenarios, selectedId) {
    scenarioSelectorContainer.innerHTML = '';
    Object.values(scenarios).forEach(scen => {
      const isSelected = (scen.id === selectedId);
      const btn = document.createElement('button');
      btn.className = `px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
        isSelected
          ? 'bg-indigo-600 text-white shadow-sm ring-1 ring-indigo-400/50'
          : 'bg-slate-800 text-slate-300 hover:bg-slate-700/80 border border-slate-700'
      }`;
      btn.innerHTML = `
        <span>${scen.name.split(':')[0]}</span>
        <span class="text-[10px] opacity-75 font-normal">(${scen.badge})</span>
      `;
      btn.onclick = () => selectScenario(scen.id);
      scenarioSelectorContainer.appendChild(btn);
    });

    if (scenarios[selectedId]) {
      updateRequestDisplay(scenarios[selectedId]);
    }
  }

  async function selectScenario(id) {
    currentScenarioId = id;
    // Instant optimistic render from cache
    if (scenariosCache[id]) {
      updateRequestDisplay(scenariosCache[id]);
      renderScenarioButtons(scenariosCache, id);
    }
    resetUI();

    // Async server sync
    fetch('/api/scenarios/select', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id: id })
    }).catch(console.error);
  }

  function updateRequestDisplay(scen) {
    reqDomainBadge.textContent = scen.domain || 'Procurement';
    reqTitle.textContent = scen.request_title || scen.name;
    reqId.textContent = scen.id.toUpperCase();
    reqSummary.textContent = scen.description;
    reqRequester.textContent = scen.requester || 'Requester';
    reqDept.textContent = scen.department || 'Operations';
    reqAmount.textContent = scen.amount ? `$${Number(scen.amount).toLocaleString()}` : 'N/A';
  }

  function resetUI() {
    pipelineRunning = false;
    pipelineStatusText.textContent = 'Ready to execute (Select speed & click Run)';
    
    // Reset Stepper
    for (let i = 1; i <= 8; i++) {
      const node = document.getElementById(`step-node-${i}`);
      node.className = 'step-card flex flex-col p-2.5 rounded-xl border border-slate-800 bg-slate-900/60 transition';
      node.querySelector('.step-status-icon').textContent = '⚪';
    }
    const step1 = document.getElementById('step-node-1');
    step1.classList.add('active');
    step1.querySelector('.step-status-icon').textContent = '🔵';

    // Reset Completeness
    completenessScoreBadge.textContent = '0%';
    completenessProgressBar.style.width = '0%';
    completenessProgressBar.className = 'h-3 rounded-full bg-gradient-to-r from-amber-500 to-indigo-500 transition-all duration-300';

    gatekeeperStatusBox.className = 'p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300';
    gateIcon.textContent = '🛡️';
    gateTitle.textContent = 'Gatekeeper Ready';
    gateDesc.textContent = 'Enforces zero-hallucination policy before deciding.';

    metricVerified.textContent = '0';
    metricHealed.textContent = '0';
    metricMissing.textContent = '0';

    evidenceTableBody.innerHTML = `
      <tr>
        <td colspan="6" class="py-8 text-center text-slate-500">
          Click <strong>Run Pipeline</strong> to execute full evidence verification.
        </td>
      </tr>
    `;

    verdictContainer.classList.add('hidden');
    hitlTabBadge.classList.add('hidden');
  }

  btnReset.addEventListener('click', () => {
    selectScenario(currentScenarioId);
  });

  // -------------------------------------------------------------
  // High-Speed Single-Request Pipeline Execution
  // -------------------------------------------------------------
  btnRunFull.addEventListener('click', async () => {
    if (pipelineRunning) return;
    pipelineRunning = true;
    btnRunFull.disabled = true;
    if (btnStepNext) btnStepNext.disabled = true;

    const speedMode = speedModeSelect ? speedModeSelect.value : 'turbo';
    const autoHitl = autoHitlCheck ? autoHitlCheck.checked : false;

    pipelineStatusText.textContent = '⚡ Running Decision Completeness Pipeline...';

    const t0 = performance.now();

    try {
      let trace;
      try {
        const res = await fetch('/api/pipeline/run-full', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ auto_resolve_hitl: autoHitl })
        });
        if (!res.ok) throw new Error('API unavailable');
        trace = await res.json();
      } catch (apiErr) {
        console.warn('API unavailable. Running client-side simulation:', apiErr);
        if (window.DCE_STATIC_DATA && window.DCE_STATIC_DATA.scenarios[currentScenarioId]) {
          const scenData = window.DCE_STATIC_DATA.scenarios[currentScenarioId];
          trace = autoHitl ? scenData.trace_auto : scenData.trace_normal;
        } else {
          throw apiErr;
        }
      }

      const elapsed = Math.round(performance.now() - t0);
      const delayStep = (speedMode === 'turbo') ? 0 : (speedMode === 'fast' ? 50 : 250);

      // Execute visual progression
      await renderFullPipelineTrace(trace, delayStep, autoHitl, elapsed);

    } catch (err) {
      console.error('Error running pipeline', err);
      pipelineStatusText.textContent = 'Error executing pipeline. Check console.';
    } finally {
      btnRunFull.disabled = false;
      if (btnStepNext) btnStepNext.disabled = false;
      pipelineRunning = false;
    }
  });

  if (btnStepNext) {
    btnStepNext.addEventListener('click', () => {
      if (speedModeSelect) speedModeSelect.value = 'walkthrough';
      btnRunFull.click();
    });
  }

  // -------------------------------------------------------------
  // Fast Visual Renderer for Pipeline Trace
  // -------------------------------------------------------------
  async function renderFullPipelineTrace(trace, delay, autoHitl, elapsed) {
    const s = trace.steps;

    // Step 1: Intake
    setStepState(1, 'completed', '✅');
    if (delay > 0) await sleep(delay);

    // Step 2: Planning Requirements
    setStepState(2, 'completed', '✅');
    renderRequirementsTable(s.step2_planning.requirements);
    if (delay > 0) await sleep(delay);

    // Step 3: Gap Audit
    setStepState(3, 'completed', '✅');
    updateAuditDisplay(s.step3_initial_audit);
    if (delay > 0) await sleep(delay);

    // Step 4: Gatekeeper Evaluation
    const isInitiallyBlocked = s.step4_gatekeeper.is_blocked;
    if (isInitiallyBlocked) {
      setStepState(4, 'blocked', '🚫');
      gatekeeperStatusBox.className = 'p-3 rounded-xl bg-rose-950/40 border border-rose-800/60 text-xs text-rose-200';
      gateIcon.textContent = '🚫';
      gateTitle.textContent = 'DECISION GATE ENGAGED';
      gateDesc.textContent = s.step4_gatekeeper.blocking_reason || 'Incomplete evidence. Halting speculative verdict.';
    } else {
      setStepState(4, 'completed', '✅');
      gatekeeperStatusBox.className = 'p-3 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-xs text-emerald-200';
      gateIcon.textContent = '✅';
      gateTitle.textContent = 'Initial Dossier Complete';
    }
    if (delay > 0) await sleep(delay);

    // Step 5: Autonomous Self-Healing
    const healedCount = s.step5_self_healing.self_healed_count;
    if (healedCount > 0) {
      setStepState(5, 'healed', '✨');
    } else {
      setStepState(5, 'completed', '🔍');
    }
    // Update table with post-heal audit
    updateAuditDisplay(s.post_heal_audit);
    if (delay > 0) await sleep(delay);

    // Step 6: Precision HITL Check
    const hitlStep = s.step6_hitl;
    if (hitlStep.status === 'PENDING_HUMAN' && !autoHitl) {
      setStepState(6, 'active', '🎯');
      populateHitlPrompt(hitlStep.hitl_prompt);
      hitlTabBadge.classList.remove('hidden');

      gatekeeperStatusBox.className = 'p-3 rounded-xl bg-amber-950/40 border border-amber-800/60 text-xs text-amber-200';
      gateIcon.textContent = '🎯';
      gateTitle.textContent = 'Precision HITL Triggered';
      gateDesc.textContent = `Awaiting 1-click confirmation from ${hitlStep.hitl_prompt.target_role}.`;

      pipelineStatusText.textContent = `🎯 Micro-Ask dispatched to ${hitlStep.hitl_prompt.target_role}. Click Approve in HITL tab! (${elapsed}ms)`;
      
      // Auto-switch to HITL tab
      document.querySelector('[data-tab="tab-hitl-card"]').click();
      return;
    } else {
      setStepState(6, 'completed', '✅');
    }
    if (delay > 0) await sleep(delay);

    // Step 7: Deliberation Verdict
    setStepState(7, 'completed', '✅');
    renderVerdictCard(s.step7_verdict);

    gatekeeperStatusBox.className = 'p-3 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-xs text-emerald-200';
    gateIcon.textContent = '✅';
    gateTitle.textContent = 'Decision Completed & Actions Dispatched';
    gateDesc.textContent = `${s.step7_verdict.verdict} (${Math.round(s.step7_verdict.confidence_score * 100)}% calibrated confidence).`;

    // Step 8: Meta-Learning
    setStepState(8, 'completed', '🧠');
    fetchAnalytics(); // non-blocking update

    pipelineStatusText.textContent = `⚡ Executed in ${elapsed}ms • Zero hallucinations • Audit hash committed`;
  }

  // -------------------------------------------------------------
  // Fast Table & Display Updaters
  // -------------------------------------------------------------
  function setStepState(stepNum, statusClass, icon) {
    const node = document.getElementById(`step-node-${stepNum}`);
    if (!node) return;
    node.className = `step-card flex flex-col p-2.5 rounded-xl border transition-colors duration-150 ${statusClass}`;
    node.querySelector('.step-status-icon').textContent = icon;
  }

  function renderRequirementsTable(reqs) {
    const rows = reqs.map(r => `
      <tr id="row-req-${r.id}" class="hover:bg-slate-900/50 transition-colors">
        <td class="py-2.5 px-4">
          <div class="font-semibold text-white">${r.name}</div>
          <div class="text-[11px] text-slate-400">${r.description}</div>
        </td>
        <td class="py-2.5 px-3">
          <span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 font-medium">${r.category}</span>
        </td>
        <td class="py-2.5 px-3">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold ${
            r.importance === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' :
            r.importance === 'MANDATORY' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
            'bg-slate-800 text-slate-400'
          }">${r.importance}</span>
        </td>
        <td class="py-2.5 px-3">
          <span class="status-badge px-2 py-0.5 rounded-md text-[10px] font-bold badge-missing">
            PENDING AUDIT
          </span>
        </td>
        <td class="py-2.5 px-4 text-slate-400 text-[11px] citation-cell font-mono">
          --
        </td>
        <td class="py-2.5 px-3 font-mono font-semibold text-slate-400 confidence-cell">
          --
        </td>
      </tr>
    `).join('');
    evidenceTableBody.innerHTML = rows;
  }

  function updateAuditDisplay(auditReport) {
    if (!auditReport) return;

    const score = auditReport.completeness_score;
    completenessScoreBadge.textContent = `${score}%`;
    completenessProgressBar.style.width = `${score}%`;

    if (score >= 100) {
      completenessProgressBar.className = 'h-3 rounded-full bg-emerald-500 transition-all duration-300';
    } else if (score >= 60) {
      completenessProgressBar.className = 'h-3 rounded-full bg-gradient-to-r from-amber-500 to-indigo-500 transition-all duration-300';
    } else {
      completenessProgressBar.className = 'h-3 rounded-full bg-rose-500 transition-all duration-300';
    }

    let verifiedCount = 0;
    let healedCount = 0;
    let missingCount = 0;

    auditReport.items.forEach(item => {
      const tr = document.getElementById(`row-req-${item.requirement_id}`);
      if (!tr) return;

      const statusBadge = tr.querySelector('.status-badge');
      const citationCell = tr.querySelector('.citation-cell');
      const confCell = tr.querySelector('.confidence-cell');

      if (item.status === 'VERIFIED') {
        verifiedCount++;
        statusBadge.className = 'status-badge px-2 py-0.5 rounded-md text-[10px] font-bold badge-verified';
        statusBadge.textContent = 'VERIFIED';
        citationCell.innerHTML = `<span class="text-emerald-400 font-semibold">${item.source}</span>: ${item.summary}`;
        confCell.textContent = `${Math.round(item.confidence * 100)}%`;
        confCell.className = 'py-2.5 px-3 font-mono font-semibold text-emerald-400';
      } else if (item.status === 'SELF_HEALED') {
        healedCount++;
        statusBadge.className = 'status-badge px-2 py-0.5 rounded-md text-[10px] font-bold badge-healed';
        statusBadge.textContent = '✨ SELF-HEALED';
        citationCell.innerHTML = `<span class="text-cyan-400 font-bold">${item.source}</span> (${item.source_location})<div class="text-slate-300 mt-0.5">${item.summary}</div>`;
        confCell.textContent = `${Math.round(item.confidence * 100)}%`;
        confCell.className = 'py-2.5 px-3 font-mono font-semibold text-cyan-400';
      } else if (item.status === 'HUMAN_PROVIDED') {
        statusBadge.className = 'status-badge px-2 py-0.5 rounded-md text-[10px] font-bold badge-hitl';
        statusBadge.textContent = '👤 HITL APPROVED';
        citationCell.innerHTML = `<span class="text-amber-400 font-bold">${item.source}</span>: ${item.summary}`;
        confCell.textContent = '100%';
        confCell.className = 'py-2.5 px-3 font-mono font-semibold text-amber-400';
      } else if (item.status === 'REJECTED') {
        statusBadge.className = 'status-badge px-2 py-0.5 rounded-md text-[10px] font-bold badge-rejected';
        statusBadge.textContent = '✕ REJECTED';
        citationCell.innerHTML = `<span class="text-rose-400 font-bold">${item.source}</span>: ${item.summary}`;
        confCell.textContent = '100%';
        confCell.className = 'py-2.5 px-3 font-mono font-semibold text-rose-400';
      } else {
        missingCount++;
        statusBadge.className = 'status-badge px-2 py-0.5 rounded-md text-[10px] font-bold badge-missing';
        statusBadge.textContent = '❌ MISSING';
        citationCell.innerHTML = `<span class="text-rose-400 italic">Not found in initial dossier or connected repositories</span>`;
        confCell.textContent = '0%';
        confCell.className = 'py-2.5 px-3 font-mono font-semibold text-rose-400';
      }
    });

    metricVerified.textContent = verifiedCount;
    metricHealed.textContent = healedCount;
    metricMissing.textContent = missingCount;
  }

  function renderVerdictCard(dec) {
    verdictContainer.classList.remove('hidden');

    verdictBadge.textContent = dec.verdict;
    if (dec.verdict === 'APPROVED') {
      verdictBadge.className = 'px-3.5 py-1.5 rounded-xl font-bold text-sm bg-emerald-500/20 text-emerald-300 border border-emerald-500/40';
      verdictTitle.textContent = 'Decision Approved & Action Dispatched';
    } else if (dec.verdict === 'REJECTED') {
      verdictBadge.className = 'px-3.5 py-1.5 rounded-xl font-bold text-sm bg-rose-500/20 text-rose-300 border border-rose-500/40';
      verdictTitle.textContent = 'Decision Rejected / Terminated';
    } else {
      verdictBadge.className = 'px-3.5 py-1.5 rounded-xl font-bold text-sm bg-amber-500/20 text-amber-300 border border-amber-500/40';
      verdictTitle.textContent = 'Decision Blocked by Gatekeeper';
    }

    verdictConfidence.textContent = `${Math.round(dec.confidence_score * 100)}%`;
    verdictId.textContent = dec.decision_id;
    verdictSummary.textContent = dec.executive_summary;

    verdictReasoningList.innerHTML = dec.reasoning_chain.map(r => `
      <li class="flex items-start gap-2 bg-slate-900/40 p-2 rounded-lg border border-slate-800/50">
        <span class="text-indigo-400 font-bold">›</span><span>${r}</span>
      </li>
    `).join('');

    actionsList.innerHTML = dec.actions_executed.map(act => `
      <div class="p-2 rounded-lg bg-slate-950 border border-slate-800">
        <div class="flex items-center justify-between text-[11px] font-semibold text-emerald-400">
          <span>✓ ${act.action_name}</span>
          <span class="text-slate-400 font-mono text-[10px]">${act.system}</span>
        </div>
        <div class="text-[11px] text-slate-300 mt-0.5">${act.details}</div>
      </div>
    `).join('');
  }

  // -------------------------------------------------------------
  // Precision HITL Resolution
  // -------------------------------------------------------------
  function populateHitlPrompt(prompt) {
    hitlTargetRole.textContent = prompt.target_role;
    hitlTargetEmail.textContent = prompt.target_email;
    hitlVerifiedSummary.textContent = prompt.verified_summary;
    hitlMissingItem.textContent = prompt.missing_item_name;
    hitlActionRequired.textContent = prompt.specific_action_required;
  }

  btnHitlApprove.addEventListener('click', () => submitHitlResponse('Grant One-Click Approval'));
  btnHitlUpload.addEventListener('click', () => submitHitlResponse('Uploaded Signed Memo and Verified'));
  btnHitlReject.addEventListener('click', () => submitHitlResponse('Deny Exception / Reject Request'));

  async function submitHitlResponse(action) {
    const notes = hitlNotesInput.value.trim() || 'Verified and approved by authorized executive.';
    pipelineStatusText.textContent = `⚡ Resolving human authorization (${action})...`;

    try {
      let data;
      try {
        const res = await fetch('/api/hitl/respond', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: action,
            reviewer_name: hitlTargetRole.textContent,
            notes: notes
          })
        });
        if (!res.ok) throw new Error('API offline');
        data = await res.json();
      } catch (apiErr) {
        console.warn('API offline. Resolving HITL client-side:', apiErr);
        if (window.DCE_STATIC_DATA && window.DCE_STATIC_DATA.scenarios[currentScenarioId]) {
          const scenData = window.DCE_STATIC_DATA.scenarios[currentScenarioId];
          data = {
            status: 'RESOLVED',
            decision: scenData.trace_auto.steps.step7_verdict.decision,
            final_audit: scenData.trace_auto.steps.post_heal_audit
          };
        } else {
          throw apiErr;
        }
      }
      
      // Update UI in single pass
      hitlTabBadge.classList.add('hidden');
      updateAuditDisplay(data.final_audit);
      setStepState(6, 'completed', '✅');
      
      renderVerdictCard(data.decision);
      setStepState(7, 'completed', '✅');
      setStepState(8, 'completed', '🧠');
      
      fetchAnalytics();
      pipelineStatusText.textContent = '✅ Sign-off received! Verdict rendered and actions dispatched instantly.';

      // Switch back to decision console
      document.querySelector('[data-tab="tab-decision-room"]').click();
    } catch (err) {
      console.error('Error submitting HITL response', err);
    }
  }

  // -------------------------------------------------------------
  // Knowledge Vault & Analytics (Non-blocking)
  // -------------------------------------------------------------
  async function fetchSources() {
    try {
      const res = await fetch('/api/sources');
      const data = await res.json();
      const container = document.getElementById('sources-container');
      container.innerHTML = data.sources.map(src => `
        <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800 space-y-2">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800">
            <h4 class="font-bold text-white text-xs flex items-center gap-1.5">
              <span>🗂️</span> ${src.name}
            </h4>
            <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">${src.item_count} records</span>
          </div>
          <p class="text-[11px] text-slate-400">Indexed for autonomous semantic queries, citation retrieval, and validation.</p>
        </div>
      `).join('');
    } catch (err) {
      console.error('Error loading sources', err);
    }
  }

  async function fetchAnalytics() {
    try {
      let data;
      try {
        const res = await fetch('/api/analytics');
        if (!res.ok) throw new Error('API offline');
        data = await res.json();
      } catch (apiErr) {
        if (window.DCE_STATIC_DATA && window.DCE_STATIC_DATA.analytics) {
          data = window.DCE_STATIC_DATA.analytics;
        } else {
          throw apiErr;
        }
      }
      const m = data.metrics;

      document.getElementById('metric-total-runs').textContent = m.total_decisions_processed || 0;
      document.getElementById('metric-block-rate').textContent = `${m.initial_block_rate_pct || 0}%`;
      document.getElementById('metric-heal-rate').textContent = `${m.autonomous_self_heal_rate_pct || 0}%`;
      document.getElementById('metric-hours-saved').textContent = `${m.estimated_hours_saved || 0} hrs`;

      const recContainer = document.getElementById('recommendations-container');
      recContainer.innerHTML = data.recommendations.map(rec => `
        <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-indigo-400">[${rec.domain}] Pattern: ${rec.pattern_observed}</span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded ${
              rec.impact_level === 'HIGH' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
            }">${rec.impact_level} IMPACT</span>
          </div>
          <div class="text-xs text-slate-300"><strong class="text-slate-400">Root Cause:</strong> ${rec.root_cause}</div>
          <div class="p-2.5 rounded-lg bg-indigo-950/30 border border-indigo-500/30 text-xs text-indigo-200">
            <strong class="text-indigo-300">Actionable Intake Re-engineering:</strong> ${rec.suggested_action}
            <div class="text-[11px] text-emerald-400 mt-1 font-semibold">✨ ${rec.estimated_turnaround_improvement}</div>
          </div>
        </div>
      `).join('');
    } catch (err) {
      console.error('Error fetching analytics', err);
    }
  }

  // -------------------------------------------------------------
  // Custom Modal Handler
  // -------------------------------------------------------------
  btnCustomModal.addEventListener('click', () => customModal.classList.remove('hidden'));
  btnCloseModal.addEventListener('click', () => customModal.classList.add('hidden'));
  btnCancelModal.addEventListener('click', () => customModal.classList.add('hidden'));

  btnSubmitModal.addEventListener('click', async () => {
    const payload = {
      title: document.getElementById('cust-title').value,
      domain: document.getElementById('cust-domain').value,
      amount: document.getElementById('cust-amount').value,
      requester: document.getElementById('cust-requester').value,
      summary: document.getElementById('cust-summary').value
    };

    try {
      const res = await fetch('/api/custom-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      customModal.classList.add('hidden');
      resetUI();

      reqDomainBadge.textContent = payload.domain;
      reqTitle.textContent = payload.title;
      reqId.textContent = data.request.id;
      reqSummary.textContent = payload.summary;
      reqRequester.textContent = payload.requester;
      reqDept.textContent = 'Custom Intake';
      reqAmount.textContent = `$${Number(payload.amount).toLocaleString()}`;
    } catch (err) {
      console.error('Error submitting custom request', err);
    }
  });

  const btnDownloadN8n = document.getElementById('btn-download-n8n');
  if (btnDownloadN8n) {
    btnDownloadN8n.addEventListener('click', () => {
      window.open('/static/n8n/decision_completeness_engine.json', '_blank');
    });
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
});
