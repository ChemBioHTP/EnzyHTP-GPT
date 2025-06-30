#! python3
# -*- coding: utf-8 -*-
"""
@File   : experiment_config.py
@Created: 2025/06/26 20:06
@Author : Zhong, Yinjie
@Email  : yinjie.zhong@vanderbilt.edu
"""

# Here put the import lib.
from __future__ import annotations  # To enable the annotation that a staticmethod/classmethod of a class returns an instance of the class.

class StatusCode():
    """
    Class representing various execution statuses.

    Attributes:
        CREATED (int): The initial status when a WorkUnit or WorkFlow instance is created. Value: -9
        PENDING (int): The status when a WorkUnit or WorkFlow instance is pending for initialization and execution. Value: -8
        INITIALIZING (int): The status when a WorkUnit or WorkFlow instance is undergoing initialization. Value: -7
        READY_TO_START (int): The status when a WorkUnit or WorkFlow instance has passed the self-inspection but hasn't yet been started. Value: -6
        READY_WITH_UPDATES (int): The status when a previously executed WorkUnit or WorkFlow instance have its input arguments changed
                                due to the influence from the update in the input values of the task during continue computing. Value: -5
        SUSPECIOUS_UPDATES (int): The status when a previously `EXIT_OK` WorkUnit or WorkFlow instance has detected but unsure argument updates
                                    during reloading. Value: -4
        RUNNING (int): Indicates that the workunit or workflow is currently in execution. Value: -3
        PAUSE_IN_INNER_UNITS (int): Specific to WorkFlow and ControlWorkUnit instances. Indicates
                                    that the workflow is running but an inner unit is paused as expected. Value: -2
        EXPECTED_PAUSE (int): Specific to Basic WorkUnit instances. Indicates that a unit is paused and its outer
                              layers should be marked as `RUNNING_WITH_PAUSE_IN_INNER_UNITS`. Value: -1
        EXIT_OK (int): Indicates successful completion of the work unit or workflow. Value: 0
        ERROR_IN_INNER_UNITS (int): Specific to WorkFlow and ControlWorkUnit. Indicates error(s) in the
                                    inner units of a workflow. Value: 1
        EXIT_WITH_ERROR (int): Specific to Basic WorkUnit instances. Indicates that the work unit or workflow
                               exited with an error. Value: 2
        EXIT_WITH_ERROR_AND_PAUSE (int): Specific to WorkFlow and ControlWorkUnit. Indicates the coexistence of error(s)
                                        and expected pause(s) in the inner units of a workflow. Value: 3
        CANCELLED (int): Indicates that the workunit or workflow is cancelled.
                        Any workflows or workunits inside it should be marked with this status. Value: 8
        DEPRECATED (int): Indicates that the workunit or workflow is deprecated.
                        Any workflows or workunits inside it should be marked with this status and deleted. Value: 8
        FAILED_INITIALIZATION (int): Indicates that the initialization of the workunit or workflow failed. Value: 9
    """
    CREATED = -9
    PENDING = -8
    INITIALIZING = -7
    READY_TO_START = -6
    READY_WITH_UPDATES = -5
    SUSPECIOUS_UPDATES = -4             # For Reload time only.
    RUNNING = -3
    RUNNING_WITH_PAUSE_IN_INNER_UNITS = -2   # For WorkFlow and ControlWorkUnit only.
    EXPECTED_PAUSE = -1                 # For Basic WorkUnit only. If a unit is paused, set its outer layers as `RUNNING_WITH_PAUSE_IN_INNER_UNITS`.
    EXIT_OK = 0
    EXIT_WITH_ERROR_IN_INNER_UNITS = 1  # For WorkFlow and ControlWorkUnit only.
    EXIT_WITH_ERROR = 2                 # For Science API only.
    EXIT_WITH_ERROR_AND_PAUSE = 3       # For WorkFlow and ControlWorkUnit only.
    CANCELLED = 7
    DEPRECATED = 8
    FAILED_INITIALIZATION = 9

    #region Status Group, for logical judgment only.
    queued_status = [PENDING, INITIALIZING, RUNNING, RUNNING_WITH_PAUSE_IN_INNER_UNITS]
    pause_excluding_error_statuses = [EXPECTED_PAUSE, RUNNING_WITH_PAUSE_IN_INNER_UNITS]
    pause_including_error_statuses = [EXPECTED_PAUSE, RUNNING_WITH_PAUSE_IN_INNER_UNITS, EXIT_WITH_ERROR_AND_PAUSE]
    error_excluding_pause_statuses = [EXIT_WITH_ERROR, EXIT_WITH_ERROR_IN_INNER_UNITS, FAILED_INITIALIZATION]
    error_including_pause_statuses = [EXIT_WITH_ERROR, EXIT_WITH_ERROR_IN_INNER_UNITS, FAILED_INITIALIZATION, EXIT_WITH_ERROR_AND_PAUSE]
    error_or_pause_statuses = [EXIT_WITH_ERROR, EXIT_WITH_ERROR_IN_INNER_UNITS, EXPECTED_PAUSE, RUNNING_WITH_PAUSE_IN_INNER_UNITS, EXIT_WITH_ERROR_AND_PAUSE]
    unexecutable_statuses = [CREATED, PENDING, INITIALIZING, DEPRECATED, FAILED_INITIALIZATION]
    unexecuted_statuses = [CREATED, PENDING, INITIALIZING, READY_TO_START, FAILED_INITIALIZATION]    # Note its distinction from `unexecutable_statuses`.
    skippable_statuses = [EXIT_OK]
    #endregion

    status_text_mapper = {
        CREATED: "Created",
        PENDING: "Pending",
        INITIALIZING: "Initializing",
        READY_TO_START: "Ready to Start",
        READY_WITH_UPDATES: "Ready with Updates",
        SUSPECIOUS_UPDATES: "Suspecious Updates",
        RUNNING: "Running",
        RUNNING_WITH_PAUSE_IN_INNER_UNITS: "Running with Pause in Inner Units",
        EXPECTED_PAUSE: "Expected Pause",
        EXIT_OK: "Completed",
        EXIT_WITH_ERROR_IN_INNER_UNITS: "Exit with Error in Inner Units",
        EXIT_WITH_ERROR: "Exit with Error",
        EXIT_WITH_ERROR_AND_PAUSE: "Exit with Error and Pause",
        CANCELLED: "Cancelled",
        DEPRECATED: "Deprecated",
        FAILED_INITIALIZATION: "Initialization Failed."
    }
