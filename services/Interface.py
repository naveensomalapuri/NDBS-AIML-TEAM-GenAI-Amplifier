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
    Functional_Design_reference_sap_fiori_apps_transactions_tables_programs: str = Field(
        description="Functional Design - Reference SAP Fiori Apps/Transactions/Tables/Programs: (Note all known transactions, tables and programs that are used, or reports containing similar data, screenshots are recommended)"
    )
    Functional_Design_process: str = Field(
        description="Functional Design - Process: (Describe the process, what the program should do, if possible, in form of a flowchart)"
    )
    Functional_Design_interface_direction: str = Field(
        description="Functional Design - Interface Direction: (To SAP, from SAP or Bi-directional)"
    )
    Functional_Design_error_handling: str = Field(
        description="Functional Design - Error Handling: (Owner Definition & Business Needs)"
    )
    Functional_Design_frequency: str = Field(
        description="Functional Design - Frequency: (How often will the report be run?)"
    )
    Functional_Design_data_volume: str = Field(
        description="Functional Design - Data Volume:"
    )
    Functional_Design_security_requirements_yes_no: Optional[str] = Field(
        description="Functional Design - Security Requirements: Yes/No"
    )
    Functional_Design_security_requirements_no_specific_restrictions: Optional[str] = Field(
        description="Functional Design - Security Requirements: No Specific Restrictions"
    )
    Functional_Design_security_requirements_restriction_based_on_certain_criteria: Optional[str] = Field(
        description="Functional Design - Security Requirements: Restriction Based on Certain Criteria. - (ex: Restricted by Sales area?)"
    )
    Functional_Design_security_requirements_other: Optional[str] = Field(
        description="Functional Design - Security Requirements: Other"
    )
    Functional_Design_comments: str = Field(
        description="Functional Design - Comments:"
    )
    Functional_Design_data_sensitivity: str = Field(
        description="Functional Design - Data Sensitivity: (Plant/Level of restrictions, please explain)"
    )
    Functional_Design_unit_testing: str = Field(
        description="Functional Design - Unit Testing: (Information the developer can use to unit test the application. This needs to include test scenarios: positive and negative test scenarios, instructions, test data, and expected results)"
    )
    Functional_Design_unit_test_scenarios: List[dict] = Field(
        description="Functional Design - Unit Test Scenarios: Details for unit testing.",
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
        description="Technical Design - Design Points: (Describe anything that will make the definition of the design clear, including calculations and formulas, particular conditions where the program should behave differently, recommendations, etc. If applicable, include recommendations or concerns regarding performance.)"
    )
    Technical_Design_special_configuration_settings_assumptions: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions: (Describe any special or temporary pre-requisite configuration requirements)"
    )
    Technical_Design_outbound: str = Field(
        description="Technical Design - Outbound: (define the outbound file(s) with corresponding data structure & file format)"
    )
    Technical_Design_target_environment: str = Field(
        description="Technical Design - Target Environment: (Describe target environment where data is going to be send, identify any requirements to that environment [IEFTP/PI])"
    )
    Technical_Design_starting_transaction_application: str = Field(
        description="Technical Design - Starting Transaction/Application:"
    )
    Technical_Design_triggering_events_outbound: str = Field(
        description="Technical Design - Triggering Event(s): (From SAP business process – ex: IE Transfer Order)"
    )
    Technical_Design_data_transformation_process_outbound: str = Field(
        description="Technical Design - Data Transformation Process: (With SAP or within middleware)"
    )
    Technical_Design_data_transfer_process_outbound: str = Field(
        description="Technical Design - Data Transfer Process:"
    )
    Technical_Design_data_format_outbound: str = Field(
        description="Technical Design - Data Format: (XML, EDI, Flat File, etc.)"
    )
    Technical_Design_error_handling_outbound: str = Field(
        description="Technical Design - Error Handling: (Owner Definition and Technical Components)"
    )
    Technical_Design_additional_process_requirements_outbound: str = Field(
        description="Technical Design - Additional Process Requirements:"
    )
    Technical_Design_inbound: str = Field(
        description="Technical Design - Inbound: (Define the Inbound file(s) with corresponding data structure & file format)"
    )
    Technical_Design_source_environment: str = Field(
        description="Technical Design - Source Environment: (Define origin of data, where external system is coming from)"
    )
    Technical_Design_receiving_transaction_application: str = Field(
        description="Technical Design - Receiving Transaction/Application:  New/Existing:"
    )
    Technical_Design_triggering_events_inbound: str = Field(
        description="Technical Design - Triggering Event(s): (Define Existing Events on the SAP process that triggers that data to be brought or apply to SAP)"
    )
    Technical_Design_data_transformation_process_inbound: str = Field(
        description="Technical Design - Data Transformation Process: (With SAP or within middleware)"
    )
    Technical_Design_data_transfer_process_inbound: str = Field(
        description="Technical Design - Data Transfer Process: (Describe the process of the incoming data & how is it applied to SAP)"
    )
    Technical_Design_data_format_inbound: str = Field(
        description="Technical Design - Data Format: (XML, EDI, Flat File, etc)"
    )
    Technical_Design_error_handling_inbound: str = Field(
        description="Technical Design - Error Handling: (Owner Definition and Technical Components)"
    )
    Technical_Design_additional_process_requirements_inbound: str = Field(
        description="Technical Design - Additional Process Requirements:"
    )
    Technical_Design_additional_comments: str = Field(
        description="Technical Design - Additional Comments: (Add any additional information necessary to assist in development as needed)"
    )
    Technical_Design_clean_core_implications: str = Field(
        description="Technical Design - Clean Core Implications: (Are there any implication in relation to Clean Core Extension methodology. Explain the potential Tier-2 and Tier-3 technologies that might be used to achieve the solution. Add these in the clean core governance excel sheet.)"
    )