"""Example test file."""
import pytest


class TestExample:
    """Example test class."""

    def test_sample_assertion(self):
        """Sample test assertion."""
        assert True

    @pytest.mark.asyncio
    async def test_async_example(self):
        """Example async test."""
        result = True
        assert result is True
