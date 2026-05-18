"""
HashiCorp Certified Terraform Associate (TA-004)
Exam #3 - All Questions with Correct Answers & Explanations
Source: Udemy - Bryan Krausen
"""

exam3 = {

    "exam_title": "Terraform Associate 004 - Exam #3",
    "total_questions": 57,

    "questions": {

        1: {
            "question": "What is the purpose of Terraform's dependency graph?",
            "type": "multiple_choice",
            "correct_answer": "builds a graph of dependencies to perform create/update/destroy operations from it",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3d - Generate and review an execution plan for Terraform",
            "result": "correct",
            "explanation": "Terraform builds a dependency graph and uses it to determine the correct order of create, update, and destroy operations based on resource dependencies.",
            "all_options": {
                "A": "executes resources in the order .tf files appear",
                "B": "builds a graph of dependencies to perform create/update/destroy operations from it",
                "C": "lets providers decide ordering, relying on cloud APIs",
                "D": "sorts resources by type and name and builds a visual graph"
            },
            "key_takeaway": "Terraform dependency graph determines creation/update/destroy order based on dependencies, not file order."
        },

        2: {
            "question": "What sets Infrastructure as Code (IaC) apart from managing infrastructure directly instead of making raw API calls or executing CLI commands?",
            "type": "multiple_choice",
            "correct_answer": "Terraform uses declarative configuration to describe the desired end state and generates a plan of action before applying changes.",
            "domain": "Objective 1 - Infrastructure as Code (IaC) with Terraform",
            "objective": "1a - Explain what IaC is",
            "result": "correct",
            "explanation": "IaC uses declarative configuration (describing desired end state) and generates a plan before applying. This differs from imperative API/CLI calls that execute step-by-step.",
            "all_options": {
                "A": "Terraform replaces provider APIs with its own protocol",
                "B": "Terraform guarantees resources consistently reflect desired state by auto-updating",
                "C": "Terraform uses declarative configuration to describe desired end state and generates a plan",
                "D": "Terraform keeps infrastructure logic in version control to ensure imperative step-by-step runs"
            },
            "key_takeaway": "IaC = declarative (describe WHAT, not HOW) + plan before apply. Not imperative step-by-step."
        },

        3: {
            "question": "You deployed resources using the CLI, but want to start managing them with Terraform moving forward. What steps are required without impacting the resources themselves? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "write Terraform resource blocks that match the existing settings",
                "run terraform apply to import them in state with no changes",
                "add import blocks mapping each address to its real ID"
            ],
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7a - Import existing infrastructure into your Terraform workspace",
            "result": "correct",
            "explanation": "To adopt existing infrastructure: write matching resource blocks + add import blocks + run terraform apply. Do NOT recreate or use -refresh-state (invalid flag).",
            "all_options": {
                "A": "write Terraform resource blocks that match the existing settings (correct)",
                "B": "run terraform apply to import them in state with no changes (correct)",
                "C": "run terraform apply to recreate all resources (wrong)",
                "D": "define data sources for all existing resources (wrong)",
                "E": "add import blocks mapping each address to its real ID (correct)",
                "F": "run terraform apply -refresh-state (wrong - invalid flag)"
            },
            "key_takeaway": "Import existing infra: resource blocks + import blocks + apply. No recreation needed."
        },

        4: {
            "question": "When assigning a value to a Terraform input variable through an environment variable, which prefix string is necessary?",
            "type": "multiple_choice",
            "correct_answer": "TF_VAR_",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4c - Use variables and outputs",
            "result": "correct",
            "explanation": "Use TF_VAR_ prefix for environment variables: export TF_VAR_variable_name='value'. Example: export TF_VAR_instructor_name='bryan'",
            "all_options": {
                "A": "TF_VAR_VALUE",
                "B": "TF_VAR_",
                "C": "TF_ENV_",
                "D": "TF_ENV_VAR_name"
            },
            "key_takeaway": "Environment variable for Terraform inputs: TF_VAR_<variable_name>=value"
        },

        5: {
            "question": "What does the reference aws_vpc.main.id in the subnet configuration accomplish?\nvpc_id = aws_vpc.main.id",
            "type": "multiple_choice",
            "correct_answer": "it retrieves the VPC's ID and creates an implicit dependency",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4b - Refer to resource attributes and create cross-resource references",
            "result": "correct",
            "explanation": "Referencing another resource's attribute (resource_type.resource_name.attribute) both retrieves the value AND creates an implicit dependency, ensuring VPC is created before the subnet.",
            "all_options": {
                "A": "it retrieves the VPC's ID and creates an implicit dependency",
                "B": "it copies the VPC's CIDR block to the subnet configuration",
                "C": "it validates that the VPC name matches the subnet's requirements",
                "D": "it creates a data source that queries AWS for the VPC information"
            },
            "key_takeaway": "Cross-resource reference = retrieve attribute value + create implicit dependency (two effects in one)."
        },

        6: {
            "question": "Which of the following are valid reasons why Terraform requires state? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "improve performance by caching resource attributes",
                "map real-world resources to your Terraform configuration",
                "track metadata such as resource dependencies"
            ],
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2d - Explain how Terraform uses and manages state",
            "result": "correct",
            "explanation": "State serves three purposes: (1) maps config to real resources, (2) tracks dependency metadata, (3) caches attributes for performance. State does NOT validate credentials, fix syntax, or encrypt config.",
            "all_options": {
                "A": "improve performance by caching resource attributes ✓",
                "B": "map real-world resources to your Terraform configuration ✓",
                "C": "validate provider credentials ✗",
                "D": "track metadata such as resource dependencies ✓",
                "E": "automatically fix HCL configuration syntax errors ✗",
                "F": "encrypt sensitive data in configuration files ✗"
            },
            "key_takeaway": "State purposes: map real resources → config, track dependency metadata, cache attributes for performance."
        },

        7: {
            "question": "You have a list variable ['10.0.5.0/24', '10.0.0.0/24', '10.0.2.0/24']. Which function returns the number of elements?",
            "type": "multiple_choice",
            "correct_answer": "length(var.subnet_cidrs)",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4e - Write dynamic configuration using expressions and functions",
            "result": "correct",
            "explanation": "length() returns the number of elements in a list, map, or string. Commonly used with count meta-argument.",
            "all_options": {
                "A": "contains(var.subnet_cidrs)  → checks if value exists",
                "B": "length(var.subnet_cidrs)  → returns element count ✓",
                "C": "values(var.subnet_cidrs)  → returns map values",
                "D": "keys(var.subnet_cidrs)  → returns map keys"
            },
            "key_takeaway": "length(list) = count of elements. length(map) = count of key-value pairs. length(string) = character count."
        },

        8: {
            "question": "You added a new module block sourcing from a remote source. What do you need to do so that Terraform downloads the module?",
            "type": "multiple_choice",
            "correct_answer": "Run terraform init to install the module into the current working directory.",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5a - Explain how Terraform sources modules",
            "result": "correct",
            "explanation": "terraform init downloads both provider plugins AND remote modules into the working directory. terraform plan does NOT download modules.",
            "all_options": {
                "A": "Run terraform init to install the module ✓",
                "B": "Run terraform plan so Terraform can fetch the module",
                "C": "Add the module to required_providers",
                "D": "Copy the module into the .terraform/modules/downloads directory"
            },
            "key_takeaway": "New module added → run terraform init to download it before plan/apply."
        },

        9: {
            "question": "You are using a local backend and accidentally delete the terraform.tfstate file. What is the most serious consequence?",
            "type": "multiple_choice",
            "correct_answer": "Terraform can no longer track the resources it manages, so the next plan or apply might attempt to create duplicate resources.",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6a - Describe the local backend",
            "result": "correct",
            "explanation": "Without the state file, Terraform loses the mapping between config and real infrastructure. Next plan/apply may try to create duplicates or fail to destroy existing resources.",
            "all_options": {
                "A": "Terraform can no longer track resources; next plan/apply might create duplicates ✓",
                "B": "Terraform will download last good state file from provider API",
                "C": "Terraform will require switching to a remote backend",
                "D": "Terraform will recreate state by reading variables and outputs"
            },
            "key_takeaway": "Lost state = lost resource tracking. Recovery requires reimporting or restoring from backup."
        },

        10: {
            "question": "After creating several new Terraform configurations, you want to quickly format all files at once without editing each manually.",
            "type": "multiple_choice",
            "correct_answer": "terraform fmt",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3g - Apply formatting and style adjustments to a configuration",
            "result": "correct",
            "explanation": "terraform fmt automatically formats all .tf files in the current directory to canonical style. Run after Terraform version upgrades too.",
            "all_options": {
                "A": "terraform validate  → syntax check only",
                "B": "terraform init  → initialization only",
                "C": "terraform refresh  → reconciles state with reality",
                "D": "terraform fmt  → auto-formats all .tf files ✓"
            },
            "key_takeaway": "terraform fmt = auto-format all .tf files in directory. Add -recursive for subdirectories."
        },

        11: {
            "question": "What environment variable can be set to enable detailed logging for Terraform?",
            "type": "multiple_choice",
            "correct_answer": "TF_LOG",
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7c - Describe when and how to use verbose logging",
            "result": "incorrect",
            "user_answer": "TF_DEBUG",
            "explanation": "TF_LOG is the correct variable. Set to TRACE, DEBUG, INFO, WARN, or ERROR. TRACE is most verbose. Use TF_LOG_PATH to write logs to a file.",
            "all_options": {
                "A": "TF_INFO  → invalid",
                "B": "TF_DEBUG  → invalid",
                "C": "TF_LOG  → CORRECT ✓",
                "D": "TF_TRACE  → invalid"
            },
            "key_takeaway": "TF_LOG=TRACE|DEBUG|INFO|WARN|ERROR. TF_LOG_PATH=./terraform.log to write to file."
        },

        12: {
            "question": "You need to create a variable that looks up the correct AMI ID based on the region name. Which variable type is most appropriate?",
            "type": "multiple_choice",
            "correct_answer": "variable \"image\" {\n  type = map(string)\n  ...\n}",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4d - Understand and use complex types",
            "result": "incorrect",
            "user_answer": "variable \"image\" {\n  type = object({ region = string, image_id = string })\n  ...\n}",
            "explanation": "map(string) is ideal for key-value lookups: region name → AMI ID. Access with var.image[var.region]. object() is overly complex and requires predefined structure. list() requires numeric indexing. set() has no key-value relationship.",
            "all_options": {
                "A": "map(string)  → CORRECT for key-value lookups ✓",
                "B": "list(string)  → requires numeric indexing",
                "C": "set(string)  → no key-value relationship",
                "D": "object({ region = string, image_id = string })  → overly complex, fixed structure"
            },
            "key_takeaway": "map(string) = best for key-based lookups (region → AMI ID). Access: var.map_name[\"key\"]"
        },

        13: {
            "question": "Which of the following variable declarations will cause Terraform to return a type error before apply?",
            "type": "multiple_choice",
            "correct_answer": "variable \"names\" {\n  type    = list(string)\n  default = {}\n}",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4c - Use variables and outputs",
            "result": "correct",
            "explanation": "list(string) expects square brackets [ ], but the default {} uses curly braces (map syntax). Type mismatch → Terraform returns error.",
            "all_options": {
                "A": "names: type=list(string), default={} → TYPE ERROR ✓ (curly braces are map, not list)",
                "B": "tags: type=map(string), default={...} → valid",
                "C": "enabled: type=bool, default=true → valid",
                "D": "instance_count: type=number, default=3 → valid"
            },
            "key_takeaway": "list = [ ], map = { }, set = [ ]. Wrong bracket type = type error."
        },

        14: {
            "question": "Your root module calls a database module with output 'connection_string'. It then calls a webapp module needing this string. How do you correctly pass it?",
            "type": "multiple_choice",
            "correct_answer": "module \"webapp\" {\n  source            = \"./modules/webapp\"\n  db_connection_str = module.database.connection_string\n}",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5c - Use modules in configuration",
            "result": "correct",
            "explanation": "Reference module outputs as module.<module_name>.<output_name>. This also creates an implicit dependency ensuring database module runs before webapp module.",
            "all_options": {
                "A": "output 'connection_string' { to = module.webapp }  → invalid syntax",
                "B": "db_connection_str = output.database.connection_string  → wrong syntax",
                "C": "db_connection_str = module.database.connection_string  → CORRECT ✓",
                "D": "db_connection_str = var.database.connection_string  → wrong, uses var not module"
            },
            "key_takeaway": "Module output reference: module.<name>.<output_name>. Creates implicit dependency between modules."
        },

        15: {
            "question": "In a Terraform module block sourcing from a registry, why should you include the version argument?",
            "type": "multiple_choice",
            "correct_answer": "to pin a specific module release and avoid unexpected upgrades",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5d - Manage module versions",
            "result": "correct",
            "explanation": "version pins the module release for reproducible runs and prevents accidental upgrades. It applies only to registry sources, not local or Git sources.",
            "all_options": {
                "A": "to lock provider versions inside the child module",
                "B": "to lock down the version of Terraform that can be used",
                "C": "to pin a specific module release and avoid unexpected upgrades ✓",
                "D": "to set the required Terraform CLI version for the workspace"
            },
            "key_takeaway": "Module version argument = pin specific release for reproducibility. Required for registry sources."
        },

        16: {
            "question": "In HCP Terraform, what is the purpose of using a run trigger?",
            "type": "multiple_choice",
            "correct_answer": "to automatically queue a new run in one workspace after another workspace applies successfully",
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8c - Describe how to organize and use HCP Terraform workspaces and projects",
            "result": "correct",
            "explanation": "Run triggers connect workspaces: when source workspace completes a successful apply, downstream workspace gets a new run queued automatically. Used for dependent stacks.",
            "all_options": {
                "A": "to provide temporary cloud credentials with least privilege",
                "B": "to require human approval before applying changes",
                "C": "to force workspace to always run from newest VCS commit",
                "D": "to automatically queue a run in one workspace after another applies successfully ✓"
            },
            "key_takeaway": "Run trigger: source workspace apply succeeds → downstream workspace run queued automatically."
        },

        17: {
            "question": "In Terraform, how can a dependency on a provider be established? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "Declaring a provider block in the configuration, including any required version constraints.",
                "Using a resource or data block that belongs to that provider in the configuration.",
                "Having existing resource instances for that provider recorded in the current state."
            ],
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2b - Describe how Terraform uses providers",
            "result": "incorrect",
            "user_answer_missing": "Having existing resource instances for that provider recorded in the current state.",
            "explanation": "Provider dependency established by: (1) explicit provider block, (2) resource/data block using that provider, (3) existing state records for that provider. Documentation URLs and local plugin files don't establish dependencies.",
            "all_options": {
                "A": "Adding provider documentation URL as a comment ✗",
                "B": "Declaring a provider block with version constraints ✓",
                "C": "Using a resource or data block from that provider ✓",
                "D": "Existence of provider plugins found locally ✗",
                "E": "Having existing resource instances in current state ✓"
            },
            "key_takeaway": "Provider dependency: provider block OR resource/data block OR existing state records."
        },

        18: {
            "question": "Why is using a single tool like Terraform for multi-cloud deployments more beneficial than using separate tools per cloud?",
            "type": "multiple_choice",
            "correct_answer": "It provides a common workflow and reusable modules, enabling consistent CI/CD and policy across clouds.",
            "domain": "Objective 1 - Infrastructure as Code (IaC) with Terraform",
            "objective": "1c - Explain how Terraform manages multi-cloud, hybrid cloud, and service-agnostic workflows",
            "result": "correct",
            "explanation": "Single tool benefits: unified workflow (init/plan/apply), one language (HCL), reusable modules, consistent CI/CD, policy enforcement, and reduced learning overhead. Cloud-specific credentials are still needed.",
            "all_options": {
                "A": "It provides common workflow and reusable modules, consistent CI/CD and policy ✓",
                "B": "It guarantees identical resource types and APIs across all clouds",
                "C": "It eliminates need for cloud-specific credentials",
                "D": "It automatically migrates existing resources from other tools"
            },
            "key_takeaway": "Single tool benefits: unified workflow + HCL + reusable modules. Still needs per-provider credentials."
        },

        19: {
            "question": "You are using HCP Terraform with a VCS-driven workflow. Which sequence follows the recommended workflow to deploy a new resource?",
            "type": "multiple_choice",
            "correct_answer": "1. Add the new resource block to the repo\n2. Open a pull request\n3. After plan is generated, approve the apply in HCP Terraform",
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8a - Use HCP Terraform to create infrastructure",
            "result": "correct",
            "explanation": "VCS-driven workflow: code in VCS → PR → HCP Terraform auto-generates plan → review → approve apply. Never write config in UI or run local applies.",
            "all_options": {
                "A": "Write resource in UI → Queue plan → Approve apply ✗",
                "B": "Add resource to repo → Open PR → Approve apply after plan ✓",
                "C": "Apply locally → Push tfstate to repo → Skip review ✗",
                "D": "Commit to main branch → Disable policy checks → Re-enable after ✗"
            },
            "key_takeaway": "VCS-driven: code in repo → PR → auto plan → review → approve apply. No local applies."
        },

        20: {
            "question": "Which statement best describes a Terraform data source?",
            "type": "multiple_choice",
            "correct_answer": "a read-only construct that queries provider APIs and returns attributes for use elsewhere in the configuration",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4a - Use and differentiate resource and data blocks",
            "result": "correct",
            "explanation": "Data sources are read-only — they query existing resources/APIs without creating or managing anything. Contrast with resource blocks which create and own resources.",
            "all_options": {
                "A": "a local cache that stores computed values between runs",
                "B": "a mechanism for persisting variable defaults into state",
                "C": "a read-only construct that queries provider APIs and returns attributes ✓",
                "D": "a reusable package defining multiple resources (that's a module)"
            },
            "key_takeaway": "data block = read-only query of existing resources. resource block = create and manage resources."
        },

        21: {
            "question": "How do you specify which provider Terraform should install for a configuration?",
            "type": "multiple_choice",
            "correct_answer": "Define the provider in required_providers and add a matching provider block in the configuration.",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2a - Install and version Terraform providers",
            "result": "correct",
            "explanation": "Two-part setup: (1) required_providers in terraform block declares source/version, (2) provider block configures auth/region/etc. Then terraform init downloads the plugin.",
            "all_options": {
                "A": "Download the provider binary and place in working directory",
                "B": "Define in required_providers and add a matching provider block ✓",
                "C": "Set provider name in variable and pass with -var during init",
                "D": "Run terraform apply first so Terraform detects provider automatically"
            },
            "key_takeaway": "Specify provider: required_providers (source + version) + provider block (config) + terraform init."
        },

        22: {
            "question": "The security team requires you to protect sensitive values like API keys. Which methods follow Terraform guidance? (select two)",
            "type": "multi_select",
            "correct_answer": [
                "Mark variables as sensitive so Terraform redacts their values in CLI output and logs.",
                "Provide secrets as short-lived, ephemeral values from an external system (e.g., Vault) at runtime."
            ],
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4h - Understand best practices for managing sensitive data",
            "result": "correct",
            "explanation": "Best practices: mark sensitive=true (redacts from CLI/UI) + use Vault/external secrets for ephemeral values. NEVER commit credentials to git or expose in outputs.",
            "all_options": {
                "A": "Mark variables as sensitive to redact CLI output ✓",
                "B": "Expose secrets in output blocks for troubleshooting ✗",
                "C": "Provide ephemeral secrets from Vault/external system at runtime ✓",
                "D": "Store credentials in terraform.tfvars and commit to Git ✗"
            },
            "key_takeaway": "Sensitive data: sensitive=true (hides from output) + ephemeral secrets from Vault. Never commit secrets to git."
        },

        23: {
            "question": "Some production resources were created manually in the Azure portal. How do you bring them under Terraform management without disrupting them?",
            "type": "multiple_choice",
            "correct_answer": "Use the import block to import the existing resources under Terraform management.",
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7a - Import existing infrastructure into your Terraform workspace",
            "result": "correct",
            "explanation": "Import block (or terraform import command) brings existing resources into state without recreating them. Write resource block → add import block → terraform plan → terraform apply.",
            "all_options": {
                "A": "Rewrite config, deploy new resources, and manually delete old ones ✗",
                "B": "Use the import block to import without disruption ✓",
                "C": "Resources created outside Terraform cannot be managed by Terraform ✗",
                "D": "Run terraform get to retrieve unmanaged resources ✗"
            },
            "key_takeaway": "Adopt existing resources: import block + resource block + plan + apply. No recreation or downtime."
        },

        24: {
            "question": "You split a large module into multiple .tf files and rearranged resource blocks without changing arguments. What impact does this have on terraform plan?",
            "type": "multiple_choice",
            "correct_answer": "No changes. Block order doesn't affect the plan because Terraform parses all .tf files in a module together during execution.",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3d - Generate and review an execution plan for Terraform",
            "result": "correct",
            "explanation": "Terraform language is declarative. Block ordering and file organization are not significant — only implicit/explicit resource relationships matter for ordering.",
            "all_options": {
                "A": "No changes. Block order doesn't affect the plan because Terraform parses all .tf files in a module together during execution.",
                "B": "Terraform will destroy and recreate all resources because the resource block order changed.",
                "C": "The plan will show an error because Terraform requires all resources in a single main.tf file.",
                "D": "Terraform will re-read only the modified files and partially refresh the state."
            },
            "key_takeaway": "Terraform is declarative: file order and block order are irrelevant. Only dependencies matter for execution order."
        },

        25: {
            "question": "Why should users not commit the terraform.tfstate file to version control? (select two)",
            "type": "multi_select",
            "correct_answer": [
                "State can include plaintext secrets and detailed resource data and commit history can expose them.",
                "VCS provides no state locking, so concurrent runs can cause conflicting commits and corrupt state."
            ],
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6a - Describe the local backend",
            "result": "incorrect",
            "user_answer_wrong": "Committing the file to version control prevents Terraform from reading it to properly manage state.",
            "explanation": "TWO real reasons: (1) state contains plaintext secrets exposed in commit history, (2) no state locking in VCS = concurrent run conflicts = corrupt state. Committing state doesn't prevent Terraform from reading it.",
            "all_options": {
                "A": "State contains plaintext secrets exposed in commit history ✓",
                "B": "Committing prevents Terraform from reading it ✗ (wrong reason)",
                "C": "Storing in Git prevents safely reverting resource changes ✗",
                "D": "VCS provides no state locking → concurrent corruption risk ✓"
            },
            "key_takeaway": "Don't commit state: (1) plaintext secrets in history, (2) no locking = concurrent corruption."
        },

        26: {
            "question": "You attempt to reference module.network.vpc_id from your root module but get an error that vpc_id is not a valid attribute. What is the most likely cause?",
            "type": "multiple_choice",
            "correct_answer": "The network module did not define an output block that exports the VPC ID, resulting in the error.",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5b - Describe variable scope within modules",
            "result": "correct",
            "explanation": "Module values are only accessible from the parent if explicitly defined as outputs in the child module. Without an output block, the parent cannot reference the value.",
            "all_options": {
                "A": "vpc_id must be declared as a variable in the root module",
                "B": "The network module did not define an output block ✓",
                "C": "Root module must use a data block instead",
                "D": "Module outputs can only be referenced during apply, not plan"
            },
            "key_takeaway": "Child module values only accessible to parent via output blocks. No output = can't reference it."
        },

        27: {
            "question": "True or False? By default, the terraform destroy command will prompt the user for confirmation before proceeding.",
            "type": "true_false",
            "correct_answer": "True",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3f - Destroy Terraform-managed infrastructure",
            "result": "correct",
            "explanation": "terraform destroy always prompts for confirmation by default. Use -auto-approve to skip the prompt. No undo after confirmation.",
            "key_takeaway": "terraform destroy prompts by default. Skip with -auto-approve flag."
        },

        28: {
            "question": "You have subdirectories /dev, /staging, and /prod each with separate Terraform configs. Where do you need to run terraform init?",
            "type": "multiple_choice",
            "correct_answer": "In each directory (/dev, /staging, and /prod) since each is a separate working directory.",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3b - Initialize a Terraform working directory",
            "result": "correct",
            "explanation": "Each directory with .tf files is a separate working directory requiring its own terraform init. Never copy the .terraform folder between directories.",
            "all_options": {
                "A": "In each directory since each is separate ✓",
                "B": "Only in the root directory to initialize all at once",
                "C": "Only in /prod since dev and staging can share config",
                "D": "In one directory, then copy .terraform folder to others"
            },
            "key_takeaway": "Each working directory needs its own terraform init. Never copy .terraform folder."
        },

        29: {
            "question": "A user sets instance_count = 15 for a variable with validation: condition = var.instance_count > 0 && var.instance_count <= 10. When does Terraform report the error?",
            "type": "multiple_choice",
            "correct_answer": "During terraform validate or terraform plan, before attempting to create any resources",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4g - Validate configuration using custom conditions",
            "result": "correct",
            "explanation": "Variable validation blocks run during the validation phase (validate or plan), before any resource creation. This catches config errors early in the workflow.",
            "all_options": {
                "A": "During terraform validate or terraform plan, before resource creation ✓",
                "B": "The validation passes because 15 is a valid number type",
                "C": "During terraform apply when Terraform attempts to create instances",
                "D": "During terraform init when configuration is first loaded"
            },
            "key_takeaway": "Variable validation: runs during validate/plan, BEFORE any resource creation."
        },

        30: {
            "question": "Which statements about sensitive data and Terraform state are correct? (select two)",
            "type": "multi_select",
            "correct_answer": [
                "The state file can contain sensitive values in plaintext by default.",
                "Marking a variable sensitive = true does not prevent it from being written to state."
            ],
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4h - Understand best practices for managing sensitive data",
            "result": "correct",
            "explanation": "State stores sensitive values in plaintext by default. sensitive=true only redacts CLI output, NOT state storage. Protect state with encryption and access controls.",
            "all_options": {
                "A": "State file can contain sensitive values in plaintext ✓",
                "B": "Local state automatically encrypts secrets on disk ✗",
                "C": "sensitive=true does not prevent writing to state ✓",
                "D": "Sensitive outputs are never stored in state, only displayed at apply ✗"
            },
            "key_takeaway": "State = plaintext by default. sensitive=true only hides from CLI/UI. Protect state separately."
        },

        31: {
            "question": "You configured a workspace in HCP Terraform to use local execution. In this mode, what does HCP Terraform do?",
            "type": "multiple_choice",
            "correct_answer": "HCP Terraform only stores and syncs the workspace's state file, while you run plan and apply locally on your own machine.",
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8d - Configure and use HCP Terraform integration",
            "result": "correct",
            "explanation": "Local execution mode: HCP Terraform acts as remote state backend only. Plan and apply run on your local machine. Remote features (Sentinel, cost estimation) NOT available in local mode.",
            "all_options": {
                "A": "Local execution blocks local CLI usage ✗",
                "B": "HCP Terraform replaces state file with variables and policies ✗",
                "C": "HCP Terraform runs plans and applies in its own environment ✗",
                "D": "HCP Terraform only stores/syncs state; plan/apply run locally ✓"
            },
            "key_takeaway": "Local execution mode = HCP Terraform as state backend only. Sentinel/cost estimation NOT available."
        },

        32: {
            "question": "In Terraform, what does 'drift' mean in the context of a workspace's state?",
            "type": "multiple_choice",
            "correct_answer": "Real infrastructure has changed outside Terraform and no longer matches the desired state.",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6d - Manage resource drift and Terraform state",
            "result": "correct",
            "explanation": "Drift = real-world infrastructure differs from Terraform's desired state. Can occur from manual changes, other automation tools, resource failures, or external modifications.",
            "all_options": {
                "A": "Real infrastructure has changed outside Terraform and no longer matches ✓",
                "B": "Configuration files were refactored with different argument ordering",
                "C": "Backend was migrated but state contents remained the same",
                "D": "Provider versions were upgraded but no resources changed"
            },
            "key_takeaway": "Drift = real infra ≠ desired state. Detect with terraform plan or terraform plan -refresh-only."
        },

        33: {
            "question": "You run terraform init in a new working directory. Where does Terraform store the downloaded provider plugins?",
            "type": "multiple_choice",
            "correct_answer": "The .terraform/providers directory in the current working directory",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2a - Install and version Terraform providers",
            "result": "correct",
            "explanation": "terraform init downloads provider plugins to .terraform/providers/ in the current working directory, keeping each working directory self-contained.",
            "all_options": {
                "A": "The .terraform.d directory in the current working directory",
                "B": "The .terraform/plugins directory",
                "C": "/etc/terraform/plugins",
                "D": "The .terraform/providers directory ✓"
            },
            "key_takeaway": ".terraform/providers/ = provider binaries. .terraform/modules/ = downloaded modules."
        },

        34: {
            "question": "A resource was changed manually outside Terraform. You want to see how state would be updated to match real-world values WITHOUT making any changes yet.",
            "type": "multiple_choice",
            "correct_answer": "terraform plan -refresh-only",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6d - Manage resource drift and Terraform state",
            "result": "correct",
            "explanation": "terraform plan -refresh-only shows what state updates would occur to match real infrastructure, without making changes. terraform apply -refresh-only would actually update state.",
            "all_options": {
                "A": "terraform validate  → syntax check only",
                "B": "terraform state pull  → retrieves current state data",
                "C": "terraform plan -refresh-only  → shows state updates without applying ✓",
                "D": "terraform apply -refresh-only  → actually updates state (avoid per question)"
            },
            "key_takeaway": "terraform plan -refresh-only = preview state drift reconciliation. terraform apply -refresh-only = execute it."
        },

        35: {
            "question": "Which Terraform command checks modules, attribute names, and value types to ensure the configuration is syntactically valid and internally consistent?",
            "type": "multiple_choice",
            "correct_answer": "terraform validate",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3c - Validate a Terraform configuration",
            "result": "correct",
            "explanation": "terraform validate checks for syntax errors, missing attributes, invalid values, and incorrect code structure without accessing remote services.",
            "all_options": {
                "A": "terraform format  → not a valid command",
                "B": "terraform show  → displays state/plan in human-readable format",
                "C": "terraform fmt  → formats files to canonical style",
                "D": "terraform validate  → checks modules, attributes, value types ✓"
            },
            "key_takeaway": "terraform validate = syntax + attribute + type checking. No remote calls. Fast."
        },

        36: {
            "question": "You need to decommission only a Cloud SQL database instance and its backup policy from 50 resources. What is the most appropriate approach?",
            "type": "multiple_choice",
            "correct_answer": "Remove the database and backup resource blocks from your configuration, then run terraform apply.",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3f - Destroy Terraform-managed infrastructure",
            "result": "incorrect",
            "user_answer": "Add two removed blocks to your configuration, pointing to each of the Cloud SQL database and the backup policy",
            "explanation": "The config-driven approach: remove resource blocks + run terraform apply is recommended. Terraform sees the missing resources and destroys only them while preserving all others. removed blocks are for renaming/moving, not decommissioning.",
            "all_options": {
                "A": "terraform destroy then terraform apply ✗ (destroys everything)",
                "B": "Add removed blocks pointing to Cloud SQL resources ✗",
                "C": "terraform destroy -target=... ✗ (risky, not recommended)",
                "D": "Remove resource blocks from config + terraform apply ✓"
            },
            "key_takeaway": "Selective destroy: remove resource blocks from config → terraform apply. Terraform destroys only removed resources."
        },

        37: {
            "question": "You ran terraform plan -out=bk-project.tfplan and got approval two hours later. What command executes the exact reviewed changes?",
            "type": "multiple_choice",
            "correct_answer": "run terraform apply bk-project.tfplan to execute the saved plan",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3e - Apply changes to infrastructure with Terraform",
            "result": "correct",
            "explanation": "terraform apply <planfile> executes the exact saved plan without re-planning or prompting. Ensures no drift between review and execution.",
            "all_options": {
                "A": "terraform apply bk-project.tfplan  → executes exact saved plan ✓",
                "B": "terraform apply  → generates NEW plan, not the reviewed one",
                "C": "terraform apply -auto-approve  → skips prompt but generates new plan",
                "D": "terraform plan again then apply  → redundant, may show drift"
            },
            "key_takeaway": "terraform apply <planfile> = execute EXACT reviewed plan. No re-planning, no prompts."
        },

        38: {
            "question": "Which statements accurately describe tradeoffs between local and remote Terraform state? (select two)",
            "type": "multi_select",
            "correct_answer": [
                "Remote state centralizes storage with encryption, locking, and access policies for collaboration.",
                "Local state is simple and works offline, but lacks shared access, locking, and org-level controls."
            ],
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6c - Configure remote state using the backend block",
            "result": "incorrect",
            "user_answer_wrong": "Local state is best for multi-user teams because changes are automatically merged by Terraform.",
            "explanation": "Local = simple, offline, no locking/sharing. Remote = centralized, encrypted, locked, access-controlled. Local does NOT auto-merge. Remote does NOT eliminate need to protect sensitive state.",
            "all_options": {
                "A": "Remote state centralizes with encryption, locking, access policies ✓",
                "B": "Local state best for multi-user teams (auto-merge) ✗",
                "C": "Local state: simple, offline, but lacks sharing/locking/org-controls ✓",
                "D": "Remote state removes need to secure state files ✗"
            },
            "key_takeaway": "Local = simple but no locking/sharing. Remote = team-ready with encryption + locking."
        },

        39: {
            "question": "When using a module from the Terraform registry, is it necessary to specify a version argument in the module block?",
            "type": "multiple_choice",
            "correct_answer": "No, the version argument is optional, but it is recommended to ensure consistent and reproducible deployments",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5d - Manage module versions",
            "result": "correct",
            "explanation": "version is optional but highly recommended. Without it, Terraform uses latest version which may introduce breaking changes. Use version constraints for reproducibility.",
            "all_options": {
                "A": "No, Terraform automatically pins to the first version initialized permanently",
                "B": "No, optional but recommended for consistency and reproducibility ✓",
                "C": "Yes, always required for registry modules or Terraform returns error",
                "D": "Yes, but only for public registry modules"
            },
            "key_takeaway": "Module version: optional but recommended. Without it = latest version = potential breaking changes."
        },

        40: {
            "question": "Which feature of HCP Terraform enables you to publish and maintain custom modules only for use within your organization?",
            "type": "multiple_choice",
            "correct_answer": "HCP Terraform private registry",
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8b - Describe HCP Terraform collaboration and governance features",
            "result": "correct",
            "explanation": "HCP Terraform private registry lets organizations publish internal modules with the same source string format as public registry but with a hostname prefix.",
            "all_options": {
                "A": "a custom VCS integration to your repo",
                "B": "HCP Terraform private registry ✓",
                "C": "the public Terraform Registry",
                "D": "HCP Terraform agents"
            },
            "key_takeaway": "Private registry = internal module publishing. Source format: <hostname>/<org>/<module>/<provider>"
        },

        41: {
            "question": "Which of the following statements is the most accurate about the Terraform language?",
            "type": "multiple_choice",
            "correct_answer": "Terraform is an immutable, declarative Infrastructure as Code language based on HashiCorp Configuration Language or JSON.",
            "domain": "Objective 1 - Infrastructure as Code (IaC) with Terraform",
            "objective": "1a - Explain what IaC is",
            "result": "incorrect",
            "user_answer": "Terraform is a mutable, declarative, Infrastructure as Code configuration management language based on HCL or JSON.",
            "explanation": "Terraform is IMMUTABLE (not mutable) and DECLARATIVE (not imperative). Written in HCL or JSON (not YAML). Describes desired end state, not step-by-step instructions.",
            "all_options": {
                "A": "mutable, imperative, HCL or YAML ✗",
                "B": "mutable, declarative, HCL or JSON ✗ (mutable is wrong)",
                "C": "immutable, imperative, HCL or JSON ✗ (imperative is wrong)",
                "D": "immutable, declarative, HCL or JSON ✓"
            },
            "key_takeaway": "Terraform = IMMUTABLE + DECLARATIVE + HCL or JSON. Not mutable, not imperative, not YAML."
        },

        42: {
            "question": "What is the implicit dependency in this code?\nresource \"aws_eip\" \"public_ip\" { instance = aws_instance.web_server.id }\nresource \"aws_instance\" \"web_server\" { depends_on = [aws_s3_bucket.company_data] }",
            "type": "multiple_choice",
            "correct_answer": "The EC2 instance labeled web_server",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4f - Define resource dependencies in configuration",
            "result": "correct",
            "explanation": "aws_eip references aws_instance.web_server.id → implicit dependency on web_server. The S3 bucket is an EXPLICIT dependency (depends_on). Implicit = auto-detected via reference.",
            "all_options": {
                "A": "The AMI used for the EC2 instance",
                "B": "The EC2 instance labeled web_server ✓ (referenced via .id)",
                "C": "The S3 bucket labeled company_data (that's EXPLICIT via depends_on)",
                "D": "The EIP with id eip-2757f631"
            },
            "key_takeaway": "Implicit = auto-detected via attribute reference. Explicit = manually declared via depends_on."
        },

        43: {
            "question": "You invoke a subnet module and the root load balancer module requires that subnet's ID. How should you expose the ID?",
            "type": "multiple_choice",
            "correct_answer": "add an output block to the subnet module and pass the value for the load balancer module using module.subnets.subnet_id",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5c - Use modules in configuration",
            "result": "correct",
            "explanation": "Module outputs: define output block in child module → reference as module.<name>.<output_name> in parent. This is how values flow from child to parent.",
            "all_options": {
                "A": "Move subnet and load balancer into main config file",
                "B": "Add output block to subnet module and pass as module.subnets.subnet_id ✓",
                "C": "References from modules cannot be used in other modules ✗",
                "D": "Declare a local in root module set to aws_subnet.subnets.id from child"
            },
            "key_takeaway": "Child → Parent value flow: output block in child → module.<name>.<output> in parent."
        },

        44: {
            "question": "What is the correct explanation of the difference between terraform show and terraform state show? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "terraform state show requires you to specify a resource address to view that specific resource",
                "terraform show displays the entire state file without requiring any additional arguments",
                "terraform show is useful when you want a complete overview of all managed infrastructure"
            ],
            "domain": "Objective 7 - Maintain Infrastructure with Terraform",
            "objective": "7b - Use the CLI to inspect state",
            "result": "incorrect",
            "user_answer_wrong": "terraform state show can display multiple resources by separating them with commas",
            "explanation": "terraform show = full state overview, no args needed. terraform state show = single resource details, requires address argument. state show does NOT support multiple resources via commas.",
            "all_options": {
                "A": "terraform state show requires resource address ✓",
                "B": "terraform show displays entire state without arguments ✓",
                "C": "terraform show only displays resources with pending changes ✗",
                "D": "terraform state show auto-formats output as JSON ✗",
                "E": "terraform show is useful for complete infrastructure overview ✓",
                "F": "terraform state show can show multiple resources with commas ✗"
            },
            "key_takeaway": "terraform show = full state. terraform state show <address> = one resource detail. No multi-resource comma syntax."
        },

        45: {
            "question": "True or False? In the configuration below, the aws_volume_attachment.attach_data resource has an implicit dependency on both the instance and the volume.\n(aws_volume_attachment references both aws_instance.app_core.id and aws_ebs_volume.data_pr0d_east.id)",
            "type": "true_false",
            "correct_answer": "True",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4f - Define resource dependencies in configuration",
            "result": "correct",
            "explanation": "aws_volume_attachment references BOTH .id attributes → two implicit dependencies. Terraform creates instance and volume first, then attaches.",
            "key_takeaway": "Each attribute reference creates one implicit dependency. Two references = two implicit dependencies."
        },

        46: {
            "question": "You are reviewing a colleague's code and discover a .terraform/ directory. What is the purpose of this directory?",
            "type": "multiple_choice",
            "correct_answer": "The .terraform/ directory stores Terraform's local working data, including installed provider and module plugins and backend metadata.",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2b - Describe how Terraform uses providers",
            "result": "correct",
            "explanation": ".terraform/ is the local working cache: .terraform/providers/ (provider binaries), .terraform/modules/ (module code), backend metadata. NOT credentials, NOT state files, NOT plan files.",
            "all_options": {
                "A": ".terraform/ stores Terraform's local working data (providers, modules, metadata) ✓",
                "B": ".terraform/ holds cached provider credentials and sensitive variables ✗",
                "C": ".terraform/ is where Terraform saves local state files by default ✗",
                "D": ".terraform/ contains validated config and plan files used during apply ✗"
            },
            "key_takeaway": ".terraform/ = provider binaries + module code + backend metadata. Created by terraform init."
        },

        47: {
            "question": "You changed backend from S3 to HCP Terraform. After updating the backend block, which flag reconfigures the backend WITHOUT copying existing state?",
            "type": "multiple_choice",
            "correct_answer": "terraform init -reconfigure",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6c - Configure remote state using the backend block",
            "result": "incorrect",
            "user_answer": "terraform init -migrate-state",
            "explanation": "-reconfigure: reconfigures backend without copying state (fresh start). -migrate-state: migrates existing state to new backend. Use -reconfigure when you DON'T want to copy state.",
            "all_options": {
                "A": "terraform init -force-copy  → not a valid flag",
                "B": "terraform init -backend=false  → disables backend entirely",
                "C": "terraform init -migrate-state  → migrates state TO new backend",
                "D": "terraform init -reconfigure  → reconfigures WITHOUT copying state ✓"
            },
            "key_takeaway": "-reconfigure = new backend, no state copy. -migrate-state = new backend WITH state migration."
        },

        48: {
            "question": "In a module block, what do name, cidr, and azs represent and what purpose do they serve?\nmodule \"vpc\" { source = \"...\", name = var.vpc_name, cidr = var.vpc_cidr_block, azs = var.vpc_azs }",
            "type": "multiple_choice",
            "correct_answer": "these are module-specific inputs that are passed into the child module used for resource creation",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5b - Describe variable scope within modules",
            "result": "correct",
            "explanation": "Arguments in a module block (other than source, version, providers, depends_on, count, for_each) are input variables being passed into the child module.",
            "all_options": {
                "A": "these are the outputs the child module will return",
                "B": "these are where variable declarations are created",
                "C": "these values will be obtained from values created within the child module",
                "D": "these are module-specific inputs passed into the child module ✓"
            },
            "key_takeaway": "Module block arguments = inputs passed to child module. Child must declare matching variable blocks."
        },

        49: {
            "question": "Your team uses HCP Terraform with a CLI-driven workflow. After making local changes, you run terraform plan. Where does the plan execute?",
            "type": "multiple_choice",
            "correct_answer": "on HCP Terraform infrastructure with results streamed back to your terminal",
            "domain": "Objective 8 - HCP Terraform",
            "objective": "8a - Use HCP Terraform to create infrastructure",
            "result": "correct",
            "explanation": "CLI-driven + HCP Terraform = remote operations by default. Config uploaded to HCP Terraform, plan/apply runs there, output streamed back to terminal. Enables policy checks and cost estimation.",
            "all_options": {
                "A": "on a self-hosted agent you must configure in workspace settings",
                "B": "on HCP Terraform infrastructure with results streamed to terminal ✓",
                "C": "on your local machine with no HCP Terraform interaction",
                "D": "locally on your machine, then results uploaded to HCP Terraform"
            },
            "key_takeaway": "HCP Terraform CLI-driven: plan/apply run REMOTELY on HCP infra, streamed to your terminal."
        },

        50: {
            "question": "You added resources from a new provider and terraform plan returns an error regarding the provider. What should you do first?",
            "type": "multiple_choice",
            "correct_answer": "since a new provider has been introduced, terraform init needs to be run to download the new plugin",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2a - Install and version Terraform providers",
            "result": "incorrect",
            "user_answer": "since a new provider has been introduced, adding it to required_providers is sufficient",
            "explanation": "Adding to required_providers is necessary but NOT sufficient. You MUST run terraform init to download the plugin. Same applies when: adding a new provider, updating provider config, updating version, adding/removing modules.",
            "all_options": {
                "A": "Can't mix resources from different providers in same file ✗",
                "B": "Adding to required_providers is sufficient, no init needed ✗",
                "C": "Run terraform init to download the new plugin ✓",
                "D": "Run terraform validate to download plugin and verify config ✗"
            },
            "key_takeaway": "New provider added → MUST run terraform init to download the plugin. Declaration alone is not enough."
        },

        51: {
            "question": "You configure two aws provider blocks and get 'Error: Duplicate provider configuration'. Which argument must you add to the second provider block?",
            "type": "multiple_choice",
            "correct_answer": "alias",
            "domain": "Objective 2 - Terraform Fundamentals",
            "objective": "2c - Write Terraform configuration using multiple providers",
            "result": "correct",
            "explanation": "alias meta-argument distinguishes multiple configurations of the same provider. Resources using the aliased provider must specify provider = aws.alias_name.",
            "all_options": {
                "A": "locals  → not for provider blocks",
                "B": "alias  → CORRECT ✓",
                "C": "version  → specifies version constraints",
                "D": "profile  → specifies AWS credential profile"
            },
            "key_takeaway": "Multiple same-provider configs: add alias to secondary blocks. Reference: provider = aws.<alias>"
        },

        52: {
            "question": "Why is state locking necessary when using a remote backend?",
            "type": "multiple_choice",
            "correct_answer": "prevents concurrent runs from writing to the same state at the same time to avoid state corruption.",
            "domain": "Objective 6 - Terraform State Management",
            "objective": "6b - Describe state locking",
            "result": "correct",
            "explanation": "State locking prevents concurrent writes that would corrupt the state file. Happens automatically for all operations that could write state. Terraform does not continue if locking fails.",
            "all_options": {
                "A": "prevents concurrent runs from writing simultaneously → avoid corruption ✓",
                "B": "caches state data on backend server for faster plan/apply",
                "C": "encrypts state file at rest and in transit",
                "D": "automatically rolls back partial changes if apply fails"
            },
            "key_takeaway": "State locking = prevent concurrent writes = prevent corruption. Automatic for write operations."
        },

        53: {
            "question": "Your team's reusable web server module must always create exactly two instances. You want Terraform to fail if any other value is used. Which approach?",
            "type": "multiple_choice",
            "correct_answer": "Add a validation block that checks the variable equals 2 and provides an error message if it does not.",
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4g - Validate configuration using custom conditions",
            "result": "correct",
            "explanation": "validation { condition = var.instance_count == 2; error_message = '...' } enforces exact value. Runs during plan/validate, fails immediately with clear message.",
            "all_options": {
                "A": "Set default to 2 in variables.tf  → user can still override",
                "B": "Use count meta-argument to force 2  → no validation",
                "C": "Add validation block checking variable equals 2 ✓",
                "D": "Rely on number type and document in README  → no enforcement"
            },
            "key_takeaway": "Enforce exact values: validation block with condition = var.x == 2. Fails before any resources created."
        },

        54: {
            "question": "What are some advantages of using Infrastructure as Code in an organization? (select three)",
            "type": "multi_select",
            "correct_answer": [
                "IaC allows you to save your configurations in version control, enabling safe collaboration on infrastructure.",
                "IaC uses a human-readable configuration language to help you write infrastructure code quickly.",
                "IaC code can be used to manage infrastructure on multiple cloud platforms."
            ],
            "domain": "Objective 1 - Infrastructure as Code (IaC) with Terraform",
            "objective": "1b - Describe the advantages of IaC patterns",
            "result": "correct",
            "explanation": "IaC advantages: version control + collaboration, human-readable language, multi-cloud platform support. IaC is DECLARATIVE, not imperative (common misconception).",
            "all_options": {
                "A": "Version control enables safe collaboration ✓",
                "B": "Human-readable configuration language ✓",
                "C": "IaC is written as imperative approach ✗ (IaC is DECLARATIVE)",
                "D": "Manage infrastructure on multiple cloud platforms ✓"
            },
            "key_takeaway": "IaC = declarative (NOT imperative), version-controlled, human-readable, multi-cloud."
        },

        55: {
            "question": "Where is this module stored?\nmodule \"vault-aws-tgw\" { source = \"terraform-aws-modules/transit-gateway/aws\", version = \"3.0.3\" }",
            "type": "multiple_choice",
            "correct_answer": "the Terraform public registry",
            "domain": "Objective 5 - Terraform Modules",
            "objective": "5a - Explain how Terraform sources modules",
            "result": "correct",
            "explanation": "Format <namespace>/<module>/<provider> (e.g., terraform-aws-modules/transit-gateway/aws) indicates Terraform public registry. Private registry adds hostname prefix.",
            "all_options": {
                "A": "in an HCP Terraform private registry",
                "B": "the Terraform public registry ✓",
                "C": "in a local file under a directory named terraform-aws-modules/...",
                "D": "a local code repository on your network"
            },
            "key_takeaway": "Module source formats: ./local, namespace/module/provider (public registry), hostname/org/module/provider (private registry)."
        },

        56: {
            "question": "Which code snippet enables you to query information about existing resources and use that information within your configuration?",
            "type": "multiple_choice",
            "correct_answer": 'data "aws_ami" "btk-app" {\n  most_recent = true\n  owners      = ["self"]\n  filter { name = "tag:Owner", values = ["btk-platform"] }\n}',
            "domain": "Objective 4 - Terraform Configuration",
            "objective": "4a - Use and differentiate resource and data blocks",
            "result": "correct",
            "explanation": "data blocks query existing resources/APIs (read-only). resource blocks create resources. locals define values. provider blocks configure providers. module blocks call modules.",
            "all_options": {
                "A": "locals { service_name = ... }  → local values",
                "B": "provider \"google\" { ... }  → provider config",
                "C": "module \"deploy-bk-servers\" { ... }  → module call",
                "D": 'data "aws_ami" "btk-app" { ... }  → query existing resource ✓',
                "E": "resource \"aws_instance\" { ... }  → creates resource"
            },
            "key_takeaway": "data block = query/read existing resources. Only data blocks are read-only resource queries."
        },

        57: {
            "question": "Aside from traditional code reviews, which Terraform command provides an opportunity for team members to review each other's work before deployment?",
            "type": "multiple_choice",
            "correct_answer": "terraform plan",
            "domain": "Objective 3 - Core Terraform Workflow",
            "objective": "3a - Describe the Terraform workflow",
            "result": "correct",
            "explanation": "terraform plan generates a human-readable execution plan showing what changes will be made. Teams can review this output before applying, catching mistakes early.",
            "all_options": {
                "A": "terraform apply  → immediately applies changes",
                "B": "terraform validate  → syntax check only, no proposed changes shown",
                "C": "terraform plan  → shows proposed changes for review ✓",
                "D": "terraform output  → shows output values only"
            },
            "key_takeaway": "terraform plan output = review opportunity. Shows adds/changes/destroys before apply."
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # EXAM SUMMARY BY DOMAIN
    # ─────────────────────────────────────────────────────────────────────────
    "domain_summary": {
        "Objective 1 - IaC with Terraform":         ["Q2", "Q18", "Q41", "Q54"],
        "Objective 2 - Terraform Fundamentals":      ["Q17", "Q21", "Q33", "Q46", "Q50", "Q51"],
        "Objective 3 - Core Terraform Workflow":     ["Q1", "Q10", "Q24", "Q27", "Q28", "Q35", "Q36", "Q37", "Q57"],
        "Objective 4 - Terraform Configuration":     ["Q4", "Q5", "Q7", "Q12", "Q13", "Q20", "Q22", "Q29", "Q30", "Q42", "Q45", "Q53", "Q56"],
        "Objective 5 - Terraform Modules":           ["Q8", "Q14", "Q15", "Q26", "Q39", "Q43", "Q48", "Q55"],
        "Objective 6 - State Management":            ["Q9", "Q25", "Q32", "Q34", "Q38", "Q47", "Q52"],
        "Objective 7 - Maintain Infrastructure":     ["Q3", "Q6", "Q11", "Q23", "Q44"],
        "Objective 8 - HCP Terraform":               ["Q16", "Q19", "Q31", "Q40", "Q49"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # FREQUENTLY MISSED QUESTIONS (result = incorrect)
    # ─────────────────────────────────────────────────────────────────────────
    "missed_questions": {
        "Q11": {
            "mistake": "Answered TF_DEBUG instead of TF_LOG",
            "correct":  "TF_LOG=TRACE|DEBUG|INFO|WARN|ERROR",
            "rule":     "TF_LOG is the only valid Terraform logging env variable"
        },
        "Q12": {
            "mistake": "Chose object() instead of map(string) for region → AMI lookup",
            "correct":  "map(string) for key-value lookups. Access: var.image[var.region]",
            "rule":     "map = key-value lookup. object = predefined fixed structure"
        },
        "Q17": {
            "mistake": "Missed 'existing state records' as a provider dependency method",
            "correct":  "3 ways: provider block, resource/data block, OR existing state records",
            "rule":     "Provider dependency can come from current state, not just new config"
        },
        "Q25": {
            "mistake": "Selected 'prevents Terraform from reading state' as a reason",
            "correct":  "Real reasons: plaintext secrets + no VCS locking = concurrent corruption",
            "rule":     "Committing state doesn't break Terraform. It's a security + locking issue"
        },
        "Q36": {
            "mistake": "Chose 'removed blocks' instead of removing resource blocks",
            "correct":  "Remove resource blocks from config + terraform apply = selective destroy",
            "rule":     "removed blocks = refactoring/renaming. Delete block + apply = destroy"
        },
        "Q38": {
            "mistake": "Selected 'local state is best for multi-user teams (auto-merge)'",
            "correct":  "Local = no locking, no sharing. Remote = team-ready",
            "rule":     "Terraform does NOT auto-merge state. VCS has no state locking"
        },
        "Q41": {
            "mistake": "Chose 'mutable, declarative' instead of 'immutable, declarative'",
            "correct":  "Terraform is IMMUTABLE + DECLARATIVE + HCL or JSON",
            "rule":     "Terraform immutable infra principles: replaces, doesn't mutate in place"
        },
        "Q44": {
            "mistake": "Selected 'terraform state show can show multiple resources with commas'",
            "correct":  "terraform state show only shows ONE resource at a time",
            "rule":     "terraform show = all resources. terraform state show = exactly one"
        },
        "Q47": {
            "mistake": "Chose -migrate-state instead of -reconfigure",
            "correct":  "terraform init -reconfigure = no state copy. -migrate-state = copy state",
            "rule":     "reconfigure = fresh backend setup. migrate-state = move existing state"
        },
        "Q50": {
            "mistake": "Thought adding to required_providers was sufficient for new provider",
            "correct":  "Must run terraform init to download plugin after declaring provider",
            "rule":     "Declaration tells Terraform WHAT to use. init actually DOWNLOADS it"
        }
    }
}


if __name__ == "__main__":
    # Print summary stats
    total = len(exam3["questions"])
    correct = sum(1 for q in exam3["questions"].values() if q.get("result") == "correct")
    incorrect = sum(1 for q in exam3["questions"].values() if q.get("result") == "incorrect")
    skipped = sum(1 for q in exam3["questions"].values() if q.get("result") == "skipped")

    print(f"{'='*60}")
    print(f"  Terraform Associate 004 - Exam #3 Results")
    print(f"{'='*60}")
    print(f"  Total Questions : {total}")
    print(f"  Correct         : {correct}")
    print(f"  Incorrect       : {incorrect}")
    print(f"  Skipped         : {skipped}")
    print(f"  Score           : {correct}/{total} ({correct/total*100:.1f}%)")
    print(f"{'='*60}")
    print()
    print("Missed Questions:")
    for qnum, details in exam3["missed_questions"].items():
        print(f"  {qnum}: {details['mistake']}")
        print(f"       → {details['rule']}")
