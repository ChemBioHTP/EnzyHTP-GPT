import json
from pathlib import Path
from types import SimpleNamespace

from experiment.agents import ResultExplainerAssistant
from experiment.models import Experiment


def test_build_equilibration_metadata_from_assessment_json(tmp_path):
    exp_dir = tmp_path / "exp"
    assessment_dir = exp_dir / "plots" / "equilibration" / "MUTANT_A" / "replica_0"
    assessment_dir.mkdir(parents=True, exist_ok=True)
    assessment_file = assessment_dir / "equil_assessment.json"
    assessment_file.write_text(
        json.dumps(
            {
                "method": "Chodera automated equilibration detection scheme (PMCID: PMC4945107)",
                "mutant": "MUTANT_A",
                "replica_id": "0",
                "overall_status": "equilibrated",
                "series": {
                    "temp_k": {"status": "equilibrated", "discarded_fraction": 0.12},
                    "press": {"status": "equilibrated", "discarded_fraction": 0.22},
                    "etot": {"status": "equilibrated", "discarded_fraction": 0.18},
                },
            }
        ),
        encoding="utf-8",
    )

    assistant = ResultExplainerAssistant.__new__(ResultExplainerAssistant)
    assistant.experiment = SimpleNamespace(
        directory=str(exp_dir),
        type=Experiment.INDIVIDUAL_TYPE,
        subordinate_experiments=[],
    )
    metadata = assistant._build_equilibration_metadata()

    assert "equilibration_assessment" in metadata
    assert "Chodera automated equilibration detection scheme" in metadata["equilibration_assessment"]
    summary = metadata.get("equilibration_summary", {})
    assert summary.get("n_replica_assessments") == 1
    assert summary.get("n_equilibrated_replicas") == 1
