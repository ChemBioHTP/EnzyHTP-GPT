#! python3
# -*- encoding: utf-8 -*-
'''
Three OpenAI Assistant Agents:
- Question Analyzer: Decomposing and Revising scientific questions for protein simulations. 
- Metrics Planner: An expert in planning "target computational metrics" based on a user-provided natural language description of "the property of interest of the protein".
- Mutant Planner: An expert in translating natural language descriptions of mutation plans into precise EnzyHTP syntax.

@File    :   agents.py
@Created :   2024/08/28 15:07
@Author  :   Zhong, Yinjie
@Contact :   yinjie.zhong@vanderbilt.edu
'''

# Here put the import lib.
from os import path
import re
from pathlib import Path
from string import Template
from json import load, loads, dumps
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated
from datetime import datetime

from config import BASEDIR, OPENAI_MODEL_VERSION
from services import OpenAIAssistant

from .agent_tool_functions import TOOL_FUNCTION_MAPPER
from .analysis import METRICS_MAPPER
from .models import Experiment, Result

from enzy_htp import PDBParser
from enzy_htp.core import _LOGGER, file_system as fs
from enzy_htp.structure import Residue
from enzy_htp.mutation.mutation_pattern import decode_position_pattern

PROMPTS_DIRECTORY = path.join(BASEDIR, "prompts")
MODEL_VERSION = OPENAI_MODEL_VERSION
EQUILIBRATION_METHOD_LABEL = "Chodera automated equilibration detection scheme (PMCID: PMC4945107)"
SIMULATION_ENGINE_LABEL = "Amber"
DEFAULT_TEMPERATURE_K = 300
DEFAULT_EQUILIBRATION_LENGTH_NS = 1.0
DEFAULT_FORCE_FIELD_LABEL = "ff14SB+GAFF"
DEFAULT_SOLVENT_MODEL_LABEL = "TIP3P"

