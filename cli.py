"""
Command Line Interface (CLI) for The Decision Completeness Engine.
Usage:
  python cli.py run --scenario vendor_procurement
  python cli.py run --scenario commercial_lending --auto-approve
  python cli.py analytics
"""

import sys
import argparse
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from decision_engine import (
    DecisionCompletenessEngine,
    get_all_scenarios,
    get_scenario,
    DecisionRequest
)


def print_banner():
    print("=" * 72)
    print("   THE DECISION COMPLETENESS ENGINE (DCE)")
    print("   'Knows when NOT to decide • Self-heals missing evidence'")
    print("=" * 72)


def run_scenario_cli(scenario_id: str, auto_approve: bool = False):
    print_banner()
    engine = DecisionCompletenessEngine()
    scen = get_scenario(scenario_id)

    print(f"\n[STEP 1: INTAKE]")
    print(f"  Title:      {scen['request'].title}")
    print(f"  Requester:  {scen['request'].requester} ({scen['request'].department})")
    print(f"  Value:      ${scen['request'].context_data.get('amount', 0):,}")
    print(f"  Initial:    {len(scen['initial_evidence'])} item(s) in initial dossier")

    print(f"\n[STEP 2: EVIDENCE PLANNING]")
    reqs = engine.planner.plan_requirements(scen['request'])
    print(f"  Inferred {len(reqs)} dynamic requirements:")
    for r in reqs:
        print(f"    - [{r.importance.value:9}] {r.name} ({r.category})")

    print(f"\n[STEP 3 & 4: INITIAL GAP AUDIT & GATEKEEPER]")
    audit = engine.auditor.audit(reqs, scen['initial_evidence'])
    print(f"  Completeness Score: {audit.completeness_score}%")
    print(f"  Verified Items:     {audit.verified_count} / {audit.total_requirements}")
    if not audit.is_complete:
        print(f"  [GATE ENGAGED] Refusing to render verdict! {audit.critical_missing_count} critical item(s) missing.")
        print(f"  Zero-hallucination policy enforced. Starting autonomous self-healing...")
    else:
        print(f"  [PASSED] Initial dossier complete.")

    print(f"\n[STEP 5: AUTONOMOUS SELF-HEALING INVESTIGATION]")
    dossier = list(scen['initial_evidence'])
    if audit.missing_requirements:
        healed, trace = engine.retriever.investigate(scen['request'], audit.missing_requirements)
        print(f"  Traversing: Corporate Drive, Gmail Archive, ERP Ledger, Public Registries...")
        print(f"  Discovered {len(healed)} missing document(s):")
        for item in healed:
            print(f"    + Recovered: {item.requirement_name}")
            print(f"      Source:    {item.source_type.value} ({item.source_location})")
            print(f"      Citation:  {item.summary[:90]}...")
        dossier.extend(healed)
    else:
        print("  No gaps to heal.")

    post_heal_audit = engine.auditor.audit(reqs, dossier)
    print(f"\n  Post-Healing Completeness: {post_heal_audit.completeness_score}%")

    # Step 6: HITL
    if not post_heal_audit.is_complete:
        print(f"\n[STEP 6: PRECISION HUMAN-IN-THE-LOOP]")
        hitl_prompt = engine.hitl.generate_micro_request(scen['request'], post_heal_audit.missing_requirements, dossier)
        if hitl_prompt:
            print(f"  Target Reviewer: {hitl_prompt.target_role}")
            print(f"  Context Summary: {hitl_prompt.summary_context}")
            print(f"  Missing Delta:   {hitl_prompt.missing_item_name}")
            print(f"  Action Required: {hitl_prompt.specific_action_required}")

            if auto_approve:
                print("\n  [CLI Mode: Auto-approving micro-request]")
                resolved = engine.hitl.resolve_gap(
                    target_req=post_heal_audit.missing_requirements[0],
                    action_chosen="Grant One-Click Approval",
                    user_notes="Authorized via CLI runner."
                )
                dossier.append(resolved)
            else:
                user_choice = input("\n  Resolve gap? [A]pprove / [R]eject / [S]kip: ").strip().upper()
                if user_choice == "A":
                    resolved = engine.hitl.resolve_gap(
                        target_req=post_heal_audit.missing_requirements[0],
                        action_chosen="Grant One-Click Approval",
                        user_notes="Direct interactive CLI authorization."
                    )
                    dossier.append(resolved)
                elif user_choice == "R":
                    resolved = engine.hitl.resolve_gap(
                        target_req=post_heal_audit.missing_requirements[0],
                        action_chosen="Reject / Deny Request",
                        user_notes="Explicit denial via CLI."
                    )
                    dossier.append(resolved)
                else:
                    print("  Skipped. Decision remains halted.")

    # Step 7: Verdict
    print(f"\n[STEP 7: DELIBERATION & ACTION EXECUTION]")
    verdict_res = engine.decider.deliberate(scen['request'], reqs, dossier)
    print(f"  Decision ID:    {verdict_res.decision_id}")
    print(f"  Verdict:        {verdict_res.verdict.value}")
    print(f"  Confidence:     {int(verdict_res.confidence_score * 100)}%")
    print(f"  Recommendation: {verdict_res.recommendation}")
    print(f"\n  Reasoning Chain:")
    for r in verdict_res.reasoning_chain:
        print(f"    * {r}")
    print(f"\n  Actions Executed:")
    for a in verdict_res.actions_executed:
        print(f"    + {a['action_name']} ({a['system']}): {a['details']}")

    # Step 8: Telemetry
    print(f"\n[STEP 8: META-LEARNING & PROCESS OPTIMIZATION]")
    engine.analytics.record_decision(
        request_id=scen['request'].id,
        domain=scen['request'].domain,
        title=scen['request'].title,
        initially_blocked=not audit.is_complete,
        initial_missing=[r.id for r in audit.missing_requirements],
        self_healed=[i.requirement_id for i in dossier if i.status.value == "SELF_HEALED"],
        required_hitl=[i.requirement_id for i in dossier if i.status.value == "HUMAN_PROVIDED"]
    )
    insights = engine.analytics.generate_recommendations()
    if insights:
        print(f"  Discovered Intake Pattern:")
        print(f"    Pattern:    {insights[0].pattern_observed}")
        print(f"    Root Cause: {insights[0].root_cause}")
        print(f"    Intake Fix: {insights[0].suggested_action}")

    print("\n" + "=" * 72 + "\n")


