export const validatePass = async (_rule, value) => {
  const Regex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;
  if (!value) {
    return Promise.reject(
      `Your password was incorrect. Please try again or tap "Forgot password" to reset it.`
    );
  }
  if (Regex.test(value)) {
    return Promise.resolve();
  } else {
    return Promise.reject(
      "password must be at least 8 characters long, including both letters and numbers."
    );
  }
};

export const validateEmail = async (_rule, value) => {
  const Regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!value) {
    return Promise.reject(
      `The email does not exist. Please sign up for a new account.`
    );
  }
  if (Regex.test(value)) {
    return Promise.resolve();
  } else {
    return Promise.reject("Please provide a valid email.");
  }
};