class QuestionAnalyzerAssistant(OpenAIAssistant):
    """The agent acting as a Question Analyzer."""
    
    experiment: Experiment
    completion_message: str = "Question Confirmed!"

    def __init__(
        self,
        openai_secret_key: str,
        thread_id: str = str(),
        conversation_mode: bool = False,
        experiment: Experiment = None,
        model: str = MODEL_VERSION,
        base_url: str = None,
    ) -> None:
        """
        Initializes the QuestionAnalyzerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()

        with open(path.join(PROMPTS_DIRECTORY, "question_analyzer-v5.txt")) as fobj:
            instructions = fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "question_analyzer_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Question Analyzer", 
            instructions=instructions, 
            model=model,
            base_url=base_url,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )

class MetricsPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Metrics Planner."""
    
    experiment: Experiment
    completion_message: str = "Computational Details Confirmed!"

    def __init__(
        self,
        openai_secret_key: str,
        thread_id: str = str(),
        conversation_mode: bool = False,
        experiment: Experiment = None,
        model: str = MODEL_VERSION,
        base_url: str = None,
    ) -> None:
        """
        Initializes the MetricsPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()

        with open(path.join(PROMPTS_DIRECTORY, "metrics_planner-v3.txt")) as txt_fobj:
            instructions = txt_fobj.read()
            with open(path.join(PROMPTS_DIRECTORY, "supported_metrics_reference.txt")) as ref_fobj:
                metrics_reference_text = ref_fobj.read()
                instructions = Template(instructions).safe_substitute({
                    "REPLACEMARK": metrics_reference_text,
                }) 
        with open(path.join(PROMPTS_DIRECTORY, "metrics_planner_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Metrics Planner", 
            instructions=instructions, 
            model=model,
            base_url=base_url,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )

    def pre_process(self, input_prompt: str):
        """Process the input prompt before sending to Metrics Planner Agent.
        
        Args:
            input_prompt (str): The input prompt to be processed.

        Returns:
            str: The processed prompt text.
        """
        pre_process_template = "Please use the following information to config metrics, and print the compiled information in json format. \n$summary"
        processed_prompt = Template(pre_process_template).safe_substitute({
            "summary": input_prompt,
        })
        return processed_prompt
        
    def post_process(self, response_content: str, is_finishing: bool) -> str:
        """Process the `response_content` from the agent.

        Args:
            response_content (str): The response from GPT.
            is_finishing (bool): A flag indicating if the job of current agent can be completed.
        
        Returns:
            processed_response_content (str): The response content after process.
        """
        initial_processed_response_content = super().post_process(response_content, is_finishing)

        processed_response_content = initial_processed_response_content
        # Why yinjie put these lines here?
        # processed_response_content = initial_processed_response_content.replace(
        #     "substrate_selection_pattern", "ligand"
        # )
        # processed_response_content = processed_response_content.replace(
        #     "ligand_selection_pattern", "ligand"
        # )
        # processed_response_content = processed_response_content.replace(
        #     "pocket_selection_pattern", "region_pattern"
        # )

        editable_attrs = ["metrics", "constraints"]
        is_matched = False
        matched_head = str()
        match_results: List[str] = list()

        match_rule_heads = ["```\n", "```json\n"]
        match_rule_tail = "\n```"
        
        for head in match_rule_heads:
            match_rule = fr"{head}(.*?){match_rule_tail}"
            match_results = re.search(match_rule, processed_response_content, re.DOTALL)
            if (match_results):
                is_matched = True
                matched_head = head
                break
            continue
        
        if (is_matched):
            json_text = match_results[0].replace(matched_head, "").replace(match_rule_tail, "")
            configuration_mapper: Dict[str, Any] = loads(json_text)

            updated_attrs, blocked_attrs, nonexistent_attrs, message = self.experiment.update_attributes(mapper=configuration_mapper, editable_attrs=editable_attrs)
            # return True, updated_attrs
        else:
            # _LOGGER.info("Not matched results.")
            # return False, list()
            pass
        return processed_response_content

class MutantPlannerAssistant(OpenAIAssistant):
    """The agent acting as a Mutant Planner."""
    
    experiment: Experiment
    completion_message: str = "Experiment has been set up successfully!"

    def __init__(
        self,
        openai_secret_key: str,
        thread_id: str = str(),
        conversation_mode: bool = False,
        experiment: Experiment = None,
        model: str = MODEL_VERSION,
        base_url: str = None,
    ) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()
        with open(path.join(PROMPTS_DIRECTORY, "mutant_planner-v3.txt")) as fobj:
            instructions = fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "mutant_planner_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Mutant Planner", 
            instructions=instructions, 
            model=model,
            base_url=base_url,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )
    
    def pre_process(self, input_prompt: str):
        """Process the input prompt before sending to Mutant Planner Agent.
        
        Args:
            input_prompt (str): The input prompt to be processed.

        Returns:
            str: The processed prompt text.
        """
        input_prompt = super().pre_process(input_prompt)
        pattern = "Mutations: (.+)\n"
        mutation_request = re.search(pattern, input_prompt, re.DOTALL)
        if (mutation_request is not None):
            return mutation_request[0].replace("Mutations:", "Input:").replace("\n", "")
        else:
            return input_prompt
        

    def post_process(self, response_content: str, is_finishing: bool) -> str:
        """Process the `response_content` from the agent.

        Args:
            response_content (str): The response from GPT.
            is_finishing (bool): A flag indicating if the job of current agent can be completed.
        
        Returns:
            processed_response_content (str): The response content after process.
        """
        # remember we want to be able to hide output from user
        # initial_processed_response_content = super().post_process(response_content, is_finishing)
        
        response_content = response_content.replace(    # The output interface is updated with Mutant Planner V3.
            "output", "mutation_pattern"
        ).replace(
            "Output", "mutation_pattern"
        )
        re_pattern = '"mutation_pattern"\s*:\s*"*(.+)"'
        processed_response_content = response_content
        pattern_results: List[str] = re.findall(re_pattern, response_content)
        if (pattern_results):
            mutation_pattern = pattern_results[0]
            self.experiment.update_mutation_pattern(mutation_pattern=mutation_pattern)
            mutation_explainer_agent = MutationPatternExplainer(
                openai_secret_key=self.client.api_key,
                experiment=self.experiment,
                model=self.model,
                base_url=str(self.client.base_url),
            )
            is_valid, status_code, mutation_explanation = mutation_explainer_agent.ask_gpt(mutation_pattern)
            processed_response_content = f"{response_content}\n{mutation_explanation}"
            processed_response_content = f"Please confirm the mutations you want:\n```txt\n{mutation_pattern}\n```\n{mutation_explanation}"
        else:
            pass
        # pattern = "mutation_pattern: *(.+)"
        # initial_processed_response_content = initial_processed_response_content.strip("`")
        # if is_finishing or initial_processed_response_content.startswith("Output"):
        #     try:
        #         mutation_pattern = re.match(pattern, initial_processed_response_content).group(1).strip("\"")
        #         result_dict = {
        #             "mutation_pattern": mutation_pattern
        #         }
        #         processed_response_content = f"```json\n{dumps(result_dict)}\n```"
        #         return processed_response_content
        #     except Exception as exc:
        #         _LOGGER.error(f"Failed to process `response_content`: {exc}")
        #         return response_content
        # else:
        #     self.detect_vicious_output(initial_processed_response_content)  # This is about detecting potential attach, we will finish this when need it.
        #     processed_response_content = initial_processed_response_content   # by default result as is after stripping
        #     return processed_response_content
        return processed_response_content

class MutationPatternExplainer(OpenAIAssistant):
    """The agent explains the mutation pattern to natural language."""
    
    experiment: Experiment

    def __init__(
        self,
        openai_secret_key: str,
        thread_id: str = str(),
        conversation_mode: bool = False,
        experiment: Experiment = None,
        model: str = MODEL_VERSION,
        base_url: str = None,
    ) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()
        with open(path.join(PROMPTS_DIRECTORY, "mutation_pattern_explainer.txt")) as fobj:
            instructions = fobj.read()
        super().__init__(openai_secret_key, 
            assistant_name="Mutation Pattern Explainer", 
            instructions=instructions, 
            model=model,
            base_url=base_url,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )
        return

class ResultExplainerAssistant(OpenAIAssistant):
    """The agent acting as a Result Explainer."""
    
    experiment: Experiment
    # completion_message: str = "Experiment has been set up successfully!"
    
    scientific_question: str
    metrics: List[dict]
    results: List[dict]
    metadata: dict
    downloadables: List[dict]
    DOWNLOADABLE_SUMMARY_ROOTS: Tuple[str, ...] = ("plots/equilibration", "trajectories")

    def _iter_experiment_result_directories(self) -> List[str]:
        if (not self.experiment):
            return list()
        directories: List[str] = [self.experiment.directory]
        if (self.experiment.type == Experiment.GROUP_TYPE):
            for sub_experiment in self.experiment.subordinate_experiments:
                if (sub_experiment and sub_experiment.directory):
                    directories.append(sub_experiment.directory)
        # Deduplicate while preserving order.
        seen = set()
        unique_directories: List[str] = []
        for directory in directories:
            if (not directory) or (directory in seen):
                continue
            seen.add(directory)
            unique_directories.append(directory)
        return unique_directories

    @staticmethod
    def _median(values: List[float]) -> Optional[float]:
        if (not values):
            return None
        sorted_values = sorted(values)
        length = len(sorted_values)
        mid = length // 2
        if (length % 2 == 1):
            return float(sorted_values[mid])
        return float((sorted_values[mid - 1] + sorted_values[mid]) / 2.0)

    def _collect_equilibration_assessment_records(self) -> List[dict]:
        records: List[dict] = []
        for experiment_dir in self._iter_experiment_result_directories():
            equilibration_dir = path.join(experiment_dir, "plots", "equilibration")
            if (not path.isdir(equilibration_dir)):
                continue
            for json_path in sorted(Path(equilibration_dir).rglob("*equil_assessment*.json")):
                if (not json_path.is_file()):
                    continue
                try:
                    with open(json_path, "r", encoding="utf-8") as fobj:
                        record = load(fobj)
                    if (isinstance(record, dict)):
                        records.append(record)
                except Exception as exc:
                    _LOGGER.warning("Failed to load equilibration assessment file %s: %s", json_path, exc)
                    continue
        return records

    def _build_equilibration_metadata(self) -> Dict[str, Any]:
        records = self._collect_equilibration_assessment_records()
        if (not records):
            return {
                "equilibration_method": EQUILIBRATION_METHOD_LABEL,
                "equilibration_assessment": "No automated equilibration assessment was found in uploaded ACCRE artifacts.",
                "equilibration_summary": {
                    "n_replica_assessments": 0,
                    "n_equilibrated_replicas": 0,
                    "series_status_counts": {},
                },
            }

        n_replica_assessments = len(records)
        n_equilibrated_replicas = sum(1 for record in records if record.get("overall_status") == "equilibrated")
        series_status_counts: Dict[str, Dict[str, int]] = dict()
        for record in records:
            series_mapper = record.get("series", {})
            if (not isinstance(series_mapper, dict)):
                continue
            for series_key, series_info in series_mapper.items():
                if (not isinstance(series_info, dict)):
                    continue
                status = str(series_info.get("status", "unknown"))
                series_counts = series_status_counts.setdefault(series_key, dict())
                series_counts[status] = series_counts.get(status, 0) + 1

        assessment_sentence = (
            f"{n_equilibrated_replicas}/{n_replica_assessments} replica assessments were marked equilibrated "
            f"by {EQUILIBRATION_METHOD_LABEL}."
        )

        return {
            "equilibration_method": EQUILIBRATION_METHOD_LABEL,
            "equilibration_assessment": assessment_sentence,
            "equilibration_summary": {
                "n_replica_assessments": n_replica_assessments,
                "n_equilibrated_replicas": n_equilibrated_replicas,
                "series_status_counts": series_status_counts,
            },
        }

    def _count_variants(self) -> int:
        variant_keys = set()
        for result_item in self.results:
            if (not isinstance(result_item, dict)):
                continue
            wt_path = str(result_item.get("wt_path", ""))
            mutant = str(result_item.get("mutant", "WT"))
            variant_keys.add((wt_path, mutant))
        return len(variant_keys)

    def _estimate_replicas_per_variant(self, n_variants: int, equilibration_summary: Dict[str, Any]) -> Optional[int]:
        if (not self.experiment):
            return None

        raw_results = Result.get_experiment_raw_results(experiment_id=self.experiment.id)
        replicas_by_variant: Dict[Tuple[str, str], set] = dict()
        for raw_result in raw_results:
            if (not isinstance(raw_result, dict)):
                continue
            wt_path = str(raw_result.get("pdb_filename", ""))
            mutant = str(raw_result.get("mutant", "WT"))
            key = (wt_path, mutant)
            replica_set = replicas_by_variant.setdefault(key, set())
            replica_id = raw_result.get("replica_id", None)
            if (replica_id is not None) and (str(replica_id) != ""):
                replica_set.add(str(replica_id))

        replica_counts = [len(replica_ids) for replica_ids in replicas_by_variant.values() if replica_ids]
        if (replica_counts):
            median_count = self._median([float(count) for count in replica_counts])
            if (median_count is not None):
                return max(1, int(round(median_count)))

        n_replica_assessments = equilibration_summary.get("n_replica_assessments", 0)
        if (
            isinstance(n_replica_assessments, int)
            and (n_replica_assessments > 0)
            and (n_variants > 0)
        ):
            return max(1, int(round(n_replica_assessments / n_variants)))
        return None

    @staticmethod
    def _summarize_files_by_basename(file_paths: List[str]) -> List[Dict[str, Union[str, int]]]:
        basename_counts: Dict[str, int] = dict()
        for relpath in file_paths:
            basename = path.basename(str(relpath))
            if (not basename):
                continue
            basename_counts[basename] = basename_counts.get(basename, 0) + 1
        return [
            {
                "filename": filename,
                "count": count,
            }
            for filename, count in sorted(basename_counts.items(), key=lambda item: item[0])
        ]

    def _build_downloadables_payload(self, file_paths: List[str]) -> List[dict]:
        summary_buckets: Dict[str, List[str]] = {
            root: list() for root in self.DOWNLOADABLE_SUMMARY_ROOTS
        }
        direct_entries: List[dict] = list()

        for raw_file_path in file_paths:
            relpath = str(raw_file_path).replace("\\", "/")
            matched_root = None
            for root in self.DOWNLOADABLE_SUMMARY_ROOTS:
                if (relpath == root) or relpath.startswith(f"{root}/"):
                    matched_root = root
                    break
            if matched_root:
                summary_buckets[matched_root].append(relpath)
                continue
            direct_entries.append(
                {
                    "file_type": fs.get_file_ext(relpath),
                    "filename": relpath,
                }
            )

        summary_entries: List[dict] = list()
        for root in self.DOWNLOADABLE_SUMMARY_ROOTS:
            matched_files = summary_buckets.get(root, list())
            if (not matched_files):
                continue
            filename_summaries = self._summarize_files_by_basename(matched_files)
            summary_entries.append(
                {
                    "file_type": "summary",
                    "filename": root,
                    "summary_type": "filename_count",
                    "total_files": len(matched_files),
                    "unique_filenames": len(filename_summaries),
                    "files": filename_summaries,
                }
            )

        return direct_entries + summary_entries

    def __init__(
        self,
        openai_secret_key: str,
        thread_id: str = str(),
        conversation_mode: bool = False,
        experiment: Experiment = None,
        model: str = MODEL_VERSION,
        base_url: str = None,
    ) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()
        with open(path.join(PROMPTS_DIRECTORY, "result_explainer-v2.txt")) as fobj:
            instructions = fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "result_explainer_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Result Explainer", 
            instructions=instructions, 
            model=model,
            base_url=base_url,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )
        self.scientific_question = experiment.scientific_question

        self.metrics = list()
        with open(path.join(PROMPTS_DIRECTORY, "result_explainer_metrics.json")) as json_fobj:
            metrics_pool: List[dict] = load(json_fobj)
            metric_names = [metric["name"] for metric in experiment.metrics]
            for metric in metrics_pool:
                if (metric["name"] in metric_names):
                    self.metrics.append(metric)
                else:
                    pass
                continue

        self.results = list()
        for exp_result in Result.get_experiment_results(experiment_id=experiment.id):
            metric_schema = {
                "wt_path": exp_result.get("pdb_filename", str()),
                "mutant": exp_result.get("mutant", "WT"),
            }
            for result_key, result_value in exp_result.items():
                if (result_key in METRICS_MAPPER):
                    metric = metric_schema.copy()
                    metric["metric"] = result_key
                    metric["value"] = result_value
                    self.results.append(metric)
                else:
                    pass
                continue
        self.downloadables = self._build_downloadables_payload(experiment.downloadable_files)
        equilibration_metadata = self._build_equilibration_metadata()
        equilibration_summary = equilibration_metadata.get("equilibration_summary", {})
        n_variants = self._count_variants()
        n_replicas_per_variant = self._estimate_replicas_per_variant(
            n_variants=n_variants,
            equilibration_summary=equilibration_summary if isinstance(equilibration_summary, dict) else {},
        )

        self.metadata = {
            "simulation_engine": SIMULATION_ENGINE_LABEL,
            "temperature_K": DEFAULT_TEMPERATURE_K,
            "md_production_length_in_ns": experiment.md_length if experiment else None,
            "date": str(datetime.now()),
            "n_variants": n_variants,
            "n_replicas_per_variant": n_replicas_per_variant,
            "equilibration_length_in_ns": DEFAULT_EQUILIBRATION_LENGTH_NS,
            "force_field": DEFAULT_FORCE_FIELD_LABEL,
            "solvent_model": DEFAULT_SOLVENT_MODEL_LABEL,
            **equilibration_metadata,
        }
        return
    
    def ask_gpt(self):
        """Ask GPT for analysis of the experiment. The prompt is formulated automatically.

        Returns:
            is_valid (bool): Whether the API key is valid.
            status_code (int): The HTTP status code from the API response.
            response_content (str): The actual response from GPT or an error message.
        """
        prompt_dict = {
            "scientific_question": self.scientific_question,
            "metrics": self.metrics,
            "results": self.results,
            "downloadables": self.downloadables,
            "metadata": self.metadata,
        }
        prompt = dumps(prompt_dict)
        experiment_id = self.experiment.id if self.experiment else "unknown"
        _LOGGER.info(
            "ResultExplainer prompt payload (experiment_id=%s): %s",
            experiment_id,
            prompt,
        )
        return super().ask_gpt(prompt)

class QuestionSummarizerAssistant(OpenAIAssistant):
    """The agent acting as a Question Summarizer."""
    
    experiment: Experiment

    def __init__(
        self,
        openai_secret_key: str,
        thread_id: str = str(),
        conversation_mode: bool = False,
        experiment: Experiment = None,
        model: str = MODEL_VERSION,
        base_url: str = None,
    ) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
            experiment (Experiment): The Experiment instance calling this assistant.
        """
        self.experiment = experiment
        instructions = str()
        tools = list()
        with open(path.join(PROMPTS_DIRECTORY, "question_summarizer.txt")) as fobj:
            instructions = fobj.read()
        with open(path.join(PROMPTS_DIRECTORY, "question_summarizer_functions.json")) as json_fobj:
            tool_functions: List[dict] = load(json_fobj)
            tools = [
                {
                    "type": "function",
                    "function": tool_function
                } for tool_function in tool_functions
            ]
        super().__init__(openai_secret_key, 
            assistant_name="Question Summarizer", 
            instructions=instructions, 
            model=model,
            base_url=base_url,
            tools=tools,
            tool_function_mapper=TOOL_FUNCTION_MAPPER,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
            tool_function_callable_kwargs={
                "experiment": experiment
            },
        )
        return

