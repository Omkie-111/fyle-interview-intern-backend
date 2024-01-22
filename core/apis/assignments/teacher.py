from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.libs.exceptions import FyleError

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    try:
        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

        assignment_to_grade = Assignment.get_by_id(int(grade_assignment_payload.id))

        if not assignment_to_grade:
            raise FyleError(400, 'Assignment not found')

        if assignment_to_grade.teacher_id != p.teacher_id:
            raise FyleError(400, 'You are not authorized to grade this assignment')

        if assignment_to_grade.state != AssignmentStateEnum.SUBMITTED:
            raise FyleError(400, 'Only a submitted assignment can be graded')

        if grade_assignment_payload.grade not in ['A', 'B', 'C', 'D']:
            raise FyleError(400, 'Invalid grade')

        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth_principal=p
        )

        db.session.commit()

        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return APIResponse.respond(data=graded_assignment_dump)

    except FyleError as e:
        return jsonify({
            'error': 'FyleError',
            'message': e.message,
        }), e.status_code

