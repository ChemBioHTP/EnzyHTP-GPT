import router from "@/router";
import axios from "@/utils/axios";
import { removeToken } from "@/utils/cache-token";

// sign up
export const signUp = data => {
  return axios.post("/api/auth/register", data);
};

/**
 *
 * @param {*} data
 * @returns
 */
export const login = data => {
  return axios.post("/api/auth/login", data);
};

/**
 *
 * @param {*} data
 * @returns
 */
export const resetGenerate = data => {
  return axios.post("/api/auth/password/reset/generate", data);
};

export const logout = data => {
  return new Promise((resolve, reject) => {
    axios
      .post("/api/auth/logout", data)
      .then(response => {
        resolve(response);
        removeToken();
        
        router.push("/login");
      })
      .catch(error => {
        reject(error);
      });
  });
};

export const googleLogin = (data, oauth_vendor = "google") => {
  return axios.post(`/api/auth/oauth/${oauth_vendor}/login`, data);
};

export const resetPassword = data => {
  return axios.put("/api/auth/password/reset", data);
};

export const changePassword = data => {
  return axios.put("/api/auth/password/change", data);
};

export const updateProfile = data => {
  return axios.put("/api/auth/profile", data);
};

export const getProfile = data => {
  return axios.get("/api/auth/profile", data);
};
