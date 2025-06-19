from pydantic import BaseModel, Field
from typing import Optional, List

class VOC(BaseModel):
    Voice_Of_Customer_WHAT_Functional_Description: str = Field(
        description="WHAT: Provide a descriptive explanation of the essential functionality and capabilities that the enhancement or solution must deliver, based on the input requirement."
    )
    
    Voice_Of_Customer_WHY_Business_Benefit_Need: str = Field(
        description="WHY: Provide a detailed explanation of the business need for the enhancement, including the problems it solves and the benefits it offers, based on the input requirement."
    )
    
    Voice_Of_Customer_WHO_WHERE: str = Field(
        description="WHO/WHERE: Provide a descriptive response identifying the primary users, departments, or roles that will interact with or benefit from the enhancement, and explain where it will be applied, based on the input requirement."
    )
    
    Voice_Of_Customer_WHEN: str = Field(
        description="WHEN: Provide a detailed description of how often, under what circumstances, or during which stages of the process the enhancement will be used, based on the input requirement."
    )
    
    Voice_Of_Customer_HOW_Input: str = Field(
        description="HOW (Input): Provide a descriptive breakdown of the input data or information that the enhancement will handle, including any specific changes or data types, based on the input requirement."
    )
    
    Voice_Of_Customer_HOW_Process: str = Field(
        description="HOW (Process): Describe in detail the internal processes, actions, or logic that the enhancement should perform on the inputs to achieve the expected results, based on the input requirement."
    )
    
    Voice_Of_Customer_HOW_Output: str = Field(
        description="HOW (Output): Provide a descriptive explanation of the final outcome or results expected from the enhancement after processing the inputs, including how the output should be structured or used, based on the input requirement."
    )





class ROC(BaseModel):
    

    alternatives_considered: str = Field(description="A listing of the various alternative approaches that were considered.")
    agreed_upon_approach: str = Field(description="Which alternative was selected?")
    # Additional Section
    important_assumptions: str = Field(description="Important assumptions considered during the decision-making process.")
    additional_comments: str = Field(description="Any additional information considered during the decision-making process.")
    



"""
class FD(BaseModel):

    # Functional Design Section
    project_name: str = Field(description="Extracted project name")
    RICEF_id: str = Field(description="Generated or extracted RICEF ID")
    client_name: str = Field(description="Extracted client name")

    Functional_Design_Process: str = Field(
        description="Functional Design - Process: Generated or extracted process flow for the functional design."
    )
    Functional_Design_Interface_Direction: str = Field(
        description="Functional Design - Interface Direction: Direction of data flow (to/from or bi-directional with SAP)."
    )
    Functional_Design_Error_Handling: str = Field(
        description="Functional Design - Error Handling: Generated or extracted error-handling owner definition and business needs."
    )
    Functional_Design_Frequency: str = Field(
        description="Functional Design - Frequency: Frequency at which the report will be run."
    )
    Functional_Design_Data_Volume: str = Field(
        description="Functional Design - Data Volume: Estimated data volume for the report."
    )
    Functional_Design_Security_Requirements: str = Field(
        description="Functional Design - Security Requirements: Security requirements requiring explicit authorization checks or special processing."
    )
    Functional_Design_Data_Sensitivity: str = Field(
        description="Functional Design - Data Sensitivity: Sensitivity of data, including level of restrictions."
    )
    Functional_Design_Unit_Testing: str = Field(
        description="Functional Design - Unit Testing: Information for unit testing scenarios, instructions, test data, and expected results."
    )
    Functional_Design_Additional_Comments: str = Field(
        description="Functional Design - Additional Comments: Additional information for functional design."
    )
    Functional_Design_Rework_Log: str = Field(
        description="Functional Design - Rework Log: Rework log containing previous version(s) of the section."
    )

"""






