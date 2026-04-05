import importlib.util
import json
import sys
from pathlib import Path


def _load_md_main_script_module():
    flask_server_dir = Path(__file__).resolve().parents[2]
    script_path = flask_server_dir / "templates" / "slurm_run" / "md_main_script.py"
    script_dir = script_path.parent
    sys.path.insert(0, str(script_dir))
    try:
        spec = importlib.util.spec_from_file_location("md_main_script", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if sys.path and sys.path[0] == str(script_dir):
            sys.path.pop(0)


def test_parse_mdout_records_should_ignore_average_and_rms_sections():
    module = _load_md_main_script_module()
    equi_out_path = Path(__file__).resolve().parents[1] / "test_files" / "example_equi.out"

    records = module._parse_mdout_records(str(equi_out_path))
    raw_lines = equi_out_path.read_text(encoding="utf-8").splitlines()
    trailer_index = len(raw_lines)
    for idx, line in enumerate(raw_lines):
        if module.MDOUT_TRAILER_SECTION_PATTERN.search(line):
            trailer_index = idx
            break
    expected_state_line_count = sum(
        1 for line in raw_lines[:trailer_index] if module.MDOUT_STATE_PATTERN.search(line)
    )

    assert len(records) == expected_state_line_count
    assert records
    assert records[0]["nstep"] >= 0
    assert all(
        records[idx]["time_ps"] >= records[idx - 1]["time_ps"]
        for idx in range(1, len(records))
    )


def test_generate_equilibration_plots_for_manual_inspection():
    module = _load_md_main_script_module()
    equi_out_path = Path(__file__).resolve().parents[1] / "test_files" / "example_equi.out"
    output_dir = Path(__file__).resolve().parents[1] / "test_files" / "generated_plots"
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_records = module._parse_mdout_records(str(equi_out_path))
    records = [{**record, "stage": "equi_npt_free_bb"} for record in raw_records]

    plot_cases = [
        ("temp_k", "Temperature (K)", "Temperature", output_dir / "example_equi_temperature.png"),
        ("press", "Pressure (bar)", "Pressure", output_dir / "example_equi_pressure.png"),
        ("etot", "Total Energy", "Total Energy", output_dir / "example_equi_energy.png"),
    ]

    for y_key, y_label, title, output_path in plot_cases:
        is_successful = module._plot_equilibration_curve(
            records=records,
            y_key=y_key,
            y_label=y_label,
            title=f"Example Equi {title}",
            output_filepath=str(output_path),
            stage_order=["equi_npt_free_bb"],
        )
        assert is_successful
        assert output_path.is_file()
        assert output_path.stat().st_size > 0


def test_generate_equilibration_assessment_json(tmp_path):
    module = _load_md_main_script_module()
    test_files_dir = Path(__file__).resolve().parents[1] / "test_files"
    output_dir = tmp_path / "generated_assessment"
    output_dir.mkdir(parents=True, exist_ok=True)

    stage_file = output_dir / "equi_npt_free_bb.out"
    stage_file.write_text((test_files_dir / "example_equi.out").read_text(encoding="utf-8"), encoding="utf-8")

    assessment_path = module.generate_equilibration_assessment(
        trajectory_filepath=str(output_dir / "prod_npt.nc"),
        mutant="TEST_MUTANT",
        replica_id="0",
    )

    assert assessment_path is not None
    assessment_file = Path(assessment_path)
    assert assessment_file.is_file()
    assessment = json.loads(assessment_file.read_text(encoding="utf-8"))
    assert "Chodera automated equilibration detection scheme" in assessment.get("method", "")
    assert assessment.get("mutant") == "TEST_MUTANT"
    assert isinstance(assessment.get("series"), dict) and assessment["series"]
    assert "temp_k" in assessment["series"]
    assert "press" in assessment["series"]
    assert "etot" in assessment["series"]
    assert "recommended_discard_ps" not in assessment
