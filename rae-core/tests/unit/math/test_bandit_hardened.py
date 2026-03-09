"""Hardened unit tests for Multi-Armed Bandit (Math Auto-Tuning)."""

import pytest
from pathlib import Path
from rae_core.math.bandit.bandit import MultiArmedBandit, BanditConfig
from rae_core.math.bandit.arm import Arm
from rae_core.math.types import MathLevel, TaskType
from rae_core.math.features_v2 import FeaturesV2

class TestBanditHardened:
    @pytest.fixture
    def config(self, tmp_path):
        return BanditConfig(
            c=2.0,
            exploration_rate=0.1,
            persistence_path=tmp_path / "bandit_stats.json"
        )

    @pytest.fixture
    def bandit(self, config):
        # Create a small set of arms for precise testing
        arms = [
            Arm(level=MathLevel.L1, strategy="cheap", total_reward=8.0, pulls=10, history=[0.8]*10),
            Arm(level=MathLevel.L2, strategy="research", total_reward=2.5, pulls=5, history=[0.5]*5)
        ]
        return MultiArmedBandit(config, arms=arms)

    @pytest.fixture
    def sample_features(self):
        return FeaturesV2(task_type=TaskType.MEMORY_RETRIEVE)

    def test_arm_mean_reward(self):
        arm = Arm(level=MathLevel.L1, strategy="test")
        assert arm.mean_reward() == 0.0
        arm.update(reward=1.0)
        assert arm.mean_reward() == 1.0

    def test_select_arm_ucb(self, bandit, sample_features):
        bandit.config.exploration_rate = 0.0
        # Returns (Arm, is_exploration)
        selected_arm, is_exploring = bandit.select_arm(features=sample_features)
        assert isinstance(selected_arm, Arm)
        assert is_exploring is False
        assert selected_arm.level in [MathLevel.L1, MathLevel.L2]

    def test_update_reward(self, bandit, sample_features):
        arm = bandit.arms[0]
        old_pulls = arm.pulls
        # New Signature: update(arm, reward, features)
        bandit.update(arm, 1.0, sample_features)
        assert arm.pulls == old_pulls + 1

    def test_persistence_save_load(self, bandit, tmp_path):
        path = tmp_path / "save_test.json"
        bandit.config.persistence_path = path
        
        # Unique value to check on a default-like arm ID
        # Default arms use "w_txt..." or "default"
        # Let's add a known arm to the bandit first
        test_arm = Arm(level=MathLevel.L1, strategy="default", total_reward=555.5)
        bandit.arms.append(test_arm)
        bandit.arm_map[(MathLevel.L1, "default")] = test_arm
        
        bandit.save_state()
        assert path.exists()
        
        # Load into fresh bandit
        new_bandit = MultiArmedBandit(bandit.config)
        new_bandit.load_state()
        
        # Verify the specific arm was loaded
        assert any(abs(a.total_reward - 555.5) < 0.01 for a in new_bandit.arms)

    def test_degradation_detection(self, bandit):
        is_degraded, score = bandit.check_degradation()
        assert isinstance(is_degraded, bool)
        assert isinstance(score, float)

    def test_bandit_statistics(self, bandit):
        stats = bandit.get_statistics()
        assert "total_pulls" in stats
        assert "arms" in stats
        assert len(stats["arms"]) >= 2
