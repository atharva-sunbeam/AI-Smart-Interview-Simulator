from backend.report_generator import ReportGenerator

def test_generate_final_report():

    
    generator = ReportGenerator()

    report = generator.generate_final_report(
        candidate_name="Alice",
        predicted_role="Python Developer",
        questions_asked=["What is Python?"],
        scores=[90],
        strengths=["Good OOP knowledge"],
        weaknesses=["Needs SQL practice"],
        recommendations=["Practice SQL joins"],
    )

    assert report["candidate_name"] == "Alice"
    assert report["predicted_role"] == "Python Developer"
    assert report["average_score"] == 90
    

def test_save_report(tmp_path):


    generator = ReportGenerator()

    report = generator.generate_final_report(
        candidate_name="Alice",
        predicted_role="Python Developer",
        questions_asked=[],
        scores=[],
        strengths=[],
        weaknesses=[],
        recommendations=[],
    )

    output_file = tmp_path / "interview_report.json"

    generator.save_report(
        report,
        str(output_file),
    )

    assert output_file.exists()

