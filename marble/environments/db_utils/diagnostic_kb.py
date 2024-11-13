import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
import re
from collections import defaultdict

@dataclass
class Diagnostic:
    cause_name: str
    desc: str
    metrics: str
    source_file: str

class DiagnosticKB:
    """
    Available Experts (folder names):
    - ConfigurationExpert
    - CpuExpert
    - DiskExpert
    - IndexExpert
    - IoExpert
    - MemoryExpert
    - QueryExpert
    - RecoveryExpert
    - WorkloadExpert
    """
    
    def __init__(self, base_folder: str = ''):
        """Initialize knowledge base from a folder containing expert subdirectories"""
        if not base_folder:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            knowledge_base_dir = os.path.join(current_dir, 'knowledge_base')
            self.base_folder = knowledge_base_dir  
        else:
            self.base_folder = base_folder
            
        if not os.path.exists(self.base_folder):
            raise ValueError(f"Knowledge base directory not found at {self.base_folder}")
            
        self.diagnostics: List[Diagnostic] = []
        self.cause_to_diagnostic: Dict[str, Diagnostic] = {}
        self.load_documents()
    
    def get_experts(self) -> List[str]:
        """Get list of all expert names (folder names)"""
        return [d for d in os.listdir(self.base_folder) 
                if os.path.isdir(os.path.join(self.base_folder, d))]
    
    def load_documents(self):
        """Load all JSON documents from expert subdirectories"""
        self.diagnostics = []
        self.cause_to_diagnostic = {}
        
        for root, dirs, files in os.walk(self.base_folder):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            diagnoses = json.load(f)
                            for diag in diagnoses:
                                if diag['cause_name'] not in self.cause_to_diagnostic:
                                    diagnostic = Diagnostic(
                                        cause_name=diag['cause_name'],
                                        desc=diag['desc'],
                                        metrics=diag['metrics'],
                                        source_file=file_path
                                    )
                                    self.diagnostics.append(diagnostic)
                                    self.cause_to_diagnostic[diag['cause_name']] = diagnostic
                    except json.JSONDecodeError as e:
                        print(f"Error loading {file_path}: {e}")

    def search(self, query: str, expert: str = '', top_k: int = 3) -> List[Dict]:
        """
        Search diagnostics using keyword matching with improved relevance scoring
        Args:
            query: Search terms
            expert: Specific expert to search from (e.g., 'CpuExpert'). Empty string means search all.
            top_k: Maximum number of results to return
        """
        def calculate_relevance(diagnostic: Diagnostic, search_terms: List[str]) -> tuple:
            text = f"{diagnostic.cause_name} {diagnostic.desc} {diagnostic.metrics}".lower()
            
            scores = {
                'cause_name': 0,
                'desc': 0,
                'metrics': 0
            }
            
            for term in search_terms:
                term = term.lower()
                scores['cause_name'] += len(re.findall(r'\b' + re.escape(term) + r'\b', 
                                                     diagnostic.cause_name.lower())) * 3
                scores['metrics'] += len(re.findall(r'\b' + re.escape(term) + r'\b', 
                                                  diagnostic.metrics.lower())) * 2
                scores['desc'] += len(re.findall(r'\b' + re.escape(term) + r'\b', 
                                               diagnostic.desc.lower()))
            
            total_score = sum(scores.values())
            return (total_score, scores['cause_name'])

        search_terms = [term.strip() for term in query.split() if term.strip()]
        
        if not search_terms:
            return []

        # Filter diagnostics by expert if specified
        diagnostics_to_search = self.diagnostics
        if expert:
            expert_path = os.path.join(self.base_folder, expert)
            diagnostics_to_search = [
                diag for diag in self.diagnostics 
                if diag.source_file.startswith(expert_path)
            ]
            
            if not diagnostics_to_search:
                print(f"Warning: No diagnostics found for expert '{expert}'")
                return []

        scored_results = [
            (diag, *calculate_relevance(diag, search_terms))
            for diag in diagnostics_to_search
        ]
        
        scored_results.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        results = []
        seen_causes = set()
        
        for diag, total_score, _ in scored_results:
            if total_score > 0 and diag.cause_name not in seen_causes:
                seen_causes.add(diag.cause_name)
                results.append({
                    'cause_name': diag.cause_name,
                    'desc': diag.desc,
                    'metrics': diag.metrics.split('\n'),
                    'score': total_score,
                    'source': diag.source_file,
                    'expert': os.path.basename(os.path.dirname(os.path.dirname(diag.source_file)))
                })
                
                if len(results) >= top_k:
                    break
        
        return results

    def get_diagnostic_by_cause(self, cause_name: str) -> Optional[Dict]:
        """Get specific diagnostic by cause name"""
        diag = self.cause_to_diagnostic.get(cause_name)
        if diag:
            return {
                'cause_name': diag.cause_name,
                'desc': diag.desc,
                'metrics': diag.metrics.split('\n'),
                'source': diag.source_file,
                'expert': os.path.basename(os.path.dirname(os.path.dirname(diag.source_file)))
            }
        return None