def print_analytics_cli():
    print_banner()
    engine = DecisionCompletenessEngine()
    m = engine.analytics.get_summary_metrics()
    print("\n[HISTORICAL META-LEARNING TELEMETRY]")
    print(f"  Total Decisions Processed:    {m['total_decisions_processed']}")
    print(f"  Gatekeeper Block Rate:        {m['initial_block_rate_pct']}% (Zero-hallucination halts)")
    print(f"  Autonomous Self-Heal Rate:    {m['autonomous_self_heal_rate_pct']}%")
    print(f"  Precision HITL Rate:          {m['human_micro_request_rate_pct']}%")
    print(f"  Estimated Manual Hours Saved: {m['estimated_hours_saved']} hours")

    print("\n[TOP EVIDENCE BOTTLENECKS]")
    for b in m['top_blockers']:
        print(f"  * {b['item']:30} {b['count']} times ({b['frequency_pct']}%)")

    print("\n[PROCESS RE-ENGINEERING PROPOSALS]")
    recs = engine.analytics.generate_recommendations()
    for r in recs:
        print(f"  [{r.domain}] {r.pattern_observed}")
        print(f"    Root Cause: {r.root_cause}")
        print(f"    Proposal:   {r.suggested_action}")
        print(f"    Turnaround: {r.estimated_turnaround_improvement}\n")


def main():
    parser = argparse.ArgumentParser(description="The Decision Completeness Engine CLI")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run a decision scenario")
    run_parser.add_argument("--scenario", default="vendor_procurement", help="Scenario ID (vendor_procurement, commercial_lending, executive_hiring, healthcare_claim)")
    run_parser.add_argument("--auto-approve", action="store_true", help="Auto approve precision HITL micro-request")

    subparsers.add_parser("analytics", help="View meta-learning telemetry & recommendations")
    subparsers.add_parser("scenarios", help="List available scenarios")

    args = parser.parse_args()

    if args.command == "run":
        run_scenario_cli(args.scenario, auto_approve=args.auto_approve)
    elif args.command == "analytics":
        print_analytics_cli()
    elif args.command == "scenarios":
        print_banner()
        print("\nAvailable Pre-configured Scenarios:")
        for sid, s in get_all_scenarios().items():
            print(f"  * {sid:22} : {s['name']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
