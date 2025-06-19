from pydantic import BaseModel, Field

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

    Functional_Design_reference_sap_fiori_assets: str = Field(
        description="Functional Design - Reference SAP/Fiori Assets: Include all known SAP transactions, tables, programs, and reports used or containing similar data. Screenshots recommended. Model should use this information based on functional design context."
    )
    Functional_Design_new_or_extended_tables: str = Field(
        description="Functional Design - New or Extended Tables: List of new SAP tables required or SAP tables to be extended. This is part of the functional design specification."
    )
    Functional_Design_user_exit_badi_info: str = Field(
        description="Functional Design - User Exit/BADI Info: Provide User Exit/BADI Name, Enhancement Spot, and Switch Framework used. Model should interpret this within the functional design scope."
    )
    Functional_Design_process_description: str = Field(
        description="Functional Design - Process Description: Describe when and how the enhancement will be triggered, and what the enhancement code should do. A flowchart is recommended. Response should align with functional design principles."
    )
    Functional_Design_special_functionality: str = Field(
        description="Functional Design - Special Functionality: List any additional functionality required, including links to other transactions. This forms part of the enhancement’s functional requirements."
    )
    Functional_Design_error_handling: str = Field(
        description="Functional Design - Error Handling: Provide owner definition and describe business needs for error handling. This information should be interpreted from a functional design perspective."
    )
    Functional_Design_frequency: str = Field(
        description="Functional Design - Frequency: Specify how often the enhancement will be executed. Model should consider this frequency in the context of functional operations."
    )
    Functional_Design_security_requirements: str = Field(
        description="Functional Design - Security Requirements: Describe any security requirements including authorization checks or special processing. Examples include: 'No Specific Restrictions', 'Restriction Based on Criteria', etc. Relevant to functional design."
    )
    Functional_Design_data_sensitivity: str = Field(
        description="Functional Design - Data Sensitivity: Explain the data sensitivity (e.g., based on plant or level of restriction). This is important in functional requirement planning."
    )
    Functional_Design_unit_testing: str = Field(
        description="Functional Design - Unit Testing: Provide test scenarios, test data, expected results (positive and negative), and testing instructions for the developer. Based on functional validation requirements."
    )
    Functional_Design_additional_comments: str = Field(
        description="Functional Design - Additional Comments: Include any other relevant information needed for development from a functional perspective."
    )
    Functional_Design_rework_log: str = Field(
        description="Functional Design - Rework Log: Maintain previous versions or iterations of the functional design."
    )



class TD(BaseModel):


    Technical_Design_Design_Points: str = Field(
        description="Technical Design - Design Points: Describe anything that makes the definition of the technical design clearer, including calculations, formulas, specific conditions, and performance recommendations or concerns. Model should respond based on this technical design context."
    )
    Technical_Design_Error_Handling: str = Field(
        description="Technical Design - Error Handling: Describe technical error handling components and owner definitions. Model should use this information from a technical design perspective."
    )
    Technical_Design_Error_Messages: str = Field(
        description="Technical Design - Error Messages: Define issues that trigger messages, their message text, and corresponding Msg. ID. This supports technical design-related error documentation."
    )
    Technical_Design_Special_Configuration_Settings: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions: List any special or temporary configuration prerequisites required by the technical design."
    )
    Technical_Design_Additional_Comments: str = Field(
        description="Technical Design - Additional Comments: Include any extra technical details, clarifications, or considerations needed for implementation, especially performance-related ones."
    )
    Technical_Design_Rework_Log: str = Field(
        description="Technical Design - Rework Log: Maintain the history of previous versions or changes made to the technical design."
    )
    Technical_Design_Clean_Core_Implications: str = Field(
        description="Technical Design - Clean Core Implications: Explain the implications of this technical design in relation to the Clean Core Extension methodology, including possible Tier-2 and Tier-3 technologies. Model should provide Clean Core insights based on this design."
    )