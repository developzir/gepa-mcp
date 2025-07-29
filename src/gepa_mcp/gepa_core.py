import os
import json
import random
import time
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class GEPACore:
    def __init__(self, gemini_api_key: Optional[str] = None):
        """Initialize GEPA with Gemini API key"""
        api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Gemini API key required")
        
        genai.configure(api_key=api_key)
        self.target_model = genai.GenerativeModel("gemini-1.5-flash-latest")
        self.reflector_model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    def log_message(self, message: str, type: str = 'info') -> str:
        """Format log messages with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        if type == 'success':
            return f"[{timestamp}] ✅ SUCCESS: {message}"
        elif type == 'fail':
            return f"[{timestamp}] ❌ FAIL: {message}"
        elif type == 'best':
            return f"[{timestamp}] ⭐ BEST: {message}"
        return f"[{timestamp}] ℹ️ INFO: {message}"
    
    def run_rollout(self, prompt: str, input_text: str) -> str:
        """Execute a rollout with the target model"""
        full_prompt = f"{prompt}\n\nText: \"{input_text}\"\n\nResponse:"
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=100,
            temperature=0.7,
            top_p=0.95
        )
        
        try:
            response = self.target_model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            if not response.parts:
                raise Exception("Model returned empty response")
            return response.text
        except Exception as e:
            if "api_key" in str(e).lower():
                raise Exception("Google AI API Error: Authorization failed")
            raise Exception(f"Google AI API Error: {str(e)}")
    
    def evaluation_function(self, output: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate output quality and provide feedback"""
        if not output or not isinstance(output, str):
            return {"score": 0.0, "feedback": "No valid output generated."}
        
        score = 0.0
        feedback = ""
        found_keywords = 0
        expected_keywords = task.get("expected_keywords", [])
        
        if not expected_keywords:
            return {"score": 0.0, "feedback": "No evaluation criteria found."}
        
        for keyword in expected_keywords:
            if keyword.lower() in output.lower():
                found_keywords += 1
                feedback += f"SUCCESS: Output contained '{keyword}'.\n"
            else:
                feedback += f"FAILURE: Output missing '{keyword}'.\n"
        
        score = found_keywords / len(expected_keywords)
        feedback += f"Final Score: {score:.2f}"
        return {"score": score, "feedback": feedback}
    
    def reflect_and_propose_new_prompt(self, current_prompt: str, examples: List[Dict[str, Any]]) -> str:
        """Use reflector model to generate improved prompt"""
        examples_text = '---'.join(
            f'Task Input: "{e["input"]}"\nGenerated Output: "{e["output"]}"\nFeedback:\n{e["feedback"]}\n\n'
            for e in examples
        )
        
        reflection_prompt = f"""You are an expert prompt engineer. Refine this prompt based on performance feedback.

Current prompt:
--- CURRENT PROMPT ---
{current_prompt}
--------------------

Performance examples:
--- EXAMPLES & FEEDBACK ---
{examples_text}
-------------------------

Write a new, improved prompt that addresses the failures and incorporates successful strategies. 
Provide ONLY the new prompt text, nothing else."""
        
        try:
            response = self.reflector_model.generate_content(reflection_prompt)
            if not response.parts:
                raise Exception("Reflector model returned empty response")
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini API Error during reflection: {str(e)}")
    
    def optimize_prompt(self, seed_prompt: str, training_data: List[Dict[str, Any]], budget: int = 10) -> Dict[str, Any]:
        """Main GEPA optimization function"""
        print(self.log_message("Starting GEPA Optimization Process..."))
        
        rollout_count = 0
        candidate_pool = []
        best_candidate = {"prompt": seed_prompt, "avg_score": -1.0}
        
        # Initial evaluation
        print(self.log_message("Evaluating seed prompt"))
        initial_scores = []
        total_score = 0.0
        
        for i, task in enumerate(training_data):
            try:
                output = self.run_rollout(seed_prompt, task["input"])
                eval_result = self.evaluation_function(output, task)
                initial_scores.append(eval_result["score"])
                total_score += eval_result["score"]
                rollout_count += 1
            except Exception as e:
                print(self.log_message(f"Error on task {i+1}: {str(e)}", 'fail'))
                initial_scores.append(0.0)
        
        avg_score = total_score / len(training_data) if training_data else 0.0
        initial_candidate = {
            "id": 0,
            "prompt": seed_prompt,
            "scores": initial_scores,
            "avg_score": avg_score
        }
        
        candidate_pool.append(initial_candidate)
        best_candidate = initial_candidate
        
        print(self.log_message(f"Seed prompt score: {avg_score:.2f}", 'best'))
        
        # Optimization loop
        print(self.log_message(f"Starting optimization loop (Budget: {budget} rollouts)"))
        
        while rollout_count < budget:
            # Select random task for reflection
            task_index = random.randint(0, len(training_data) - 1)
            reflection_task = training_data[task_index]
            
            try:
                # Generate output and feedback
                rollout_output = self.run_rollout(best_candidate["prompt"], reflection_task["input"])
                rollout_count += 1
                eval_result = self.evaluation_function(rollout_output, reflection_task)
                
                # Generate new prompt
                new_prompt = self.reflect_and_propose_new_prompt(
                    best_candidate["prompt"],
                    [{
                        "input": reflection_task["input"],
                        "output": rollout_output,
                        "feedback": eval_result["feedback"]
                    }]
                )
                
                # Evaluate new prompt
                new_scores = []
                new_total_score = 0.0
                
                for task in training_data:
                    if rollout_count >= budget:
                        break
                    try:
                        output = self.run_rollout(new_prompt, task["input"])
                        eval_result = self.evaluation_function(output, task)
                        new_scores.append(eval_result["score"])
                        new_total_score += eval_result["score"]
                        rollout_count += 1
                    except Exception as e:
                        new_scores.append(0.0)
                
                new_avg_score = new_total_score / len(training_data)
                
                if new_avg_score > best_candidate["avg_score"]:
                    best_candidate = {
                        "id": len(candidate_pool),
                        "prompt": new_prompt,
                        "scores": new_scores,
                        "avg_score": new_avg_score
                    }
                    candidate_pool.append(best_candidate)
                    print(self.log_message(f"New best prompt! Score: {new_avg_score:.2f}", 'best'))
                
            except Exception as e:
                print(self.log_message(f"Error in optimization: {str(e)}", 'fail'))
                rollout_count += 1  # Count failed attempts
        
        print(self.log_message("Optimization complete", 'success'))
        return {
            "optimized_prompt": best_candidate["prompt"],
            "final_score": best_candidate["avg_score"],
            "improvement": best_candidate["avg_score"] - initial_candidate["avg_score"],
            "rollouts_used": rollout_count
        }