class FD(BaseModel):
    Functional_Design_reference_sap_r3_transactions_tables_programs: str = Field(
        description="Functional Design - Reference SAP R/3 Transactions/Tables/Programs: (Include: all known transactions, tables and programs that are used, or reports containing similar data. Screenshots are recommended.)"
    )
    Functional_Design_input_selection_criteria: List[dict] = Field(
        description="Functional Design - Input/ Selection Criteria: (What should the user see on the selection screen?)",
        default=[{"Parameter Name": None, "Required / Optional": None, "Special Requirements": None, "Reference Table-Field": None}]
    )
    Functional_Design_process: str = Field(
        description="Functional Design - Process: (If possible, in the form of a flowchart, describe the process and what the program should do)"
    )
    Functional_Design_solution: str = Field(
        description="Functional Design - Solution: (Please enter: SAPScript / Smartform / Adobe Print Form)"
    )
    Functional_Design_output_format_details: List[dict] = Field(
        description="Functional Design - Output/Format Details: (If applicable, what should the user see on the selection screen?)",
        default=[{"Page (First or Next)": None, "Window (ex: Main)": None, "Font Name (if Applicable)": None, "Font Type (Bold, Italic, Underline)": None, "Data Origin (SAP field Name)": None, "Field Label/Description": None}]
    )
    Functional_Design_bar_code_requirements: List[dict] = Field(
        description="Functional Design - Bar Code Requirements:",
        default=[{"Serial Number": None, "Field Name": None, "Bar Type Code": None}]
    )
    Functional_Design_paper_requirements: str = Field(
        description="Functional Design - Paper Requirements: (Please Specify: pre-printed stationary, multi-page, or multi-form. If left blank, output on letter paper is assumed.)"
    )
    Functional_Design_logo_requirements: str = Field(
        description="Functional Design - Logo Requirements: (Please provide company logo in TIF, JPEG, VMP, other)"
    )
    Functional_Design_software_requirements: str = Field(
        description="Functional Design - Software Requirements: (ex: TEC.it/ Printer Vendors DLL’s)"
    )
    Functional_Design_printer_requirements: str = Field(
        description="Functional Design - Printer Requirements: (ex: Label Printer, barcode chip, laser, Jet, Matrix)"
    )
    Functional_Design_output_type_and_application: str = Field(
        description="Functional Design - Output Type and Application:"
    )
    Functional_Design_security_requirements_no_specific_restrictions: Optional[str] = Field(
        description="Functional Design - Security Requirements: No Specific Restrictions"
    )
    Functional_Design_security_requirements_restriction_based_on_certain_criteria: Optional[str] = Field(
        description="Functional Design - Security Requirements: Restriction Based on Certain Criteria (ex: Restricted by sales area?)"
    )
    Functional_Design_security_requirements_other: Optional[str] = Field(
        description="Functional Design - Security Requirements: Other"
    )
    Functional_Design_data_sensitivity: str = Field(
        description="Functional Design - Data Sensitivity: (Plant/Level of restrictions, please explain)"
    )
    Functional_Design_unit_testing: List[dict] = Field(
        description="Functional Design - Unit Testing: (Information the developer can use to unit test the application. This needs to include test scenarios, instructions, test data, and expected results)",
        default=[{"Test Condition / Test Scenario": None, "Steps Involved": None, "Input Values (Test Data)": None, "Expected Results": None}]
    )
    Functional_Design_additional_comments: str = Field(
        description="Functional Design - Additional Comments: (Add any additional information necessary to assist in development as needed)"
    )
    Functional_Design_rework_log: str = Field(
        description="Functional Design - Rework Log: (The version shown above is the latest, this area may contain previous version(s) of the same section)"
    )



class TD(BaseModel):
    Technical_Design_design_points: str = Field(
        description="Technical Design - Design Points: (Describe anything that will make the definition of the design clearer, including: calculations and formulas, particular conditions where the program should behave differently, recommendations, etc. If applicable, include recommendations or concerns regarding performance.)"
    )
    Technical_Design_program_logic: str = Field(
        description="Technical Design - Program Logic: (Insert Visio/Pseudo code/Table or Diagram with definition of Project Flow)"
    )
    Technical_Design_program_logic_steps: List[dict] = Field(
        description="Technical Design - Program Logic Steps:",
        default=[{"Step No.": None, "System object accessed / Processing done": None, "Parameters passed": None, "Extracted Fields": None, "Remarks": None}]
    )
    Technical_Design_special_configuration_settings_assumptions: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions: (Describe any special or temporary pre-requisite configuration requirements)"
    )
    Technical_Design_additional_comments: str = Field(
        description="Technical Design - Additional Comments: (Add any additional information necessary to assist in development as needed, e.g. performance concerns)"
    )
    Technical_Design_rework_log: str = Field(
        description="Technical Design - Rework Log: (The version shown above is the latest, this area may contain previous version(s) of the same section)"
    )