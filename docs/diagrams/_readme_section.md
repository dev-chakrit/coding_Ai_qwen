
---

## Architecture Diagrams

### 1. System Architecture Diagram

แสดงภาพรวมทั้งระบบ: Editor Layer, MCP Protocol, MCP Server (Resources, Prompts, Tools), Model/Runtime Layer, Clean Architecture Layers, File System

> รูป PNG: [`docs/diagrams/system_architecture.png`](./docs/diagrams/system_architecture.png)

```mermaid
graph TB
    subgraph EDITOR["Editor Layer"]
        direction LR
        ZED["Zed Editor\nNative Agent + MCP Client"]
        VSCODE["VS Code\nCustom Agents + Hooks"]
    end

    subgraph MCP_PROTO["MCP Protocol Layer"]
        STDIO["MCP over stdio"]
    end

    subgraph MCP_SERVER["MCP Server FastMCP"]
        direction TB
        subgraph RESOURCES["Resources"]
            R1["architecture://clean-architecture-guide"]
            R2["workflow://delivery-quality"]
            R3["design://frontend-quality-guide"]
            R4["workflow://senior-delivery-guide"]
            R5["workflow://quality-gates"]
            R6["workflow://vision-workflow-guide"]
        end

        subgraph PROMPTS["Prompts"]
            P1["clean_architecture_prompt"]
            P2["repair_loop_prompt"]
            P3["frontend_polish_prompt"]
            P4["senior_delivery_prompt"]
            P5["quality_gate_prompt"]
            P6["ui_reference_prompt"]
            P7["screenshot_debug_prompt"]
        end

        subgraph TOOLS["Tools"]
            T1["workspace_summary"]
            T2["find_files"]
            T3["search_code"]
            T4["read_text_file"]
            T5["write_text_file"]
            T6["replace_in_file"]
            T7["create_clean_architecture_feature"]
            T8["run_project_command"]
            T9["get_quality_gates"]
            T10["suggest_quality_gate_commands"]
            T11["run_quality_gates"]
        end

        subgraph CONFIG["Config"]
            CFG1["Settings.from_env"]
            CFG2["quality-gates.json"]
        end
    end

    subgraph CLEAN_ARCH["Clean Architecture Layers"]
        direction LR
        DOMAIN["Domain\nEntity, Value Object,\nRepository Contract"]
        APP["Application\nUse Case,\nOrchestration"]
        INFRA["Infrastructure\nFile System, LLM Adapter,\nExternal API"]
        PRES["Presentation\nCLI, HTTP DTO,\nEditor Payload"]
    end

    subgraph MODELS["Model / Runtime Layer"]
        direction LR
        LLAMA["llama.cpp Server\nGemma4 E4B Q4_K_M\nOpenAI-compatible API"]
        VISION["vLLM Vision Sidecar\nQwen3-VL-2B-Instruct\nImage Analysis"]
        OPENAI["OpenAI Stable MCP\nGPT-5.4 mini\nCloud Fallback"]
    end

    subgraph WORKSPACE["Workspace / File System"]
        FS["Project Files"]
        QG["quality-gates.json"]
        SCRIPTS["scripts/"]
    end

    ZED -->|"MCP calls"| STDIO
    VSCODE -->|"MCP calls"| STDIO
    STDIO --> MCP_SERVER

    ZED -.->|"LLM inference"| LLAMA
    ZED -.->|"LLM inference"| OPENAI
    ZED -.->|"Vision analysis"| VISION

    TOOLS --> WORKSPACE
    CONFIG --> QG
    MCP_SERVER --> CLEAN_ARCH

    PRES --> APP
    INFRA --> APP
    APP --> DOMAIN
```

---

### 2. Sequence Diagram

แสดง flow การทำงาน 6 phases: Task Understanding, Code Inspection, Implementation, Quality Gate + Repair Loop, Vision Workflow, Report

