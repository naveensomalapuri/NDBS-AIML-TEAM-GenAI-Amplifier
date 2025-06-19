
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
    
    # Functional Description Section
    functional_description: str = Field(
        description="Short Description of the required interface. What functionality is needed?"
    )
    business_benefit_need: str = Field(
        description="Short Description of why the interface is needed, and the impact if the interface is not implemented."
    )
    
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
    Functional_Design_functional_description: str = Field(
        description="Functional Design - Functional Description: (Short summary of the requirement)"
    )
    Functional_Design_business_benefits_need: str = Field(
        description="Functional Design - Business Benefits/Need: (Short Description of why the workflow is needed, impact if workflow is not implemented)"
    )
    Functional_Design_process: str = Field(
        description="Functional Design - Process: (Describe the process, what the program should do, if possible in form of a flowchart)"
    )
    Functional_Design_assumptions: str = Field(
        description="Functional Design - Assumptions: (Describe any assumption made)"
    )
    Functional_Design_start_conditions: str = Field(
        description="Functional Design - Start Conditions: (What condition/business event triggers the workflow?)"
    )
    Functional_Design_process_flow: str = Field(
        description="Functional Design - Process Flow: (Functional Flow Diagram)"
    )
    Functional_Design_organizational_structure: str = Field(
        description="Functional Design - Organizational Structure: (Organization structure to be used)"
    )
    Functional_Design_applications_objects_transactions_affected: str = Field(
        description="Functional Design - Applications, Objects or Transactions Affected: (Transactions that are affected in the workflow process, Volume, Frequency Details)"
    )
    Functional_Design_new_tables_required_sap_tables_extended: str = Field(
        description="Functional Design - New Tables required or SAP tables extended:"
    )
    Functional_Design_input: str = Field(
        description="Functional Design - Input: (Functional Description of the Input)"
    )
    Functional_Design_input_fields: List[dict] = Field(
        description="Functional Design - Input Fields: (What Transaction should the user use to trigger the workflow, if applicable?)",
        default=[{"Transaction Name": None, "Transaction Description": None}]
    )
    Functional_Design_output: str = Field(
        description="Functional Design - Output: (Functional Description of the output)"
    )
    Functional_Design_security_requirements_no_specific_restrictions: Optional[str] = Field(
        description="Functional Design - Security Requirements: No Specific Restrictions"
    )
    Functional_Design_security_requirements_restriction_based_on_certain_criteria: Optional[str] = Field(
        description="Functional Design - Security Requirements: Restriction Based on Certain Criteria (ex: Restricted by Sales area?)"
    )
    Functional_Design_security_requirements_other: Optional[str] = Field(
        description="Functional Design - Security Requirements: Other"
    )
    Functional_Design_unit_testing: List[dict] = Field(
        description="Functional Design - Unit Testing: (Information the developer can use to unit test the application, including test scenarios, instructions, test data, and expected results)",
        default=[{"Test Condition / Test Scenario": None, "Steps Involved": None, "Input Values (Test Data)": None, "Expected Results": None}]
    )
    Functional_Design_additional_comments: str = Field(
        description="Functional Design - Additional Comments: (Add any additional information necessary to assist in development as needed)"
    )
    Functional_Design_rework_log: str = Field(
        description="Functional Design - Rework Log: (The version shown above is the latest, this area may contain previous version(s) of the same section)"
    )




