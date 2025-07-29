import json
from typing import List, Dict, Any, Optional
from .gepa_core import GEPACore
import google.generativeai as genai

class EnhancedGEPA(GEPACore):
    """Enhanced GEPA with additional features for conversational optimization and prompt archaeology"""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        super().__init__(gemini_api_key)
        self.optimization_history = []
        self.pattern_library = {}
    
    def conversational_optimize(self, prompt: str, conversation_history: str, 
                               user_satisfaction_signals: str = "") -> Dict[str, Any]:
        """Optimize prompts based on real conversational outcomes"""
        # Analyze conversation history to extract training data
        analysis_prompt = f"""Analyze this conversation and extract key patterns for prompt optimization:

Conversation History:
{conversation_history}

User Satisfaction Signals:
{user_satisfaction_signals}

Extract:
1. What worked well in the conversation
2. What could be improved
3. Key topics and required outputs

Format as training examples with expected keywords."""

        try:
            response = self.reflector_model.generate_content(analysis_prompt)
            extracted_patterns = response.text
            
            # Create dynamic training data from conversation
            training_data = self._extract_training_data(extracted_patterns)
            
            # Run optimization with conversation-aware training
            result = self.optimize_prompt(prompt, training_data, budget=5)
            
            # Store in history for pattern learning
            self.optimization_history.append({
                "original": prompt,
                "optimized": result["optimized_prompt"],
                "context": conversation_history,
                "improvement": result["improvement"]
            })
            
            return result
        except Exception as e:
            raise Exception(f"Conversational optimization failed: {str(e)}")
    
    def explain_optimization(self, original_prompt: str, optimized_prompt: str) -> str:
        """Analyze WHY the optimization worked - Prompt Archaeology"""
        explanation_prompt = f"""You are a prompt engineering expert. Analyze these prompts and explain the improvements:

Original Prompt:
{original_prompt}

Optimized Prompt:
{optimized_prompt}

Provide a detailed analysis of:
1. What specific changes were made
2. Why each change improves the prompt
3. The underlying principles applied
4. When to use similar optimizations

Be educational and insightful."""

        try:
            response = self.reflector_model.generate_content(explanation_prompt)
            return response.text
        except Exception as e:
            return f"Could not generate explanation: {str(e)}"
    
    def holistic_optimize(self, prompt: str, optimize_for: List[str] = None) -> Dict[str, Any]:
        """Optimize for multiple criteria simultaneously"""
        if optimize_for is None:
            optimize_for = ["clarity", "engagement", "accuracy", "creativity"]
        
        # Create multi-dimensional training data
        training_data = []
        for criterion in optimize_for:
            training_data.append({
                "input": f"Optimize this prompt for {criterion}",
                "expected_keywords": [criterion, "improved", "effective", "optimized"]
            })
        
        # Run optimization with multi-criteria evaluation
        result = self.optimize_prompt(prompt, training_data, budget=8)
        
        # Add criterion scores
        result["criterion_scores"] = {
            criterion: self._evaluate_criterion(result["optimized_prompt"], criterion)
            for criterion in optimize_for
        }
        
        return result
    
    def transfer_optimization_patterns(self, source_domain: str, target_domain: str, 
                                     successful_patterns: str) -> str:
        """Apply successful patterns from one domain to another"""
        transfer_prompt = f"""Apply successful optimization patterns from {source_domain} to {target_domain}:

Successful Patterns from {source_domain}:
{successful_patterns}

Adapt these patterns for {target_domain} context. Consider:
1. Domain-specific terminology
2. Different user expectations
3. Structural adaptations needed

Provide adapted optimization strategies."""

        try:
            response = self.reflector_model.generate_content(transfer_prompt)
            
            # Store transferred patterns
            if target_domain not in self.pattern_library:
                self.pattern_library[target_domain] = []
            self.pattern_library[target_domain].append({
                "source": source_domain,
                "patterns": response.text
            })
            
            return response.text
        except Exception as e:
            return f"Pattern transfer failed: {str(e)}"
    
    def optimize_with_generated_training(self, prompt: str, domain: str = "general", 
                                       task_examples: str = "", generate_training: bool = True) -> Dict[str, Any]:
        """Optimize prompt with AI-generated training data"""
        if generate_training:
            # Generate domain-specific training data
            generation_prompt = f"""Generate 5 diverse training examples for optimizing a {domain} prompt.

Context: {task_examples if task_examples else f"General {domain} tasks"}

For each example provide:
1. A realistic input text
2. Expected keywords that indicate good performance

Format as JSON array with 'input' and 'expected_keywords' fields."""

            try:
                response = self.reflector_model.generate_content(generation_prompt)
                # Extract JSON from response
                json_start = response.text.find('[')
                json_end = response.text.rfind(']') + 1
                if json_start >= 0 and json_end > json_start:
                    training_data = json.loads(response.text[json_start:json_end])
                else:
                    # Fallback to simple training data
                    training_data = [{
                        "input": f"Sample {domain} task",
                        "expected_keywords": [domain, "clear", "effective"]
                    }]
            except:
                # Fallback training data
                training_data = [{
                    "input": f"Sample {domain} task",
                    "expected_keywords": [domain, "clear", "effective"]
                }]
        else:
            # Use provided examples
            training_data = json.loads(task_examples) if isinstance(task_examples, str) else task_examples
        
        # Run optimization
        result = self.optimize_prompt(prompt, training_data, budget=10)
        result["training_generated"] = generate_training
        result["domain"] = domain
        
        return result
    
    def auto_optimize_prompt(self, prompt: str, context: str) -> Dict[str, Any]:
        """Intelligently choose optimization strategy and generate training data as needed"""
        # Analyze prompt and context to determine strategy
        analysis_prompt = f"""Analyze this prompt and context to determine optimization needs:

Prompt: {prompt}
Context: {context}

Determine:
1. Domain/task type
2. Optimization priority (quick vs thorough)
3. Key improvement areas

Respond with a JSON object containing: domain, priority (quick/thorough), improvement_areas (list)"""

        try:
            response = self.reflector_model.generate_content(analysis_prompt)
            # Parse analysis
            json_start = response.text.find('{')
            json_end = response.text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                analysis = json.loads(response.text[json_start:json_end])
            else:
                analysis = {"domain": "general", "priority": "quick", "improvement_areas": ["clarity"]}
            
            # Choose strategy based on analysis
            if analysis.get("priority") == "quick":
                return self.quick_improve_internal(prompt, context, analysis.get("domain", "general"))
            else:
                return self.optimize_with_generated_training(
                    prompt, 
                    domain=analysis.get("domain", "general"),
                    task_examples=context,
                    generate_training=True
                )
        except Exception as e:
            # Fallback to quick optimization
            return self.quick_improve_internal(prompt, context, "general")
    
    def _extract_training_data(self, patterns_text: str) -> List[Dict[str, Any]]:
        """Extract training data from pattern analysis"""
        # Simple extraction - could be enhanced
        return [
            {
                "input": "Extracted from conversation patterns",
                "expected_keywords": ["relevant", "accurate", "helpful", "clear"]
            }
        ]
    
    def _evaluate_criterion(self, prompt: str, criterion: str) -> float:
        """Evaluate how well a prompt meets a specific criterion"""
        # Simple keyword-based evaluation - could use more sophisticated metrics
        criterion_keywords = {
            "clarity": ["clear", "specific", "unambiguous", "precise"],
            "engagement": ["engaging", "interesting", "compelling", "interactive"],
            "accuracy": ["accurate", "factual", "correct", "reliable"],
            "creativity": ["creative", "innovative", "unique", "imaginative"]
        }
        
        keywords = criterion_keywords.get(criterion, [])
        score = sum(1 for keyword in keywords if keyword in prompt.lower()) / len(keywords)
        return score
    
    def quick_improve_internal(self, prompt: str, context: str, task_type: str) -> Dict[str, Any]:
        """Internal quick improvement method"""
        training_data = [{
            "input": context if context else "general task improvement",
            "expected_keywords": [task_type, "improved", "better"]
        }]
        
        result = self.optimize_prompt(prompt, training_data, budget=3)
        result["optimization_type"] = "quick"
        return result