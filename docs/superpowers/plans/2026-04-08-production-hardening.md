# Production Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix all critical security, reliability, code quality, and Azure-specific issues (items 1, 3–23) excluding authentication/authorization (item 2).

**Architecture:** Harden the existing FastAPI app in-place — no structural rewrites. Introduce a shared `services/shared_models.py` for deduplicated Pydantic schemas, a `services/llm_client.py` for singleton LLM/graph initialization, replace `pymongo` with `motor` for async MongoDB, replace `print()` with structured `logging`, add input allowlisting, path safety, health endpoint, CORS, retry logic, and OpenTelemetry instrumentation.

**Tech Stack:** FastAPI, motor (async MongoDB), LangGraph, Azure OpenAI, tenacity, azure-monitor-opentelemetry, Python logging, pathlib

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `services/shared_models.py` | **Create** | Single source of truth for shared `VOC` and `ROC` Pydantic classes |
| `services/llm_client.py` | **Create** | Module-level singleton: AzureChatOpenAI, TavilySearch, compiled graphs |
| `services/Enhancements.py` | **Modify** | Remove dead code, import VOC/ROC from shared_models |
| `services/Forms.py` | **Modify** | Remove dead code, import VOC/ROC from shared_models |
| `services/General.py` | **Modify** | Remove dead code, import VOC/ROC from shared_models |
| `services/Interface.py` | **Modify** | Remove dead code, import VOC/ROC from shared_models |
| `services/Reports.py` | **Modify** | Remove dead code, import VOC/ROC from shared_models |
| `services/Workflow.py` | **Modify** | Remove dead code, import VOC/ROC from shared_models |
| `services/jsondatastructure.py` | **Modify** | Remove dead code, import VOC/ROC from shared_models |
| `services/model.py` | **Modify** | Use llm_client singleton, remove dead commented code, add timeout + tenacity retry, add allowlist for wricefType |
| `services/resume_service.py` | **Modify** | Remove duplicate imports/RESUME_DIR, convert file I/O to aiofiles |
| `configuration.py` | **Modify** | Replace pymongo with motor, add connection pool config + serverSelectionTimeoutMS |
| `routes/resume_routes.py` | **Modify** | Add wricef_type allowlist, sanitize ricefw_number, fix `$push` cap, use `model_dump()` |
| `main.py` | **Modify** | Add CORSMiddleware, /health endpoint, absolute paths via pathlib, OpenTelemetry setup |
| `requirements.txt` | **Modify** | Add motor, aiofiles, azure-monitor-opentelemetry; remove pymongo |
| `.env.example` | **Create** | Document required env vars (no secrets) |
| `.gitignore` | **Verify** | Confirm `.env` is listed (already is — just verify) |

---

## Task 1: Verify .env is gitignored and create .env.example

**Files:**
- Verify: `.gitignore`
- Create: `.env.example`

- [ ] **Step 1: Confirm .env is in .gitignore**

Read `.gitignore` — it already contains `.env` on line 3. No change needed.

- [ ] **Step 2: Create `.env.example`**

Create file `/Users/somalapurinaveen/Desktop/Work/AIFS/aifs/.env.example` with this content (no real values):

```
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
AZURE_OPENAI_API_KEY=<your-azure-openai-key>
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
TAVILY_API_KEY=<your-tavily-key>
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.azurewebsites.net
```

- [ ] **Step 3: Commit**

```bash
git add .env.example
git commit -m "docs: add .env.example documenting required environment variables"
```

---

## Task 2: Update requirements.txt

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Replace pymongo with motor, add aiofiles and azure-monitor-opentelemetry**

In `requirements.txt`, make these changes:
- Remove line: `pymongo==4.11`
- Add these lines:
```
motor==3.6.0
aiofiles==24.1.0
azure-monitor-opentelemetry==1.6.4
```

- [ ] **Step 2: Install updated dependencies**

```bash
pip install motor==3.6.0 aiofiles==24.1.0 azure-monitor-opentelemetry==1.6.4
pip uninstall pymongo -y
```

Expected output: Successfully installed motor-3.6.0 ...

- [ ] **Step 3: Commit**

```bash
git add requirements.txt
git commit -m "deps: replace pymongo with motor, add aiofiles and azure-monitor-opentelemetry"
```

---