class TimezoneConsultantAssistant(OpenAIAssistant):
    """The agent acting as a Time Zone Consultant.
    The agent is for test use only.
    """

    def __init__(
        self,
        openai_secret_key: str,
        thread_id: str = str(),
        conversation_mode: bool = False,
        model: str = MODEL_VERSION,
        base_url: str = None,
    ) -> None:
        """
        Initializes the MutantPlannerAssistant agent with the OpenAI API key.

        Args:
            openai_secret_key (str): API key for accessing OpenAI services.
            thread_id (str, optional): The identifier of a context thread, which can be referenced in OpenAI API endpoints.
            conversation_mode (bool): If True, retains the conversation context. Default is False.
        """
        instructions = str()
        with open(path.join(PROMPTS_DIRECTORY, "timezone_consultant.txt")) as fobj:
            instructions = fobj.read()
        super().__init__(openai_secret_key, 
            assistant_name="Time Zone Consultant", 
            instructions=instructions, 
            model=model,
            base_url=base_url,
            thread_id=thread_id,
            conversation_mode=conversation_mode,
        )


AGENT_MAPPER = {
    # -1: TimezoneConsultantAssistant,
    0: QuestionAnalyzerAssistant,
    1: MetricsPlannerAssistant,
    2: MutantPlannerAssistant,
}

DefinedAgent = Annotated[
    Union[
        QuestionAnalyzerAssistant,
        MetricsPlannerAssistant,
        MutantPlannerAssistant,
        MutationPatternExplainer,
        ResultExplainerAssistant,
        QuestionSummarizerAssistant,
    ],
    "DefinedAgent",
]
