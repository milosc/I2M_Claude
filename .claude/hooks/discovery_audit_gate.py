import os
import sys
import re

def verify_audit(analysis_dir):
    report_path = os.path.join(analysis_dir, "05-documentation", "AUDIT_REPORT.md")
    
    if not os.path.exists(report_path):
        print("❌ FAIL: Zero Hallucination Audit has not been performed. Run /discovery-audit first.")
        return False

    with open(report_path, "r") as f:
        content = f.read()
        
    # Check for PASS status in the report
    if "Status: PASS" not in content and "status: PASS" not in content.upper():
        print("❌ FAIL: Zero Hallucination Audit failed or is incomplete. Check HALUCINATIONS_LOG.md.")
        return False

    print("✅ Zero Hallucination Audit Verified (PASS).")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 discovery_audit_gate.py <ClientAnalysis_Directory>")
        sys.exit(1)
    
    if not verify_audit(sys.argv[1]):
        sys.exit(1)