## Task 3: Replace pymongo with motor in configuration.py

**Files:**
- Modify: `configuration.py`

- [ ] **Step 1: Rewrite configuration.py**

Replace the entire contents of `configuration.py` with:

```python
import os
import logging
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

logger = logging.getLogger(__name__)

mongodb_uri = os.getenv("MONGODB_URI")
if not mongodb_uri:
    raise ValueError("MONGODB_URI environment variable is not set")

client = AsyncIOMotorClient(
    mongodb_uri,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
    socketTimeoutMS=30000,
    maxPoolSize=20,
    minPoolSize=2,
    retryWrites=True,
)

async def ping_db():
    try:
        await client.admin.command("ping")
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error("MongoDB connection failed: %s", e)
        raise
```

- [ ] **Step 2: Update main.py to call ping_db on startup**

In `main.py`, add a startup event that calls `ping_db()` (this will be done in Task 9 together with other main.py changes — skip for now, come back after Task 9).

- [ ] **Step 3: Update routes/resume_routes.py import of client**

In `resume_routes.py` line 13, the import `from configuration import client` still works — motor's `AsyncIOMotorClient` is used the same way but all its methods are now awaitable. Mark this as a dependency to be handled in Task 7.

- [ ] **Step 4: Commit**

```bash
git add configuration.py
git commit -m "fix: replace blocking pymongo with async motor client with connection pool config"
```

---

## Task 4: Create shared_models.py to eliminate VOC/ROC duplication

**Files:**
- Create: `services/shared_models.py`

- [ ] **Step 1: Create the shared file**

Create `/Users/somalapurinaveen/Desktop/Work/AIFS/aifs/services/shared_models.py`:

```python
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
    alternatives_considered: str = Field(
        description="A listing of the various alternative approaches that were considered."
    )
    agreed_upon_approach: str = Field(description="Which alternative was selected?")
    important_assumptions: str = Field(
        description="Important assumptions considered during the decision-making process."
    )
    additional_comments: str = Field(
        description="Any additional information considered during the decision-making process."
    )
```

- [ ] **Step 2: Commit**

```bash
git add services/shared_models.py
git commit -m "refactor: add shared_models.py as single source of truth for VOC and ROC schemas"
```

---

## Task 5: Remove dead code and deduplicate VOC/ROC in all service schema files

**Files:**
- Modify: `services/Enhancements.py`, `services/Forms.py`, `services/General.py`, `services/Interface.py`, `services/Reports.py`, `services/Workflow.py`, `services/jsondatastructure.py`

- [ ] **Step 1: Update services/Enhancements.py**

Replace the entire file with:

```python
from pydantic import BaseModel, Field
from services.shared_models import VOC, ROC


class FD(BaseModel):
    Functional_Design_reference_sap_fiori_assets: str = Field(
        description="Functional Design - Reference SAP/Fiori Assets: Include all known SAP transactions, tables, programs, and reports used or containing similar data. Screenshots recommended."
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
```

- [ ] **Step 2: Update services/Forms.py**

Replace the entire file with:

```python
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
        description="Functional Design - Security Requirements: No Specific Restrictions"
    )
    Functional_Design_security_requirements_restriction_based_on_certain_criteria: Optional[str] = Field(
        description="Functional Design - Security Requirements: Restriction Based on Certain Criteria."
    )
    Functional_Design_security_requirements_other: Optional[str] = Field(
        description="Functional Design - Security Requirements: Other"
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
```

- [ ] **Step 3: Update services/General.py**

Replace the entire file with:

```python
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
```

- [ ] **Step 4: Update services/Interface.py**

Replace the entire file with:

```python
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
        description="Functional Design - Security Requirements: Yes/No"
    )
    Functional_Design_security_requirements_no_specific_restrictions: Optional[str] = Field(
        description="Functional Design - Security Requirements: No Specific Restrictions"
    )
    Functional_Design_security_requirements_restriction_based_on_certain_criteria: Optional[str] = Field(
        description="Functional Design - Security Requirements: Restriction Based on Certain Criteria."
    )
    Functional_Design_security_requirements_other: Optional[str] = Field(
        description="Functional Design - Security Requirements: Other"
    )
    Functional_Design_comments: str = Field(
        description="Functional Design - Comments."
    )
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
    Functional_Design_additional_comments: str = Field(
        description="Functional Design - Additional Comments."
    )
    Functional_Design_rework_log: str = Field(
        description="Functional Design - Rework Log."
    )


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
    Technical_Design_additional_comments: str = Field(
        description="Technical Design - Additional Comments."
    )
    Technical_Design_clean_core_implications: str = Field(
        description="Technical Design - Clean Core Implications: Tier-2 and Tier-3 technologies."
    )
```

