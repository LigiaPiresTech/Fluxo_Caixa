import pytest

@pytest.mark.xfail(reason="Requer infraestrutura AWS implantada com EventBridge/SQS e consumidor Consolidado.")
def test_launches_remain_available_when_consolidated_is_down():
    """
    Acceptance test to run in an AWS homologation environment.

    Scenario:
    1. Disable/stop the Consolidado consumer.
    2. POST a valid financial launch.
    3. Assert HTTP 201 and transaction persisted in RDS.
    4. Assert an event/message is pending in SQS.
    5. Recover Consolidado.
    6. Assert pending message is consumed exactly once.
    7. Assert consolidated balance reflects the launch.
    """
    raise AssertionError("Executar contra AWS após EventBridge/SQS e idempotência serem implementados")

@pytest.mark.xfail(reason="Requer ambiente AWS e teste de carga real.")
def test_consolidated_peak_50_rps_with_max_5_percent_loss():
    """Run Locust with the case profile and validate <= 5% failures."""
    raise AssertionError("Executar com Locust contra API Gateway de homologação")

@pytest.mark.xfail(reason="RPO/RTO dependem do ambiente de DR que ainda não foi provisionado.")
def test_rpo_zero_for_confirmed_launches():
    """Simulate primary-region failure and prove no confirmed launch is lost."""
    raise AssertionError("Executar após implantação do DR")
