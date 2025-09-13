## To Run

```
mv .env.example .env
set 'OPENAI_API_KEY' to .env file
./setup.sh 
python src/main.py 
```

```mermaid 
flowchart TB
    %% Define Layers
    subgraph L1[User]
        SC["High Level Scenario(YAML)"]
        CFG["Config(YAML)"]
    end

    subgraph L2[AI Execution Engine]
        TSG["Test Step Generator"]
        CE["AMP Engine"]
        MCP["Browser MCP Server"]
    end

    subgraph L3[System Under Test]
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

### Website to Practice UI Automation 
- https://www.saucedemo.com
- https://the-internet.herokuapp.com
- https://practice-automation.com
- http://www.uitestingplayground.com
- https://qa-practice.netlify.app
- https://weathershopper.pythonanywhere.com