- [ ] **Step 5: Update services/Reports.py**

Replace the entire file with:

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from services.shared_models import VOC, ROC


class InputSelectionCriterion(BaseModel):
    field_name: str = Field(..., description="Name of the input field")
    data_type: str = Field(..., description="Data type of the field")
    default_value: Optional[str] = Field(None, description="Default value if any")
    is_required: Optional[bool] = Field(True, description="Is this field required?")


class SecurityRequirements(BaseModel):
    yes_no: Optional[str] = Field(None, description="Functional Design - Security Requirements: Yes/No")
    no_specific_restrictions: Optional[str] = Field(None, description="No Specific Restrictions")
    restriction_based_on_certain_criteria: Optional[str] = Field(None, description="Restriction Based on Certain Criteria")
    other: Optional[str] = Field(None, description="Other")


class UnitTesting(BaseModel):
    unit_testing: str = Field(..., description="Functional Design - Unit Testing: test scenarios, instructions, test data, expected results")
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
    Functional_Design_error_handling: str = Field(
        ..., description="Functional Design - Error Handling: Owner Definition & Business Needs."
    )
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
    Technical_Design_additional_comments: str = Field(
        description="Technical Design - Additional Comments."
    )
    Technical_Design_rework_log: str = Field(
        description="Technical Design - Rework Log."
    )
