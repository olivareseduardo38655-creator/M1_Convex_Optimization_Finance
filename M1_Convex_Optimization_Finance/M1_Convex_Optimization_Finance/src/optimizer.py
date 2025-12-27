import numpy as np
import pandas as pd  # <--- NECESARIO PARA LAS TYPE HINTS
from scipy.optimize import minimize
from typing import Dict, List, Tuple

def portfolio_variance(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
    return 0.5 * np.dot(weights.T, np.dot(cov_matrix, weights))

def optimize_portfolio(expected_returns: pd.Series, cov_matrix: pd.DataFrame, target_return: float) -> Dict:
    num_assets = len(expected_returns)
    initial_guess = np.array([1.0 / num_assets] * num_assets)
    bounds = tuple((0.0, 1.0) for _ in range(num_assets))
    
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'ineq', 'fun': lambda w: np.dot(w.T, expected_returns) - target_return}
    ]
    
    result = minimize(portfolio_variance, initial_guess, args=(cov_matrix,), 
                      method='SLSQP', bounds=bounds, constraints=constraints)
    
    if not result.success:
        return {"success": False, "message": result.message}
        
    return {
        "success": True,
        "weights": result.x,
        "risk": np.sqrt(2 * result.fun),
        "return": np.dot(result.x, expected_returns)
    }

if __name__ == "__main__":
    # Datos Dummy para prueba
    print("🧪 Probando optimizador...")
    mu = pd.Series([0.12, 0.05, 0.15], index=['A', 'B', 'C'])
    cov = pd.DataFrame([[0.04, 0, 0], [0, 0.01, 0], [0, 0, 0.09]], index=['A','B','C'], columns=['A','B','C'])
    
    res = optimize_portfolio(mu, cov, 0.06)
    if res['success']:
        print("✨ ¡Éxito! Riesgo calculado:", round(res['risk'], 4))
    else:
        print("❌ Fallo:", res['message'])
