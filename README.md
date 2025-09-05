```
[YAML Intent] --> [Goal Parser] --> [Action Planner (LLM)] --> [Playwright Agent]
                                               ↓
                                  [DOM Scraper + Element Ranker]

 ```
 ## To Run
 
 ```
 ./setup.sh 
 python main.py   
 ```
 
 ```mermaid 
flowchart TB
    %% Define Layers
    subgraph L1[User Layer]
        SC["High Level Scenario(YAML)"]
        CFG["Config(YAML)"]
    end

    subgraph L2[AI Execution Engine]
        TSG["Test Step Generator"]
        CE["AMP Engine"]
        MCP["Browser MCP Server"]
    end

    subgraph L3[System Under Test Layer]
        B[Browser]
    end

    %% Connections
    CFG --> TSG
    SC --> TSG
    TSG -->|"Detailed Actions & Expectations"| CE
    CE --> MCP
    MCP --> B
    B --> MCP
    MCP --> CE
    CE -->|"Output"| TestResult
```

