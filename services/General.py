from pydantic import BaseModel, Field
from services.shared_models import VOC, ROC


class FD(BaseModel):
    project_name: str = Field(description="Extracted project name")
    RICEF_id: str = Field(description="Generated or extracted RICEF ID")
    client_name: str = Field(description="Extracted client name")
    Functional_Design_Process: str = Field(
        description="Functional Design - Process: Generated or extracted process flow."
    )
    Functional_Design_Interface_Direction: str = Field(
        description="Functional Design - Interface Direction: Direction of data flow (to/from or bi-directional with SAP)."
    )
    Functional_Design_Error_Handling: str = Field(
        description="Functional Design - Error Handling: Error-handling owner definition and business needs."
    )
    Functional_Design_Frequency: str = Field(
        description="Functional Design - Frequency: Frequency at which the report will be run."
    )
    Functional_Design_Data_Volume: str = Field(
        description="Functional Design - Data Volume: Estimated data volume for the report."
    )
    Functional_Design_Security_Requirements: str = Field(
        description="Functional Design - Security Requirements: Authorization checks or special processing."
    )
    Functional_Design_Data_Sensitivity: str = Field(
        description="Functional Design - Data Sensitivity: Sensitivity of data, including level of restrictions."
    )
    Functional_Design_Unit_Testing: str = Field(
        description="Functional Design - Unit Testing: Test scenarios, instructions, test data, and expected results."
    )
    Functional_Design_Additional_Comments: str = Field(
        description="Functional Design - Additional Comments."
    )
    Functional_Design_Rework_Log: str = Field(
        description="Functional Design - Rework Log."
    )
    Functional_Design_reference_transactions_tables_programs: str = Field(
        description="List all known SAP R/3 transactions, tables, programs, and reports relevant to this functional design."
    )
    Functional_Design_input_selection_criteria: str = Field(
        description="Detailed description of the input and selection criteria presented on the selection screen."
    )
    Functional_Design_solution_format: str = Field(
        description="Output format: SapScript, Smartform, or Adobe Print Form."
    )
    Functional_Design_output_format_details: str = Field(
        description="How the output should be presented: page designation, window, font, data origin, field labels."
    )
    Functional_Design_barcode_requirements: str = Field(
        description="Details for barcode generation: serial number, field name, barcode type/code."
    )
    Functional_Design_paper_requirements: str = Field(
        description="Paper/stationery requirements for printed outputs."
    )
    Functional_Design_logo_requirements: str = Field(
        description="Requirements for incorporating the company logo: file formats, resolution, size, placement."
    )
    Functional_Design_software_requirements: str = Field(
        description="Additional software requirements or dependencies necessary for this project."
    )
    Functional_Design_printer_requirements: str = Field(
        description="Detailed specifications for the printer(s) to be used."
    )
    Functional_Design_output_type_application: str = Field(
        description="Overall output type and context of use."
    )


class TD(BaseModel):
    project_name: str = Field(description="Extracted project name")
    RICEF_id: str = Field(description="Generated or extracted RICEF ID")
    client_name: str = Field(description="Extracted client name")
    Technical_Design_Design_Points: str = Field(
        description="Technical Design - Design Points: calculations, formulas, and performance recommendations."
    )
    Technical_Design_Special_Configuration_Settings: str = Field(
        description="Technical Design - Special Configuration Settings: temporary prerequisites."
    )
    Technical_Design_Outbound_Definition: str = Field(
        description="Technical Design - Outbound Definition: Outbound file(s) structure and format details."
    )
    Technical_Design_Target_Environment: str = Field(
        description="Technical Design - Target Environment: where data will be sent and any requirements."
    )
    Technical_Design_Starting_Transaction: str = Field(
        description="Technical Design - Starting Transaction: Starting transaction or application name."
    )
    Technical_Design_Triggering_Events: str = Field(
        description="Technical Design - Triggering Events: SAP business process event that triggers the report."
    )
    Technical_Design_Data_Transformation_Process: str = Field(
        description="Technical Design - Data Transformation Process: Data transformation within SAP or middleware."
    )
    Technical_Design_Data_Transfer_Process: str = Field(
        description="Technical Design - Data Transfer Process: Description of data transfer process to SAP."
    )
    Technical_Design_Data_Format: str = Field(
        description="Technical Design - Data Format: Format of data (XML, EDI, Flat File, etc.)."
    )
    Technical_Design_Error_Handling: str = Field(
        description="Technical Design - Error Handling: Technical error handling components and owner definition."
    )
    Technical_Design_Additional_Process_Requirements: str = Field(
        description="Technical Design - Additional Process Requirements."
    )
    Technical_Design_Inbound_Definition: str = Field(
        description="Technical Design - Inbound Definition: Inbound file structure and format."
    )
    Technical_Design_Source_Environment: str = Field(
        description="Technical Design - Source Environment: Origin of data from an external system."
    )
    Technical_Design_Receiving_Transaction: str = Field(
        description="Technical Design - Receiving Transaction: Receiving transaction/application, new or existing."
    )
    Technical_Design_Rework_Log: str = Field(
        description="Technical Design - Rework Log."
    )
