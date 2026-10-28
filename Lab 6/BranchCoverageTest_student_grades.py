import pytest
from student_grades import letter_grade, final_marks, exam_eligibility


# ---------- letter_grade: validation decision (marks < 0 or marks > 100) ----------
def test_letter_grade_negative_raises():            # marks < 0 True
    with pytest.raises(ValueError):
        letter_grade(-1)


def test_letter_grade_over_100_raises():            # marks < 0 False, marks > 100 True
    with pytest.raises(ValueError):
        letter_grade(101)


def test_letter_grade_valid_limits_do_not_raise():  # both False
    assert letter_grade(0) == "F"
    assert letter_grade(100) == "S"


# ---------- letter_grade: grade ladder, True and False of each elif ----------
@pytest.mark.parametrize("marks, expected", [
    (95, "S"), (90, "S"),
    (89, "A"), (80, "A"),
    (79, "B"), (70, "B"),
    (69, "C"), (60, "C"),
    (59, "D"), (50, "D"),
    (49, "E"), (40, "E"),
    (39, "F"), (10, "F"),
])
def test_letter_grade_ladder(marks, expected):
    assert letter_grade(marks) == expected


# ---------- final_marks: validation decision (internal > 40 or external > 60) ----------
def test_final_marks_internal_too_high():           # internal > 40 True
    with pytest.raises(ValueError):
        final_marks(41, 0, False)


def test_final_marks_external_too_high():           # internal > 40 False, external > 60 True
    with pytest.raises(ValueError):
        final_marks(0, 61, False)


def test_final_marks_max_valid_inputs_do_not_raise():  # both False (boundary)
    assert final_marks(40, 60, False) == 100


# ---------- final_marks: has_project and cap decisions ----------
def test_final_marks_no_project_skips_bonus():      # has_project False
    assert final_marks(20, 30, False) == 50


def test_final_marks_project_below_cap():           # has_project True, total > 100 False
    assert final_marks(20, 30, True) == 55


def test_final_marks_project_exactly_100_not_capped():  # boundary: total == 100
    assert final_marks(40, 55, True) == 100


def test_final_marks_project_above_cap_is_clamped():    # total > 100 True
    assert final_marks(40, 60, True) == 100
    assert final_marks(38, 58, True) == 100


# ---------- exam_eligibility ----------
def test_blocked_when_fees_unpaid():                # not fees_paid True
    assert exam_eligibility(95, False, True) == "blocked"


def test_eligible_with_75_attendance():             # fees paid, attendance >= 75 True
    assert exam_eligibility(75, True, False) == "eligible"
    assert exam_eligibility(100, True, False) == "eligible"


def test_eligible_medical_between_65_and_74():      # attendance >= 65 True and has_medical True
    assert exam_eligibility(65, True, True) == "eligible"
    assert exam_eligibility(74, True, True) == "eligible"


def test_detained_between_65_and_74_without_medical():  # attendance >= 65 True, has_medical False
    assert exam_eligibility(65, True, False) == "detained"
    assert exam_eligibility(74, True, False) == "detained"


def test_detained_below_65_even_with_medical():     # attendance >= 65 False
    assert exam_eligibility(64, True, True) == "detained"
    assert exam_eligibility(0, True, False) == "detained"
