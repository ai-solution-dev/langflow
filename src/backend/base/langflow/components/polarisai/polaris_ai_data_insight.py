from typing import List
from langflow.inputs.inputs import DropdownInput, SecretStrInput, StrInput
from langflow.custom import Component
from langflow.io import Output, FileInput
from langflow.schema import Data
from langchain_polaris_ai_datainsight import PolarisAIDataInsightLoader

class PolarisAIDataInsightComponent(Component):
    name="polaris_ai_data_insight"
    display_name: str = "Polaris AI Data Insight"
    description: str = (
        "Load documents in various formats"
        "Supported file formats: `.doc`, `.docx`, `.ppt`, `.pptx`, `.xls`, `.xlsx`, `.hwp`, `.hwpx`"
    )
    documentation: str = "https://datainsight.polarisoffice.com/documentation"
    trace_type: str = "documentloaders"
    icon: str = "PolarisAI"

    inputs = [
        FileInput(
            name="file_path",
            display_name="File",
            info="The file to extract data from.",
            file_types=['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'hwp', 'hwpx'],
            required=True,
            temp_file=True,
        ),
        SecretStrInput(
            name="api_key", 
            display_name="API Key",
            required=True
        ),
        StrInput(
            name="resources_dir", 
            display_name="Directory For Resources", 
            value="tmp/",
            info=(
                "Directory to store resources. "
                "If the directory does not exist, it will be created."
            ),
            required=True
        ),        
        DropdownInput(
            name="mode",
            display_name="Loading Mode",
            options=["element", "page", "single"],
            value="single",
            info=(
                "Choose the loading mode:\n"
                "- `element`: Load each element separately.\n"
                "- `page`: Load each page separately.\n"
                "- `single`: Load the entire document as a single object."
            ),
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="Data", name="data", method="extract_document"),
    ]    
    
    def extract_document(self) -> List[Data]:
        loader = PolarisAIDataInsightLoader(
            file_path=self.file_path,
            api_key=self.api_key,
            resources_dir=self.resources_dir,
            mode=self.mode,
        )
        print("Loading documents...")
        print(loader.load())
        docs = [Data.from_document(doc) for doc in loader.lazy_load()]
        self.status = docs
        return docs
    