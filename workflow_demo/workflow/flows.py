from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow import frontend

from .models import WorkflowProcess

@frontend.register
class WorkFlow(Flow):
    process_class = WorkflowProcess

    start = (
        flow.Start(
            CreateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )

    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
            .Then(this.send)
            .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_workflow_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_workflow_request(self, activation):
        print(activation.process.text)
