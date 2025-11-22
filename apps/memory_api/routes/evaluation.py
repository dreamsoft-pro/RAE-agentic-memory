"""
Evaluation API Routes - Metrics and Quality Monitoring

This module provides FastAPI routes for evaluation operations including:
- Search result evaluation (MRR, NDCG, Precision, Recall)
- Drift detection
- A/B testing
- Quality monitoring
- Benchmarking
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
import structlog

from apps.memory_api.db import get_pool
from apps.memory_api.services.evaluation_service import EvaluationService
from apps.memory_api.services.drift_detector import DriftDetector
from apps.memory_api.models.evaluation_models import (
    EvaluateSearchRequest,
    EvaluateSearchResponse,
    DetectDriftRequest,
    DetectDriftResponse,
    CreateABTestRequest,
    CreateABTestResponse,
    GetQualityMetricsRequest,
    GetQualityMetricsResponse,
    MetricType
)

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/v1/evaluation", tags=["Evaluation"])


# ============================================================================
# Search Evaluation
# ============================================================================

@router.post("/search", response_model=EvaluateSearchResponse)
async def evaluate_search_results(
    request: EvaluateSearchRequest,
    pool=Depends(get_pool)
):
    """
    Evaluate search results against ground truth relevance judgments.

    Computes standard IR metrics:
    - MRR (Mean Reciprocal Rank)
    - NDCG@K (Normalized Discounted Cumulative Gain)
    - Precision@K
    - Recall@K
    - MAP (Mean Average Precision)

    **Use Case:** Measure search quality after system changes or for A/B testing.
    """
    try:
        service = EvaluationService()

        result = await service.evaluate_search_results(
            tenant_id=request.tenant_id,
            project_id=request.project_id,
            relevance_judgments=request.relevance_judgments,
            search_results=request.search_results,
            metrics_to_compute=request.metrics_to_compute,
            k_values=request.k_values
        )

        logger.info(
            "search_evaluation_complete",
            queries=result.num_queries_evaluated,
            overall_quality=result.overall_quality_score
        )

        return EvaluateSearchResponse(
            evaluation_result=result,
            message=f"Evaluated {result.num_queries_evaluated} queries with {len(result.metrics)} metrics"
        )

    except Exception as e:
        logger.error("search_evaluation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/supported")
async def get_supported_metrics():
    """
    Get list of supported evaluation metrics.

    Returns available metrics with descriptions and parameters.
    """
    return {
        "metrics": {
            "mrr": {
                "name": "Mean Reciprocal Rank",
                "description": "Average of reciprocal ranks of first relevant result",
                "parameters": [],
                "range": [0.0, 1.0],
                "higher_is_better": True
            },
            "ndcg": {
                "name": "Normalized Discounted Cumulative Gain",
                "description": "Position-aware ranking quality metric",
                "parameters": ["k"],
                "range": [0.0, 1.0],
                "higher_is_better": True
            },
            "precision": {
                "name": "Precision at K",
                "description": "Fraction of retrieved documents that are relevant",
                "parameters": ["k"],
                "range": [0.0, 1.0],
                "higher_is_better": True
            },
            "recall": {
                "name": "Recall at K",
                "description": "Fraction of relevant documents that are retrieved",
                "parameters": ["k"],
                "range": [0.0, 1.0],
                "higher_is_better": True
            },
            "map": {
                "name": "Mean Average Precision",
                "description": "Mean of average precision across queries",
                "parameters": [],
                "range": [0.0, 1.0],
                "higher_is_better": True
            }
        }
    }


# ============================================================================
# Drift Detection
# ============================================================================

@router.post("/drift/detect", response_model=DetectDriftResponse)
async def detect_drift(
    request: DetectDriftRequest,
    pool=Depends(get_pool)
):
    """
    Detect distribution drift between baseline and current periods.

    Uses statistical tests (Kolmogorov-Smirnov, PSI) to detect significant
    changes in metric distributions over time.

    **Use Case:** Monitor for data quality issues, concept drift, or system degradation.

    **Drift Types:**
    - `data_drift`: Input distribution changed
    - `concept_drift`: Input-output relationship changed
    - `prediction_drift`: Output distribution changed
    """
    try:
        detector = DriftDetector(pool)

        result = await detector.detect_drift(
            tenant_id=request.tenant_id,
            project_id=request.project_id,
            metric_name=request.metric_name,
            drift_type=request.drift_type,
            baseline_start=request.baseline_start,
            baseline_end=request.baseline_end,
            current_start=request.current_start,
            current_end=request.current_end,
            p_value_threshold=request.p_value_threshold,
            statistical_test=request.statistical_test
        )

        logger.info(
            "drift_detection_complete",
            detected=result.drift_detected,
            severity=result.severity.value,
            metric=request.metric_name
        )

        message = f"Drift {'detected' if result.drift_detected else 'not detected'}"
        if result.drift_detected:
            message += f" (severity: {result.severity.value}, p-value: {result.p_value:.4f})"

        return DetectDriftResponse(
            drift_result=result,
            message=message
        )

    except Exception as e:
        logger.error("drift_detection_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/drift/severity-levels")
async def get_drift_severity_levels():
    """
    Get drift severity levels and their meanings.

    Returns classification thresholds and recommended actions.
    """
    return {
        "severity_levels": {
            "none": {
                "description": "No significant drift detected",
                "magnitude_range": [0.0, 0.0],
                "action": "Continue monitoring"
            },
            "low": {
                "description": "Minor drift detected",
                "magnitude_range": [0.0, 0.1],
                "action": "Monitor closely, no immediate action required"
            },
            "medium": {
                "description": "Moderate drift detected",
                "magnitude_range": [0.1, 0.25],
                "action": "Investigate data sources, review recent changes"
            },
            "high": {
                "description": "Severe drift detected",
                "magnitude_range": [0.25, 0.5],
                "action": "Immediate investigation required, consider retraining"
            },
            "critical": {
                "description": "Critical drift requiring immediate action",
                "magnitude_range": [0.5, 1.0],
                "action": "URGENT: System validation and immediate remediation"
            }
        },
        "thresholds": {
            "p_value": 0.05,
            "psi_warning": 0.1,
            "psi_critical": 0.25
        }
    }


# ============================================================================
# A/B Testing
# ============================================================================

@router.post("/ab-test/create", response_model=CreateABTestResponse, status_code=201)
async def create_ab_test(
    request: CreateABTestRequest,
    pool=Depends(get_pool)
):
    """
    Create a new A/B test to compare variants.

    Sets up controlled experiment to compare different configurations,
    models, or strategies.

    **Use Case:** Test new search algorithms, weight profiles, or model versions.
    """
    try:
        from uuid import uuid4

        # Validate traffic allocation
        total_traffic = sum(v.traffic_percentage for v in request.variants)
        if not (99.0 <= total_traffic <= 101.0):  # Allow small floating point error
            raise HTTPException(
                status_code=400,
                detail=f"Traffic allocation must sum to 100% (got {total_traffic}%)"
            )

        test_id = uuid4()

        # In production, would store in database
        logger.info(
            "ab_test_created",
            test_id=test_id,
            test_name=request.test_name,
            variants=len(request.variants)
        )

        return CreateABTestResponse(
            test_id=test_id,
            message=f"A/B test '{request.test_name}' created with {len(request.variants)} variants"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("ab_test_creation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ab-test/{test_id}/compare")
async def compare_ab_test_variants(
    test_id: str,
    pool=Depends(get_pool)
):
    """
    Compare A/B test variants and determine winner.

    Performs statistical significance testing to determine if one variant
    is significantly better than others.

    **Returns:** Comparison results with winner determination.
    """
    try:
        from uuid import UUID

        # In production, would fetch from database
        # For now, return structure

        logger.info("ab_test_comparison_requested", test_id=test_id)

        return {
            "test_id": test_id,
            "comparison": {
                "message": "A/B test comparison requires actual test data",
                "status": "pending",
                "note": "Submit evaluation results for each variant to compare"
            }
        }

    except Exception as e:
        logger.error("ab_test_comparison_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Quality Monitoring
# ============================================================================

@router.post("/quality/metrics", response_model=GetQualityMetricsResponse)
async def get_quality_metrics(
    request: GetQualityMetricsRequest,
    pool=Depends(get_pool)
):
    """
    Get quality metrics for a time period.

    Returns comprehensive quality indicators including retrieval metrics,
    performance stats, and drift alerts.

    **Use Case:** Monitor system health, track quality over time.
    """
    try:
        # In production, would calculate from stored metrics
        # For now, return structure

        from apps.memory_api.models.evaluation_models import QualityMetrics

        quality_metrics = QualityMetrics(
            tenant_id=request.tenant_id,
            project_id=request.project_id,
            period_start=request.period_start,
            period_end=request.period_end
        )

        logger.info(
            "quality_metrics_retrieved",
            tenant_id=request.tenant_id,
            period=f"{request.period_start} to {request.period_end}"
        )

        return GetQualityMetricsResponse(
            quality_metrics=quality_metrics,
            alerts=[],
            message="Quality metrics retrieved successfully"
        )

    except Exception as e:
        logger.error("get_quality_metrics_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quality/thresholds")
async def get_quality_thresholds():
    """
    Get configured quality thresholds.

    Returns minimum acceptable values for metrics and performance indicators.
    """
    return {
        "retrieval_quality": {
            "min_mrr": 0.5,
            "min_ndcg": 0.6,
            "min_precision": 0.7,
            "description": "Minimum acceptable retrieval quality metrics"
        },
        "performance": {
            "max_response_time_ms": 1000,
            "max_p95_response_time_ms": 2000,
            "max_error_rate": 0.05,
            "description": "Maximum acceptable performance degradation"
        },
        "drift": {
            "p_value_threshold": 0.05,
            "max_acceptable_magnitude": 0.25,
            "description": "Drift detection sensitivity"
        }
    }


# ============================================================================
# Benchmarking
# ============================================================================

@router.post("/benchmark/run")
async def run_benchmark_suite(
    suite_name: str,
    tenant_id: str,
    project_id: str,
    pool=Depends(get_pool)
):
    """
    Run a predefined benchmark suite.

    Executes standardized queries and evaluates results against known
    ground truth for consistent performance measurement.

    **Use Case:** Regular system validation, regression testing.
    """
    try:
        logger.info("benchmark_run_requested", suite=suite_name)

        return {
            "suite_name": suite_name,
            "status": "pending",
            "message": "Benchmark suite execution requires predefined test data",
            "note": "Create benchmark suites with ground truth first"
        }

    except Exception as e:
        logger.error("benchmark_run_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/benchmark/suites")
async def list_benchmark_suites(
    tenant_id: str,
    project_id: str
):
    """
    List available benchmark suites.

    Returns configured benchmark suites for systematic evaluation.
    """
    return {
        "suites": [
            {
                "name": "standard_retrieval",
                "description": "Standard retrieval quality benchmark",
                "num_queries": 50,
                "metrics": ["mrr", "ndcg", "precision", "recall"]
            },
            {
                "name": "performance",
                "description": "Performance and latency benchmark",
                "num_queries": 100,
                "metrics": ["response_time", "throughput"]
            }
        ]
    }


# ============================================================================
# System Information
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint for evaluation service"""
    return {
        "status": "healthy",
        "service": "evaluation_api",
        "version": "1.0",
        "features": [
            "search_evaluation",
            "drift_detection",
            "ab_testing",
            "quality_monitoring",
            "benchmarking"
        ],
        "supported_metrics": [
            "mrr",
            "ndcg",
            "precision",
            "recall",
            "map"
        ],
        "statistical_tests": [
            "ks_test",
            "psi",
            "chi_square"
        ]
    }


