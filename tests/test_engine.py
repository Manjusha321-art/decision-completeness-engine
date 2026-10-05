"""
Unit and Integration Test Suite for The Decision Completeness Engine (DCE).
"""

import unittest
from decision_engine import (
    DecisionCompletenessEngine,
    DecisionRequest,
    EvidenceRequirement,
    EvidenceItem,
    EvidenceStatus,
    ImportanceLevel,
    DecisionVerdict,
    get_all_scenarios,
    get_scenario
)
from decision_engine.planner import EvidencePlanner
from decision_engine.auditor import EvidenceAuditor
from decision_engine.retriever import AutonomousRetriever
from decision_engine.hitl import PrecisionHITL
from decision_engine.decider import DecisionDeliberator
from decision_engine.analytics import ProcessAnalyticsEngine


class TestDecisionCompletenessEngine(unittest.TestCase):

    def setUp(self):
        self.engine = DecisionCompletenessEngine()
        self.scenarios = get_all_scenarios()

    def test_evidence_planner_procurement(self):
        scen = self.scenarios["vendor_procurement"]
        planner = EvidencePlanner()
        reqs = planner.plan_requirements(scen["request"])

        req_ids = [r.id for r in reqs]
        self.assertIn("PRICE_BENCHMARK", req_ids)
        self.assertIn("SECURITY_CERTIFICATION", req_ids)
        self.assertIn("BUDGET_EXECUTIVE_APPROVAL", req_ids)

        # Budget approval should be CRITICAL for $85k
        budget_req = next(r for r in reqs if r.id == "BUDGET_EXECUTIVE_APPROVAL")
        self.assertEqual(budget_req.importance, ImportanceLevel.CRITICAL)

    def test_evidence_planner_lending(self):
        scen = self.scenarios["commercial_lending"]
        planner = EvidencePlanner()
        reqs = planner.plan_requirements(scen["request"])

        req_ids = [r.id for r in reqs]
        self.assertIn("TAX_RETURNS_VERIFIED", req_ids)
        self.assertIn("BANK_CASH_FLOW_STATEMENTS", req_ids)
        self.assertIn("ENTITY_GOOD_STANDING", req_ids)

    def test_auditor_blocks_incomplete_evidence(self):
        scen = self.scenarios["vendor_procurement"]
        auditor = EvidenceAuditor()
        planner = EvidencePlanner()

        reqs = planner.plan_requirements(scen["request"])
        audit_report = auditor.audit(reqs, scen["initial_evidence"])

        # Initial evidence only has 2 items; 3 missing, 2 critical
        self.assertFalse(audit_report.is_complete)
        self.assertGreater(audit_report.critical_missing_count, 0)
        self.assertIsNotNone(audit_report.blocking_reason)
        self.assertIn("DECISION GATE ENGAGED", audit_report.blocking_reason)

    def test_autonomous_retriever_self_healing(self):
        scen = self.scenarios["vendor_procurement"]
        planner = EvidencePlanner()
        auditor = EvidenceAuditor()
        retriever = AutonomousRetriever()

        reqs = planner.plan_requirements(scen["request"])
        audit_report = auditor.audit(reqs, scen["initial_evidence"])

        recovered, trace = retriever.investigate(scen["request"], audit_report.missing_requirements)
        recovered_ids = [r.requirement_id for r in recovered]

        # Should recover SOC2 from Drive and Vendor history from ERP
        self.assertIn("SECURITY_CERTIFICATION", recovered_ids)
        self.assertIn("VENDOR_PERFORMANCE_HISTORY", recovered_ids)

        # But budget approval cannot be recovered autonomously
        self.assertNotIn("BUDGET_EXECUTIVE_APPROVAL", recovered_ids)

    def test_precision_hitl_generation_and_resolution(self):
        scen = self.scenarios["vendor_procurement"]
        planner = EvidencePlanner()
        auditor = EvidenceAuditor()
        retriever = AutonomousRetriever()
        hitl = PrecisionHITL()

        reqs = planner.plan_requirements(scen["request"])
        dossier = list(scen["initial_evidence"])
        audit_1 = auditor.audit(reqs, dossier)
        recovered, _ = retriever.investigate(scen["request"], audit_1.missing_requirements)
        dossier.extend(recovered)

        audit_2 = auditor.audit(reqs, dossier)
        self.assertFalse(audit_2.is_complete)

        # Generate targeted micro-request
        micro_request = hitl.generate_micro_request(scen["request"], audit_2.missing_requirements, dossier)
        self.assertIsNotNone(micro_request)
        self.assertEqual(micro_request.missing_item_name, "Departmental Budget Sign-off (VP / Finance Head)")
        self.assertIn("VP of Finance", micro_request.target_role)

        # Human resolves the single gap
        resolved_item = hitl.resolve_gap(
            target_req=audit_2.missing_requirements[0],
            action_chosen="Grant One-Click Approval",
            user_notes="Funds authorized from Q4 IT budget.",
            user_identity="Sarah Jenkins (VP Finance)"
        )
        self.assertIsNotNone(resolved_item)
        self.assertEqual(resolved_item.status, EvidenceStatus.HUMAN_PROVIDED)

        dossier.append(resolved_item)
        audit_3 = auditor.audit(reqs, dossier)
        self.assertTrue(audit_3.is_complete)

    def test_gatekeeper_blocks_verdict_without_hitl(self):
        scen = self.scenarios["vendor_procurement"]
        result = self.engine.run_full_pipeline(
            scen["request"],
            scen["initial_evidence"],
            auto_resolve_hitl=False
        )

        # Must halt at gate
        self.assertEqual(result["steps"]["step7_verdict"]["verdict"], DecisionVerdict.BLOCKED.value)
        self.assertIsNotNone(result["steps"]["step6_hitl"]["hitl_prompt"])

    def test_full_pipeline_success_with_hitl(self):
        scen = self.scenarios["vendor_procurement"]
        result = self.engine.run_full_pipeline(
            scen["request"],
            scen["initial_evidence"],
            auto_resolve_hitl=True,
            hitl_action="Grant One-Click Approval"
        )

        # Must approve with high confidence and audit trail
        self.assertEqual(result["steps"]["step7_verdict"]["verdict"], DecisionVerdict.APPROVED.value)
        self.assertGreaterEqual(result["steps"]["step7_verdict"]["confidence_score"], 0.90)
        self.assertGreater(len(result["steps"]["step7_verdict"]["actions_executed"]), 0)
        self.assertGreater(len(result["steps"]["step7_verdict"]["reasoning_chain"]), 0)

    def test_meta_learning_pattern_mining(self):
        analytics = ProcessAnalyticsEngine()
        metrics = analytics.get_summary_metrics()
        self.assertGreater(metrics["total_decisions_processed"], 0)
        self.assertGreater(metrics["gatekeeper_blocks_triggered"], 0)

        insights = analytics.generate_recommendations()
        self.assertGreater(len(insights), 0)
        self.assertTrue(any("Procurement" in i.domain for i in insights))

    def test_all_eight_scenarios_execute(self):
        all_scens = get_all_scenarios()
        self.assertEqual(len(all_scens), 8)
        for scen_id, scen in all_scens.items():
            res = self.engine.run_full_pipeline(
                scen["request"],
                scen["initial_evidence"],
                auto_resolve_hitl=True
            )
            self.assertEqual(
                res["steps"]["step7_verdict"]["verdict"],
                DecisionVerdict.APPROVED.value,
                f"Scenario '{scen_id}' failed to approve"
            )
            self.assertGreaterEqual(
                res["steps"]["step7_verdict"]["confidence_score"],
                0.90,
                f"Scenario '{scen_id}' confidence too low"
            )


if __name__ == "__main__":
    unittest.main()
