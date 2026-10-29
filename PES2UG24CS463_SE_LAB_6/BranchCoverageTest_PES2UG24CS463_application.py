
import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate

#Example test cases:
def test_excellent_band():
    assert credit_band(800) == "excellent"

def test_eligible():
    assert is_eligible(30, 50000, "salaried", 800) is True

#Write the rest of the test cases so that the code is 90- 100% covered.

# Test all credit score bands
def test_good_band():
    assert credit_band(650) == "good"

def test_fair_band():
    assert credit_band(550) == "fair"

def test_poor_band():
    assert credit_band(400) == "poor"

def test_minimum_score():
    assert credit_band(300) == "poor"

def test_maximum_score():
    assert credit_band(900) == "excellent"


# Test invalid credit scores
@pytest.mark.parametrize("score", [299, 901])
def test_invalid_score(score):
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(score)


# Test employment validation
def test_unknown_employment():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "unemployed", 800)


# Test age limits
@pytest.mark.parametrize("age", [20, 61])
def test_ineligible_age(age):
    assert is_eligible(age, 50000, "salaried", 800) is False

def test_minimum_eligible_age():
    assert is_eligible(21, 50000, "salaried", 800) is True

def test_maximum_eligible_age():
    assert is_eligible(60, 50000, "salaried", 800) is True


# Test minimum income requirements
def test_salaried_income_too_low():
    assert is_eligible(30, 24999, "salaried", 800) is False

def test_salaried_income_at_minimum():
    assert is_eligible(30, 25000, "salaried", 800) is True

def test_self_employed_income_too_low():
    assert is_eligible(30, 39999, "self_employed", 800) is False

def test_self_employed_income_at_minimum():
    assert is_eligible(30, 40000, "self_employed", 650) is True


# Test poor credit eligibility
def test_poor_credit_ineligible():
    assert is_eligible(30, 50000, "salaried", 400) is False


# Test interest rate calculations
def test_good_interest_rate():
    assert interest_rate(650, "salaried", False) == 10

def test_fair_interest_rate():
    assert interest_rate(550, "salaried", False) == 13

def test_poor_interest_rate():
    assert interest_rate(400, "salaried", False) == 13

def test_self_employed_interest_rate():
    assert interest_rate(800, "self_employed", False) == 9

def test_collateral_interest_rate():
    assert interest_rate(800, "salaried", True) == 6

def test_self_employed_with_collateral():
    assert interest_rate(800, "self_employed", True) == 7
