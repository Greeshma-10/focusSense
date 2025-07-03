class FocusScoreCalculator:
    def __init__(self):
        self.max_score = 100
        self.focus_score = self.max_score

    def update_score(self, features):
        score = self.max_score
        if features:
            if features['ear'] < 0.21:
                score -= 20
            if abs(features['head_angle']) > 15:
                score -= 30
        return max(0, score)
