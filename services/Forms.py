from pydantic import BaseModel, Field
from typing import Optional, List
from services.shared_models import VOC, ROC


class FD(BaseModel):
    Functional_Design_reference_sap_r3_transactions_tables_programs: str = Field(
        description="Functional Design - Reference SAP R/3 Transactions/Tables/Programs: Include all known transactions, tables and programs that are used, or reports containing similar data."
    )
    Functional_Design_input_selection_criteria: List[dict] = Field(
        description="Functional Design - Input/Selection Criteria: What should the user see on the selection screen?",
        default=[{"Parameter Name": None, "Required / Optional": None, "Special Requirements": None, "Reference Table-Field": None}]
    )
    Functional_Design_process: str = Field(
        description="Functional Design - Process: Describe the process and what the program should do, if possible in form of a flowchart."
    )
    Functional_Design_solution: str = Field(
        description="Functional Design - Solution: SAPScript / Smartform / Adobe Print Form."
    )
    Functional_Design_output_format_details: List[dict] = Field(
        description="Functional Design - Output/Format Details:",
        default=[{"Page (First or Next)": None, "Window (ex: Main)": None, "Font Name (if Applicable)": None, "Font Type (Bold, Italic, Underline)": None, "Data Origin (SAP field Name)": None, "Field Label/Description": None}]
    )
    Functional_Design_bar_code_requirements: List[dict] = Field(
        description="Functional Design - Bar Code Requirements:",
        default=[{"Serial Number": None, "Field Name": None, "Bar Type Code": None}]
    )
    Functional_Design_paper_requirements: str = Field(
        description="Functional Design - Paper Requirements: pre-printed stationary, multi-page, or multi-form."
    )
    Functional_Design_logo_requirements: str = Field(
        description="Functional Design - Logo Requirements: provide company logo in TIF, JPEG, VMP, other."
    )
    Functional_Design_software_requirements: str = Field(
        description="Functional Design - Software Requirements: e.g. TEC.it/Printer Vendors DLLs."
    )
    Functional_Design_printer_requirements: str = Field(
        description="Functional Design - Printer Requirements: e.g. Label Printer, barcode chip, laser, Jet, Matrix."
    )
    Functional_Design_output_type_and_application: str = Field(
        description="Functional Design - Output Type and Application."
    )
    Functional_Design_security_requirements_no_specific_restrictions: Optional[str] = Field(
        default=None, description="Functional Design - Security Requirements: No Specific Restrictions"
    )
    Functional_Design_security_requirements_restriction_based_on_certain_criteria: Optional[str] = Field(
        default=None, description="Functional Design - Security Requirements: Restriction Based on Certain Criteria."
    )
    Functional_Design_security_requirements_other: Optional[str] = Field(
        default=None, description="Functional Design - Security Requirements: Other"
    )
    Functional_Design_data_sensitivity: str = Field(
        description="Functional Design - Data Sensitivity: Plant/Level of restrictions, please explain."
    )
    Functional_Design_unit_testing: List[dict] = Field(
        description="Functional Design - Unit Testing: test scenarios, instructions, test data, and expected results.",
        default=[{"Test Condition / Test Scenario": None, "Steps Involved": None, "Input Values (Test Data)": None, "Expected Results": None}]
    )
    Functional_Design_additional_comments: str = Field(
        description="Functional Design - Additional Comments."
    )
    Functional_Design_rework_log: str = Field(
        description="Functional Design - Rework Log."
    )


class TD(BaseModel):
    Technical_Design_design_points: str = Field(
        description="Technical Design - Design Points: calculations, formulas, conditions, performance recommendations."
    )
    Technical_Design_program_logic: str = Field(
        description="Technical Design - Program Logic: Visio/Pseudo code/Table or Diagram with definition of Project Flow."
    )
    Technical_Design_program_logic_steps: List[dict] = Field(
        description="Technical Design - Program Logic Steps:",
        default=[{"Step No.": None, "System object accessed / Processing done": None, "Parameters passed": None, "Extracted Fields": None, "Remarks": None}]
    )
    Technical_Design_special_configuration_settings_assumptions: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions."
    )
    Technical_Design_additional_comments: str = Field(
        description="Technical Design - Additional Comments."
    )
    Technical_Design_rework_log: str = Field(
        description="Technical Design - Rework Log."
    )
