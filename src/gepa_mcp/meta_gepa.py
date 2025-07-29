"""
Meta-GEPA: Using GEPA to optimize GEPA itself
This is the "bigger" vision - a self-improving optimization system
"""

import json
from typing import List, Dict, Any, Optional
from .claude_native_features import ClaudeNativeGEPA

class MetaGEPA(ClaudeNativeGEPA):
    """Meta-GEPA: Using GEPA's own evolutionary approach to optimize GEPA optimization strategies"""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        super().__init__(gemini_api_key)
        self.optimization_strategy_history = []
        self.performance_metrics = []
    
    def evolve_optimization_strategy(self, 
                                   historical_performance: List[Dict[str, Any]], 
                                   target_domains: List[str]) -> Dict[str, Any]:
        """
        Use GEPA to evolve better GEPA optimization strategies.
        This is meta-optimization - optimizing the optimizer.
        
        Args:
            historical_performance: Past optimization results with their strategies
            target_domains: Domains to optimize the strategy for
        
        Returns:
            Evolved optimization strategy
        """
        # Create "prompts" that are actually optimization strategies
        seed_strategy = {
            "budget_allocation": "uniform",
            "reflection_depth": "standard", 
            "mutation_approach": "single_task",
            "selection_criteria": "avg_score"
        }
        
        # Convert strategy optimization into a GEPA-compatible problem
        strategy_prompt = f"Optimization Strategy: {json.dumps(seed_strategy)}"
        
        # Create training data from historical performance
        training_data = []
        for perf in historical_performance:
            if perf.get("improvement", 0) > 0.1:  # Only successful optimizations
                training_data.append({
                    "input": f"Domain: {perf.get('domain', 'general')}, Task: {perf.get('task_type', 'optimization')}",
                    "expected_keywords": ["effective", "improved", "successful", perf.get("domain", "general")]
                })
        
        # Use GEPA to evolve the optimization strategy
        result = self.optimize_prompt(strategy_prompt, training_data, budget=15)
        
        # Parse the evolved strategy back
        evolved_strategy = self._extract_strategy_from_prompt(result["optimized_prompt"])
        
        return {
            "evolved_strategy": evolved_strategy,
            "original_strategy": seed_strategy,
            "expected_improvement": result["improvement"],
            "optimization_type": "meta_gepa"
        }
    
    def claude_enhanced_training_generation(self, prompt: str, claude_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate GEPA-compatible training data using Claude's deep analysis capabilities.
        This feeds richer data INTO the proven GEPA system.
        
        Args:
            prompt: The prompt being optimized
            claude_analysis: Claude's rich analysis of the prompt and context
        
        Returns:
            Training data optimized for GEPA's evolutionary process
        """
        # Extract Claude's insights about what makes prompts effective
        semantic_patterns = claude_analysis.get("semantic_patterns", [])
        success_indicators = claude_analysis.get("success_indicators", [])
        failure_modes = claude_analysis.get("failure_modes", [])
        context_requirements = claude_analysis.get("context_requirements", [])
        
        training_data = []
        
        # Convert semantic patterns into GEPA training examples
        for pattern in semantic_patterns:
            training_data.append({
                "input": pattern.get("example_context", "Pattern application context"),
                "expected_keywords": pattern.get("success_markers", ["effective", "clear"]) + 
                                   success_indicators[:3]  # Top success indicators
            })
        
        # Create training examples that address failure modes
        for failure in failure_modes:
            training_data.append({
                "input": f"Avoid failure mode: {failure}",
                "expected_keywords": ["robust", "reliable", "clear"] + success_indicators[:2]
            })
        
        # Add context-aware training examples
        for context in context_requirements:
            training_data.append({
                "input": f"Context requirement: {context}",
                "expected_keywords": ["contextual", "appropriate", "relevant"] + success_indicators[:2]
            })
        
        return training_data
    
    def adaptive_budget_gepa(self, prompt: str, claude_complexity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dynamically adjust GEPA's budget based on Claude's complexity analysis.
        Uses Claude's understanding to optimize GEPA's resource allocation.
        
        Args:
            prompt: The prompt to optimize
            claude_complexity_analysis: Claude's analysis of optimization complexity
        
        Returns:
            GEPA result with adaptive budget allocation
        """
        # Analyze complexity to determine optimal budget
        complexity_score = claude_complexity_analysis.get("complexity_score", 0.5)
        domain_familiarity = claude_complexity_analysis.get("domain_familiarity", 0.5)
        ambiguity_level = claude_complexity_analysis.get("ambiguity_level", 0.5)
        
        # Calculate adaptive budget (proven GEPA range: 5-20 rollouts)
        base_budget = 10
        complexity_factor = max(0.5, min(2.0, complexity_score * 2))
        unfamiliarity_factor = max(0.8, min(1.5, 2 - domain_familiarity))
        ambiguity_factor = max(0.8, min(1.3, 1 + ambiguity_level * 0.6))
        
        adaptive_budget = int(base_budget * complexity_factor * unfamiliarity_factor * ambiguity_factor)
        adaptive_budget = max(5, min(20, adaptive_budget))  # Keep within proven effective range
        
        # Generate enhanced training data
        training_data = self.claude_enhanced_training_generation(
            prompt, 
            claude_complexity_analysis
        )
        
        # Run GEPA with adaptive budget
        result = self.optimize_prompt(prompt, training_data, budget=adaptive_budget)
        
        # Add adaptive metrics
        result["adaptive_budget_used"] = adaptive_budget
        result["complexity_factors"] = {
            "complexity_score": complexity_score,
            "domain_familiarity": domain_familiarity,
            "ambiguity_level": ambiguity_level
        }
        
        return result
    
    def gepa_with_claude_reflection_enhancement(self, prompt: str, reflection_guidance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance GEPA's reflection process with Claude's meta-cognitive capabilities.
        This supercharges the core GEPA reflection mechanism.
        
        Args:
            prompt: The prompt to optimize
            reflection_guidance: Claude's guidance for the reflection process
        
        Returns:
            Enhanced GEPA optimization result
        """
        # Create enhanced reflection prompts for GEPA's reflector model
        standard_training = [{
            "input": "Standard optimization task",
            "expected_keywords": ["improved", "better", "optimized"]
        }]
        
        # Run GEPA but intercept and enhance the reflection process
        # This is like "coaching" GEPA's reflector model
        enhanced_result = self._enhanced_gepa_with_reflection_coaching(
            prompt, 
            standard_training, 
            reflection_guidance,
            budget=12
        )
        
        return enhanced_result
    
    def _enhanced_gepa_with_reflection_coaching(self, prompt: str, training_data: List[Dict], 
                                              reflection_guidance: Dict[str, Any], budget: int) -> Dict[str, Any]:
        """Enhanced GEPA that coaches the reflection process"""
        
        # Override the reflection prompt to include Claude's guidance
        original_reflect = self.reflect_and_propose_new_prompt
        
        def enhanced_reflect(current_prompt: str, examples: List[Dict[str, Any]]) -> str:
            examples_text = '---'.join(
                f'Task Input: "{e["input"]}"\nGenerated Output: "{e["output"]}"\nFeedback:\n{e["feedback"]}\n\n'
                for e in examples
            )
            
            # Enhanced reflection prompt with Claude's guidance
            enhanced_reflection_prompt = f"""You are an expert prompt engineer with advanced reflection capabilities.

Current prompt:
--- CURRENT PROMPT ---
{current_prompt}
--------------------

Performance examples:
--- EXAMPLES & FEEDBACK ---
{examples_text}
-------------------------

REFLECTION GUIDANCE (from advanced analysis):
{json.dumps(reflection_guidance, indent=2)}

Using this guidance, write a new, improved prompt that:
1. Addresses the failures identified in the feedback
2. Incorporates the successful strategies observed
3. Applies the specific reflection guidance provided
4. Maintains the evolutionary improvement approach

Provide ONLY the new prompt text, nothing else."""
            
            try:
                response = self.reflector_model.generate_content(enhanced_reflection_prompt)
                if not response.parts:
                    raise Exception("Reflector model returned empty response")
                return response.text.strip()
            except Exception as e:
                # Fallback to original reflection if enhanced fails
                return original_reflect(current_prompt, examples)
        
        # Temporarily replace reflection method
        self.reflect_and_propose_new_prompt = enhanced_reflect
        
        # Run GEPA with enhanced reflection
        result = self.optimize_prompt(prompt, training_data, budget)
        
        # Restore original method
        self.reflect_and_propose_new_prompt = original_reflect
        
        result["reflection_enhancement"] = "claude_guided"
        return result
    
    def _extract_strategy_from_prompt(self, strategy_prompt: str) -> Dict[str, Any]:
        """Extract optimization strategy from evolved prompt"""
        # Simple extraction - could be enhanced with more sophisticated parsing
        if "dynamic" in strategy_prompt.lower():
            budget_allocation = "dynamic"
        elif "focused" in strategy_prompt.lower():
            budget_allocation = "focused"
        else:
            budget_allocation = "balanced"
        
        if "deep" in strategy_prompt.lower():
            reflection_depth = "deep"
        elif "quick" in strategy_prompt.lower():
            reflection_depth = "quick"
        else:
            reflection_depth = "standard"
        
        return {
            "budget_allocation": budget_allocation,
            "reflection_depth": reflection_depth,
            "mutation_approach": "adaptive",
            "selection_criteria": "pareto_optimal"
        }