> รูป PNG: [`docs/diagrams/sequence_diagram.png`](./docs/diagrams/sequence_diagram.png)

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant Editor as Editor Zed/VSCode
    participant MCP as MCP Server FastMCP
    participant LLM as llama.cpp Gemma4
    participant Vision as vLLM Sidecar Qwen3-VL
    participant FS as File System

    rect rgb(30, 41, 59)
    Note over Dev,FS: Phase 1 Task Understanding
    Dev->>Editor: send prompt
    Editor->>LLM: send prompt + context
    LLM-->>Editor: analyze + plan tool calls
    end

    rect rgb(30, 41, 59)
    Note over Dev,FS: Phase 2 Code Inspection
    Editor->>MCP: workspace_summary()
    MCP->>FS: read workspace tree
    FS-->>MCP: return tree structure
    MCP-->>Editor: return project structure

    Editor->>MCP: search_code(query)
    MCP->>FS: search files
    FS-->>MCP: return search results
    MCP-->>Editor: return matching code

    Editor->>MCP: read_text_file(path)
    MCP->>FS: read file
    FS-->>MCP: return file content
    MCP-->>Editor: return content + line numbers
    end

    rect rgb(30, 41, 59)
    Note over Dev,FS: Phase 3 Implementation
    Editor->>LLM: generate code from context
    LLM-->>Editor: return code changes

    alt New Feature
        Editor->>MCP: create_clean_architecture_feature(name)
        MCP->>FS: scaffold domain/app/infra/pres
        FS-->>MCP: confirm scaffold
        MCP-->>Editor: return created paths
    end

    Editor->>MCP: write_text_file(path, content)
    MCP->>FS: write new file
    FS-->>MCP: confirm write
    MCP-->>Editor: return success

    Editor->>MCP: replace_in_file(path, search, replace)
    MCP->>FS: edit code
    FS-->>MCP: confirm edit
    MCP-->>Editor: return success
    end

    rect rgb(30, 41, 59)
    Note over Dev,FS: Phase 4 Quality Gate Verification
    Editor->>MCP: suggest_quality_gate_commands(changed_paths)
    MCP->>FS: read quality-gates.json
    FS-->>MCP: return config
    MCP-->>Editor: return suggested commands

    loop Repair Loop until pass
        Editor->>MCP: run_quality_gates(changed_paths)
        MCP->>FS: run verification commands
        FS-->>MCP: return results pass/fail
        MCP-->>Editor: return gate results

        alt Gate Failed
            Editor->>LLM: analyze failure + find root cause
            LLM-->>Editor: return fix
            Editor->>MCP: replace_in_file(fix)
            MCP->>FS: apply fix
            FS-->>MCP: confirm
            MCP-->>Editor: return success
        end
    end
    end

    rect rgb(30, 41, 59)
    Note over Dev,FS: Phase 5 Vision Workflow Optional
    Dev->>Editor: attach screenshot / UI reference
    Editor->>Vision: analyze image
    Vision-->>Editor: return visual brief
    Editor->>LLM: implement from brief
    LLM-->>Editor: return implementation
    end

    rect rgb(30, 41, 59)
    Note over Dev,FS: Phase 6 Report
    Editor-->>Dev: summary + verification results
    end
```

---

### 3. Logic / State Diagram

แสดง state machine ของ agent: รับ task, ตัดสินใจ vision/code, implement, quality gates, repair loop, report

> รูป PNG: [`docs/diagrams/logic_state_diagram.png`](./docs/diagrams/logic_state_diagram.png)

```mermaid
stateDiagram-v2
    [*] --> ReceiveTask

    state ReceiveTask {
        [*] --> ParsePrompt
        ParsePrompt --> ClassifyTask
    }

    ReceiveTask --> TaskDecision

    state TaskDecision <<choice>>
    TaskDecision --> VisionAnalysis: Has image/UI ref
    TaskDecision --> CodeInspection: No image

    state VisionAnalysis {
        [*] --> SendToVision
        SendToVision --> ExtractInfo
        state ExtractInfo {
            UIRef: UI Ref layout spacing typography
            ErrorShot: Screenshot error text paths root cause
        }
        ExtractInfo --> GenerateBrief
    }

    VisionAnalysis --> CodeInspection

    state CodeInspection {
        [*] --> WorkspaceSummary
        WorkspaceSummary --> SearchCode
        SearchCode --> ReadFiles
        ReadFiles --> UnderstandContext
    }

    CodeInspection --> PlanDecision

    state PlanDecision <<choice>>
    PlanDecision --> ScaffoldFeature: Need new feature
    PlanDecision --> Implementation: Edit existing

    state ScaffoldFeature {
        [*] --> CreateSlice
        CreateSlice --> CreateDomain
        CreateDomain --> CreateApp
        CreateApp --> CreateInfra
        CreateInfra --> CreatePres
    }

    ScaffoldFeature --> Implementation

    state Implementation {
        [*] --> GenerateCode
        GenerateCode --> WriteFile
        GenerateCode --> EditFile
        WriteFile --> ChangesApplied
        EditFile --> ChangesApplied
    }

    Implementation --> QualityGates

    state QualityGates {
        [*] --> SuggestCommands
        SuggestCommands --> RunGates
        RunGates --> GateResult

        state GateResult <<choice>>
        GateResult --> RepairLoop: FAIL
        GateResult --> AllPassed: PASS

        state RepairLoop {
            [*] --> DiagnoseFailure
            DiagnoseFailure --> FindRootCause
            FindRootCause --> ApplyFix
            ApplyFix --> RerunCheck
        }
        RepairLoop --> RunGates
    }

    state AllPassed {
        [*] --> CheckDOD
        state CheckDOD {
            CodeCorrect: Code correct
            TestPass: Tests pass
            NoRegression: No regression
            UIQuality: UI quality bar pass
        }
    }

    AllPassed --> Report

    state Report {
        [*] --> SummarizeWork
        SummarizeWork --> ListVerified
        ListVerified --> ListUnverified
        ListUnverified --> NotifyDev
    }

    Report --> [*]
```
