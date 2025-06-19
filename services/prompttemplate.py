from langchain.prompts import PromptTemplate


def promtfun(client_problem):

  if "voc" in client_problem:
    prompt_template = PromptTemplate(
    input_variables=["client_problem"],
    template="""
    Client Business Problem: {client_problem}

    Task:
    1. Analyze the provided client business problem and extract all necessary information relevant to filling out the RICEF form.
    2. Ensure each field in the RICEF form is accurately filled based on the extracted information or generate values where necessary, while adhering to the form's context.

    The RICEF form should be structured in JSON format with the following fields:

    Start JSON
    {{"project_name":"Extracted project name", "RICEF_id": "Generated or extracted RICEF ID", "client_name": "Extracted client name", "WHAT: Functional Description": "Generated or extracted short description of the required report", "WHY: Business Benefit / Need": "Generated or extracted short description of why the report is needed and the impact if not implemented", "WHO / WHERE": "Generated or extracted description of who will be using this report and where it will be used, including stakeholders, departments, and organizational units", "WHEN": "Generated or extracted timeline indicating when this report will be used (e.g., daily, weekly, monthly)", "HOW: Input": "Generated or extracted functional description of the input", "HOW: Process": "Generated or extracted description of the process, outlining what the program should do at a functional level", "HOW: Output": "Generated or extracted functional description of the output", "Additional Comments": "Generated or extracted additional information to assist in development"}}
    End JSON

    Ensure that:
    1. All extracted or generated values align with the context of the client's business problem.
    2. The JSON output strictly adheres to proper syntax.
    3. Use only double quotes for keys and values.
    4. The final output JSON must be formatted as a single-line string without any newline characters or "\\n".
    5. Ensure the JSON is enclosed strictly between the "Start JSON" and "End JSON" markers without any newline characters in between.
    6. Do not use any escape characters in the output.
    """
)



    return prompt_template
  
  elif "roc" in client_problem:
    prompt_template = PromptTemplate(
        input_variables=["client_problem"],
        template="""
        Client Business Problem: {client_problem}

        Task:
        1. Analyze the provided client business problem and extract all necessary information relevant to filling out the RICEF form.
        2. Ensure each field in the RICEF form is accurately filled based on the extracted information or generate values where necessary, while adhering to the form's context.

        The RICEF form should be structured in JSON format with the following fields:

        {{
          "file_name" : "Extract file name form prompt" 
          "Alternatives Considered": "Generated or extracted listing of the various alternative approaches considered",
          "Agreed Upon Approach": "Generated or extracted description of which alternative was selected",
          "Functional Description": "Generated or extracted short description of the required interface",
          "Business Benefit/Need": "Generated or extracted description of why the interface is needed and the impact if not implemented",
          "Important Assumptions": "Generated or extracted important assumptions for the project",
          "Additional Comments": "Generated or extracted additional information considered during the decision-making process"
        }}

        Ensure that:
        1. All extracted or generated values align with the context of the client's business problem.
        2. The JSON output strictly adheres to proper syntax.
        """
    )
    return prompt_template