```

- [ ] **Step 6: Update services/Workflow.py**

Replace the entire file with:

```python
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
        description="Functional Design - Security Requirements: No Specific Restrictions"
    )
    Functional_Design_security_requirements_restriction_based_on_certain_criteria: Optional[str] = Field(
        description="Functional Design - Security Requirements: Restriction Based on Certain Criteria."
    )
    Functional_Design_security_requirements_other: Optional[str] = Field(
        description="Functional Design - Security Requirements: Other"
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
    Technical_Design_development_objectives_summary: str = Field(
        description="Technical Design - 1. Development Objectives: Summary."
    )
    Technical_Design_workflow_id: Optional[str] = Field(description="Technical Design - Workflow ID.")
    Technical_Design_workflow_name: Optional[str] = Field(description="Technical Design - Workflow Name.")
    Technical_Design_development_class_package: Optional[str] = Field(description="Technical Design - Development Class/Package.")
    Technical_Design_workflow_location: Optional[str] = Field(description="Technical Design - Workflow Location.")
    Technical_Design_development_type: Optional[str] = Field(description="Technical Design - Development Type: Workflow, Other.")
    Technical_Design_frequency: Optional[str] = Field(description="Technical Design - Frequency.")
    Technical_Design_trigger: Optional[str] = Field(description="Technical Design - Trigger: Event, Batch, Method.")
    Technical_Design_volume: Optional[str] = Field(description="Technical Design - Volume.")
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
    Technical_Design_dependencies: Optional[str] = Field(description="Technical Design - Dependencies.")
    Technical_Design_restart_recovery_procedures: Optional[str] = Field(description="Technical Design - Restart/Recovery Procedures.")
    Technical_Design_data_maintenance_requirements: Optional[str] = Field(description="Technical Design - Data Maintenance Requirements.")
    Technical_Design_external_programs: str = Field(description="Technical Design - External Programs.")
    Technical_Design_rework_log: str = Field(description="Technical Design - Rework Log.")
    Technical_Design_clean_core_implications: str = Field(description="Technical Design - Clean Core Implications.")
```

- [ ] **Step 7: Update services/jsondatastructure.py**

Replace the entire file with:

```python
from services.shared_models import VOC, ROC
from services.General import FD, TD

__all__ = ["VOC", "ROC", "FD", "TD"]
```

- [ ] **Step 8: Commit**

```bash
git add services/Enhancements.py services/Forms.py services/General.py services/Interface.py services/Reports.py services/Workflow.py services/jsondatastructure.py
git commit -m "refactor: eliminate dead commented code and VOC/ROC duplication across schema files"
```

---

## Task 6: Fix resume_service.py — duplicate imports and async file I/O

**Files:**
- Modify: `services/resume_service.py`

- [ ] **Step 1: Rewrite resume_service.py**

Replace the entire file with:

```python
import os
import json
import logging
import aiofiles

from services.model import openmodel

logger = logging.getLogger(__name__)

RESUME_DIR = "resumes_data"
os.makedirs(RESUME_DIR, exist_ok=True)


def generate_resume(client_problem: str, client_name: str) -> dict:
    response = openmodel(client_problem, client_name)
    if response is None:
        logger.error("No response received from openmodel")
        return {}
    return response


async def save_resume(resume_data: dict) -> str:
    try:
        os.makedirs(RESUME_DIR, exist_ok=True)
        client_name = resume_data.get("client_name", "unknown_client").replace(" ", "_")
        file_name = f"{client_name}.json"
        file_path = os.path.join(RESUME_DIR, file_name)

        if os.path.exists(file_path):
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
            existing_data = json.loads(content)
            if not isinstance(existing_data, list):
                raise ValueError(f"File {file_name} does not contain a list.")
            existing_data.append(resume_data)
        else:
            resume_data["file_name"] = file_name
            existing_data = [resume_data]

        async with aiofiles.open(file_path, "w") as f:
            await f.write(json.dumps(existing_data, indent=4))

        return file_name
    except Exception as e:
        logger.error("Error saving resume to file: %s", e)
        return None


async def get_all_resumes() -> list:
    resumes = []
    try:
        for file_name in os.listdir(RESUME_DIR):
            file_path = os.path.join(RESUME_DIR, file_name)
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
            resumes.append(json.loads(content))
    except Exception as e:
        logger.error("Error reading resumes from file: %s", e)
    return resumes


async def view_resume(resume_name: str) -> dict:
    try:
        for file_name in os.listdir(RESUME_DIR):
            file_path = os.path.join(RESUME_DIR, file_name)
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
            resume_data = json.loads(content)
            generated_resume = resume_data[0].get("generated_resume", {})
            if generated_resume.get("client_name") == resume_name:
                return resume_data
        return {"error": "RICEF not found"}
    except Exception as e:
        logger.error("Error reading RICEF file: %s", e)
        return {"error": str(e)}
```

- [ ] **Step 2: Update resume_routes.py view() to await view_resume**

In `resume_routes.py`, the `view()` function calls `view_resume(resume_name)` — this must be awaited now. This will be fixed in Task 7 together with other route changes.

- [ ] **Step 3: Commit**

```bash
git add services/resume_service.py
git commit -m "fix: remove duplicate imports in resume_service.py, convert file I/O to async aiofiles"
```

---

## Task 7: Create llm_client.py — singleton LLM, graphs, and wricefType allowlist

**Files:**
- Create: `services/llm_client.py`
- Modify: `services/model.py`

- [ ] **Step 1: Create services/llm_client.py**

Create `/Users/somalapurinaveen/Desktop/Work/AIFS/aifs/services/llm_client.py`:

```python
import os
import importlib
import logging
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()

logger = logging.getLogger(__name__)

ALLOWED_WRICEF_TYPES = {"Workflow", "Reports", "Interface", "Conversions", "Enhancements", "Forms", "General"}

def get_azure_model() -> AzureChatOpenAI:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("OPENAI_API_VERSION")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    missing = [k for k, v in {
        "AZURE_OPENAI_API_KEY": api_key,
        "AZURE_OPENAI_ENDPOINT": api_base,
        "OPENAI_API_VERSION": api_version,
        "AZURE_OPENAI_DEPLOYMENT": deployment,
    }.items() if not v]

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return AzureChatOpenAI(
        api_key=api_key,
        azure_endpoint=api_base,
        api_version=api_version,
        azure_deployment=deployment,
        model_name=deployment,
        temperature=0,
        model_kwargs={"extra_headers": {"x-ms-model-mesh-model-name": deployment}},
        timeout=120,
        max_retries=3,
    )


def get_tavily_tool() -> TavilySearch:
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY not found in environment.")
    os.environ["TAVILY_API_KEY"] = tavily_api_key
    return TavilySearch(max_results=5, topic="general", search_depth="advanced")


def validate_wricef_type(wricef_type: str) -> str:
    if wricef_type not in ALLOWED_WRICEF_TYPES:
        raise ValueError(
            f"Invalid wricefType '{wricef_type}'. Must be one of: {', '.join(sorted(ALLOWED_WRICEF_TYPES))}"
        )
    return wricef_type


def get_pydantic_class(wricef_type: str, class_name: str):
    validate_wricef_type(wricef_type)
    try:
        module = importlib.import_module(f"services.{wricef_type}")
        return getattr(module, class_name)
    except ModuleNotFoundError:
        raise ImportError(f"Module 'services.{wricef_type}' not found.")
    except AttributeError as e:
        raise ImportError(f"Class '{class_name}' not found in 'services.{wricef_type}': {e}")


_azure_model: AzureChatOpenAI = None
_tavily_tool: TavilySearch = None


def get_model() -> AzureChatOpenAI:
    global _azure_model
    if _azure_model is None:
        _azure_model = get_azure_model()
    return _azure_model


def get_tool() -> TavilySearch:
    global _tavily_tool
    if _tavily_tool is None:
        _tavily_tool = get_tavily_tool()
    return _tavily_tool
```

- [ ] **Step 2: Rewrite services/model.py**

Replace the entire contents of `services/model.py` with:

```python
import logging
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from httpx import TimeoutException
import asyncio

from services.llm_client import get_model, get_tool, get_pydantic_class

logger = logging.getLogger(__name__)

INDEX_TO_CLASS = {0: "VOC", 1: "ROC", 2: "FD", 3: "TD"}
PREFIX_TO_CLASS = {"VOC": "VOC", "ROC": "ROC", "FD": "FD", "TD": "TD"}


def _build_graph(Pydantic_Object):
    model = get_model()
    tool = get_tool()
    model_with_tools = model.bind_tools([tool])
    model_with_structured_output = model.with_structured_output(Pydantic_Object)

    class AgentState(MessagesState):
        final_response: Pydantic_Object

    def call_model(state: AgentState):
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def respond(state: AgentState):
        response = model_with_structured_output.invoke(
            [HumanMessage(content=state["messages"][-2].content)]
        )
        return {"final_response": response}

    def should_continue(state: AgentState):
        last_message = state["messages"][-1]
        return "respond" if not last_message.tool_calls else "continue"

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("respond", respond)
    workflow.add_node("tools", ToolNode([tool]))
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"continue": "tools", "respond": "respond"})
    workflow.add_edge("tools", "agent")
    workflow.add_edge("respond", END)
    return workflow.compile()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((TimeoutException, RuntimeError)),
    reraise=True,
)
def openmodel(client_business_requirement: str, wricef_type: str) -> dict:
    prefix = client_business_requirement.split(" ")[0] if client_business_requirement else ""
    class_name = PREFIX_TO_CLASS.get(prefix)
    if not class_name:
        raise ValueError(f"Business requirement must start with one of: {', '.join(PREFIX_TO_CLASS.keys())}")

    Pydantic_Object = get_pydantic_class(wricef_type, class_name)
    graph = _build_graph(Pydantic_Object)

    logger.info("Invoking LLM graph for wricefType=%s class=%s", wricef_type, class_name)
    result = graph.invoke(input={"messages": [("human", client_business_requirement)]})
    answer = result["final_response"]
    return answer.dict()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((TimeoutException, RuntimeError)),
    reraise=True,
)
def openmodel_regeneration(
    client_business_requirement: str,
    wricefType: str,
    previous_response: str,
    current_response: str,
    index_value: int,
) -> dict:
    class_name = INDEX_TO_CLASS.get(index_value)
    if not class_name:
        raise ValueError(f"Invalid index_value {index_value}. Must be 0–3.")

    Pydantic_Object = get_pydantic_class(wricefType, class_name)
    graph = _build_graph(Pydantic_Object)

    human_input = (
        f"Client Business Requirement: {client_business_requirement} "
        f"Previous Response: {previous_response} "
        f"Current Response: {current_response} "
        f"Based on the Client Business Requirement & Previous Response Enhance Current Response"
    )

    logger.info("Invoking regeneration LLM graph for wricefType=%s class=%s", wricefType, class_name)
    result = graph.invoke(input={"messages": [("human", human_input)]})
    answer = result["final_response"]
    return answer.dict()
