"""
Policy Impact Predictor Agent - ML-based impact analysis and predictions
"""

from typing import Dict, List, Optional, Any
import numpy as np
from datetime import datetime
from app.agents.base_agent import BaseAgent


class PolicyImpactPredictor(BaseAgent):
    """
    Agent that predicts policy impact using ML models and statistical analysis.
    
    Features:
    - Predict number of beneficiaries
    - Budget estimation
    - Success probability
    - Regional impact analysis
    - ROI for government
    """
    
    def __init__(self):
        super().__init__(llm=None)
        self.name = "Policy Impact Predictor"
        self.description = "Predicts policy impact using ML models and statistical analysis"
        
        # Historical data for ML training (simulated for now)
        self.historical_data = self._initialize_historical_data()
        
        # Model weights (simplified ML coefficients)
        self.beneficiary_weights = {
            'income_threshold': 0.35,
            'age_range': 0.25,
            'geographic_scope': 0.20,
            'awareness_factor': 0.20
        }
        
        self.success_weights = {
            'policy_clarity': 0.30,
            'implementation_ease': 0.25,
            'funding_adequacy': 0.25,
            'stakeholder_support': 0.20
        }
    
    def _initialize_historical_data(self) -> Dict:
        """Initialize historical policy performance data"""
        return {
            'education_schemes': {
                'avg_beneficiaries': 50000,
                'avg_budget': 100000000,
                'success_rate': 0.75,
                'adoption_rate': 0.65
            },
            'housing_schemes': {
                'avg_beneficiaries': 30000,
                'avg_budget': 500000000,
                'success_rate': 0.70,
                'adoption_rate': 0.55
            },
            'welfare_schemes': {
                'avg_beneficiaries': 100000,
                'avg_budget': 200000000,
                'success_rate': 0.80,
                'adoption_rate': 0.70
            },
            'disability_schemes': {
                'avg_beneficiaries': 20000,
                'avg_budget': 50000000,
                'success_rate': 0.85,
                'adoption_rate': 0.75
            }
        }
    
    async def predict_impact(
        self,
        policy_data: Dict,
        population_data: Optional[Dict] = None,
        regional_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Predict comprehensive impact of a policy
        
        Args:
            policy_data: Policy details (rules, benefits, category)
            population_data: Target population statistics
            regional_context: Regional economic/demographic data
        
        Returns:
            Comprehensive impact prediction
        """
        try:
            # Extract policy features
            policy_features = self._extract_policy_features(policy_data)
            
            # Predict beneficiaries
            beneficiary_prediction = await self._predict_beneficiaries(
                policy_features, 
                population_data
            )
            
            # Estimate budget
            budget_estimation = await self._estimate_budget(
                policy_features,
                beneficiary_prediction
            )
            
            # Calculate success probability
            success_probability = await self._calculate_success_probability(
                policy_features
            )
            
            # Analyze regional impact
            regional_impact = await self._analyze_regional_impact(
                policy_features,
                regional_context
            )
            
            # Calculate ROI
            roi_analysis = await self._calculate_roi(
                budget_estimation,
                beneficiary_prediction,
                success_probability
            )
            
            return {
                'success': True,
                'policy_name': policy_data.get('name', 'Unnamed Policy'),
                'predictions': {
                    'beneficiaries': beneficiary_prediction,
                    'budget': budget_estimation,
                    'success_probability': success_probability,
                    'regional_impact': regional_impact,
                    'roi': roi_analysis
                },
                'confidence_score': self._calculate_confidence(policy_features),
                'generated_at': datetime.now().isoformat(),
                'recommendations': self._generate_recommendations(
                    beneficiary_prediction,
                    budget_estimation,
                    success_probability
                )
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to predict policy impact'
            }
    
    def _extract_policy_features(self, policy_data: Dict) -> Dict:
        """Extract ML features from policy data"""
        rules = policy_data.get('rules', [])
        
        features = {
            'category': self._categorize_policy(policy_data),
            'num_eligibility_rules': len(rules),
            'has_income_criteria': any(r.get('key') == 'income' for r in rules),
            'has_age_criteria': any(r.get('key') == 'age' for r in rules),
            'has_location_criteria': any(r.get('key') in ['state', 'region'] for r in rules),
            'complexity_score': self._calculate_complexity(rules),
            'benefit_value': self._estimate_benefit_value(policy_data)
        }
        
        return features
    
    def _categorize_policy(self, policy_data: Dict) -> str:
        """Categorize policy based on content"""
        name = policy_data.get('name', '').lower()
        description = policy_data.get('description', '').lower()
        
        if 'education' in name or 'scholarship' in name or 'student' in name:
            return 'education_schemes'
        elif 'housing' in name or 'home' in name:
            return 'housing_schemes'
        elif 'disability' in name or 'disabled' in name:
            return 'disability_schemes'
        else:
            return 'welfare_schemes'
    
    def _calculate_complexity(self, rules: List[Dict]) -> float:
        """Calculate policy complexity score (0-1)"""
        if not rules:
            return 0.3
        
        complexity = 0.0
        complexity += min(len(rules) * 0.15, 0.5)  # Number of rules
        
        # Check for compound conditions
        for rule in rules:
            operator = rule.get('operator', '==')
            if operator in ['>', '<', '>=', '<=']:
                complexity += 0.1
        
        return min(complexity, 1.0)
    
    def _estimate_benefit_value(self, policy_data: Dict) -> float:
        """Estimate monetary benefit value"""
        benefits = policy_data.get('benefits', '')
        
        # Extract numbers from benefit description
        import re
        numbers = re.findall(r'\d+', benefits)
        
        if numbers:
            return float(numbers[0])
        
        # Default estimates based on category
        category = self._categorize_policy(policy_data)
        defaults = {
            'education_schemes': 50000,
            'housing_schemes': 200000,
            'welfare_schemes': 30000,
            'disability_schemes': 40000
        }
        
        return defaults.get(category, 25000)
    
    async def _predict_beneficiaries(
        self,
        features: Dict,
        population_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Predict number of beneficiaries using ML model"""
        
        # Get base estimate from historical data
        category = features['category']
        base_beneficiaries = self.historical_data[category]['avg_beneficiaries']
        
        # Apply feature-based adjustments
        multiplier = 1.0
        
        # Income criteria reduces eligible population
        if features['has_income_criteria']:
            multiplier *= 0.4
        
        # Location criteria reduces scope
        if features['has_location_criteria']:
            multiplier *= 0.3
        
        # Complexity reduces adoption
        complexity_factor = 1.0 - (features['complexity_score'] * 0.3)
        multiplier *= complexity_factor
        
        # Population data adjustment
        if population_data:
            pop_multiplier = population_data.get('size', 1000000) / 10000000
            multiplier *= pop_multiplier
        
        predicted = int(base_beneficiaries * multiplier)
        
        # Add confidence intervals
        lower_bound = int(predicted * 0.7)
        upper_bound = int(predicted * 1.3)
        
        return {
            'predicted': predicted,
            'confidence_interval': {
                'lower': lower_bound,
                'upper': upper_bound
            },
            'yearly_growth_rate': self._estimate_growth_rate(features),
            'adoption_timeline': {
                'year_1': int(predicted * 0.5),
                'year_2': int(predicted * 0.75),
                'year_3': predicted,
                'year_5': int(predicted * 1.2)
            }
        }
    
    def _estimate_growth_rate(self, features: Dict) -> float:
        """Estimate yearly growth rate of beneficiaries"""
        base_rate = 0.15  # 15% base growth
        
        # Lower complexity leads to faster growth
        complexity_adjustment = -0.05 * features['complexity_score']
        
        return round(base_rate + complexity_adjustment, 3)
    
    async def _estimate_budget(
        self,
        features: Dict,
        beneficiary_prediction: Dict
    ) -> Dict[str, Any]:
        """Estimate required budget"""
        
        predicted_beneficiaries = beneficiary_prediction['predicted']
        benefit_value = features['benefit_value']
        
        # Direct benefit costs
        direct_cost = predicted_beneficiaries * benefit_value
        
        # Administrative overhead (10-20% based on complexity)
        overhead_rate = 0.10 + (features['complexity_score'] * 0.10)
        admin_cost = direct_cost * overhead_rate
        
        # Implementation costs
        implementation_cost = direct_cost * 0.05
        
        total_budget = direct_cost + admin_cost + implementation_cost
        
        return {
            'total_estimated_budget': int(total_budget),
            'breakdown': {
                'direct_benefits': int(direct_cost),
                'administrative_overhead': int(admin_cost),
                'implementation_costs': int(implementation_cost)
            },
            'per_beneficiary_cost': int(total_budget / predicted_beneficiaries) if predicted_beneficiaries > 0 else 0,
            'yearly_projection': {
                'year_1': int(total_budget * 0.5),
                'year_2': int(total_budget * 0.75),
                'year_3': int(total_budget),
                'year_5': int(total_budget * 1.2)
            },
            'currency': 'INR'
        }
    
    async def _calculate_success_probability(self, features: Dict) -> Dict[str, Any]:
        """Calculate probability of policy success"""
        
        # Base success rate from historical data
        category = features['category']
        base_rate = self.historical_data[category]['success_rate']
        
        # Factors affecting success
        factors = {
            'policy_clarity': 0.8 if features['complexity_score'] < 0.5 else 0.6,
            'implementation_ease': 0.85 if features['num_eligibility_rules'] <= 3 else 0.65,
            'funding_adequacy': 0.75,  # Assumed adequate
            'stakeholder_support': 0.80  # Assumed good support
        }
        
        # Weighted calculation
        weighted_score = sum(
            factors[k] * self.success_weights[k] 
            for k in factors
        )
        
        # Combine with historical data
        final_probability = (base_rate * 0.4) + (weighted_score * 0.6)
        
        return {
            'overall_probability': round(final_probability, 3),
            'confidence_level': 'High' if final_probability > 0.75 else 'Medium' if final_probability > 0.6 else 'Low',
            'contributing_factors': factors,
            'risk_factors': self._identify_risk_factors(features, factors)
        }
    
    def _identify_risk_factors(self, features: Dict, factors: Dict) -> List[str]:
        """Identify potential risk factors"""
        risks = []
        
        if features['complexity_score'] > 0.7:
            risks.append('High policy complexity may hinder adoption')
        
        if features['num_eligibility_rules'] > 5:
            risks.append('Multiple eligibility criteria may reduce applicant pool')
        
        if factors['implementation_ease'] < 0.7:
            risks.append('Implementation challenges may delay rollout')
        
        if not risks:
            risks.append('No major risk factors identified')
        
        return risks
    
    async def _analyze_regional_impact(
        self,
        features: Dict,
        regional_context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Analyze impact across different regions"""
        
        regions = ['Urban', 'Rural', 'Semi-Urban']
        
        # Base distribution (can be adjusted with real regional data)
        if features['has_location_criteria']:
            distribution = {
                'Urban': 0.25,
                'Rural': 0.60,
                'Semi-Urban': 0.15
            }
        else:
            distribution = {
                'Urban': 0.40,
                'Rural': 0.40,
                'Semi-Urban': 0.20
            }
        
        # Regional effectiveness (some policies work better in certain regions)
        effectiveness = {
            'Urban': 0.75,
            'Rural': 0.70,
            'Semi-Urban': 0.72
        }
        
        regional_analysis = {}
        for region in regions:
            regional_analysis[region] = {
                'beneficiary_percentage': distribution[region],
                'effectiveness_score': effectiveness[region],
                'implementation_priority': 'High' if distribution[region] > 0.35 else 'Medium'
            }
        
        return {
            'regional_breakdown': regional_analysis,
            'highest_impact_region': max(distribution, key=distribution.get),
            'coverage_assessment': 'Nationwide' if not features['has_location_criteria'] else 'State-specific'
        }
    
    async def _calculate_roi(
        self,
        budget: Dict,
        beneficiaries: Dict,
        success: Dict
    ) -> Dict[str, Any]:
        """Calculate Return on Investment for government"""
        
        total_budget = budget['total_estimated_budget']
        num_beneficiaries = beneficiaries['predicted']
        success_prob = success['overall_probability']
        
        # Economic benefits (simplified model)
        # Assume each beneficiary generates economic value through:
        # - Increased productivity
        # - Reduced social costs
        # - Multiplier effects
        
        economic_value_per_beneficiary = 150000  # INR per year
        expected_value = num_beneficiaries * economic_value_per_beneficiary * success_prob
        
        # ROI calculation
        roi_percentage = ((expected_value - total_budget) / total_budget) * 100 if total_budget > 0 else 0
        
        # Payback period (years)
        payback_period = total_budget / (expected_value / 5) if expected_value > 0 else float('inf')
        
        return {
            'roi_percentage': round(roi_percentage, 2),
            'payback_period_years': round(min(payback_period, 10), 1),
            'expected_economic_value': int(expected_value),
            'net_benefit': int(expected_value - total_budget),
            'social_roi': {
                'poverty_reduction_impact': 'High' if num_beneficiaries > 50000 else 'Medium',
                'social_welfare_score': round(success_prob * 100, 1),
                'quality_of_life_improvement': 'Significant'
            },
            'value_assessment': self._assess_value(roi_percentage)
        }
    
    def _assess_value(self, roi_percentage: float) -> str:
        """Assess overall value proposition"""
        if roi_percentage > 100:
            return 'Excellent - High return on investment'
        elif roi_percentage > 50:
            return 'Good - Positive return expected'
        elif roi_percentage > 0:
            return 'Fair - Modest return expected'
        else:
            return 'Poor - Consider optimization'
    
    def _calculate_confidence(self, features: Dict) -> float:
        """Calculate overall confidence in predictions"""
        confidence = 0.85  # Base confidence
        
        # Adjust based on data quality
        if features['complexity_score'] > 0.8:
            confidence -= 0.15
        
        if features['num_eligibility_rules'] > 7:
            confidence -= 0.10
        
        return round(max(confidence, 0.5), 2)
    
    def _generate_recommendations(
        self,
        beneficiaries: Dict,
        budget: Dict,
        success: Dict
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if beneficiaries['predicted'] < 10000:
            recommendations.append('Consider broadening eligibility criteria to reach more beneficiaries')
        
        if success['overall_probability'] < 0.6:
            recommendations.append('Simplify policy implementation to improve success probability')
        
        overhead_rate = budget['breakdown']['administrative_overhead'] / budget['total_estimated_budget']
        if overhead_rate > 0.15:
            recommendations.append('Optimize administrative processes to reduce overhead costs')
        
        if budget['per_beneficiary_cost'] > 100000:
            recommendations.append('Consider phased implementation to manage high per-beneficiary costs')
        
        if not recommendations:
            recommendations.append('Policy parameters are well-optimized for implementation')
        
        return recommendations
    
    async def process(self, task: str) -> str:
        """Process generic tasks"""
        return f"Policy Impact Predictor: {task}"
    
    def handle(self, *args, **kwargs):
        """Handle method for BaseAgent interface"""
        if args and isinstance(args[0], dict):
            import asyncio
            return asyncio.run(self.predict_impact(args[0]))
        return {"error": "Invalid input format"}


# Global instance
policy_impact_predictor = PolicyImpactPredictor()
