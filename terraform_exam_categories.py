"""
HashiCorp Certified Terraform Associate (TA-004)
Practice Exam - Question Categories/Types Dictionary
Extracted from: Udemy Course by Bryan Krausen
URL: https://www.udemy.com/course/terraform-associate-004-practice-exams/
"""

terraform_exam = {

    # ─────────────────────────────────────────────────────────────────────────
    # QUESTION FORMATS / TYPES
    # ─────────────────────────────────────────────────────────────────────────
    "question_formats": {
        "multiple_choice": {
            "description": "Single correct answer selected from 4-5 options.",
            "tip": "Eliminate distractors; look for the MOST correct answer.",
            "example": "Which command initializes a Terraform working directory?",
            "answer": "terraform init"
        },
        "multi_select": {
            "description": "Two or more correct answers must be selected (exam specifies how many).",
            "tip": "Read the stem carefully – it usually says 'Select TWO' or 'Select all that apply'.",
            "example": "Which TWO statements are true about Terraform state?",
            "answer": ["State maps real infrastructure to config", "State stores resource metadata"]
        },
        "true_false": {
            "description": "Simple True / False statement about a Terraform concept.",
            "tip": "Watch for absolute words like 'always', 'never', 'only'.",
            "example": "True or False: terraform plan modifies infrastructure.",
            "answer": "False – plan only shows proposed changes."
        },
        "scenario_based": {
            "description": "A real-world situation is described; you pick the best action or explanation.",
            "tip": "Focus on the goal and constraints mentioned in the scenario.",
            "example": "A team needs to share state across CI/CD pipelines. What should they configure?",
            "answer": "A remote backend (e.g., HCP Terraform / S3 with DynamoDB)"
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # EXAM DOMAINS / TOPIC CATEGORIES  (TA-004 Objectives)
    # ─────────────────────────────────────────────────────────────────────────
    "exam_domains": {

        "1_infrastructure_as_code": {
            "weight": "~8%",
            "description": "Understand IaC concepts and why Terraform is used.",
            "key_topics": [
                "What is IaC and its benefits (consistency, repeatability, version control)",
                "Declarative vs imperative IaC",
                "Terraform vs other IaC tools (Ansible, CloudFormation, Pulumi)",
                "Idempotency in IaC",
                "GitOps and IaC workflows"
            ],
            "correct_answer_example": {
                "question": "Which characteristic best describes Infrastructure as Code?",
                "answer": "Infrastructure is defined and managed using configuration files that can be version-controlled.",
                "explanation": "IaC treats infrastructure configuration like software code, enabling versioning, review, and automation."
            }
        },

        "2_terraform_fundamentals": {
            "weight": "~26%",
            "description": "Core Terraform concepts, providers, and the dependency lock file.",
            "key_topics": [
                "Terraform architecture (core, providers, state)",
                "Provider installation and configuration",
                "Dependency lock file (.terraform.lock.hcl) – purpose, usage, updates",
                "terraform init – initialization, provider download",
                "Resource vs data sources",
                "Input variables, output values, local values",
                "Complex types: list, map, set, object, tuple",
                "Built-in functions (toset, merge, lookup, length, etc.)",
                "Validations and custom conditions (check blocks – Terraform 1.x)",
                "Sensitive values handling"
            ],
            "correct_answer_example": {
                "question": "What is the purpose of the .terraform.lock.hcl file?",
                "answer": "It records the exact provider versions and hashes selected during `terraform init`, ensuring reproducible installations.",
                "explanation": "The lock file prevents unexpected provider upgrades by pinning versions across team members and CI/CD pipelines."
            }
        },

        "3_terraform_workflow": {
            "weight": "~22%",
            "description": "Day-to-day CLI workflow: write → plan → apply → destroy.",
            "key_topics": [
                "terraform fmt – formatting",
                "terraform validate – syntax and logic validation",
                "terraform plan – execution plan, saved plan files",
                "terraform apply – applying changes, auto-approve",
                "terraform destroy – destroying infrastructure",
                "terraform output – reading outputs",
                "terraform console – expression evaluation",
                "terraform graph – dependency visualization",
                "Targeting resources with -target flag",
                "Refresh-only mode (terraform apply -refresh-only)"
            ],
            "correct_answer_example": {
                "question": "Which command should you run to reformat your Terraform code to the canonical style?",
                "answer": "terraform fmt",
                "explanation": "`terraform fmt` rewrites Terraform configuration files in the canonical format and style."
            }
        },

        "4_configuration_language": {
            "weight": "~24%",
            "description": "HCL syntax, resources, data sources, expressions, and meta-arguments.",
            "key_topics": [
                "Resource blocks and meta-arguments: depends_on, count, for_each, provider, lifecycle",
                "lifecycle rules: create_before_destroy, prevent_destroy, ignore_changes, replace_triggered_by",
                "Data source blocks – reading existing infrastructure",
                "References and expressions: local references, module outputs, resource attributes",
                "Variable types and validation rules",
                "Output values and sensitive outputs",
                "Conditional expressions and ternary operator",
                "for expressions and dynamic blocks",
                "Terraform 1.12 new features (ephemeral values, write-only attributes)",
                "Terraform checks and custom assertions"
            ],
            "correct_answer_example": {
                "question": "What meta-argument prevents Terraform from destroying a resource?",
                "answer": "lifecycle { prevent_destroy = true }",
                "explanation": "When `prevent_destroy` is set to true, Terraform will return an error and refuse to destroy that resource during `terraform destroy` or when the resource would be replaced."
            }
        },

        "5_modules": {
            "weight": "~12%",
            "description": "Creating, sourcing, versioning, and composing Terraform modules.",
            "key_topics": [
                "Module structure: main.tf, variables.tf, outputs.tf",
                "Module sources: local path, Terraform Registry, GitHub, S3",
                "Module versioning with version constraints",
                "Passing input variables into modules",
                "Accessing module output values",
                "Module composition and nesting",
                "Published vs private modules",
                "terraform get command"
            ],
            "correct_answer_example": {
                "question": "Which module source type is used to download a module from the public Terraform Registry?",
                "answer": "hashicorp/<module_name>/<provider> (registry.terraform.io)",
                "explanation": "Public Registry modules use the format <NAMESPACE>/<MODULE>/<PROVIDER> and do not need a hostname prefix."
            }
        },

        "6_state_management": {
            "weight": "~20%",
            "description": "Terraform state files, backends, locking, and state operations.",
            "key_topics": [
                "Purpose of terraform.tfstate",
                "Local vs remote backends",
                "Supported remote backends: S3, Azure Blob, GCS, HCP Terraform",
                "State locking – prevents concurrent modifications",
                "terraform state list / show / mv / rm / pull / push",
                "Sensitive data in state – encryption at rest",
                "Drift detection (terraform plan detects drift)",
                "Refresh-only plans",
                "Partial state and resource tainting",
                "terraform force-unlock"
            ],
            "correct_answer_example": {
                "question": "What happens when two engineers run `terraform apply` simultaneously with a remote backend that supports locking?",
                "answer": "The second apply will be blocked until the first releases the state lock.",
                "explanation": "State locking prevents race conditions. Backends like S3+DynamoDB and HCP Terraform implement locking automatically."
            }
        },

        "7_import_and_moved": {
            "weight": "~8%",
            "description": "Importing existing infrastructure and safely refactoring state.",
            "key_topics": [
                "terraform import command (legacy)",
                "import blocks (Terraform 1.5+) – declarative import",
                "moved blocks – refactoring resource addresses without destroying",
                "removed blocks (Terraform 1.7+) – safely removing resources from config",
                "Generating config with terraform plan -generate-config-out",
                "When to use import vs moved vs removed blocks"
            ],
            "correct_answer_example": {
                "question": "A resource was renamed in the Terraform config. How can you avoid destroying and recreating it?",
                "answer": "Use a `moved` block to map the old resource address to the new one.",
                "explanation": "`moved` blocks tell Terraform that an existing resource has been renamed, preventing unnecessary destroy/create cycles."
            }
        },

        "8_hcp_terraform": {
            "weight": "~18%",
            "description": "HCP Terraform (formerly Terraform Cloud) collaboration and governance features.",
            "key_topics": [
                "Workspaces in HCP Terraform – purpose and organization",
                "Projects – grouping workspaces",
                "Variable sets – reusable variables across workspaces",
                "Remote operations: remote plans and applies",
                "Run triggers – chaining workspace runs",
                "Private module registry",
                "Policy enforcement with Sentinel and OPA",
                "Drift detection in HCP Terraform",
                "Teams and RBAC – role-based access control",
                "Audit logging and governance",
                "Cost estimation",
                "HCP Terraform vs Terraform Enterprise",
                "Agent pools for private infrastructure"
            ],
            "correct_answer_example": {
                "question": "What HCP Terraform feature allows you to define variables once and apply them to multiple workspaces?",
                "answer": "Variable Sets",
                "explanation": "Variable Sets let you define a group of variables (including credentials) once and attach them to multiple workspaces, avoiding repetition."
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # COMMONLY TESTED COMMANDS (quick reference)
    # ─────────────────────────────────────────────────────────────────────────
    "key_commands": {
        "terraform init":       "Initialize working directory, download providers & modules",
        "terraform fmt":        "Auto-format HCL code to canonical style",
        "terraform validate":   "Check syntax and configuration validity (no API calls)",
        "terraform plan":       "Show execution plan (what will change); use -out to save plan",
        "terraform apply":      "Apply changes to reach desired state",
        "terraform destroy":    "Destroy all managed infrastructure",
        "terraform output":     "Print output values from state",
        "terraform show":       "Show current state or a saved plan",
        "terraform state list": "List all resources tracked in state",
        "terraform state mv":   "Move/rename a resource in state",
        "terraform state rm":   "Remove a resource from state (without destroying it)",
        "terraform import":     "Import existing resource into state",
        "terraform taint":      "Mark a resource for recreation on next apply (deprecated → use -replace)",
        "terraform untaint":    "Unmark a tainted resource (deprecated)",
        "terraform refresh":    "Sync state with actual infrastructure (deprecated → use -refresh-only)",
        "terraform get":        "Download modules",
        "terraform console":    "Evaluate expressions interactively",
        "terraform graph":      "Output resource dependency graph (DOT format)",
        "terraform force-unlock": "Release a stuck state lock",
        "terraform workspace":  "Manage CLI workspaces (list / new / select / delete / show)"
    },

    # ─────────────────────────────────────────────────────────────────────────
    # EXAM META-INFO
    # ─────────────────────────────────────────────────────────────────────────
    "exam_info": {
        "certification": "HashiCorp Certified: Terraform Associate (004)",
        "exam_code": "TA-004",
        "terraform_version_tested": "Terraform 1.12",
        "total_questions_in_course": "~350 questions across 6 practice exams",
        "question_types": ["Multiple Choice", "Multi-Select", "True/False", "Scenario-based"],
        "domains": [
            "IaC Concepts",
            "Terraform Fundamentals & Providers",
            "Terraform Workflow (CLI)",
            "Configuration Language (HCL)",
            "Modules",
            "State Management",
            "Import & Moved/Removed Blocks",
            "HCP Terraform"
        ],
        "course_author": "Bryan Krausen (HashiCorp Ambassador, Authorized Terraform Trainer)",
        "passing_tips": [
            "Understand WHY each answer is correct, not just memorization",
            "Pay special attention to HCP Terraform – it is heavily tested in TA-004",
            "Know the difference between local and remote backends",
            "Understand the dependency lock file and provider versioning",
            "Study Terraform 1.12 features: ephemeral values, write-only attributes, checks",
            "Know moved, removed, and import blocks (declarative import)",
            "Practice scenario-based questions – they require contextual understanding"
        ]
    }
}


# ─────────────────────────────────────────────────────────────────────────────
# PRETTY PRINT SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
    print(json.dumps(terraform_exam, indent=2, ensure_ascii=False))