```

- [ ] **Step 3: Commit**

```bash
git add services/llm_client.py services/model.py
git commit -m "fix: extract LLM singleton to llm_client.py, add wricefType allowlist, tenacity retry, remove dead code"
```

---

## Task 8: Harden resume_routes.py — path safety, input validation, $push cap, model_dump, async mongo

**Files:**
- Modify: `routes/resume_routes.py`

- [ ] **Step 1: Add wricef_type allowlist and sanitize ricefw_number**

At the top of `resume_routes.py`, add after the existing imports:

```python
import re
import logging
from services.llm_client import ALLOWED_WRICEF_TYPES

logger = logging.getLogger(__name__)

RICEFW_NUMBER_PATTERN = re.compile(r'^[A-Za-z0-9_\-]{1,50}$')
MAX_GENERATED_RESUME_ENTRIES = 20


def _validate_ricefw_number(ricefw_number: str) -> str:
    if not RICEFW_NUMBER_PATTERN.match(ricefw_number):
        raise HTTPException(status_code=400, detail="Invalid ricefw_number format")
    return ricefw_number


def _validate_wricef_type(wricef_type: str) -> str:
    if wricef_type not in ALLOWED_WRICEF_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid wricef type '{wricef_type}'")
    return wricef_type
```

- [ ] **Step 2: Fix form_data.dict() → model_dump() in /add endpoint**

In the `/add` endpoint (line ~51), change:
```python
new_item = form_data.dict()
```
to:
```python
new_item = form_data.model_dump()
```

- [ ] **Step 3: Add wricef_type validation and ricefw_number sanitization to /success endpoint**

In the `/success` endpoint, change:
```python
async def success_page(request: Request, ricefwNumber: str, wricef_type: str):
    resume = collection.find_one({"ricefw_number": ricefwNumber})
