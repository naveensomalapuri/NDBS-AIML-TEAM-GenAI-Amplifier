from pydantic import BaseModel, Field
from services.shared_models import VOC, ROC


class FD(BaseModel):
    Functional_Design_reference_sap_fiori_assets: str = Field(
        description="Functional Design - Reference SAP/Fiori Assets: Include all known SAP transactions, tables, programs, and reports used or containing similar data."
    )
    Functional_Design_new_or_extended_tables: str = Field(
        description="Functional Design - New or Extended Tables: List of new SAP tables required or SAP tables to be extended."
    )
    Functional_Design_user_exit_badi_info: str = Field(
        description="Functional Design - User Exit/BADI Info: Provide User Exit/BADI Name, Enhancement Spot, and Switch Framework used."
    )
    Functional_Design_process_description: str = Field(
        description="Functional Design - Process Description: Describe when and how the enhancement will be triggered, and what the enhancement code should do."
    )
    Functional_Design_special_functionality: str = Field(
        description="Functional Design - Special Functionality: List any additional functionality required, including links to other transactions."
    )
    Functional_Design_error_handling: str = Field(
        description="Functional Design - Error Handling: Provide owner definition and describe business needs for error handling."
    )
    Functional_Design_frequency: str = Field(
        description="Functional Design - Frequency: Specify how often the enhancement will be executed."
    )
    Functional_Design_security_requirements: str = Field(
        description="Functional Design - Security Requirements: Describe any security requirements including authorization checks or special processing."
    )
    Functional_Design_data_sensitivity: str = Field(
        description="Functional Design - Data Sensitivity: Explain the data sensitivity (e.g., based on plant or level of restriction)."
    )
    Functional_Design_unit_testing: str = Field(
        description="Functional Design - Unit Testing: Provide test scenarios, test data, expected results (positive and negative), and testing instructions."
    )
    Functional_Design_additional_comments: str = Field(
        description="Functional Design - Additional Comments: Include any other relevant information needed for development."
    )
    Functional_Design_rework_log: str = Field(
        description="Functional Design - Rework Log: Maintain previous versions or iterations of the functional design."
    )


class TD(BaseModel):
    Technical_Design_Design_Points: str = Field(
        description="Technical Design - Design Points: Describe anything that makes the technical design clearer, including calculations, formulas, conditions, and performance recommendations."
    )
    Technical_Design_Error_Handling: str = Field(
        description="Technical Design - Error Handling: Describe technical error handling components and owner definitions."
    )
    Technical_Design_Error_Messages: str = Field(
        description="Technical Design - Error Messages: Define issues that trigger messages, their message text, and corresponding Msg. ID."
    )
    Technical_Design_Special_Configuration_Settings: str = Field(
        description="Technical Design - Special Configuration Settings/Assumptions: List any special or temporary configuration prerequisites."
    )
    Technical_Design_Additional_Comments: str = Field(
        description="Technical Design - Additional Comments: Include any extra technical details or considerations needed for implementation."
    )
    Technical_Design_Rework_Log: str = Field(
        description="Technical Design - Rework Log: Maintain the history of previous versions or changes made to the technical design."
    )
    Technical_Design_Clean_Core_Implications: str = Field(
        description="Technical Design - Clean Core Implications: Explain implications in relation to Clean Core Extension methodology, including Tier-2 and Tier-3 technologies."
    )