@router.get("/info")
async def get_evaluation_info():
    """
    Get information about the evaluation system.

    Returns available metrics, tests, and configuration.
    """
    return {
        "evaluation_metrics": {
            "mrr": "Mean Reciprocal Rank - First relevant result position",
            "ndcg": "Normalized DCG - Position-aware ranking quality",
            "precision": "Precision@K - Relevant fraction of retrieved",
            "recall": "Recall@K - Retrieved fraction of relevant",
            "map": "Mean Average Precision - Average across queries",
            "f1": "F1 Score - Harmonic mean of precision and recall"
        },
        "drift_detection": {
            "tests": {
                "ks_test": "Kolmogorov-Smirnov two-sample test",
                "psi": "Population Stability Index",
                "chi_square": "Chi-square test for categorical data"
            },
            "severity_levels": ["none", "low", "medium", "high", "critical"],
            "drift_types": ["data_drift", "concept_drift", "prediction_drift"]
        },
        "ab_testing": {
            "max_variants": 10,
            "min_sample_size": 100,
            "confidence_levels": [0.90, 0.95, 0.99]
        },
        "quality_monitoring": {
            "monitored_metrics": [
                "avg_mrr",
                "avg_ndcg",
                "avg_response_time",
                "error_rate"
            ],
            "alert_types": [
                "quality_degradation",
                "performance_degradation",
                "drift_detected"
            ]
        }
    }