```
to:
```python
async def success_page(request: Request, ricefwNumber: str, wricef_type: str):
    ricefwNumber = _validate_ricefw_number(ricefwNumber)
    _validate_wricef_type(wricef_type)
    resume = await collection.find_one({"ricefw_number": ricefwNumber})
```

And change `if not resume:` line — already raises 404, no change needed there.

Also change the template response to use the validated `wricef_type` — it already uses the variable, so no further change needed.

- [ ] **Step 4: Await all MongoDB calls in resume_routes.py**

Motor requires `await` on all collection operations. Go through every MongoDB call in the file and add `await`:

- `collection.find_one(...)` → `await collection.find_one(...)`
- `collection.update_one(...)` → `await collection.update_one(...)`
- `list(collection.find(...))` → `[doc async for doc in collection.find(...)]` (motor cursor is async)

Specifically update these locations:

**`/add` endpoint** (~line 56):
```python
result = await collection.update_one(
    {"ricefw_number": new_item["ricefw_number"]},
    {"$setOnInsert": new_item},
    upsert=True,
)
```

**`/success` endpoint** (~line 82):
```python
resume = await collection.find_one({"ricefw_number": ricefwNumber})
```

**`/view/{ricefw_number}` endpoint** (~line 108):
```python
ricefw_number = _validate_ricefw_number(ricefw_number)
resume = await collection.find_one({"ricefw_number": ricefw_number})
```

**`/api/wricef_data/{ricefw_number}` endpoint** (~line 137):
```python
ricefw_number = _validate_ricefw_number(ricefw_number)
doc = await collection.find_one(
    {"ricefw_number": ricefw_number},
    {"_id": 0, "customer": 1, "fileText": 1},
)
```

**`/listofwricefs` endpoint** (~line 156):
```python
ricefs_list = [
    doc async for doc in collection.find({}, {"_id": 0, "ricefw_number": 1, "customer": 1})
]
```

**`/generate_response` endpoint** (~line 176):
```python
ricefwNumber = _validate_ricefw_number(ricefwNumber)
resume = await collection.find_one({"ricefw_number": ricefwNumber})
```

And for the update (~line 202), add the `$push` cap with `$slice`:
```python
result = await collection.update_one(
    {"ricefw_number": ricefwNumber},
    {
        "$push": {
            "generated_resume": {
                "$each": [new_field_data["generated_resume"]],
                "$slice": -MAX_GENERATED_RESUME_ENTRIES,
            },
            "client_problem": {
                "$each": [new_field_data["client_problem"]],
                "$slice": -MAX_GENERATED_RESUME_ENTRIES,
            },
        }
    },
)
```

**`/resume_view/{resume_name}` endpoint** (~line 239): await `view_resume`:
```python
resume = await view_resume(resume_name)
```

**`get_document_by_customer` function** (~line 253): make async:
```python
async def get_document_by_customer(ricefw_number: str):
    _validate_ricefw_number(ricefw_number)
    return await collection.find_one({"ricefw_number": ricefw_number})
