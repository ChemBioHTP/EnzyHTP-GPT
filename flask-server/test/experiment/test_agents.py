from experiment.agents import QuestionAnalyzerAssistant

def test_QA_with_no_money_api_key():
    qa = QuestionAnalyzerAssistant(
        "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",
    )
    is_valid, status_code, message = qa.ask_gpt("Hello, world!")
    assert (is_valid, status_code) == (True, 429)
    assert "You exceeded your current quota" in message