class TD(BaseModel):
    Technical_Design_development_objectives_summary: str = Field(
        description="Technical Design - 1. Development Objectives: Summary"
    )
    Technical_Design_workflow_id: Optional[str] = Field(
        description="Technical Design - Workflow ID:"
    )
    Technical_Design_workflow_name: Optional[str] = Field(
        description="Technical Design - Workflow Name:"
    )
    Technical_Design_development_class_package: Optional[str] = Field(
        description="Technical Design - Development Class/Package:"
    )
    Technical_Design_workflow_location: Optional[str] = Field(
        description="Technical Design - Workflow Location:"
    )
    Technical_Design_development_type: Optional[str] = Field(
        description="Technical Design - Development Type: (Workflow, Other)"
    )
    Technical_Design_frequency: Optional[str] = Field(
        description="Technical Design - Frequency:"
    )
    Technical_Design_trigger: Optional[str] = Field(
        description="Technical Design - Trigger (Event, Batch, Method):"
    )
    Technical_Design_volume: Optional[str] = Field(
        description="Technical Design - Volume:"
    )
    Technical_Design_requirements_summary: str = Field(
        description="Technical Design - Requirements Summary:"
    )
    Technical_Design_assumptions_dev_objectives: str = Field(
        description="Technical Design - Assumptions: (The assumptions made during development)"
    )
    Technical_Design_applications_objects_transactions_affected_dev_objectives: str = Field(
        description="Technical Design - Applications, objects or Transactions Affected: (Transaction used, Business objects used)"
    )
    Technical_Design_special_configuration_settings_assumptions_dev_objectives: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions: (Describe any special or temporary pre-requisite configuration requirements)"
    )
    Technical_Design_error_handling_dev_objectives: List[dict] = Field(
        description="Technical Design - Error Handling (Please include all the Error messages to be used in the development Object)",
        default=[{"Error Number": None, "Error Condition": None, "Error Message": None, "Corrective Action": None}]
    )
    Technical_Design_technical_flow_diagram: str = Field(
        description="Technical Design - 2. Detailed Technical Specifications: Technical Flow Diagram:"
    )
    Technical_Design_technical_flow_description: str = Field(
        description="Technical Design - 2. Detailed Technical Specifications: Technical Flow Description:[This will include the technical flow description of the workflow process with: the number of steps created, business object to be used, any new subtypes created, new attributes added, step type, business object methods used. Each step will have the following information]"
    )
    Technical_Design_technical_flow_steps: List[dict] = Field(
        description="Technical Design - Technical Flow Steps: Details for each step in the technical flow.",
        default=[{"Step n": None, "Step type": None, "Business object": None, "Attribute": None, "Description": None}]
    )
    Technical_Design_object_details: str = Field(
        description="Technical Design - 2. Detailed Technical Specifications: Object Details: [Business object used, any subtypes created, any new attributes methods, events created]"
    )
    Technical_Design_task_details: List[dict] = Field(
        description="Technical Design - Task Details: Information for each task in the workflow.",
        default=[{"Type": None, "Link Object Method to Task": None, "Container Elements": None, "Binding": None, "Exits": None, "Deadline": None, "Terminating Events": None}]
    )
    Technical_Design_security_and_authorization: str = Field(
        description="Technical Design - Security and Authorization: [List all Security / Authorization checks that should be included for the Workflow]"
    )
    Technical_Design_processing_and_operational_considerations: str = Field(
        description="Technical Design - Processing and Operational Considerations:"
    )
    Technical_Design_dependencies: Optional[str] = Field(
        description="Technical Design - Dependencies: [Any dependencies for the workflow to run efficiently]"
    )
    Technical_Design_restart_recovery_procedures: Optional[str] = Field(
        description="Technical Design - Restart /Recovery Procedures: [in case of workflow error]"
    )
    Technical_Design_data_maintenance_requirements: Optional[str] = Field(
        description="Technical Design - Data Maintenance Requirements: [any Z tables created and data maintenance required for the workflow to run efficiently]"
    )
    Technical_Design_external_programs: str = Field(
        description="Technical Design - External Programs: (used with the workflow to complete the Business Process)"
    )
    Technical_Design_rework_log: str = Field(
        description="Technical Design - Rework Log: (The version shown above is the latest, this area may contain previous version(s) of the same section)"
    )
    Technical_Design_clean_core_implications: str = Field(
        description="Technical Design - Clean Core Implications: (Are there any implication in relation to Clean Core Extension methodology. Explain the potential Tier-2 and Tier-3 technologies that might be used to achieve the solution. Add these in the clean core governance excel sheet.)"
    )