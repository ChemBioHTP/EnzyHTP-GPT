class Constants {
  static TOKEN = `MutexaGPT-token-key`;
  static WhiteList = [
    "/login",
    "/forgotPassword",
    "/siginUp",
    "/404",
    "/resetPassword",
    // "/register",
    // "/dashboard",
  ];
  static StaticMap = new Map([
    [-9, "Created"],
    [-8, "Pending"],
    [-7,"Initializing"],
    [-6,"Ready to Start"],
    [-5,"Ready with Updates"],
    [-4,"Suspecious Updates"],
    [-3,"Running"],
    [-2,"Running with Pause in Inner Units"],
    [-1,"Expected Pause"],
    [0,"Completed"],
    [1,"Exit with Error in Inner Units"],
    [2,"Exit with Error"],
    [3,"Exit with Error and Pause"],
    [7,"Cancelled"],
    [8,"Deprecated"],
    [9,"Initialization Failed."], 
  ]);
}
/**
 * 
 *
    CREATED = -9
    PENDING = -8
    INITIALIZING = -7
    READY_TO_START = -6
    READY_WITH_UPDATES = -5
    SUSPECIOUS_UPDATES = -4             # For Reload time only.
    RUNNING = -3
    RUNNING_WITH_PAUSE_IN_INNER_UNITS = -2   # For WorkFlow and ControlWorkUnit only.
    EXPECTED_PAUSE = -1                 # For Basic WorkUnit only. If a unit is paused, set its outer layers as `RUNNING_WITH_PAUSE_IN_INNER_UNITS`.
    EXIT_OK = 0
    EXIT_WITH_ERROR_IN_INNER_UNITS = 1  # For WorkFlow and ControlWorkUnit only.
    EXIT_WITH_ERROR = 2                 # For Science API only.
    EXIT_WITH_ERROR_AND_PAUSE = 3       # For WorkFlow and ControlWorkUnit only.
    CANCELLED = 7
    DEPRECATED = 8
    FAILED_INITIALIZATION = 9


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
 * 
 * 
 */
// 使对象不可变
Object.freeze(Constants);

export default Constants;
