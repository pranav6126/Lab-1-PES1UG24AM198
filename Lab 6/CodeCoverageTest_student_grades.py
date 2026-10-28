import pytest
from student_grades import letter_grade, final_marks, exam_eligibility


# ---------- letter_grade ----------
def test_s_grade():
    assert letter_grade(95) == "S"


def test_a_grade():
    assert letter_grade(85) == "A"


def test_b_grade():
    assert letter_grade(75) == "B"


def test_c_grade():
    assert letter_grade(65) == "C"


def test_d_grade():
    assert letter_grade(55) == "D"


def test_e_grade():
    assert letter_grade(45) == "E"


def test_f_grade():
    assert letter_grade(20) == "F"


def test_letter_grade_boundaries():
    assert letter_grade(100) == "S"
    assert letter_grade(90) == "S"
    assert letter_grade(89) == "A"
    assert letter_grade(40) == "E"
    assert letter_grade(39) == "F"
    assert letter_grade(0) == "F"


def test_letter_grade_negative_marks_invalid():
    with pytest.raises(ValueError):
        letter_grade(-1)


def test_letter_grade_above_100_invalid():
    with pytest.raises(ValueError):
        letter_grade(101)


# ---------- final_marks ----------
def test_final_marks_without_project():
    assert final_marks(30, 50, False) == 80


def test_final_marks_with_project_bonus():
    assert final_marks(30, 50, True) == 85


def test_final_marks_bonus_capped_at_100():
    assert final_marks(40, 60, True) == 100


def test_final_marks_internal_out_of_range():
    with pytest.raises(ValueError):
        final_marks(41, 50, False)


def test_final_marks_external_out_of_range():
    with pytest.raises(ValueError):
        final_marks(20, 61, False)


# ---------- exam_eligibility ----------
def test_eligible():
    assert exam_eligibility(80, True, False) == "eligible"


def test_blocked_when_fees_not_paid():
    assert exam_eligibility(90, False, False) == "blocked"


def test_eligible_with_medical_condonation():
    assert exam_eligibility(70, True, True) == "eligible"


def test_detained_low_attendance_no_medical():
    assert exam_eligibility(70, True, False) == "detained"