```

And in `download_pdf` (~line 258): await the call:
```python
document = await get_document_by_customer(ricefw_number)
```
Also add wricef_type validation before building the template path:
```python
wricef_type_val = document.get("ricefw", "")
_validate_wricef_type(wricef_type_val)
template_path = f"templates/{wricef_type_val}.docx"
```

**`/update_customer_data` endpoint** (~line 308):
```python
document = await collection.find_one({"customer": customer_name})
...
result = await collection.update_one({"_id": document["_id"]}, pipeline)
```

**`/regeneration` endpoint** (~line 372):
```python
ricefwNumber = _validate_ricefw_number(ricefwNumber)
document = await collection.find_one({"ricefw_number": ricefwNumber})
...
result = await collection.update_one(
    {"ricefw_number": ricefwNumber},
    {"$set": {"generated_resume": generated_resume}},
)
```

- [ ] **Step 5: Commit**

```bash
git add routes/resume_routes.py
git commit -m "fix: add wricef_type allowlist, sanitize ricefw_number, await motor calls, cap \$push, fix model_dump"
```

---

## Task 9: Harden main.py — absolute paths, CORS, health endpoint, OpenTelemetry, startup ping

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Rewrite main.py**

Replace the entire contents of `main.py` with:

```python
import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from routes.resume_routes import router as resume_router
from configuration import ping_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ping_db()
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan)

_connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if _connection_string:
    from azure.monitor.opentelemetry import configure_azure_monitor
    configure_azure_monitor(connection_string=_connection_string)
    logger.info("Azure Monitor OpenTelemetry configured")

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(resume_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

- [ ] **Step 2: Add APPLICATIONINSIGHTS_CONNECTION_STRING to .env.example**

Append to `.env.example`:
```
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=<key>;IngestionEndpoint=https://...
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.azurewebsites.net
```

- [ ] **Step 3: Commit**

```bash
git add main.py .env.example
git commit -m "fix: use absolute paths, add CORS, /health endpoint, OpenTelemetry, structured logging, startup DB ping"
```

---

## Task 10: Add Gunicorn production config

**Files:**
- Create: `gunicorn.conf.py`

- [ ] **Step 1: Create gunicorn.conf.py**

Create `/Users/somalapurinaveen/Desktop/Work/AIFS/aifs/gunicorn.conf.py`:

```python
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
timeout = 180
keepalive = 5
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

- [ ] **Step 2: Add gunicorn to requirements.txt**

Add to `requirements.txt`:
```
gunicorn==23.0.0
```

Install it:
```bash
pip install gunicorn==23.0.0
```

- [ ] **Step 3: Commit**

```bash
git add gunicorn.conf.py requirements.txt
git commit -m "feat: add gunicorn production config for Azure deployment"
```

---

## Task 11: Final smoke test

- [ ] **Step 1: Start the app with uvicorn (dev)**

```bash
cd /Users/somalapurinaveen/Desktop/Work/AIFS/aifs
uvicorn main:app --reload --port 8000
```

Expected: no import errors, "Successfully connected to MongoDB" in logs, server starts on port 8000.

- [ ] **Step 2: Hit the health endpoint**

```bash
curl http://localhost:8000/health
```

Expected output:
```json
{"status": "ok"}
```

- [ ] **Step 3: Verify /listofwricefs returns without error**

```bash
curl http://localhost:8000/listofwricefs
```

Expected: HTML response with the list table (or empty list), no 500 error.

- [ ] **Step 4: Commit final state**

```bash
git add -A
git commit -m "chore: production hardening complete - all 22 issues resolved except auth"
```
