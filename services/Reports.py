from pydantic import BaseModel, Field
from typing import Optional, List
from services.shared_models import VOC, ROC


class InputSelectionCriterion(BaseModel):
    field_name: str = Field(..., description="Name of the input field")
    data_type: str = Field(..., description="Data type of the field")
    default_value: Optional[str] = Field(None, description="Default value if any")
    is_required: Optional[bool] = Field(True, description="Is this field required?")


class SecurityRequirements(BaseModel):
    yes_no: Optional[str] = Field(None, description="Security Requirements: Yes/No")
    no_specific_restrictions: Optional[str] = Field(None, description="No Specific Restrictions")
    restriction_based_on_certain_criteria: Optional[str] = Field(None, description="Restriction Based on Certain Criteria")
    other: Optional[str] = Field(None, description="Other")


class UnitTesting(BaseModel):
    unit_testing: str = Field(..., description="Unit Testing: test scenarios, instructions, test data, expected results")
    test_condition_test_scenario: Optional[str] = Field(None, description="Test Condition / Test Scenario")
    steps_involved: Optional[str] = Field(None, description="Steps Involved")
    input_values_test_data: Optional[str] = Field(None, description="Input Values (Test Data)")
    expected_results: Optional[str] = Field(None, description="Expected Results")


class FD(BaseModel):
    Functional_Design_reference_sap_fiori_tiles_transactions_tables_programs: str = Field(
        ..., description="Functional Design - Reference SAP Fiori Tiles/Transactions/Tables/Programs."
    )
    Functional_Design_input_selection_criteria: List[InputSelectionCriterion] = Field(
        ..., description="Functional Design - Input/Selection Criteria."
    )
    Functional_Design_process: str = Field(
        ..., description="Functional Design - Process: describe the process in form of a flowchart."
    )
    Functional_Design_output_report_layout: str = Field(
        ..., description="Functional Design - Output/Report Layout: layout, columns, headings, summations."
    )
    Functional_Design_column_title_as_it_should_appear_on_the_report_output: Optional[str] = Field(None, description="Column Title as it should appear on the report output")
    Functional_Design_reference_table_field_output: Optional[str] = Field(None, description="Reference Table-Field for Output")
    Functional_Design_sort: Optional[str] = Field(None, description="Sort")
    Functional_Design_group_level: Optional[str] = Field(None, description="Group Level")
    Functional_Design_hotspot: Optional[str] = Field(None, description="Hotspot")
    Functional_Design_drill_down: Optional[str] = Field(None, description="Drill Down")
    Functional_Design_column_description: Optional[str] = Field(None, description="Description of the Column")
    Functional_Design_special_functionality: str = Field(
        ..., description="Functional Design - Special Functionality: drill-down/hotspots, links to other transactions."
    )
    Functional_Design_error_handling: str = Field(..., description="Functional Design - Error Handling: Owner Definition & Business Needs.")
    Functional_Design_frequency: str = Field(..., description="Functional Design - Frequency.")
    Functional_Design_data_volume: str = Field(..., description="Functional Design - Data Volume.")
    Functional_Design_security_requirements: Optional[SecurityRequirements] = Field(None, description="Functional Design - Security Requirements")
    Functional_Design_comments: str = Field(..., description="Functional Design - Comments.")
    Functional_Design_data_sensitivity: str = Field(..., description="Functional Design - Data Sensitivity.")
    Functional_Design_unit_testing: UnitTesting = Field(..., description="Functional Design - Unit Testing Section")
    Functional_Design_additional_comments: str = Field(..., description="Functional Design - Additional Comments.")
    Functional_Design_rework_log: str = Field(..., description="Functional Design - Rework Log.")


class TD(BaseModel):
    Technical_Design_design_points: str = Field(
        description="Technical Design - Design Points: calculations, formulas, conditions, performance."
    )
    Technical_Design_program_logic: str = Field(
        description="Technical Design - Program Logic: Pseudo code/Table or Diagram with definition of Project Flow."
    )
    Technical_Design_program_logic_steps: List[dict] = Field(
        description="Technical Design - Program Logic Steps:",
        default=[{"Step No.": None, "System object accessed / Processing done": None, "Parameters passed": None, "Extracted Fields": None, "Remarks": None}]
    )
    Technical_Design_special_configuration_settings_assumptions: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions."
    )
    Technical_Design_additional_comments: str = Field(description="Technical Design - Additional Comments.")
    Technical_Design_rework_log: str = Field(description="Technical Design - Rework Log.")
