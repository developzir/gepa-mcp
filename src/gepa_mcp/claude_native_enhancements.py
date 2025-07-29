"""
Claude-Native GEPA Enhancements
These enhancements work WITH GEPA's proven architecture to amplify its core mechanisms.
Based on the GEPA research showing that reflection-based evolution outperforms RL by 10-20%.
"""

import json
from typing import List, Dict, Any, Optional
from .enhanced_features import EnhancedGEPA

class GepaWithClaudeEnhancements(EnhancedGEPA):
    """
    Enhancements that feed INTO GEPA's proven evolutionary architecture.
    These amplify GEPA's core mechanisms rather than replacing them.
    """
    
    def generate_enhanced_training_data(self, prompt: str, claude_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate rich training data using Claude's analysis capabilities.
        This feeds directly into GEPA's proven evaluation system.
        
        Args:
            prompt: The prompt being optimized
            claude_analysis: Claude's deep analysis of the optimization context
        
        Returns:
            Enhanced training data compatible with GEPA's keyword evaluation
        """
        # Extract Claude's insights
        domain_patterns = claude_analysis.get("domain_patterns", [])
        success_indicators = claude_analysis.get("success_indicators", [])
        failure_modes = claude_analysis.get("failure_modes", [])
        contextual_requirements = claude_analysis.get("contextual_requirements", [])
        
        # Generate training data that GEPA can use effectively
        enhanced_training = []
        
        # Domain-specific examples with rich keyword sets
        for pattern in domain_patterns:
            enhanced_training.append({
                "input": pattern.get("example_context", "Domain-specific context"),
                "expected_keywords": (
                    pattern.get("success_markers", []) + 
                    success_indicators[:3] +  # Top success indicators
                    [pattern.get("domain_term", "domain-specific")]
                )
            })
        
        # Failure-prevention examples
        for failure in failure_modes[:3]:  # Limit to avoid overwhelming GEPA
            enhanced_training.append({
                "input": f"Context requiring avoidance of: {failure}",
                "expected_keywords": ["robust", "reliable", "correct"] + success_indicators[:2]
            })
        
        # Context-aware examples
        for context in contextual_requirements[:3]:
            enhanced_training.append({
                "input": f"Context requirement: {context}",
                "expected_keywords": ["contextual", "appropriate", "relevant"] + success_indicators[:2]
            })
        
        return enhanced_training
    
    def enhance_gepa_reflection(self, current_prompt: str, examples: List[Dict[str, Any]], 
                               claude_guidance: Dict[str, Any]) -> str:
        """
        Enhance GEPA's reflection process with Claude's meta-cognitive capabilities.
        This supercharges GEPA's proven LLM-based mutation mechanism.
        
        Args:
            current_prompt: Current prompt being reflected on
            examples: GEPA's standard example format
            claude_guidance: Claude's meta-cognitive insights
        
        Returns:
            Enhanced reflection prompt for GEPA's reflector model
        """
        # Build enhanced reflection prompt that feeds into GEPA's system
        examples_text = '---'.join(
            f'Task Input: "{e["input"]}"\nGenerated Output: "{e["output"]}"\nFeedback:\n{e["feedback"]}\n\n'
            for e in examples
        )
        
        # Claude's enhancement to GEPA's reflection prompt
        enhanced_reflection_prompt = f"""You are an expert prompt engineer with advanced analytical capabilities.

Current prompt needing optimization:
--- CURRENT PROMPT ---
{current_prompt}
--------------------

Performance analysis from rollouts:
--- EXAMPLES & FEEDBACK ---
{examples_text}
-------------------------

ENHANCED ANALYTICAL GUIDANCE:
Based on deep analysis, consider these optimization vectors:

Semantic Patterns: {claude_guidance.get('semantic_patterns', 'Standard optimization patterns')}
Success Indicators: {claude_guidance.get('success_indicators', ['effective', 'accurate', 'clear'])}
Failure Modes to Avoid: {claude_guidance.get('failure_modes', ['ambiguity', 'vagueness'])}
Context Requirements: {claude_guidance.get('context_requirements', ['appropriate scope'])}

META-COGNITIVE INSIGHTS:
{claude_guidance.get('meta_insights', 'Apply systematic improvement strategies')}

Using this enhanced analysis, write a new, improved prompt that:
1. Addresses the specific failures identified in the feedback
2. Incorporates the successful strategies observed
3. Leverages the semantic patterns and success indicators provided
4. Avoids the identified failure modes
5. Maintains GEPA's evolutionary improvement approach

Provide ONLY the new prompt text, nothing else."""

        try:
            response = self.reflector_model.generate_content(enhanced_reflection_prompt)
            if not response.parts:
                raise Exception("Enhanced reflector returned empty response")
            return response.text.strip()
        except Exception as e:
            # Fallback to standard GEPA reflection if enhancement fails
            return super().reflect_and_propose_new_prompt(current_prompt, examples)
    
    def run_gepa_with_claude_enhancements(self, prompt: str, claude_analysis: Dict[str, Any], 
                                        budget: int = 10) -> Dict[str, Any]:
        """
        Run GEPA with Claude-generated training data and enhanced reflection.
        This is the main integration point that preserves GEPA's proven architecture.
        
        Args:
            prompt: Seed prompt to optimize
            claude_analysis: Claude's rich analysis of the optimization context
            budget: GEPA's rollout budget
        
        Returns:
            GEPA optimization results with Claude enhancements
        """
        # Generate enhanced training data using Claude's capabilities
        enhanced_training = self.generate_enhanced_training_data(prompt, claude_analysis)
        
        # Temporarily enhance the reflection method with Claude's insights
        original_reflect = self.reflect_and_propose_new_prompt
        
        def claude_enhanced_reflect(current_prompt: str, examples: List[Dict[str, Any]]) -> str:
            return self.enhance_gepa_reflection(current_prompt, examples, claude_analysis)
        
        # Replace reflection method temporarily
        self.reflect_and_propose_new_prompt = claude_enhanced_reflect
        
        try:
            # Run GEPA's proven optimization with enhancements
            result = self.optimize_prompt(prompt, enhanced_training, budget)
            
            # Add enhancement metadata
            result["enhancement_type"] = "claude_enhanced_gepa"
            result["training_data_generated"] = len(enhanced_training)
            result["claude_insights_applied"] = list(claude_analysis.keys())
            
            return result
            
        finally:
            # Restore original reflection method
            self.reflect_and_propose_new_prompt = original_reflect
    
    def adaptive_gepa_with_complexity_analysis(self, prompt: str, 
                                             claude_complexity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt GEPA's budget and approach based on Claude's complexity analysis.
        This optimizes GEPA's resource allocation using Claude's understanding.
        
        Args:
            prompt: Prompt to optimize
            claude_complexity: Claude's analysis of optimization complexity
        
        Returns:
            GEPA results optimized for the specific complexity profile
        """
        # Analyze complexity factors
        complexity_score = claude_complexity.get("complexity_score", 0.5)
        domain_familiarity = claude_complexity.get("domain_familiarity", 0.5)
        ambiguity_level = claude_complexity.get("ambiguity_level", 0.5)
        
        # Adapt GEPA's proven budget range (research shows 5-20 rollouts optimal)
        base_budget = 10
        complexity_factor = max(0.5, min(2.0, complexity_score * 2))
        unfamiliarity_factor = max(0.8, min(1.5, 2 - domain_familiarity))
        ambiguity_factor = max(0.8, min(1.3, 1 + ambiguity_level * 0.6))
        
        adaptive_budget = int(base_budget * complexity_factor * unfamiliarity_factor * ambiguity_factor)
        adaptive_budget = max(5, min(20, adaptive_budget))  # Stay within GEPA's proven range
        
        # Generate complexity-aware training data
        enhanced_training = self.generate_enhanced_training_data(prompt, claude_complexity)
        
        # Run GEPA with adaptive parameters
        result = self.optimize_prompt(prompt, enhanced_training, adaptive_budget)
        
        # Add adaptation metadata
        result["adaptive_budget_used"] = adaptive_budget
        result["complexity_factors"] = {
            "complexity_score": complexity_score,
            "domain_familiarity": domain_familiarity,
            "ambiguity_level": ambiguity_level
        }
        result["enhancement_type"] = "adaptive_claude_gepa"
        
        return result
    
    def multi_perspective_training_generation(self, prompt: str, perspectives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate training data considering multiple AI model perspectives.
        This creates diverse training examples that feed into GEPA's evaluation system.
        
        Args:
            prompt: The prompt being optimized
            perspectives: Different AI model perspective analyses
        
        Returns:
            Training data optimized for cross-model effectiveness
        """
        training_data = []
        
        for perspective in perspectives:
            model_type = perspective.get("model_type", "general")
            strengths = perspective.get("strengths", [])
            issues = perspective.get("potential_issues", [])
            
            # Create training examples that leverage strengths
            for strength in strengths[:2]:  # Limit to avoid overwhelming GEPA
                training_data.append({
                    "input": f"Leverage {model_type} strength: {strength}",
                    "expected_keywords": [strength, "effective", model_type.replace("-", "_")]
                })
            
            # Create training examples that avoid issues
            for issue in issues[:2]:
                training_data.append({
                    "input": f"Avoid {model_type} issue: {issue}",
                    "expected_keywords": ["robust", "clear", "universal"]
                })
        
        # Add cross-model optimization example
        training_data.append({
            "input": "Create universally clear prompt across different AI models",
            "expected_keywords": ["universal", "clear", "unambiguous", "effective"]
        })
        
        return training_data
    
    def gepa_with_conversation_patterns(self, prompt: str, 
                                      conversation_patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Use conversation patterns to enhance GEPA's training data.
        This feeds successful interaction patterns into GEPA's evolutionary process.
        
        Args:
            prompt: Prompt to optimize  
            conversation_patterns: Successful patterns from conversation history
        
        Returns:
            GEPA optimization leveraging conversation insights
        """
        # Filter for high-value patterns (following GEPA's Pareto principle)
        valuable_patterns = [
            p for p in conversation_patterns 
            if p.get("success_rate", 0) > 0.7 and p.get("occurrences", 0) > 2
        ]
        
        # Convert patterns to GEPA-compatible training data
        training_data = []
        for pattern in valuable_patterns:
            training_data.append({
                "input": pattern.get("example_context", "Pattern context"),
                "expected_keywords": (
                    pattern.get("key_elements", []) + 
                    ["effective", "successful", pattern.get("pattern_type", "pattern")]
                )
            })
        
        # Run GEPA with pattern-enhanced training
        result = self.optimize_prompt(prompt, training_data, budget=12)
        
        # Add pattern analysis
        result["patterns_utilized"] = len(valuable_patterns)
        result["pattern_types"] = list(set(p.get("pattern_type", "") for p in valuable_patterns))
        result["enhancement_type"] = "conversation_pattern_enhanced_gepa"
        
        return result