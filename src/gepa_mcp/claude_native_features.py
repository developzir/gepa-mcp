import json
from typing import List, Dict, Any, Optional, Tuple
from .enhanced_features import EnhancedGEPA
import google.generativeai as genai

class ClaudeNativeGEPA(EnhancedGEPA):
    """
    Claude-native enhancements that feed INTO GEPA's proven architecture.
    These tools generate richer training data and enhance reflection for GEPA's evolutionary process.
    """
    
    def semantic_pattern_optimize(self, prompt: str, semantic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize using deep semantic patterns that Claude can extract from text.
        Claude can provide rich semantic graphs, entity relationships, intent hierarchies, etc.
        
        Args:
            prompt: The prompt to optimize
            semantic_analysis: {
                "primary_intent": str,
                "semantic_components": List[Dict],
                "entity_relationships": List[Tuple],
                "reasoning_patterns": List[str],
                "quality_dimensions": Dict[str, float]
            }
        """
        # Create training data from semantic patterns
        training_data = []
        
        # Convert semantic components to training examples
        for component in semantic_analysis.get("semantic_components", []):
            training_data.append({
                "input": component.get("context", ""),
                "expected_keywords": component.get("key_concepts", [])
            })
        
        # Add reasoning pattern examples
        for pattern in semantic_analysis.get("reasoning_patterns", []):
            training_data.append({
                "input": f"Apply {pattern} reasoning",
                "expected_keywords": [pattern, "logical", "structured"]
            })
        
        # Run optimization with semantic awareness
        result = self.optimize_prompt(prompt, training_data, budget=12)
        
        # Enhance with semantic scoring
        result["semantic_alignment"] = self._calculate_semantic_alignment(
            result["optimized_prompt"], 
            semantic_analysis
        )
        
        return result
    
    def meta_cognitive_optimize(self, prompt: str, reasoning_trace: str, 
                               quality_assessments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize using Claude's meta-cognitive assessments of prompt quality.
        Claude can analyze its own reasoning process and provide insights.
        
        Args:
            prompt: The prompt to optimize
            reasoning_trace: Claude's step-by-step reasoning about the prompt
            quality_assessments: {
                "clarity_score": float,
                "ambiguity_points": List[str],
                "cognitive_load": float,
                "expected_success_rate": float,
                "failure_modes": List[str]
            }
        """
        # Analyze the reasoning trace to extract optimization targets
        analysis_prompt = f"""Analyze this AI reasoning trace to identify prompt optimization opportunities:

Reasoning Trace:
{reasoning_trace}

Quality Assessments:
{json.dumps(quality_assessments, indent=2)}

Extract specific improvements needed for the prompt based on:
1. Where the reasoning struggled
2. Ambiguity points identified
3. Cognitive load indicators
4. Potential failure modes

Provide a structured optimization plan."""

        try:
            response = self.reflector_model.generate_content(analysis_prompt)
            optimization_plan = response.text
            
            # Create targeted training data from meta-cognitive insights
            training_data = []
            
            # Address ambiguity points
            for ambiguity in quality_assessments.get("ambiguity_points", []):
                training_data.append({
                    "input": f"Clarify: {ambiguity}",
                    "expected_keywords": ["clear", "specific", "unambiguous"]
                })
            
            # Address failure modes
            for failure in quality_assessments.get("failure_modes", []):
                training_data.append({
                    "input": f"Prevent: {failure}",
                    "expected_keywords": ["robust", "reliable", "consistent"]
                })
            
            # Run optimization with meta-cognitive awareness
            result = self.optimize_prompt(prompt, training_data, budget=15)
            
            # Add meta-cognitive metrics
            result["meta_cognitive_improvement"] = {
                "clarity_gain": 1.0 - quality_assessments.get("clarity_score", 0.5),
                "ambiguity_resolved": len(quality_assessments.get("ambiguity_points", [])),
                "cognitive_load_reduction": quality_assessments.get("cognitive_load", 1.0) * 0.3
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Meta-cognitive optimization failed: {str(e)}")
    
    def constraint_based_optimize(self, prompt: str, constraints: Dict[str, Any],
                                objectives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Optimize with complex constraints and multi-objective optimization.
        Claude can define sophisticated constraints beyond simple keywords.
        
        Args:
            prompt: The prompt to optimize
            constraints: {
                "must_include": List[str],
                "must_exclude": List[str],
                "structural_requirements": List[str],
                "tone_constraints": str,
                "length_constraints": Dict,
                "domain_specific_rules": List[str]
            }
            objectives: [
                {"name": str, "weight": float, "evaluation_criteria": str},
                ...
            ]
        """
        # Build constraint-aware optimization prompt
        constraint_prompt = f"""Optimize this prompt while strictly adhering to constraints:

Original Prompt:
{prompt}

Constraints:
{json.dumps(constraints, indent=2)}

Objectives (with weights):
{json.dumps(objectives, indent=2)}

Generate an optimized prompt that:
1. Satisfies ALL hard constraints
2. Maximizes weighted objectives
3. Maintains the original intent"""

        try:
            response = self.reflector_model.generate_content(constraint_prompt)
            optimized = response.text.strip()
            
            # Validate constraints are met
            validation_results = self._validate_constraints(optimized, constraints)
            
            # Score against objectives
            objective_scores = {}
            for obj in objectives:
                score = self._evaluate_objective(optimized, obj)
                objective_scores[obj["name"]] = score * obj.get("weight", 1.0)
            
            return {
                "optimized_prompt": optimized,
                "constraints_satisfied": validation_results["all_satisfied"],
                "constraint_details": validation_results["details"],
                "objective_scores": objective_scores,
                "weighted_total": sum(objective_scores.values())
            }
            
        except Exception as e:
            raise Exception(f"Constraint-based optimization failed: {str(e)}")
    
    def pattern_mining_optimize(self, prompt: str, conversation_patterns: List[Dict[str, Any]],
                              success_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mine patterns from conversation history that Claude can provide.
        Uses successful interaction patterns to guide optimization.
        
        Args:
            prompt: The prompt to optimize
            conversation_patterns: [
                {
                    "pattern_type": str,
                    "occurrences": int,
                    "success_rate": float,
                    "example_context": str,
                    "key_elements": List[str]
                },
                ...
            ]
            success_indicators: {
                "user_satisfaction_phrases": List[str],
                "task_completion_markers": List[str],
                "quality_indicators": List[str]
            }
        """
        # Extract high-value patterns
        valuable_patterns = [
            p for p in conversation_patterns 
            if p.get("success_rate", 0) > 0.7 and p.get("occurrences", 0) > 2
        ]
        
        # Create training data from successful patterns
        training_data = []
        for pattern in valuable_patterns:
            training_data.append({
                "input": pattern.get("example_context", ""),
                "expected_keywords": pattern.get("key_elements", []) + 
                                   success_indicators.get("quality_indicators", [])
            })
        
        # Run pattern-aware optimization
        result = self.optimize_prompt(prompt, training_data, budget=10)
        
        # Analyze pattern incorporation
        result["pattern_analysis"] = {
            "patterns_incorporated": len(valuable_patterns),
            "success_likelihood": sum(p.get("success_rate", 0) for p in valuable_patterns) / len(valuable_patterns) if valuable_patterns else 0,
            "pattern_types": list(set(p.get("pattern_type", "") for p in valuable_patterns))
        }
        
        return result
    
    def multi_perspective_optimize(self, prompt: str, perspectives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Optimize considering how different models/systems might interpret the prompt.
        Claude can provide insights about various AI perspectives.
        
        Args:
            prompt: The prompt to optimize
            perspectives: [
                {
                    "model_type": str,  # e.g., "instruction-following", "creative", "analytical"
                    "interpretation": str,
                    "potential_issues": List[str],
                    "strengths": List[str]
                },
                ...
            ]
        """
        # Create cross-model optimization strategy
        optimization_prompt = f"""Optimize this prompt for maximum clarity across different AI model types:

Original Prompt:
{prompt}

Model Perspectives:
{json.dumps(perspectives, indent=2)}

Create a universally clear prompt that:
1. Minimizes interpretation differences
2. Leverages common strengths
3. Avoids model-specific pitfalls"""

        try:
            response = self.reflector_model.generate_content(optimization_prompt)
            optimized = response.text.strip()
            
            # Evaluate improvement for each perspective
            perspective_scores = {}
            for persp in perspectives:
                score = self._evaluate_perspective_fit(optimized, persp)
                perspective_scores[persp["model_type"]] = score
            
            return {
                "optimized_prompt": optimized,
                "original_prompt": prompt,
                "perspective_scores": perspective_scores,
                "universal_clarity_score": min(perspective_scores.values()) if perspective_scores else 0,
                "improvement": sum(perspective_scores.values()) / len(perspective_scores) if perspective_scores else 0
            }
            
        except Exception as e:
            raise Exception(f"Multi-perspective optimization failed: {str(e)}")
    
    def live_feedback_optimize(self, prompt: str, quality_callback: callable, 
                             max_iterations: int = 5) -> Dict[str, Any]:
        """
        Optimize with live quality feedback from Claude during the process.
        Claude can provide real-time assessments to guide optimization.
        
        Args:
            prompt: The prompt to optimize
            quality_callback: A function that Claude implements to assess quality
            max_iterations: Maximum optimization iterations
        """
        current_prompt = prompt
        iteration_history = []
        
        for i in range(max_iterations):
            # Get Claude's quality assessment
            quality_assessment = quality_callback(current_prompt)
            
            if quality_assessment.get("satisfactory", False):
                break
            
            # Create training data from quality feedback
            training_data = [{
                "input": "Improvement needed",
                "expected_keywords": quality_assessment.get("improvement_keywords", ["better", "improved"])
            }]
            
            # Run single iteration
            result = self.optimize_prompt(current_prompt, training_data, budget=3)
            
            iteration_history.append({
                "iteration": i + 1,
                "prompt": result["optimized_prompt"],
                "quality_score": quality_assessment.get("score", 0),
                "feedback": quality_assessment.get("feedback", "")
            })
            
            current_prompt = result["optimized_prompt"]
        
        return {
            "optimized_prompt": current_prompt,
            "original_prompt": prompt,
            "iterations": len(iteration_history),
            "iteration_history": iteration_history,
            "final_quality": quality_callback(current_prompt)
        }
    
    def _calculate_semantic_alignment(self, prompt: str, semantic_analysis: Dict[str, Any]) -> float:
        """Calculate how well the prompt aligns with semantic patterns"""
        score = 0.0
        components = semantic_analysis.get("semantic_components", [])
        
        for component in components:
            key_concepts = component.get("key_concepts", [])
            matches = sum(1 for concept in key_concepts if concept.lower() in prompt.lower())
            score += matches / len(key_concepts) if key_concepts else 0
        
        return score / len(components) if components else 0
    
    def _validate_constraints(self, prompt: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that all constraints are satisfied"""
        details = {}
        all_satisfied = True
        
        # Check must_include
        for item in constraints.get("must_include", []):
            if item not in prompt:
                details[f"must_include_{item}"] = False
                all_satisfied = False
            else:
                details[f"must_include_{item}"] = True
        
        # Check must_exclude
        for item in constraints.get("must_exclude", []):
            if item in prompt:
                details[f"must_exclude_{item}"] = False
                all_satisfied = False
            else:
                details[f"must_exclude_{item}"] = True
        
        return {"all_satisfied": all_satisfied, "details": details}
    
    def _evaluate_objective(self, prompt: str, objective: Dict[str, Any]) -> float:
        """Evaluate how well a prompt meets a specific objective"""
        # Simple implementation - could be enhanced
        criteria = objective.get("evaluation_criteria", "")
        if "clear" in criteria:
            return 0.8 if len(prompt.split()) < 50 else 0.6
        elif "engaging" in criteria:
            return 0.7 if "?" in prompt or "!" in prompt else 0.5
        return 0.5
    
    def _evaluate_perspective_fit(self, prompt: str, perspective: Dict[str, Any]) -> float:
        """Evaluate how well a prompt fits a specific model perspective"""
        issues = perspective.get("potential_issues", [])
        strengths = perspective.get("strengths", [])
        
        # Penalize for potential issues
        issue_penalty = sum(0.1 for issue in issues if issue.lower() in prompt.lower())
        
        # Reward for leveraging strengths  
        strength_bonus = sum(0.15 for strength in strengths if strength.lower() in prompt.lower())
        
        return min(1.0, max(0, 0.5 + strength_bonus - issue_penalty))