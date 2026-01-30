# SOP: Test Case Generation

## Goal
Generate comprehensive, deterministic Gherkin test cases from a user-provided description using a local LLM.

## Inputs
- **Prompt**: User description of the feature or scenario.
- **Model**: Default `llama3.2`.

## Logic Rules
1.  **Format**: Output must be valid Markdown.
2.  **Structure**:
    -   **Feature**: Name of the feature.
    -   **Scenario**: Title of the test case.
    -   **Given/When/Then**: Gherkin steps.
3.  **Tone**: Professional, technical, QA-focused.
4.  **Validation**: Ensure no truncated output.

## Edge Cases
- **Empty Prompt**: Return specific error message.
- **Ollama Offline**: Retry once, then fail gracefully.
