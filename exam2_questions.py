"""
HashiCorp Certified Terraform Associate (TA-004)
Exam #2 - All Questions with Correct Answers & Explanations
Source: Udemy - Bryan Krausen
"""

exam2 = {

    "exam_title": "Terraform Associate 004 - Exam #2",
    "total_questions": 57,

    "questions": {

        1: {
            "question": "A root module includes several variables in terraform.tfvars. You add a child module as shown below. What values can the child module access by default?\n\nmodule \"web\" {\n  source = \"./modules/web\"\n}",
            "type": "multiple_choice",
            "correct_answer": "Only values passed to it via the module block since root variables are not automatically accessible inside the module.",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5b - Describe variable scope within modules",
            "result": "correct",
            "explanation": "Child modules have no implicit access to the parent's variables, locals, or outputs. Pass inputs explicitly in the module block; outputs flow upward from child to parent, not the other way.",
            "all_options": {
                "A": "Only values passed to it via the module block since root variables are not automatically accessible inside the module.",
                "B": "Only values that are defined as outputs in the root module since outputs are always available to children in the same run.",
                "C": "Any root variables, as long as they are defined by a locals block, since locals are global across the configuration.",
                "D": "All of the root variables from terraform.tfvars since children inherit parent variable values automatically."
            },
            "key_takeaway": "Child modules NEVER inherit parent variables automatically. Values must be explicitly passed via the module block."
        },

        2: {
            "question": "You discovered a module on the Terraform Registry that will provision the resources you need. What other information can you find on the Terraform Registry to help you quickly use this module? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "dependencies to use the module",
                "a list of outputs",
                "required input variables"
            ],
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5a - Explain how Terraform sources modules",
            "result": "correct",
            "explanation": "The Terraform Registry provides: required inputs, list of outputs, and dependencies. A download button is not a key piece of information for using the module.",
            "all_options": {
                "A": "dependencies to use the module",
                "B": "a list of outputs",
                "C": "a download button to quickly get the module code",
                "D": "required input variables"
            },
            "key_takeaway": "Registry module pages show: inputs, outputs, dependencies, README, and submodules."
        },

        3: {
            "question": "Your team has multiple infrastructure projects with different compliance requirements. Some projects require advisory policy checks while others need mandatory enforcement. How should you configure policies in HCP Terraform to meet these varying requirements?",
            "type": "multiple_choice",
            "correct_answer": "Configure different enforcement levels for each policy set and apply them to the appropriate workspaces or projects.",
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8b - Describe HCP Terraform collaboration and governance features",
            "result": "correct",
            "explanation": "HCP Terraform supports Advisory (warnings only), Soft Mandatory (override allowed), and Hard Mandatory (blocks run) enforcement levels. Apply different policy sets with appropriate levels to different workspaces/projects.",
            "all_options": {
                "A": "Create separate HCP Terraform organizations for each compliance level.",
                "B": "Configure different enforcement levels for each policy set and apply them to the appropriate workspaces or projects.",
                "C": "Use run triggers to enforce policies based on workspace names.",
                "D": "Enable policies at the organizational level, then disable enforcement in workspaces that do not require it."
            },
            "key_takeaway": "HCP Terraform policy enforcement levels: Advisory, Soft Mandatory, Hard Mandatory. Apply per policy set."
        },

        4: {
            "question": "True or False? Terraform can only manage dependencies between resources if the depends_on argument is explicitly set for the dependent resources.",
            "type": "true_false",
            "correct_answer": "False",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4f - Define resource dependencies in configuration",
            "result": "correct",
            "explanation": "Terraform automatically detects implicit dependencies based on resource references (interpolation). depends_on is only needed for hidden dependencies not expressed through references.",
            "key_takeaway": "Terraform builds a resource graph automatically. depends_on is only for non-obvious dependencies."
        },

        5: {
            "question": "You have created a brand-new Terraform repo that has no backend block. After successfully running your first terraform apply, where does Terraform store state by default?",
            "type": "multiple_choice",
            "correct_answer": "in the current working directory in a file named terraform.tfstate",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6a - Describe the local backend",
            "result": "correct",
            "explanation": "With no backend configured, Terraform uses the local backend, which writes terraform.tfstate to the current working directory.",
            "all_options": {
                "A": "in the current working directory in a file named terraform.tfstate",
                "B": "in the directory $HOME/.terraform/state/ in a file named terraform.tfstate",
                "C": "in a temporary OS directory with a randomly created filename",
                "D": "in an S3 bucket found under the module path"
            },
            "key_takeaway": "Default backend = local. State file = ./terraform.tfstate in current working directory."
        },

        6: {
            "question": "Your team has been using Terraform to manage infrastructure. A colleague manually created a database in the console for urgent troubleshooting. The database is now needed permanently. What is the primary reason to use Terraform import in this situation?",
            "type": "multiple_choice",
            "correct_answer": "To bring the database under Terraform management so future changes can be tracked and managed through your IaC workflow.",
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7a - Import existing infrastructure into your Terraform workspace",
            "result": "correct",
            "explanation": "terraform import brings existing resources into state so you can manage them through IaC. It doesn't optimize, backup, or validate compliance.",
            "all_options": {
                "A": "To automatically generate optimized Terraform code that improves the database's performance settings.",
                "B": "To validate that the manually created database meets your organization's security compliance requirements.",
                "C": "To bring the database under Terraform management so future changes can be tracked and managed through your IaC workflow.",
                "D": "To create a backup of the database configuration."
            },
            "key_takeaway": "terraform import's ONLY purpose: bring existing infrastructure into Terraform state management."
        },

        7: {
            "question": "Which of the following best describes a Terraform provider?",
            "type": "multiple_choice",
            "correct_answer": "a plugin that Terraform uses to translate the API interactions with the service or provider",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2b - Describe how Terraform uses providers",
            "result": "correct",
            "explanation": "A provider is a plugin that enables Terraform to interact with a specific cloud or service. It translates Terraform config into API calls to create/read/update/delete resources.",
            "all_options": {
                "A": "describes an infrastructure object, such as a virtual network or compute instance",
                "B": "serves as a parameter for a Terraform module",
                "C": "a container for multiple resources that are used together",
                "D": "a plugin that Terraform uses to translate the API interactions with the service or provider"
            },
            "key_takeaway": "Provider = plugin that translates HCL config into API calls for a specific cloud/service."
        },

        8: {
            "question": "In the top-level terraform block, which setting specifies a provider's source and version constraints?",
            "type": "multiple_choice",
            "correct_answer": "required_providers",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2a - Install and version Terraform providers",
            "result": "correct",
            "explanation": "The required_providers block inside terraform {} declares provider sources and version constraints. Example: aws = { source = 'hashicorp/aws', version = '6.5.0' }",
            "all_options": {
                "A": "required_providers",
                "B": "provider",
                "C": "backend",
                "D": "required_version"
            },
            "key_takeaway": "terraform { required_providers { aws = { source = '...', version = '...' } } }"
        },

        9: {
            "question": "You have an existing GCS bucket and add an import block with a resource block. What is the correct next step?\n\nimport {\n  to = google_storage_bucket.data_lake\n  id = \"bk-existing-bucket\"\n}\nresource \"google_storage_bucket\" \"data_lake\" { ... }",
            "type": "multiple_choice",
            "correct_answer": "run terraform plan followed by terraform apply to import the resource",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3e - Apply changes to infrastructure with Terraform",
            "result": "correct",
            "explanation": "With config-driven import blocks (Terraform 1.5+), you use the standard plan/apply workflow. terraform plan shows the import intent, terraform apply performs it. Do NOT use the imperative terraform import command when using import blocks.",
            "all_options": {
                "A": "run terraform import google_storage_bucket.data_lake bk-existing-bucket",
                "B": "run terraform init followed by terraform import",
                "C": "run terraform apply -import-only to import without other changes",
                "D": "run terraform plan followed by terraform apply to import the resource"
            },
            "key_takeaway": "Import blocks (1.5+) use plan/apply. The old terraform import command is separate/imperative."
        },

        10: {
            "question": "In the snippet below, where does the value for vpc_security_group_ids come from?\n\nvpc_security_group_ids = [module.vpc.default_security_group_id]",
            "type": "multiple_choice",
            "correct_answer": "the output of another module",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5c - Use modules in configuration",
            "result": "correct",
            "explanation": "module.vpc.default_security_group_id references the default_security_group_id output from the vpc module. This is how modules share values with each other.",
            "all_options": {
                "A": "the output of another module",
                "B": "the Terraform public registry",
                "C": "an environment variable being used during a terraform apply",
                "D": "from a variable likely declared in a .tfvars file"
            },
            "key_takeaway": "Syntax module.<name>.<output> references an output value from a child module."
        },

        11: {
            "question": "Your organization wants to ensure that third-party security scanning tools can review Terraform plans before any infrastructure changes are applied. Which HCP Terraform feature allows you to integrate external tools into the workflow between the plan and apply phases?",
            "type": "multiple_choice",
            "correct_answer": "run tasks",
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8b - Describe HCP Terraform collaboration and governance features",
            "result": "correct",
            "explanation": "Run tasks integrate external tools between plan and apply phases. They can call external APIs and be configured as advisory or mandatory. Different from run triggers (which start runs in other workspaces).",
            "all_options": {
                "A": "run triggers",
                "B": "run tasks",
                "C": "change requests",
                "D": "health checks"
            },
            "key_takeaway": "Run tasks = integrating external tools (security scan, cost estimate) between plan and apply."
        },

        12: {
            "question": "Before a new Terraform provider can be used in a configuration, what steps are required? (select two)",
            "type": "multi_select",
            "correct_answer": [
                "Declare and configure the provider in the configuration with the required arguments.",
                "Initialize the working directory using terraform init to download and install the provider."
            ],
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2a - Install and version Terraform providers",
            "result": "correct",
            "explanation": "Two required steps: (1) declare/configure the provider in your .tf files, (2) run terraform init to download the provider plugin.",
            "all_options": {
                "A": "Run terraform validate to compile and fetch the plugin.",
                "B": "Declare and configure the provider in the configuration with the required arguments.",
                "C": "Add the provider name and configuration to terraform.tfvars.",
                "D": "Initialize the working directory using terraform init."
            },
            "key_takeaway": "New provider: declare in config → terraform init downloads it."
        },

        13: {
            "question": "True or False? Marking an output as sensitive does not prevent its value from being stored in the Terraform state file.",
            "type": "true_false",
            "correct_answer": "True",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4h - Understand best practices for managing sensitive data",
            "result": "correct",
            "explanation": "sensitive = true only redacts the value from CLI output and logs. The value IS still stored in plain text in the state file. Protect state access separately.",
            "key_takeaway": "sensitive=true hides from CLI/UI output ONLY. State file still stores the value in plain text."
        },

        14: {
            "question": "Which of the following is considered a Terraform plugin?",
            "type": "multiple_choice",
            "correct_answer": "provider",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2b - Describe how Terraform uses providers",
            "result": "correct",
            "explanation": "In Terraform, a plugin is a binary executable that implements a specific provider. Providers are loaded as plugins. Backends, modules, and variables are not plugins.",
            "all_options": {
                "A": "provider",
                "B": "backend",
                "C": "module",
                "D": "variable"
            },
            "key_takeaway": "Provider = Terraform plugin (Go binary that implements provider protocol)."
        },

        15: {
            "question": "You have a SQL Database in production. Changing the pricing tier requires destroying and recreating it. You want to ensure the new database is created before the old one is destroyed. What should you add?",
            "type": "multiple_choice",
            "correct_answer": "add a lifecycle block with create_before_destroy = true",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4f - Define resource dependencies in configuration",
            "result": "correct",
            "explanation": "lifecycle { create_before_destroy = true } changes Terraform's default destroy-then-create behavior. The new resource is created first, then the old one is destroyed, minimizing downtime.",
            "all_options": {
                "A": "add a depends_on argument pointing to the new database",
                "B": "add a count argument set to 2",
                "C": "add a lifecycle block with prevent_destroy = true",
                "D": "add a lifecycle block with create_before_destroy = true"
            },
            "key_takeaway": "create_before_destroy = true → new resource first, then destroy old one."
        },

        16: {
            "question": "Which of the following Terraform files should be ignored by Git when committing code to a repo?",
            "type": "multiple_choice",
            "correct_answer": "terraform.tfstate",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6a - Describe the local backend",
            "result": "correct",
            "explanation": "terraform.tfstate contains sensitive data and should NOT be in version control. The .terraform.lock.hcl SHOULD be committed. .tf config files should be committed.",
            "all_options": {
                "A": ".terraform.lock.hcl  → SHOULD be committed",
                "B": "terraform.tfstate  → SHOULD be ignored (correct answer)",
                "C": "outputs.tf  → SHOULD be committed",
                "D": "terraform.tf  → SHOULD be committed"
            },
            "key_takeaway": "Add terraform.tfstate and terraform.tfstate.backup to .gitignore. Commit .terraform.lock.hcl."
        },

        17: {
            "question": "After executing a terraform plan in your working directory, you notice that a resource has a tilde (~) next to it. What does this indicate?",
            "type": "multiple_choice",
            "correct_answer": "the resource will be updated in place",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3d - Generate and review an execution plan for Terraform",
            "result": "correct",
            "explanation": "Plan output symbols: + = create, - = destroy, ~ = update in place, -/+ = destroy and recreate.",
            "all_options": {
                "A": "the resource will be created (+)",
                "B": "the resource will be destroyed and recreated (-/+)",
                "C": "the resource will be updated in place (~)",
                "D": "Terraform can't determine how to proceed"
            },
            "key_takeaway": "~ = update in place | + = create | - = destroy | -/+ = destroy+recreate | +/- = create+destroy"
        },

        18: {
            "question": "A module creates VMs with hard-coded values like datastore='DS1'. You need it to work in Lab, QA, and Prod without code changes. What is the most appropriate change?",
            "type": "multiple_choice",
            "correct_answer": "Convert the hard-coded values to input variables and provide environment-specific settings via tfvars or variable sets at plan/apply.",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4c - Use variables and outputs",
            "result": "correct",
            "explanation": "Input variables serve as parameters for a module, allowing customization without altering source code. Use .tfvars or HCP variable sets to provide environment-specific values.",
            "all_options": {
                "A": "Add preconditions that fail when the environment differs.",
                "B": "Put the values in locals and commit separate branches per environment.",
                "C": "Convert the hard-coded values to input variables and provide environment-specific settings via tfvars or variable sets.",
                "D": "Create outputs and reference them from a second override module."
            },
            "key_takeaway": "Replace hard-coded values with input variables → pass via .tfvars or HCP variable sets."
        },

        19: {
            "question": "Which of the following options correctly demonstrates the HCL syntax for assigning a value to a variable declared with the type map(string)?",
            "type": "multiple_choice",
            "correct_answer": 'default = {\n  "environment" = "production",\n  "owner"       = "dev-team"\n}',
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4d - Understand and use complex types",
            "result": "correct",
            "explanation": "map(string) uses curly braces with string key=string value pairs. All values must be strings. Using boolean (true) is invalid for map(string).",
            "all_options": {
                "A": 'default = {\n  "environment" = "production",\n  "owner"       = "dev-team"\n}',
                "B": 'default = ["environment=production", "owner=dev-team"]',
                "C": 'default = {\n  environment = true\n  owner       = "dev-team"\n}',
                "D": 'default = (environment = "production", owner = "dev-team")'
            },
            "key_takeaway": "map(string): { \"key\" = \"value\" } — all values must be strings, not booleans or numbers."
        },

        20: {
            "question": "You want to keep sensitive backend values (bucket, region) out of version control while keeping other backend config in code. Which approach correctly implements partial backend configuration?",
            "type": "multiple_choice",
            "correct_answer": "define the backend block with only the type, then pass the bucket and region values using -backend-config flag during terraform init",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6c - Configure remote state using the backend block",
            "result": "correct",
            "explanation": "Partial backend config: define backend type in code, supply sensitive values at init time:\nterraform init -backend-config='bucket=my-bucket' -backend-config='region=us-west-2'",
            "all_options": {
                "A": "define the backend block with only the type, then pass values using -backend-config during init",
                "B": "store all backend config in terraform.tfvars and add to .gitignore",
                "C": "create a separate backends.tf file with sensitive values and add to .gitignore",
                "D": "create environment variables TF_BACKEND_BUCKET and TF_BACKEND_REGION"
            },
            "key_takeaway": "Partial backend: empty backend block in code + terraform init -backend-config='key=value'"
        },

        21: {
            "question": "You're moving a project to a remote S3 backend. How do you correctly configure and initialize the backend?",
            "type": "multiple_choice",
            "correct_answer": "Define the S3 backend in the terraform block using a backend block - run terraform init to migrate your local state.",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6c - Configure remote state using the backend block",
            "result": "correct",
            "explanation": "Add backend block to terraform {} block, then run terraform init. Terraform will prompt to migrate existing local state to the new backend.",
            "all_options": {
                "A": "Define the S3 backend in the terraform block and run terraform init to migrate.",
                "B": "Set TF_INPUT and TF_DATA_DIR environment variables and run terraform init.",
                "C": "Put the backend block inside a module and run terraform plan.",
                "D": "Create the S3 bucket using resource blocks and run terraform apply."
            },
            "key_takeaway": "To switch backends: update backend block → terraform init (offers state migration)."
        },

        22: {
            "question": "What are the advantages of using Infrastructure as Code? (select five)",
            "type": "multi_select",
            "correct_answer": [
                "Ability to recreate infrastructure for disaster recovery",
                "Provides configuration consistency and standardization",
                "Easily repeatable - reuse code to deploy similar resources",
                "Enables users to automate manual tasks",
                "Relatively easy to learn and write"
            ],
            "domain": "Objective 1 - Infrastructure as Code (IaC) with Terraform",
            "objective": "1b - Describe the advantages of IaC patterns",
            "result": "correct",
            "explanation": "IaC benefits: consistency, repeatability, automation, version control, collaboration, disaster recovery, and cost savings. IaC does NOT replace development languages like Go or .Net.",
            "all_options": {
                "A": "Ability to recreate infrastructure for disaster recovery",
                "B": "Provides configuration consistency and standardization",
                "C": "Easily repeatable - reuse code to deploy similar resources",
                "D": "Enables users to automate manual tasks",
                "E": "Replaces the need for development languages like Go or .Net",
                "F": "Relatively easy to learn and write",
                "G": "Automatically fixes security vulnerabilities in deployed resources"
            },
            "key_takeaway": "IaC core advantages: consistency, repeatability, automation, version control, disaster recovery."
        },

        23: {
            "question": "Which of the following actions are performed during a terraform init? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "initializes the backend configuration",
                "downloads the providers/plugins required to execute the configuration",
                "downloads the required modules referenced in the configuration"
            ],
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3b - Initialize a Terraform working directory",
            "result": "correct",
            "explanation": "terraform init: initializes backend, downloads providers/plugins, downloads modules. It does NOT provision resources (that's apply).",
            "all_options": {
                "A": "initializes the backend configuration ✓",
                "B": "provisions the declared resources ✗ (that's apply)",
                "C": "downloads the providers/plugins ✓",
                "D": "downloads the required modules ✓"
            },
            "key_takeaway": "terraform init = backend init + provider download + module download. NOT resource provisioning."
        },

        24: {
            "question": "In an expression, how do you correctly reference the build-tag value from:\nvariable \"metadata\" {\n  type = map(string)\n  default = { owner = \"platform\", build-tag = \"v5.0.2\", service = \"billing\" }\n}",
            "type": "multiple_choice",
            "correct_answer": 'var.metadata["build-tag"]',
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4d - Understand and use complex types",
            "result": "incorrect",
            "user_answer": "var.metadata.build-tag",
            "explanation": "Keys with hyphens (-) cannot be accessed with dot notation because hyphen is not valid in identifiers. Use bracket notation: var.metadata[\"build-tag\"]. Dot notation (var.metadata.build-tag) is invalid for hyphenated keys.",
            "all_options": {
                "A": 'var["metadata"]["build-tag"]  → WRONG syntax',
                "B": 'var.metadata["build-tag"]  → CORRECT',
                "C": 'lookup(var.metadata, build-tag, "")  → WRONG (missing quotes)',
                "D": "var.metadata.build-tag  → WRONG (hyphen invalid in dot notation)"
            },
            "key_takeaway": "Keys with hyphens MUST use bracket notation: var.map_name[\"key-with-hyphen\"]"
        },

        25: {
            "question": "You suspect the provider is interpreting your configuration differently than expected during apply. What is the primary benefit of enabling Terraform logging?",
            "type": "multiple_choice",
            "correct_answer": "Logging will show you the detailed interactions between Terraform and the provider API and help you identify where the unexpected behavior occurs",
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7c - Describe when and how to use verbose logging",
            "result": "correct",
            "explanation": "TF_LOG environment variable enables verbose logging showing API calls, provider interactions, and decision-making. It does NOT fix errors, create backups, or validate syntax.",
            "all_options": {
                "A": "Logging will show you the detailed interactions between Terraform and the provider API and help you identify where the unexpected behavior occurs",
                "B": "Logging automatically fixes provider errors and retries failed API calls",
                "C": "Logging creates a backup of the state file before each operation",
                "D": "Logging validates the HCL syntax of your configuration files"
            },
            "key_takeaway": "TF_LOG=DEBUG|TRACE|INFO|WARN|ERROR — shows provider API interactions for troubleshooting."
        },

        26: {
            "question": "You are reviewing:\nmodule \"servers\" {\n  source = \"./modules/btk-cluster\"\n  servers = 5\n}\nWhich statements about this configuration are correct? (select two)",
            "type": "multi_select",
            "correct_answer": [
                "btk-cluster refers to a local child module on disk",
                "main.tf is the root (calling) module"
            ],
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5a - Explain how Terraform sources modules",
            "result": "correct",
            "explanation": "source = './modules/btk-cluster' is a local path (not registry). The file containing the module block is the root/calling module. Terraform does NOT download local modules from the registry.",
            "all_options": {
                "A": "the argument servers must be declared as an output in the child module ✗",
                "B": "btk-cluster refers to a local child module on disk ✓",
                "C": "main.tf is the root (calling) module ✓",
                "D": "Terraform will download btk-cluster from the public registry ✗"
            },
            "key_takeaway": "./path means local module. hashicorp/name/provider means registry module."
        },

        27: {
            "question": "Rahul deployed multiple VMs outside Terraform. You need to identify which VM is Terraform-managed without making changes. What approach is best?",
            "type": "multiple_choice",
            "correct_answer": "Use Terraform state commands terraform state show to match the tracked VM's ID with the list of active VMs.",
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7b - Use the CLI to inspect state",
            "result": "correct",
            "explanation": "terraform state list shows all tracked resources, terraform state show <resource> shows details including the VM ID. Cross-reference with cloud provider VMs to find the managed one.",
            "all_options": {
                "A": "Use the provider's CLI to label all VMs.",
                "B": "Delete every VM that isn't clearly documented.",
                "C": "Update Terraform config to reference each VM ID and run terraform plan.",
                "D": "Use terraform state show to match tracked VM ID with active VMs."
            },
            "key_takeaway": "terraform state list + terraform state show → inspect state without infrastructure changes."
        },

        28: {
            "question": "Before running the terraform import command (legacy), what must you do first?",
            "type": "multiple_choice",
            "correct_answer": "update the Terraform configuration file to include new resource blocks that match the resources you want to import",
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7a - Import existing infrastructure into your Terraform workspace",
            "result": "incorrect",
            "user_answer": "add import blocks to the configuration to indicate what resources you want to bring under Terraform management",
            "explanation": "For the legacy terraform import CLI command, you must first manually write resource configuration blocks. Import blocks are for the NEW config-driven approach (Terraform 1.5+) — you use EITHER import blocks OR the terraform import command, not both.",
            "all_options": {
                "A": "modify the Terraform state file manually ✗",
                "B": "update the Terraform configuration to include new resource blocks ✓ (CORRECT for terraform import command)",
                "C": "add import blocks to the configuration ✗ (that's a different approach)",
                "D": "run terraform apply -refresh-only ✗"
            },
            "key_takeaway": "terraform import (legacy): write resource block first, THEN run terraform import. Import blocks (new): declare import block + run plan/apply."
        },

        29: {
            "question": "What is preventing you from producing a plan based on the error:\n'Error: Invalid value for variable - You must specify a value for cluster_endpoint if create_cluster is false.'",
            "type": "multiple_choice",
            "correct_answer": "A validation block on cluster_endpoint requires a non-empty value when create_cluster=false, so input evaluation failed and Terraform cannot produce a plan.",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4g - Validate configuration using custom conditions",
            "result": "incorrect",
            "user_answer": "A precondition on a resource referencing cluster_endpoint failed after the plan is computed.",
            "explanation": "Variable validation blocks check inputs BEFORE the plan is generated. A postcondition or precondition on a resource checks AFTER/DURING plan. This error is a validation block failure at input evaluation time.",
            "all_options": {
                "A": "A validation block on cluster_endpoint requires a non-empty value when create_cluster=false, so input evaluation failed and Terraform cannot produce a plan.",
                "B": "A precondition on a resource referencing cluster_endpoint failed after the plan is computed.",
                "C": "A postcondition on the cluster resource detected a missing endpoint after apply completed.",
                "D": "The provider API rejected the request because cluster_endpoint was null."
            },
            "key_takeaway": "Variable validation blocks run BEFORE plan generation. Preconditions run DURING plan. Postconditions run AFTER apply."
        },

        30: {
            "question": "You have a root module that calls modules/web. In the child, a developer used name = \"${var.env}-app\". What is the correct way to make this work?",
            "type": "multiple_choice",
            "correct_answer": 'Declare variable "env" {} in the child module and pass it from root using env = var.env',
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5b - Describe variable scope within modules",
            "result": "correct",
            "explanation": "The child module must declare the variable. The root must pass it explicitly in the module block. No implicit inheritance, no parent references, no automatic locals.",
            "all_options": {
                "A": "Use the terraform workspace command in the child module",
                "B": "Reference parent directly: name = \"${parent.var.env}-app\"",
                "C": "Define locals { env = var.env } in root since child modules inherit locals automatically",
                "D": 'Declare variable "env" {} in child and pass from root using env = var.env'
            },
            "key_takeaway": "Module variables: declare in child + pass from parent. No implicit scope crossing."
        },

        31: {
            "question": "Bryan wants to verify that configuration is syntactically valid and internally consistent without contacting any remote services. Which command should he run?",
            "type": "multiple_choice",
            "correct_answer": "terraform validate",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3c - Validate a Terraform configuration",
            "result": "correct",
            "explanation": "terraform validate checks syntax and internal consistency without accessing remote services (no API calls, no state). Faster than plan for quick syntax verification.",
            "all_options": {
                "A": "terraform apply -refresh-only",
                "B": "terraform fmt",
                "C": "terraform show",
                "D": "terraform validate"
            },
            "key_takeaway": "terraform validate = syntax + consistency check, NO remote calls, NO state access."
        },

        32: {
            "question": "You're setting up CI/CD and need a command that checks Terraform file formatting without making any changes.",
            "type": "multiple_choice",
            "correct_answer": "terraform fmt -check",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3g - Apply formatting and style adjustments to a configuration",
            "result": "correct",
            "explanation": "terraform fmt -check validates formatting without modifying files. Returns non-zero exit code if files are not properly formatted, which causes CI/CD pipelines to fail.",
            "all_options": {
                "A": "terraform validate -format  → not a valid command",
                "B": "terraform fmt -diff  → shows diff but still checks format",
                "C": "terraform fmt -validate  → not a valid command",
                "D": "terraform fmt -check  → checks without changing"
            },
            "key_takeaway": "terraform fmt -check → use in CI/CD to enforce formatting without changing files."
        },

        33: {
            "question": "You run terraform plan and it shows 3 updates, 2 creates, 1 destroy. How does Terraform determine what changes need to be made?",
            "type": "multiple_choice",
            "correct_answer": "Terraform compares the desired state in the configuration with the current state in the state file to build the plan",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2d - Explain how Terraform uses and manages state",
            "result": "correct",
            "explanation": "terraform plan: refreshes state from real infrastructure, then compares config (desired) vs state (current) to calculate proposed actions.",
            "all_options": {
                "A": "Terraform uses cloud provider services to identify drift.",
                "B": "Terraform reads the previous plan output file.",
                "C": "Terraform compares desired state (config) with current state (state file).",
                "D": "Terraform queries cloud provider APIs to discover all resources."
            },
            "key_takeaway": "Plan = config (desired) vs state file (current) comparison. Only refreshes resources already in state."
        },

        34: {
            "question": "Why should a user specify provider version constraints in their Terraform configuration?",
            "type": "multiple_choice",
            "correct_answer": "providers are released on a separate schedule from Terraform itself; therefore, a newer version could introduce breaking changes",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2a - Install and version Terraform providers",
            "result": "correct",
            "explanation": "Providers are developed independently of Terraform. Version constraints ensure reproducibility, predictability, and compatibility. Prevents unexpected breaking changes from auto-upgrades.",
            "all_options": {
                "A": "providers are released on a separate schedule from Terraform itself; therefore, a newer version could introduce breaking changes",
                "B": "Terraform requires exact provider versions to be specified or it will refuse to initialize",
                "C": "version constraints allow Terraform to automatically download the latest provider on every run",
                "D": "provider version constraints are only needed when using multiple providers in one configuration"
            },
            "key_takeaway": "Pin provider versions for: reproducibility, predictability, compatibility, version locking."
        },

        35: {
            "question": "What benefits would you see by using a multi-cloud and provider-agnostic tool like Terraform? (select two)",
            "type": "multi_select",
            "correct_answer": [
                "Delivers a consistent declarative workflow and language across providers and hypervisors.",
                "Reduces operational overhead by allowing teams to learn and govern a single tool across all environments."
            ],
            "domain": "Objective 1 - Infrastructure as Code (IaC) with Terraform",
            "objective": "1c - Explain how Terraform manages multi-cloud, hybrid cloud, and service-agnostic workflows",
            "result": "incorrect",
            "user_answer": [
                "Delivers a consistent declarative workflow and language across providers and hypervisors.",
                "Reduces operational overhead by allowing teams to learn and govern a single tool."
            ],
            "explanation": "Terraform benefits: consistent workflow across providers + single tool for all environments. Terraform does NOT standardize pricing, does NOT remove need for credentials.",
            "all_options": {
                "A": "Delivers a consistent declarative workflow and language across providers and hypervisors.",
                "B": "Standardizes cloud provider pricing by negotiating contracts automatically.",
                "C": "Reduces operational overhead by allowing teams to learn and govern a single tool across all environments.",
                "D": "Eliminates the need to configure credentials for each cloud provider."
            },
            "key_takeaway": "Multi-cloud Terraform benefits: unified workflow + single tool governance. Credentials still needed per provider."
        },

        36: {
            "question": "Your team uses Vault and stores Terraform state in a remote backend. Which statements reflect best practices for managing sensitive data and state? (select four)",
            "type": "multi_select",
            "correct_answer": [
                "A properly configured remote backend improves security via encryption and access controls.",
                "When using local state, the state file is stored in plain text by default",
                "Terraform state can include sensitive data, so it is essential to restrict access to the state and audit any changes.",
                "HCP Terraform encrypts state at rest (and in transit) and provides RBAC to restrict who can access state"
            ],
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4h - Understand best practices for managing sensitive data",
            "result": "incorrect",
            "user_answer_wrong": "Using Vault ensures that secrets never appear in state, so additional controls on state aren't required.",
            "explanation": "WRONG: sensitive=true does NOT prevent storage in state. WRONG: Vault doesn't eliminate the need for state controls — state can still contain sensitive attributes.",
            "all_options": {
                "A": "A properly configured remote backend improves security via encryption and access controls.",
                "B": "When using local state, the state file is stored in plain text by default",
                "C": "Using Vault ensures that secrets never appear in state, so additional controls on state aren't required.",
                "D": "Terraform state can include sensitive data, so it is essential to restrict access to the state and audit any changes.",
                "E": "Marking a variable as sensitive=true prevents it from ever being written to the state file.",
                "F": "HCP Terraform encrypts state at rest (and in transit) and provides RBAC to restrict who can access state"
            },
            "key_takeaway": "Local state = plain text. Remote backends = encryption + access controls. Vault ≠ state protection by itself."
        },

        37: {
            "question": "You're refactoring a large Terraform configuration. Before running terraform plan, what's the fastest way to verify you didn't introduce syntax errors?",
            "type": "multiple_choice",
            "correct_answer": "run terraform validate",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3c - Validate a Terraform configuration",
            "result": "correct",
            "explanation": "terraform validate is faster than terraform plan because it doesn't communicate with cloud providers or check state. Perfect for quick syntax verification after refactoring.",
            "all_options": {
                "A": "run terraform validate",
                "B": "run terraform plan -refresh=false",
                "C": "run terraform fmt -check",
                "D": "run terraform init -upgrade"
            },
            "key_takeaway": "After refactoring: terraform validate first (fast), then terraform plan (full check)."
        },

        38: {
            "question": "What happens when a terraform apply command is executed?",
            "type": "multiple_choice",
            "correct_answer": "applies the changes required in the target infrastructure in order to reach the desired configuration",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3e - Apply changes to infrastructure with Terraform",
            "result": "correct",
            "explanation": "terraform apply executes the changes to make real infrastructure match the desired state in config. It creates/updates/destroys resources as needed.",
            "all_options": {
                "A": "creates the execution plan (that's terraform plan)",
                "B": "initializes the backend (that's terraform init)",
                "C": "reconciles the state (partial — apply does this but it's not the primary description)",
                "D": "applies the changes required to reach the desired configuration ✓"
            },
            "key_takeaway": "terraform apply = make real infrastructure match desired config. Creates, updates, destroys resources."
        },

        39: {
            "question": "You want to see a complete list of all resources currently tracked in your Terraform state file, but don't need the detailed attributes. Which command?",
            "type": "multiple_choice",
            "correct_answer": "terraform state list",
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7b - Use the CLI to inspect state",
            "result": "incorrect",
            "user_answer": "terraform state show",
            "explanation": "terraform state list = lists all resource addresses (no attributes). terraform state show <address> = shows all attributes of ONE specific resource.",
            "all_options": {
                "A": "terraform output  → outputs only",
                "B": "terraform state show  → details of ONE resource",
                "C": "terraform state list  → list all resources (CORRECT)",
                "D": "terraform show  → full state details"
            },
            "key_takeaway": "terraform state list = all resources (no details). terraform state show = one resource (all details)."
        },

        40: {
            "question": "You have a module pinned to version 5.2.0. A new 5.3.0 is available. What steps are required to update safely? (select two)",
            "type": "multi_select",
            "correct_answer": [
                'update the version argument to allow 5.3.0 using version = "~> 5.3.0"',
                "run terraform init -upgrade to download the new module version"
            ],
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5d - Manage module versions",
            "result": "correct",
            "explanation": '~> 5.3.0 allows >= 5.3.0, < 5.4.0. Then terraform init -upgrade downloads the new version. Note: ~> 5.2.0 would NOT allow 5.3.0 (it allows >= 5.2.0, < 5.3.0).',
            "all_options": {
                "A": 'update the version argument to allow 5.3.0 using version = "~> 5.3.0"',
                "B": "run terraform apply -upgrade to download and apply the new module version",
                "C": "run terraform init -upgrade to download the new module version",
                "D": "delete the .terraform directory and run terraform init to force a fresh download"
            },
            "key_takeaway": "Version upgrade: update version constraint + terraform init -upgrade. ~> X.Y.0 locks to X.Y.Z patch range."
        },

        41: {
            "question": "In HCP Terraform, how many VCS repositories can a workspace be mapped to?",
            "type": "multiple_choice",
            "correct_answer": "1",
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8a - Use HCP Terraform to create infrastructure",
            "result": "incorrect",
            "user_answer": "5",
            "explanation": "A workspace can be mapped to only ONE VCS repository. Multiple workspaces can share the same repo, but one workspace = one repo.",
            "all_options": {
                "A": "1",
                "B": "2",
                "C": "5",
                "D": "Unlimited"
            },
            "key_takeaway": "HCP Terraform: 1 workspace = max 1 VCS repo. Multiple workspaces CAN use the same repo."
        },

        42: {
            "question": "Which Terraform command will force a resource to be destroyed and recreated even if there are no configuration changes?",
            "type": "multiple_choice",
            "correct_answer": "terraform apply -replace=<address>",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3f - Destroy Terraform-managed infrastructure",
            "result": "correct",
            "explanation": "terraform apply -replace=<address> forces a resource to be replaced (destroyed + recreated) regardless of config changes. Replaces the deprecated terraform taint command.",
            "all_options": {
                "A": "terraform destroy  → destroys ALL resources",
                "B": "terraform apply -replace=<address>  → CORRECT",
                "C": "terraform apply -refresh-only  → only updates state",
                "D": "terraform fmt  → formatting only"
            },
            "key_takeaway": "terraform apply -replace=<address> replaces deprecated terraform taint for forcing resource recreation."
        },

        43: {
            "question": "You're deploying a GCP Compute Engine instance and want to verify it receives a public IP after creation. If it doesn't, Terraform should fail. Which mechanism?",
            "type": "multiple_choice",
            "correct_answer": "add a postcondition in the lifecycle block of the instance resource",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4g - Validate configuration using custom conditions",
            "result": "correct",
            "explanation": "Postconditions verify resource attributes AFTER creation/update. Preconditions check BEFORE. Variable validations check inputs. Check blocks are broader assertions.",
            "all_options": {
                "A": "add a precondition in the lifecycle block  → checks BEFORE creation",
                "B": "add a postcondition in the lifecycle block  → CORRECT (checks AFTER creation)",
                "C": "add a check block  → broader scope, not resource-specific failure",
                "D": "add a validation block to the instance resource  → not valid for resources"
            },
            "key_takeaway": "postcondition = verify resource after apply. precondition = verify before apply. validation = verify input variables."
        },

        44: {
            "question": "What are the three core steps that make up the Terraform workflow? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "Plan - Preview changes before applying.",
                "Write - Author infrastructure as code.",
                "Apply - Provision reproducible infrastructure."
            ],
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3a - Describe the Terraform workflow",
            "result": "correct",
            "explanation": "The core Terraform workflow is: Write → Plan → Apply. Destroy, Validate, and Import are not part of the three core steps.",
            "all_options": {
                "A": "Plan - Preview changes before applying.",
                "B": "Write - Author infrastructure as code.",
                "C": "Destroy - Remove all managed infrastructure.",
                "D": "Apply - Provision reproducible infrastructure.",
                "E": "Validate - Check configuration syntax before writing.",
                "F": "Import - Bring existing resources under management."
            },
            "key_takeaway": "Core Terraform workflow = Write → Plan → Apply. Simple and fundamental."
        },

        45: {
            "question": "What is the .terraform.lock.hcl file and when does Terraform create or modify it?",
            "type": "multiple_choice",
            "correct_answer": "The .terraform.lock.hcl file is a dependency lock file used by Terraform. It is created or updated every time you run terraform init.",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3b - Initialize a Terraform working directory",
            "result": "correct",
            "explanation": "The lock file records exact provider versions and hashes. Created/updated on terraform init. Should be committed to version control for reproducibility.",
            "all_options": {
                "A": "contains backend connection settings, updated on backend change ✗",
                "B": "state snapshot, updated on terraform apply ✗",
                "C": "dependency lock file, created/updated on terraform init ✓",
                "D": "concurrency lock, created on terraform plan ✗"
            },
            "key_takeaway": ".terraform.lock.hcl = dependency lock, created by terraform init, SHOULD be committed to git."
        },

        46: {
            "question": "You're comparing local state vs remote state backends. Which statements correctly describe the key differences? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "Remote backends provide centralized state access for team collaboration, while local state requires manual file sharing.",
                "Local state is simple to set up with no additional infrastructure required, while remote backends require configuration and maintenance.",
                "Remote backends typically provide encryption at rest and access controls, while local state security depends entirely on filesystem permissions."
            ],
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6b - Describe state locking",
            "result": "correct",
            "explanation": "Local state: simple, plain text, no sharing/locking. Remote state: centralized, encrypted, access controls, state locking, team collaboration.",
            "all_options": {
                "A": "Remote backends provide centralized state access for team collaboration, while local state requires manual file sharing.",
                "B": "Local state is simple to set up with no additional infrastructure required, while remote backends require configuration and maintenance.",
                "C": "Both local and remote backends support state locking out of the box.",
                "D": "Remote backends typically provide encryption at rest and access controls, while local state security depends entirely on filesystem permissions.",
                "E": "Local state automatically syncs to a remote backend when network is available."
            },
            "key_takeaway": "Local = simple but insecure, no locking. Remote = secure, encrypted, locking, team-ready."
        },

        47: {
            "question": "One of your application teams needs to share third-party credentials across multiple workspaces. What is the most appropriate way? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "Group the team's workspaces into a project",
                "Create a variable set that includes the third-party credentials",
                "Apply the variable set to the project"
            ],
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8c - Describe how to organize and use HCP Terraform workspaces and projects",
            "result": "correct",
            "explanation": "Best practice: group workspaces in a project, create a variable set with credentials, apply the variable set to the project. This gives all workspaces in the project access automatically.",
            "all_options": {
                "A": "Group the team's workspaces into a project",
                "B": "Hardcode the credentials directly in each workspace's Terraform configuration",
                "C": "Create a variable set that includes the third-party credentials",
                "D": "Apply the variable set to the project",
                "E": "Create a separate workspace to store credentials and reference it from other workspaces"
            },
            "key_takeaway": "HCP Terraform: Project → Variable Set → Apply to Project = shared credentials across workspaces."
        },

        48: {
            "question": "In HCP Terraform, what scope levels are available for providing variables to workspaces? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "Multiple workspaces with a variable set",
                "All current and future workspaces and Stacks within a project using a variable set.",
                "A single workspace by defining variables directly in that workspace."
            ],
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8c - Describe how to organize and use HCP Terraform workspaces and projects",
            "result": "skipped",
            "explanation": "Variable set scopes in HCP Terraform: (1) Global - all workspaces in org, (2) Project-specific - all workspaces in project, (3) Workspace-specific - single workspace. NOT across multiple organizations.",
            "all_options": {
                "A": "Multiple workspaces with a variable set",
                "B": "All current and future workspaces and Stacks within a project using a variable set.",
                "C": "Across multiple HCP Terraform organizations using a shared variable set.",
                "D": "A single workspace by defining variables directly in that workspace.",
                "E": "All workspaces in a specific geographic region."
            },
            "key_takeaway": "Variable set scopes: Global org / Project / Single workspace. NOT cross-organization."
        },

        49: {
            "question": "A network team manages Azure VNets. Your team needs to deploy VMs into prod-network VNet. What is the correct approach?",
            "type": "multiple_choice",
            "correct_answer": "use a data block to reference the existing VNet, then create your VM resources that use attributes from the data source",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4a - Use and differentiate resource and data blocks",
            "result": "correct",
            "explanation": "Data blocks read existing infrastructure managed by others without taking ownership. Resource blocks create/manage resources. Use data to reference, resource to own.",
            "all_options": {
                "A": "contact the network team to add a depends_on relationship ✗",
                "B": "use a resource block to import the existing VNet ✗",
                "C": "use a data block to reference the existing VNet ✓",
                "D": "create a new resource block for the VNet with the same name ✗"
            },
            "key_takeaway": "data block = read existing (no ownership). resource block = create and own. Use data to reference other teams' resources."
        },

        50: {
            "question": "You have var.common_tags (map) and local.resource_tags (map). How do you combine both to apply to a resource?",
            "type": "multiple_choice",
            "correct_answer": "merge(var.common_tags, local.resource_tags)",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4e - Write dynamic configuration using expressions and functions",
            "result": "correct",
            "explanation": "merge() combines two or more maps into one. Later maps override earlier maps on duplicate keys. Perfect for combining common + specific tags.",
            "all_options": {
                "A": "concat()  → for lists, not maps",
                "B": "flatten()  → flattens lists, not maps",
                "C": "join()  → string concatenation",
                "D": "merge()  → combines maps ✓"
            },
            "key_takeaway": "merge(map1, map2) → combined map. Later map wins on duplicate keys. For maps only."
        },

        51: {
            "question": "True or False? Multiple providers can be declared within a single Terraform configuration file.",
            "type": "true_false",
            "correct_answer": "True",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2c - Write Terraform configuration using multiple providers",
            "result": "correct",
            "explanation": "You can declare multiple providers in one file. Common for multi-cloud setups. Each provider has its own block with unique configuration.",
            "key_takeaway": "Multiple providers in one file = valid and common for multi-cloud configurations."
        },

        52: {
            "question": "True or False? After successfully applying a moved block to refactor your resources, you should immediately remove the moved block from your configuration to keep your code clean.",
            "type": "true_false",
            "correct_answer": "False",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6d - Manage resource drift and Terraform state",
            "result": "incorrect",
            "user_answer": "True",
            "explanation": "Keep moved blocks for at least one full apply cycle to allow all team members and CI/CD pipelines to process the state migration. Removing too early causes Terraform to think old resource was destroyed and new one needs creation.",
            "key_takeaway": "moved blocks: keep for ≥1 full apply cycle across all team members before removing."
        },

        53: {
            "question": "In the example code, what order will Terraform create:\n1. google_compute_instance.web\n2. google_compute_attached_disk.data (references instance.web.name)",
            "type": "multiple_choice",
            "correct_answer": "First - google_compute_instance.web\nSecond - google_compute_attached_disk.data",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4b - Refer to resource attributes and create cross-resource references",
            "result": "correct",
            "explanation": "google_compute_attached_disk.data references google_compute_instance.web.name, creating an implicit dependency. Terraform builds a dependency graph and creates the VM first.",
            "all_options": {
                "A": "First - google_compute_instance.web\nSecond - google_compute_attached_disk.data",
                "B": "First - google_compute_attached_disk.data\nSecond - google_compute_instance.web",
                "C": "Both resources are created in parallel since Terraform parallelizes all operations",
                "D": "Terraform will error because circular dependencies are not allowed"
            },
            "key_takeaway": "Reference to another resource creates implicit dependency → Terraform respects creation order automatically."
        },

        54: {
            "question": "True or False? All remote backends in Terraform support state locking by default, so you never need to worry about concurrent modifications.",
            "type": "true_false",
            "correct_answer": "False",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6b - Describe state locking",
            "result": "correct",
            "explanation": "NOT all backends support state locking. S3 requires DynamoDB for locking. HTTP backend may not support it. HCP Terraform and Terraform Enterprise do support locking. Always verify.",
            "key_takeaway": "S3 alone ≠ state locking (needs DynamoDB). HCP Terraform = locking included. Always verify backend locking support."
        },

        55: {
            "question": "You've updated a module and run terraform plan with default settings. What happens when the command is executed?",
            "type": "multiple_choice",
            "correct_answer": "Terraform creates an execution plan and determines what changes are required to achieve the desired state in the configuration files.",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3d - Generate and review an execution plan for Terraform",
            "result": "correct",
            "explanation": "terraform plan: refreshes existing resources (unless disabled), then compares config with state to calculate proposed actions and show an execution plan.",
            "all_options": {
                "A": "Terraform creates an execution plan and determines what changes are required to achieve the desired state in the configuration files.",
                "B": "Terraform immediately applies all changes without prompting for confirmation.",
                "C": "Terraform validates the configuration syntax and exits without contacting any provider.",
                "D": "Terraform downloads the latest version of all providers referenced in the configuration."
            },
            "key_takeaway": "terraform plan = refresh existing resources + compare config vs state + show proposed actions."
        },

        56: {
            "question": "Which statements are true about provider configurations in modules? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "Child modules automatically inherit the default provider configurations from their parent module",
                "Modules containing provider blocks cannot be used with the for_each argument",
                "The providers argument in a module block allows explicit passing of specific provider configurations"
            ],
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2c - Write Terraform configuration using multiple providers",
            "result": "skipped",
            "explanation": "Provider rules for modules: (1) Child modules inherit default providers implicitly, (2) Modules with provider blocks are incompatible with for_each/count/depends_on, (3) Use providers argument for explicit passing.",
            "all_options": {
                "A": "Child modules automatically inherit the default provider configurations from their parent module",
                "B": "Modules containing provider blocks cannot be used with the for_each argument",
                "C": "Each module must always declare its own provider block to function correctly",
                "D": "The providers argument in a module block allows explicit passing of specific provider configurations",
                "E": "Provider blocks inside modules take precedence over provider blocks in the root module"
            },
            "key_takeaway": "Module with provider block = incompatible with for_each, count, depends_on. Pass providers explicitly via providers argument."
        },

        57: {
            "question": "Management wants to understand how IaC with Terraform differs from using console/CLI to deploy infrastructure. Which statement correctly identifies a major difference?",
            "type": "multiple_choice",
            "correct_answer": "Infrastructure as Code allows infrastructure to be described using a configuration syntax that can be versioned, reused, and shared.",
            "domain": "Objective 1 - Infrastructure as Code (IaC) with Terraform",
            "objective": "1a - Explain what IaC is",
            "result": "skipped",
            "explanation": "IaC's major difference: infrastructure defined as code that can be version-controlled, reviewed via PRs, shared, and consistently reproduced. Manual approaches lack this systematic management.",
            "all_options": {
                "A": "IaC requires all resources to be created through APIs instead of UI ✗",
                "B": "IaC eliminates the need for cloud provider APIs ✗",
                "C": "IaC allows infrastructure to be versioned, reused, and shared ✓",
                "D": "IaC only works with immutable infrastructure patterns ✗"
            },
            "key_takeaway": "IaC vs manual: version control + reproducibility + collaboration + consistency = key differences."
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # EXAM SUMMARY BY DOMAIN
    # ─────────────────────────────────────────────────────────────────────────
    "domain_summary": {
        "Objective 1 - IaC with Terraform":         ["Q22", "Q35", "Q57"],
        "Objective 2 - Terraform Fundamentals":      ["Q7", "Q8", "Q12", "Q13", "Q14", "Q23", "Q33", "Q34", "Q51", "Q56"],
        "Objective 3 - Core Terraform Workflow":     ["Q9", "Q17", "Q23", "Q31", "Q32", "Q37", "Q38", "Q42", "Q44", "Q45", "Q55"],
        "Objective 4 - Terraform Configuration":     ["Q4", "Q13", "Q15", "Q18", "Q19", "Q24", "Q29", "Q36", "Q43", "Q49", "Q50", "Q53"],
        "Objective 5 - Terraform Modules":           ["Q1", "Q2", "Q10", "Q18", "Q26", "Q30", "Q40"],
        "Objective 6 - State Management":            ["Q5", "Q16", "Q20", "Q21", "Q46", "Q52", "Q54"],
        "Objective 7 - Maintain Infrastructure":     ["Q6", "Q25", "Q27", "Q28", "Q39"],
        "Objective 8 - HCP Terraform":               ["Q3", "Q11", "Q41", "Q47", "Q48"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # FREQUENTLY MISSED QUESTIONS (result = incorrect)
    # ─────────────────────────────────────────────────────────────────────────
    "missed_questions": {
        "Q24": {
            "mistake": "Used var.metadata.build-tag (dot notation with hyphen)",
            "correct":  'var.metadata["build-tag"]',
            "rule":     "Hyphenated keys MUST use bracket notation"
        },
        "Q28": {
            "mistake": "Confused import blocks with the legacy terraform import command",
            "correct":  "For terraform import command: write resource block first. Import blocks use plan/apply.",
            "rule":     "Two separate approaches: legacy CLI vs config-driven (1.5+)"
        },
        "Q29": {
            "mistake": "Confused variable validation with resource precondition",
            "correct":  "Variable validation blocks fail BEFORE plan. Preconditions fail DURING plan.",
            "rule":     "Validation → Precondition → Plan → Postcondition timeline"
        },
        "Q35": {
            "mistake": "Selected wrong 2nd option (partial credit)",
            "correct":  "Consistent workflow + single tool governance",
            "rule":     "Multi-cloud benefits: unified workflow + reduced overhead. NOT pricing standardization."
        },
        "Q36": {
            "mistake": "Selected 'Using Vault ensures secrets never appear in state'",
            "correct":  "Vault helps but doesn't eliminate state security controls",
            "rule":     "Vault + state controls are complementary, not redundant"
        },
        "Q39": {
            "mistake": "Used terraform state show instead of terraform state list",
            "correct":  "terraform state list = all resources. terraform state show = one resource details.",
            "rule":     "list = overview, show = detailed for one resource"
        },
        "Q41": {
            "mistake": "Answered 5 instead of 1 VCS repo per workspace",
            "correct":  "1 workspace = max 1 VCS repo in HCP Terraform",
            "rule":     "Multiple workspaces can share one repo, but not the reverse"
        },
        "Q52": {
            "mistake": "Answered True — remove moved block immediately",
            "correct":  "False — keep moved block for at least one full apply cycle",
            "rule":     "moved blocks need time to propagate to all team state files"
        }
    }
}


if __name__ == "__main__":
    import json

    # Print summary stats
    total = len(exam2["questions"])
    correct = sum(1 for q in exam2["questions"].values() if q.get("result") == "correct")
    incorrect = sum(1 for q in exam2["questions"].values() if q.get("result") == "incorrect")
    skipped = sum(1 for q in exam2["questions"].values() if q.get("result") == "skipped")

    print(f"{'='*60}")
    print(f"  Terraform Associate 004 - Exam #2 Results")
    print(f"{'='*60}")
    print(f"  Total Questions : {total}")
    print(f"  Correct         : {correct}")
    print(f"  Incorrect       : {incorrect}")
    print(f"  Skipped         : {skipped}")
    print(f"  Score           : {correct}/{total} ({correct/total*100:.1f}%)")
    print(f"{'='*60}")
    print()
    print("Missed Questions:")
    for qnum, details in exam2["missed_questions"].items():
        print(f"  {qnum}: {details['mistake']}")
        print(f"       → {details['rule']}")
