from pydantic import BaseModel, Field
from typing import Optional, List
from services.shared_models import VOC, ROC


class FD(BaseModel):
    Functional_Design_reference_sap_fiori_apps_transactions_tables_programs: str = Field(
        description="Functional Design - Reference SAP Fiori Apps/Transactions/Tables/Programs."
    )
    Functional_Design_process: str = Field(
        description="Functional Design - Process: Describe the process in form of a flowchart."
    )
    Functional_Design_interface_direction: str = Field(
        description="Functional Design - Interface Direction: To SAP, from SAP or Bi-directional."
    )
    Functional_Design_error_handling: str = Field(
        description="Functional Design - Error Handling: Owner Definition & Business Needs."
    )
    Functional_Design_frequency: str = Field(
        description="Functional Design - Frequency: How often will the report be run?"
    )
    Functional_Design_data_volume: str = Field(
        description="Functional Design - Data Volume."
    )
    Functional_Design_security_requirements_yes_no: Optional[str] = Field(
        default=None, description="Functional Design - Security Requirements: Yes/No"
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
    Functional_Design_comments: str = Field(description="Functional Design - Comments.")
    Functional_Design_data_sensitivity: str = Field(
        description="Functional Design - Data Sensitivity: Plant/Level of restrictions."
    )
    Functional_Design_unit_testing: str = Field(
        description="Functional Design - Unit Testing: test scenarios, instructions, test data, and expected results."
    )
    Functional_Design_unit_test_scenarios: List[dict] = Field(
        description="Functional Design - Unit Test Scenarios.",
        default=[{"Test Condition / Test Scenario": None, "Steps Involved": None, "Input Values (Test Data)": None, "Expected Results": None}]
    )
    Functional_Design_additional_comments: str = Field(description="Functional Design - Additional Comments.")
    Functional_Design_rework_log: str = Field(description="Functional Design - Rework Log.")


class TD(BaseModel):
    Technical_Design_design_points: str = Field(
        description="Technical Design - Design Points: calculations, formulas, conditions, performance."
    )
    Technical_Design_special_configuration_settings_assumptions: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions."
    )
    Technical_Design_outbound: str = Field(
        description="Technical Design - Outbound: outbound file(s) data structure & file format."
    )
    Technical_Design_target_environment: str = Field(
        description="Technical Design - Target Environment: where data is going to be sent."
    )
    Technical_Design_starting_transaction_application: str = Field(
        description="Technical Design - Starting Transaction/Application."
    )
    Technical_Design_triggering_events_outbound: str = Field(
        description="Technical Design - Triggering Event(s): SAP business process trigger."
    )
    Technical_Design_data_transformation_process_outbound: str = Field(
        description="Technical Design - Data Transformation Process: With SAP or within middleware."
    )
    Technical_Design_data_transfer_process_outbound: str = Field(
        description="Technical Design - Data Transfer Process."
    )
    Technical_Design_data_format_outbound: str = Field(
        description="Technical Design - Data Format: XML, EDI, Flat File, etc."
    )
    Technical_Design_error_handling_outbound: str = Field(
        description="Technical Design - Error Handling: Owner Definition and Technical Components."
    )
    Technical_Design_additional_process_requirements_outbound: str = Field(
        description="Technical Design - Additional Process Requirements."
    )
    Technical_Design_inbound: str = Field(
        description="Technical Design - Inbound: inbound file(s) data structure & file format."
    )
    Technical_Design_source_environment: str = Field(
        description="Technical Design - Source Environment: origin of data from external system."
    )
    Technical_Design_receiving_transaction_application: str = Field(
        description="Technical Design - Receiving Transaction/Application: New/Existing."
    )
    Technical_Design_triggering_events_inbound: str = Field(
        description="Technical Design - Triggering Event(s): Events on SAP process that trigger inbound data."
    )
    Technical_Design_data_transformation_process_inbound: str = Field(
        description="Technical Design - Data Transformation Process: With SAP or within middleware."
    )
    Technical_Design_data_transfer_process_inbound: str = Field(
        description="Technical Design - Data Transfer Process: how incoming data is applied to SAP."
    )
    Technical_Design_data_format_inbound: str = Field(
        description="Technical Design - Data Format: XML, EDI, Flat File, etc."
    )
    Technical_Design_error_handling_inbound: str = Field(
        description="Technical Design - Error Handling: Owner Definition and Technical Components."
    )
    Technical_Design_additional_process_requirements_inbound: str = Field(
        description="Technical Design - Additional Process Requirements."
    )
    Technical_Design_additional_comments: str = Field(description="Technical Design - Additional Comments.")
    Technical_Design_clean_core_implications: str = Field(
        description="Technical Design - Clean Core Implications: Tier-2 and Tier-3 technologies."
    )
