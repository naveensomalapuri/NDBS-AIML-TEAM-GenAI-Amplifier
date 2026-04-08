from pydantic import BaseModel, Field
from typing import Optional, List
from services.shared_models import VOC, ROC


class FD(BaseModel):
    Functional_Design_functional_description: str = Field(
        description="Functional Design - Functional Description: Short summary of the requirement."
    )
    Functional_Design_business_benefits_need: str = Field(
        description="Functional Design - Business Benefits/Need: why the workflow is needed, impact if not implemented."
    )
    Functional_Design_process: str = Field(
        description="Functional Design - Process: describe the process in form of a flowchart."
    )
    Functional_Design_assumptions: str = Field(
        description="Functional Design - Assumptions: Describe any assumption made."
    )
    Functional_Design_start_conditions: str = Field(
        description="Functional Design - Start Conditions: What condition/business event triggers the workflow?"
    )
    Functional_Design_process_flow: str = Field(
        description="Functional Design - Process Flow: Functional Flow Diagram."
    )
    Functional_Design_organizational_structure: str = Field(
        description="Functional Design - Organizational Structure: Organization structure to be used."
    )
    Functional_Design_applications_objects_transactions_affected: str = Field(
        description="Functional Design - Applications, Objects or Transactions Affected: Volume, Frequency Details."
    )
    Functional_Design_new_tables_required_sap_tables_extended: str = Field(
        description="Functional Design - New Tables required or SAP tables extended."
    )
    Functional_Design_input: str = Field(
        description="Functional Design - Input: Functional Description of the Input."
    )
    Functional_Design_input_fields: List[dict] = Field(
        description="Functional Design - Input Fields: Transaction used to trigger the workflow.",
        default=[{"Transaction Name": None, "Transaction Description": None}]
    )
    Functional_Design_output: str = Field(
        description="Functional Design - Output: Functional Description of the output."
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
    Functional_Design_unit_testing: List[dict] = Field(
        description="Functional Design - Unit Testing: test scenarios, instructions, test data, and expected results.",
        default=[{"Test Condition / Test Scenario": None, "Steps Involved": None, "Input Values (Test Data)": None, "Expected Results": None}]
    )
    Functional_Design_additional_comments: str = Field(description="Functional Design - Additional Comments.")
    Functional_Design_rework_log: str = Field(description="Functional Design - Rework Log.")


class TD(BaseModel):
    Technical_Design_development_objectives_summary: str = Field(
        description="Technical Design - 1. Development Objectives: Summary."
    )
    Technical_Design_workflow_id: Optional[str] = Field(default=None, description="Technical Design - Workflow ID.")
    Technical_Design_workflow_name: Optional[str] = Field(default=None, description="Technical Design - Workflow Name.")
    Technical_Design_development_class_package: Optional[str] = Field(default=None, description="Technical Design - Development Class/Package.")
    Technical_Design_workflow_location: Optional[str] = Field(default=None, description="Technical Design - Workflow Location.")
    Technical_Design_development_type: Optional[str] = Field(default=None, description="Technical Design - Development Type: Workflow, Other.")
    Technical_Design_frequency: Optional[str] = Field(default=None, description="Technical Design - Frequency.")
    Technical_Design_trigger: Optional[str] = Field(default=None, description="Technical Design - Trigger: Event, Batch, Method.")
    Technical_Design_volume: Optional[str] = Field(default=None, description="Technical Design - Volume.")
    Technical_Design_requirements_summary: str = Field(description="Technical Design - Requirements Summary.")
    Technical_Design_assumptions_dev_objectives: str = Field(description="Technical Design - Assumptions made during development.")
    Technical_Design_applications_objects_transactions_affected_dev_objectives: str = Field(
        description="Technical Design - Applications, objects or Transactions Affected."
    )
    Technical_Design_special_configuration_settings_assumptions_dev_objectives: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions."
    )
    Technical_Design_error_handling_dev_objectives: List[dict] = Field(
        description="Technical Design - Error Handling: all Error messages to be used in the development Object.",
        default=[{"Error Number": None, "Error Condition": None, "Error Message": None, "Corrective Action": None}]
    )
    Technical_Design_technical_flow_diagram: str = Field(
        description="Technical Design - 2. Detailed Technical Specifications: Technical Flow Diagram."
    )
    Technical_Design_technical_flow_description: str = Field(
        description="Technical Design - Technical Flow Description: number of steps, business object, subtypes, step type, methods."
    )
    Technical_Design_technical_flow_steps: List[dict] = Field(
        description="Technical Design - Technical Flow Steps.",
        default=[{"Step n": None, "Step type": None, "Business object": None, "Attribute": None, "Description": None}]
    )
    Technical_Design_object_details: str = Field(
        description="Technical Design - Object Details: Business object, subtypes, new attributes methods, events."
    )
    Technical_Design_task_details: List[dict] = Field(
        description="Technical Design - Task Details.",
        default=[{"Type": None, "Link Object Method to Task": None, "Container Elements": None, "Binding": None, "Exits": None, "Deadline": None, "Terminating Events": None}]
    )
    Technical_Design_security_and_authorization: str = Field(
        description="Technical Design - Security and Authorization: all Security/Authorization checks."
    )
    Technical_Design_processing_and_operational_considerations: str = Field(
        description="Technical Design - Processing and Operational Considerations."
    )
    Technical_Design_dependencies: Optional[str] = Field(default=None, description="Technical Design - Dependencies.")
    Technical_Design_restart_recovery_procedures: Optional[str] = Field(default=None, description="Technical Design - Restart/Recovery Procedures.")
    Technical_Design_data_maintenance_requirements: Optional[str] = Field(default=None, description="Technical Design - Data Maintenance Requirements.")
    Technical_Design_external_programs: str = Field(description="Technical Design - External Programs.")
    Technical_Design_rework_log: str = Field(description="Technical Design - Rework Log.")
    Technical_Design_clean_core_implications: str = Field(description="Technical Design - Clean Core Implications.")
